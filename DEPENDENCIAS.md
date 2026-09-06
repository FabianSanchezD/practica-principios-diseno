# Dependencias externas

Una fila por dependencia externa que el proyecto usa hoy, incluidas las de
la práctica. Complete las cuatro columnas: sin ruta de salida, la
dependencia es un compromiso indefinido.

| Dependencia | Versión acotada | Licencia | Riesgo | Ruta de salida |
|-------------|-----------------|----------|--------|----------------|
| pytest | >=8.0, instalada 9.1.1 | MIT | Bajo: sólo desarrollo, no viaja a producción | Las pruebas son funciones planas con assert; migrar a unittest no toca el código de clinicasegura |
| pydantic | >=2.6, instalada 2.13.5 | MIT | Medio: la v1 y la v2 rompieron compatibilidad, puede volver a pasar; hoy está declarada pero todavía no se importa | Entra sólo en aplicacion/borde.py:12; sustituirla por dataclasses más re dejaría intacto el dominio |
| urllib.request | Biblioteca estándar de Python 3.14 | PSF | Medio: no reintenta ni agrupa conexiones, y obliga a escribir eso a mano | Está encapsulada en infraestructura/pasarelas.py; cambiar a httpx toca ese archivo y ninguno más |
| sqlite3 | Biblioteca estándar de Python 3.14 | PSF | Medio: un archivo local no sirve si la clínica escala a varias instancias | La bitácora es el puerto Bitacora en puertos.py:24; basta otro adaptador para Postgres |
| Python | 3.14, mínimo 3.10 por los tipos con barra vertical | PSF | Bajo: cada versión tiene cinco años de soporte | Fijar la versión en pyproject y probar en la siguiente antes de que la actual llegue a su fin de vida |
| API de FarmaUno | v3, fijada en arranque.py:17 | Contrato comercial, no abierta | Alto: la versión está en la URL y el proveedor decide cuándo apagarla | La URL entra por la variable FARMAUNO_URL; migrar a v4 es cambiar el entorno, no el código |
