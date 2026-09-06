# Diagnóstico del código de partida

Lea `clinicasegura/legado.py` entero antes de escribir una sola línea de
código nuevo. Llene una fila por principio. En la columna de evidencia
cite **archivo y línea** (por ejemplo `legado.py:38`); una fila sin
evidencia no cuenta.

Si cree que un principio **no** está violado, escriba la fila igual y
explique por qué en la columna de hallazgo.

| # | Principio | Hallazgo concreto | Evidencia (archivo:línea) | Qué cuesta si no se corrige |
|---|-----------|-------------------|---------------------------|------------------------------|
| 1 | Dividir y conquistar | Una sola clase es todo el módulo, y un solo método valida, calcula el recargo, arma el JSON, habla HTTP, escribe en sqlite y actualiza dos globales | legado.py:44, legado.py:57 | Nada se puede leer, probar ni cambiar por partes |
| 2 | Aumentar la cohesión | Cohesión es coincidental porque emitir, buscar_paciente, reporte, validar_cedula y exportar no comparten datos ni motivo de cambio, sólo el nombre de la clase | legado.py:137, legado.py:146, legado.py:154, legado.py:169 | Cinco razones para modificar el mismo archivo, y cinco oportunidades de romper algo que no debería de romper |
| 3 | Reducir el acoplamiento | Común por CONFIG y CACHE_PACIENTES globales mutables, de control por el parámetro cadena que elige la rama, y de estampado en reporte, que recibe el paciente entero para usar dos campos | legado.py:30, legado.py:39, legado.py:146 | Cambiar vigencia_dias altera el comportamiento de todo el proceso sin que ninguna firma lo declare |
| 4 | Mantener alta la abstracción | Devuelve un diccionario sin contrato, con las llaves que el llamador tiene que adivinar, y hace circular el JSON crudo del proveedor por todo el sistema | legado.py:110, legado.py:150 | Si el tercero renombra full_name se rompe cada archivo que leyó ese JSON |
| 5 | Aumentar la reusabilidad | _post no es reusable fuera de esta clase: lee el timeout de la global CONFIG en vez de recibirlo, así que no se puede llevar a otro contexto | legado.py:119, legado.py:129 | La única pieza genuinamente genérica del archivo queda amarrada a un diccionario global |
| 6 | Reusar lo existente | validar_cedula reimplementa a mano, con comparaciones de caracteres, lo que resuelven re o str.isdigit; el folio se arma con random en vez de uuid | legado.py:154, legado.py:69 | Código propio que hay que mantener y probar para algo que la biblioteca estándar ya garantiza |
| 7 | Diseñar para la flexibilidad | La variación vive en una cadena de if por nombre de cadena, dentro del mismo método que orquesta | legado.py:79 | Cada farmacia nueva obliga a abrir y editar el método central, con riesgo de romper las tres que ya funcionaban |
| 8 | Anticipar la obsolescencia | Tres URLs de terceros con la versión incrustada en el literal y sin ninguna ruta de salida documentada | legado.py:31, legado.py:32, legado.py:33 | Cuando FarmaUno apague v3 el sistema deja de emitir y no hay plan escrito de migración |
| 9 | Diseñar para la portabilidad | Ruta absoluta de Windows como valor por omisión, apertura de archivo sin codificación explícita, y /tmp incrustado para la base de datos | legado.py:169, legado.py:50 | No corre igual en Windows, Linux y macOS, y los acentos se escriben distinto según la máquina |
| 10 | Diseñar para la testabilidad | Los cuatro enemigos juntos: reloj incrustado, azar incrustado, conexión sqlite construida dentro del constructor y estado global compartido | legado.py:66, legado.py:69, legado.py:50 | No se puede probar la vigencia sin esperar treinta días ni el folio sin adivinar el azar |
| 11 | Diseñar defensivamente | Aserciones sobre datos que vienen del formulario, un except Exception con pass que se traga el fallo de la bitácora, un return None para la cadena desconocida y un return -1 en vez de lanzar | legado.py:62, legado.py:103, legado.py:95, legado.py:135 | Con python -O las validaciones desaparecen y la receta inválida se emite igual, callada |
