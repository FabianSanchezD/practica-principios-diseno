# Bitácora de la práctica

Estudiante: Fabián Alejandro Sánchez Durán
Carné: 2025064258

> Cómo se llena cada entrada, en este orden y sin saltarse pasos:
>
> 1. **Predicción** — escríbala ANTES de correr nada. Qué cree que va a
>    pasar y por qué. Equivocarse aquí y entender después vale más que
>    acertar; no vuelva a corregirla.
> 2. **Observación** — corra el experimento de la etapa y pegue la salida.
> 3. **Explicación** — por qué pasó lo que pasó, en sus palabras, citando
>    **su** archivo y **su** línea (`servicio.py:24`).
> 4. **Sello** — corra `python herramientas/marcador.py` al cerrar la
>    etapa y pegue el sello que imprime.

## Etapa 0 — Diagnóstico

**Predicción:**

Espero dos rojas y dos verdes: la plantilla ya trae las once filas con el nombre de cada principio, así que las pruebas que cuentan filas y buscan los nombres deberían pasar, pero las columnas de hallazgo y evidencia están vacías.

**Observación:**

```
$ pytest -m etapa0
..FF                                                                     [100%]
=================================== FAILURES ===================================
___________________ test_cada_hallazgo_cita_archivo_y_linea ____________________
pruebas/test_etapa0_diagnostico.py:65: in test_cada_hallazgo_cita_archivo_y_linea
    assert not sin_evidencia, (
E   AssertionError: Estas filas no citan archivo y línea (por ejemplo «legado.py:38»): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
E        Una decisión sin evidencia vale cero, también en el diagnóstico.
E   assert not ['1', '2', '3', '4', '5', '6', ...]
_________ test_ninguna_fila_quedo_vacia_o_con_el_texto_de_la_plantilla _________
pruebas/test_etapa0_diagnostico.py:76: in test_ninguna_fila_quedo_vacia_o_con_el_texto_de_la_plantilla
    assert not malas, "Filas incompletas: " + ", ".join(malas)
E   AssertionError: Filas incompletas: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
E   assert not ['1', '2', '3', '4', '5', '6', ...]
=========================== short test summary info ============================
FAILED pruebas/test_etapa0_diagnostico.py::test_cada_hallazgo_cita_archivo_y_linea
FAILED pruebas/test_etapa0_diagnostico.py::test_ninguna_fila_quedo_vacia_o_con_el_texto_de_la_plantilla
2 failed, 2 passed, 80 deselected in 0.02s
```

**Explicación:**

Acerté: dos rojas y dos verdes. Las que pasaron contaban filas y nombres que la plantilla ya traía; ninguna miraba si yo había escrito algo.

Leyendo legado.py encontré los once violados. El que no esperaba fue el 5: _post en legado.py:119 parecía la pieza genérica del archivo, pero lee el timeout de la global en legado.py:129. Los más caros son el 10 y el 11 juntos: el assert de legado.py:62 se apaga con python -O y el except con pass de legado.py:103 se traga el fallo, así que en producción la receta inválida se emite callada.

CONFIG, en legado.py:30, aparece en tres filas distintas: es una causa con tres consecuencias, no tres hallazgos.

**Sello:** 6fbae6c740cb5b95

Salida del marcador al cerrar la etapa:

```
Etapa 0  Diagnóstico                                  verde
4 pruebas en verde · 0 por resolver
corrida #4 registrada
SELLO: 6fbae6c740cb5b95
```

## Etapa 1 — Dividir y conquistar, cohesión

**Predicción:**

Espero que fallen varias pruebas de la etapa por la causa de que la carpeta clinicasegura sólo tiene legado.py, así que no existen los paquetes dominio, aplicacion ni infraestructura.

**Observación:**

Corrida antes de escribir una sola línea del rediseño, con la carpeta
clinicasegura conteniendo únicamente __init__.py y legado.py:

```
$ pytest -m etapa1
FFF....                                                                  [100%]
=================================== FAILURES ===================================
________________________ test_existen_los_tres_paquetes ________________________
pruebas/apoyo.py:22: in importar
    return importlib.import_module(ruta)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'clinicasegura.dominio'

During handling of the above exception, another exception occurred:
pruebas/test_etapa1_division_cohesion.py:37: in test_existen_los_tres_paquetes
    importar(f"clinicasegura.{paquete}")
pruebas/apoyo.py:24: in importar
    pytest.fail(
E   Failed: Falta el módulo «clinicasegura.dominio».
E      Cree el archivo clinicasegura/dominio.py (y el __init__.py de su paquete).
E      Detalle: No module named 'clinicasegura.dominio'
______________ test_el_dominio_define_sus_tipos_y_son_inmutables _______________
pruebas/apoyo.py:22: in importar
    return importlib.import_module(ruta)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'clinicasegura.dominio'

During handling of the above exception, another exception occurred:
pruebas/test_etapa1_division_cohesion.py:42: in test_el_dominio_define_sus_tipos_y_son_inmutables
    tipo = obtener("clinicasegura.dominio.modelos", nombre)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pruebas/apoyo.py:38: in obtener
    mod = importar(ruta)
          ^^^^^^^^^^^^^^
pruebas/apoyo.py:24: in importar
    pytest.fail(
E   Failed: Falta el módulo «clinicasegura.dominio.modelos».
E      Cree el archivo clinicasegura/dominio/modelos.py (y el __init__.py de su paquete).
E      Detalle: No module named 'clinicasegura.dominio'
__________________ test_el_dominio_define_sus_propios_errores __________________
pruebas/apoyo.py:22: in importar
    return importlib.import_module(ruta)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'clinicasegura.dominio'

During handling of the above exception, another exception occurred:
pruebas/test_etapa1_division_cohesion.py:54: in test_el_dominio_define_sus_propios_errores
    base = obtener("clinicasegura.dominio.errores", "ErrorDominio")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pruebas/apoyo.py:38: in obtener
    mod = importar(ruta)
          ^^^^^^^^^^^^^^
pruebas/apoyo.py:24: in importar
    pytest.fail(
E   Failed: Falta el módulo «clinicasegura.dominio.errores».
E      Cree el archivo clinicasegura/dominio/errores.py (y el __init__.py de su paquete).
E      Detalle: No module named 'clinicasegura.dominio'
=========================== short test summary info ============================
FAILED pruebas/test_etapa1_division_cohesion.py::test_existen_los_tres_paquetes
FAILED pruebas/test_etapa1_division_cohesion.py::test_el_dominio_define_sus_tipos_y_son_inmutables
FAILED pruebas/test_etapa1_division_cohesion.py::test_el_dominio_define_sus_propios_errores
3 failed, 4 passed, 77 deselected in 0.03s
```

**Explicación:**

Partí legado.py en tres paquetes según qué conoce cada uno. En modelos.py:9, modelos.py:17 y modelos.py:26 quedaron Cedula, Receta y Despacho como dataclasses congelados, en vez del diccionario crudo que antes cualquiera podía mutar. La regla de negocio quedó pura en reglas.py:11 y reglas.py:17: vencimiento recibe el instante en vez de llamarlo, y por eso la única llamada a datetime.now vive ahora en reloj.py:7. El condicional por nombre de cadena desapareció: enviar es uno solo, en pasarelas.py:49, y lo único que cambia es el método que arma el cuerpo, en pasarelas.py:65, pasarelas.py:73 y pasarelas.py:81. ServicioRecetas tenía cinco métodos públicos que no se parecían entre sí; EmisionDeRecetas, en servicio.py:10, tiene uno solo, en servicio.py:17.

**Sello:** a24ebb0bd4d7129e

Salida del marcador al cerrar la etapa:

```
Etapa 1  Dividir y conquistar · cohesión              verde
7 pruebas en verde · 0 por resolver
corrida #3 registrada
SELLO: a24ebb0bd4d7129e
```

## Etapa 2 — Reducir el acoplamiento

**Predicción:**

Espero que las cinco pasen sin tocar código, porque al rediseñar la etapa 1 ya dejé calcular_recargo con tres valores simples, emitir recibiendo una Receta y el dominio sin sqlite.

**Observación:**

```
$ python -c "cuántos lugares dependen de CONFIG"
lecturas de CONFIG en legado.py: 8
  legado.py:66  vence = datetime.now() + timedelta(days=CONFIG["vigencia_dias"])
  legado.py:74  recargo = CONFIG["tarifa_diaria"] * datos["dias"] * 2
  legado.py:76  recargo = CONFIG["tarifa_diaria"] * datos["dias"]
  legado.py:81  CONFIG["farmauno_url"],
  legado.py:86  CONFIG["saludtotal_url"],
  legado.py:91  CONFIG["cruzverde_url"],
  legado.py:129  peticion, timeout=CONFIG["timeout"]
  legado.py:143  with urllib.request.urlopen(url, timeout=CONFIG["timeout"]) as r:

metodos afectados por CONFIG["vigencia_dias"] = 1: emitir, y por tanto todo lo que emita

$ pytest -m etapa2
.....                                                                    [100%]
5 passed, 79 deselected in 0.02s
```

**Explicación:**

Todo bien, pasaron sin cambios porque ya los había hecho en la etapa 1 sin querer.

Como las pruebas no me exigían nada, busqué qué quedaba acoplado igual. Encontré que emitir leía TARIFA_DIARIA y VIGENCIA_DIAS importadas de reglas.py:6 y reglas.py:7 sin declararlas: son inmutables, así que no son estado global mutable, pero seguían siendo dependencias invisibles. Las subí a la firma como parámetros con valor por omisión en servicio.py:19, así emitir(receta, cadena) sigue funcionando igual y ahora se puede emitir con otra tarifa sin parchar el módulo.

**Sello:** 224b7bd83952cebb

Salida del marcador al cerrar la etapa:

```
Etapa 2  Reducir el acoplamiento                      verde
5 pruebas en verde · 0 por resolver
corrida #5 registrada
SELLO: 224b7bd83952cebb
```

**Sello:**

## Etapa 3 — Abstracción y reuso

**Predicción:**

Espero tres rojas porque falta dominio/puertos.py, así que las dos pruebas de puertos fallan, y ninguna parte de mi código importa re, así que la de no reinventar la validación también; las otras cuatro deberían pasar porque emitir ya devuelve Despacho, Receta.cedula ya es del tipo Cedula, y uuid y Decimal ya están importados.

**Observación:**

```
$ grep -rn "data\|attributes\|full_name\|risk_lvl" clinicasegura/ (sin __pycache__)
coincidencias totales: 8
clinicasegura/legado.py:3
clinicasegura/dominio/modelos.py:4
clinicasegura/infraestructura/pasarelas.py:1

las que son del modelo del proveedor:
clinicasegura/legado.py:150:            paciente["data"]["attributes"]["full_name"],
clinicasegura/legado.py:151:            paciente["data"]["attributes"]["risk_lvl"],

$ pytest -m etapa3
E        Nunca escriba usted parsers de formatos estándar.
E   assert ('re' in {'__future__', 'clinicasegura', 'dataclasses', 'datetime', 'decimal', 'json', ...} or 'pydantic' in '\nfrom __future__ import annotations\nfrom datetime import datetime, timedelta\nfrom decimal import Decimal\nVIGENCIA...s\nimport uuid\n\nclass FoliosUnicos:\n\n    def siguiente(self) -> str:\n        return uuid.uuid4().hex[:12].upper()')
E    +  where {'__future__', 'clinicasegura', 'dataclasses', 'datetime', 'decimal', 'json', ...} = modulos_importados_de_todo()
=========================== short test summary info ============================
FAILED pruebas/test_etapa3_abstraccion_reuso.py::test_el_dominio_declara_sus_puertos_como_protocolos
FAILED pruebas/test_etapa3_abstraccion_reuso.py::test_los_puertos_hablan_el_idioma_del_dominio_y_no_el_del_proveedor
FAILED pruebas/test_etapa3_abstraccion_reuso.py::test_no_se_reinventa_lo_que_la_biblioteca_estandar_ya_resuelve
3 failed, 4 passed, 77 deselected in 0.06s
```

**Explicación:**

Todo La segunda no falló por una aserción, sino con FileNotFoundError, porque la prueba abre dominio/puertos.py directamente para leer los nombres que elegí.

El experimento del radio de impacto da 8 coincidencias, pero el número engaña: sólo 2 son del modelo del proveedor, legado.py:150 y legado.py:151, y las otras 6 son la palabra data dentro de dataclass. En el código vivo el radio ya era 0, no porque yo lo bajara en esta etapa sino porque al partir el monolito nunca copié buscar_paciente ni reporte. Repetido al cerrar, sigue en 0.

**Sello:** b7d3d0b694a6d420

Salida del marcador al cerrar la etapa:

```
Etapa 3  Abstracción y reuso                          verde
7 pruebas en verde · 0 por resolver
corrida #6 registrada
SELLO: b7d3d0b694a6d420
```

**Sello:**

## Etapa 4 — Flexibilidad, obsolescencia y portabilidad

**Predicción:**

Espero tres rojas: falta infraestructura/registro.py, falta clinicasegura/arranque.py y DEPENDENCIAS.md sigue con las celdas de la plantilla vacías. Las otras cuatro deberían pasar, porque el servicio ya busca la cadena en un diccionario y no la ramifica, no uso open en ninguna parte y las URLs sólo entran por el constructor de las pasarelas.

**Observación:**

```
$ pytest -m etapa4
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'clinicasegura.arranque'

During handling of the above exception, another exception occurred:
pruebas/test_etapa4_flexibilidad.py:152: in test_la_configuracion_entra_por_el_entorno
    importar("clinicasegura.arranque")
pruebas/apoyo.py:24: in importar
    pytest.fail(
E   Failed: Falta el módulo «clinicasegura.arranque».
E      Cree el archivo clinicasegura/arranque.py (y el __init__.py de su paquete).
E      Detalle: No module named 'clinicasegura.arranque'
____________ test_existe_la_tabla_de_obsolescencia_de_dependencias _____________
pruebas/test_etapa4_flexibilidad.py:202: in test_existe_la_tabla_de_obsolescencia_de_dependencias
    assert not vacias, "Filas incompletas en DEPENDENCIAS.md: " + ", ".join(vacias)
E   AssertionError: Filas incompletas en DEPENDENCIAS.md: pytest, pydantic, 
E   assert not ['pytest', 'pydantic', '']
=========================== short test summary info ============================
FAILED pruebas/test_etapa4_flexibilidad.py::test_se_agrega_una_cadena_nueva_sin_tocar_el_servicio
FAILED pruebas/test_etapa4_flexibilidad.py::test_la_configuracion_entra_por_el_entorno
FAILED pruebas/test_etapa4_flexibilidad.py::test_existe_la_tabla_de_obsolescencia_de_dependencias
3 failed, 4 passed, 77 deselected in 0.04s
```

**Explicación:**

Acerté: las tres rojas fueron exactamente las que dije, y por las razones que dije.

El principio 7 se resolvió con dos líneas de verdad. construir_registro, en registro.py:8, arma un diccionario indexado por el atributo cadena de cada pasarela, y el servicio hace un get sobre ese diccionario. La prueba define una cuarta cadena, FarmaViva, dentro del propio archivo de pruebas, la registra desde fuera y emite con ella sin que yo tocara servicio.py. Eso es lo que significa cerrado a modificación: la variación vive en un objeto nuevo, no en una rama nueva.

Para el 9 y el 8 escribí arranque.py, que es la raíz de composición y el único archivo que sabe a la vez de sqlite, de URLs y del sistema de archivos. Las tres URLs quedaron en una tupla en arranque.py:16 con su variable de entorno al lado, el timeout sale de FARMACIA_TIMEOUT_MS en arranque.py:23 y la ruta de la bitácora de tempfile.gettempdir en arranque.py:27, que es lo que reemplaza al C:\ClinicaSegura del código de partida. Lo probé: con FARMAUNO_URL apuntando a v4, construir_servicio en arranque.py:32 arma el servicio contra la versión nueva sin recompilar nada.

Llenar DEPENDENCIAS.md fue lo que más me hizo pensar, porque la columna de ruta de salida obliga a admitir cuánto cuesta cada dependencia. La fila incómoda es la de la API de FarmaUno: es la única de riesgo alto y la única cuya fecha de muerte no decido yo. Lo único que me protege es que la versión está en una variable de entorno y no incrustada en el código, como estaba en legado.py:31.

**Sello:** 5e2ec5fb67c00088

Salida del marcador al cerrar la etapa:

```
Etapa 4  Flexibilidad, obsolescencia y portabilidad   verde
7 pruebas en verde · 0 por resolver
corrida #7 registrada
SELLO: 5e2ec5fb67c00088
```

**Sello:**

## Etapa 5 — Testabilidad

**Predicción:**

Espero seis verdes y una sola roja, la de mis_pruebas, porque el constructor ya recibe pasarelas, reloj, folios y bitacora, y la vigencia ya sale del reloj inyectado desde la etapa 1.

**Observación:**

```
$ pytest -m etapa5
......F                                                                  [100%]
=================================== FAILURES ===================================
__________ test_el_estudiante_escribio_al_menos_tres_pruebas_propias ___________
pruebas/test_etapa5_testabilidad.py:174: in test_el_estudiante_escribio_al_menos_tres_pruebas_propias
    pytest.fail(
E   Failed: Falta la carpeta mis_pruebas/ con sus propias pruebas.
E      Escriba al menos tres que antes eran imposibles:
E        1) la vigencia con un reloj fijo,
E        2) la cadena caída (la pasarela lanza TimeoutError),
E        3) una receta inválida rechazada en el borde.
=========================== short test summary info ============================
FAILED pruebas/test_etapa5_testabilidad.py::test_el_estudiante_escribio_al_menos_tres_pruebas_propias
1 failed, 6 passed, 77 deselected in 0.02s
```

**Explicación:**

Correcto. La roja era la única que no se puede aprobar rediseñando: hay que escribir las pruebas.

Escribí ocho en mis_pruebas/test_emision.py. Las tres del enunciado son test_la_vigencia_sale_del_reloj_inyectado_y_no_del_sistema en test_emision.py:78, test_la_cadena_caida_se_propaga_como_error_de_dominio en test_emision.py:90 y test_el_borde_rechaza_una_receta_invalida en test_emision.py:106. Ninguna de las tres era escribible contra el código de partida: la primera habría exigido esperar treinta días, la segunda apagar una farmacia de verdad, y la tercera no habría fallado nunca porque el legado usaba assert.

**Sello:** e86d5ac61bb59ce8

Salida del marcador al cerrar la etapa:

```
Etapa 5  Testabilidad                                verde
7 pruebas en verde · 0 por resolver
corrida #8 registrada
SELLO: e86d5ac61bb59ce8
```

## Etapa 6 — Diseño defensivo

**Predicción:**

Espero siete rojas y cuatro verdes: faltan SolicitudReceta y a_receta con pydantic, y además mi servicio no registra la falla en la bitácora cuando la farmacia se cae. Eso último me choca con una prueba mía, que exige justo lo contrario, así que ahí tengo un conflicto que resolver y no sólo código que escribir.

**Observación:**

```
$ python -c "...emitir({dias: 0})"
    assert datos["dias"] > 0, "los dias deben ser positivos"
           ^^^^^^^^^^^^^^^^^
AssertionError: los dias deben ser positivos

$ python -O -c "...la misma linea"
(sigue corriendo despues de 8 segundos y hubo que matarlo)

$ pytest -m etapa6
E      Revise el contrato de la etapa en la guía.
____ test_si_la_farmacia_falla_se_propaga_un_error_de_dominio_con_contexto _____
pruebas/test_etapa6_defensa.py:147: in test_si_la_farmacia_falla_se_propaga_un_error_de_dominio_con_contexto
    assert bitacora.eventos, (
E   AssertionError: La falla no quedó registrada. Fallar rápido no significa fallar en silencio: se propaga Y se deja rastro.
E   assert []
E    +  where [] = <pruebas.test_etapa6_defensa.test_si_la_farmacia_falla_se_propaga_un_error_de_dominio_con_contexto.<locals>.Bitacora object at 0x10aa3f230>.eventos
=========================== short test summary info ============================
FAILED pruebas/test_etapa6_defensa.py::test_el_borde_acepta_lo_valido_y_lo_convierte_en_un_tipo_del_dominio
FAILED pruebas/test_etapa6_defensa.py::test_el_borde_rechaza_lo_invalido[cambio0-los d\xedas deben ser mayores que cero]
FAILED pruebas/test_etapa6_defensa.py::test_el_borde_rechaza_lo_invalido[cambio1-la vigencia m\xe1xima son 90 d\xedas]
FAILED pruebas/test_etapa6_defensa.py::test_el_borde_rechaza_lo_invalido[cambio2-la dosis debe ser positiva]
FAILED pruebas/test_etapa6_defensa.py::test_el_borde_rechaza_lo_invalido[cambio3-la c\xe9dula tiene formato 0-0000-0000]
FAILED pruebas/test_etapa6_defensa.py::test_el_borde_rechaza_campos_desconocidos
FAILED pruebas/test_etapa6_defensa.py::test_si_la_farmacia_falla_se_propaga_un_error_de_dominio_con_contexto
7 failed, 4 passed, 73 deselected in 0.06s
```

**Explicación:**

Correcto: siete rojas y cuatro verdes, y las cuatro que ya pasaban eran las de higiene, porque nunca copié el except con pass ni el while True del código de partida.

**Sello:** 9bc3437e6cc69620

Salida del marcador al cerrar la etapa:

```
Etapa 6  Diseño defensivo                            verde
11 pruebas en verde · 0 por resolver
corrida #9 registrada
SELLO: 9bc3437e6cc69620
```

**Sello:**

## Cierre — Los principios en conflicto

Nombre dos principios que se estorbaron entre sí en SU rediseño, y con qué
criterio resolvió el conflicto. Cite el archivo donde se ve la decisión.

**Conflicto 1:**

**Conflicto 2:**
