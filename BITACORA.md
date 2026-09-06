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

**Observación:**

```
```

**Explicación:**

**Sello:**

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

**Observación:**

```
```

**Explicación:**

**Sello:**

## Etapa 3 — Abstracción y reuso

**Predicción:**

**Observación:**

```
```

**Explicación:**

**Sello:**

## Etapa 4 — Flexibilidad, obsolescencia y portabilidad

**Predicción:**

**Observación:**

```
```

**Explicación:**

**Sello:**

## Etapa 5 — Testabilidad

**Predicción:**

**Observación:**

```
```

**Explicación:**

**Sello:**

## Etapa 6 — Diseño defensivo

**Predicción:**

**Observación:**

```
```

**Explicación:**

**Sello:**

## Cierre — Los principios en conflicto

Nombre dos principios que se estorbaron entre sí en SU rediseño, y con qué
criterio resolvió el conflicto. Cite el archivo donde se ve la decisión.

**Conflicto 1:**

**Conflicto 2:**
