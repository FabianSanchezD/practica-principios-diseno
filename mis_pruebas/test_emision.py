from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from clinicasegura.aplicacion.borde import a_receta
from clinicasegura.dominio.errores import (CadenaNoSoportada,
                                           FarmaciaNoDisponible,
                                           RecetaInvalida)
from clinicasegura.dominio.modelos import Cedula, Despacho, Receta
from clinicasegura.dominio.servicio import EmisionDeRecetas

FIJO = datetime(2026, 3, 1, 9, 0, 0)


class RelojFijo:
    def __init__(self, cuando=FIJO):
        self.cuando = cuando

    def ahora(self) -> datetime:
        return self.cuando


class FoliosSecuenciales:
    def __init__(self):
        self.n = 0

    def siguiente(self) -> str:
        self.n += 1
        return f"F-{self.n:05d}"


class FarmaciaFalsa:
    cadena = "farmauno"

    def __init__(self):
        self.recibidas = []

    def enviar(self, receta, folio, vence):
        self.recibidas.append((receta, folio, vence))
        return Despacho(folio=folio, cadena=self.cadena, vence=vence)


class FarmaciaCaida:
    cadena = "saludtotal"

    def enviar(self, receta, folio, vence):
        raise TimeoutError("la cadena no respondió")


class BitacoraEspia:
    def __init__(self):
        self.eventos = []

    def registrar(self, evento: str, folio: str) -> None:
        self.eventos.append((evento, folio))


def armar(pasarela=None, reloj=None):
    pasarela = pasarela or FarmaciaFalsa()
    bitacora = BitacoraEspia()
    servicio = EmisionDeRecetas(
        pasarelas={pasarela.cadena: pasarela},
        reloj=reloj or RelojFijo(),
        folios=FoliosSecuenciales(),
        bitacora=bitacora,
    )
    return servicio, pasarela, bitacora


def receta(**cambios):
    datos = dict(cedula=Cedula("1-1234-5678"), medicamento="N02BE01",
                 dias=30, dosis_mg=Decimal("500"))
    datos.update(cambios)
    return Receta(**datos)


def test_la_vigencia_sale_del_reloj_inyectado_y_no_del_sistema():
    servicio, _, _ = armar(reloj=RelojFijo(datetime(2026, 1, 15, 8, 0, 0)))
    despacho = servicio.emitir(receta(), "farmauno")
    assert despacho.vence == datetime(2026, 1, 15, 8, 0, 0) + timedelta(days=30)


def test_dos_emisiones_con_el_mismo_reloj_vencen_igual():
    servicio, _, _ = armar()
    assert servicio.emitir(receta(), "farmauno").vence == \
        servicio.emitir(receta(), "farmauno").vence


def test_la_cadena_caida_se_propaga_como_error_de_dominio():
    servicio, _, bitacora = armar(FarmaciaCaida())
    with pytest.raises(FarmaciaNoDisponible) as fallo:
        servicio.emitir(receta(), "saludtotal")
    assert isinstance(fallo.value.__cause__, TimeoutError)
    assert bitacora.eventos == [], (
        "No se puede registrar una emisión que nunca ocurrió."
    )


def test_una_cadena_que_nadie_atiende_no_devuelve_none():
    servicio, _, _ = armar()
    with pytest.raises(CadenaNoSoportada):
        servicio.emitir(receta(), "farmaviva")


def test_el_borde_rechaza_una_receta_invalida():
    for datos in (
        {"cedula": "1-1234-5678", "medicamento": "N02BE01", "dias": 0,
         "dosis_mg": "500"},
        {"cedula": "abc", "medicamento": "N02BE01", "dias": 30,
         "dosis_mg": "500"},
        {"cedula": "1-1234-5678", "medicamento": "N02BE01", "dias": 30},
    ):
        with pytest.raises(RecetaInvalida):
            a_receta(datos)


def test_el_recargo_por_riesgo_alto_duplica_el_monto():
    servicio, _, _ = armar()
    normal = servicio.emitir(receta(), "farmauno").recargo
    alto = servicio.emitir(receta(riesgo_alto=True), "farmauno").recargo
    assert alto == normal * 2
    assert isinstance(normal, Decimal)


def test_al_adaptador_le_llega_una_receta_y_no_un_diccionario():
    servicio, farmacia, _ = armar()
    servicio.emitir(receta(), "farmauno")
    entregada, folio, _ = farmacia.recibidas[0]
    assert isinstance(entregada, Receta)
    assert folio == "F-00001"


def test_la_emision_queda_registrada_con_su_folio():
    servicio, _, bitacora = armar()
    despacho = servicio.emitir(receta(), "farmauno")
    assert bitacora.eventos == [("emitida", despacho.folio)]
