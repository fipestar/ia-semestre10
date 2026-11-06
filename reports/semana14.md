
# Semana 14 – Ingeniería del conocimiento
## Redes semánticas, triples e inferencia por jerarquía

**Asignatura:** Inteligencia Artificial  
**Proyecto:** Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero  
**Modalidad:** Individual  
**Fecha:** 6 de noviembre de 2026

---

## 1. Introducción

Durante la Semana 14 se desarrolló una red semántica aplicada al proyecto de reconocimiento y reposición de inventario ferretero.

El propósito fue representar conocimiento mediante conceptos, relaciones y triples semánticos, permitiendo realizar consultas e inferir información que no estuviera almacenada directamente.

La implementación se realizó en Python e incluye normalización de texto, interpretación de oraciones simples, construcción de un grafo dirigido, inferencia mediante jerarquías y herencia de propiedades.

Adicionalmente, se desarrollaron pruebas unitarias mediante `unittest` para verificar el funcionamiento del sistema.

Esta actividad complementa los mecanismos de representación del conocimiento y razonamiento lógico implementados anteriormente en el proyecto.

---

## 2. Análisis del dominio

### 2.1. Problema identificado

En una ferretería existen diferentes tipos de productos organizados en categorías y subcategorías.

Por ejemplo, una caja eléctrica puede considerarse un accesorio eléctrico, que a su vez pertenece a una categoría más general de materiales eléctricos.

Estas relaciones permiten organizar los productos y obtener información sobre características compartidas.

Sin embargo, cuando las relaciones se almacenan de manera independiente, puede ser necesario consultar varios niveles de la jerarquía para determinar la categoría general de un producto.

Por esta razón, se implementó una red semántica capaz de representar relaciones entre conceptos ferreteros e inferir información a partir de dichas relaciones.

### 2.2. Funcionalidad seleccionada

La funcionalidad desarrollada consiste en:

1. Interpretar oraciones simples relacionadas con productos.
2. Convertir las oraciones en triples semánticos.
3. Almacenar conceptos y relaciones en una red dirigida.
4. Consultar relaciones explícitas.
5. Inferir relaciones jerárquicas mediante transitividad.
6. Obtener propiedades heredadas de categorías superiores.
7. Identificar consultas que no pueden demostrarse.

### 2.3. Conceptos utilizados

Se seleccionaron ocho conceptos principales del dominio:

| Concepto | Descripción |
|---|---|
| `caja_5800` | Tipo de caja eléctrica utilizado como ejemplo del inventario. |
| `caja_electrica` | Categoría que agrupa cajas para instalaciones eléctricas. |
| `conector_rapido` | Tipo de conector utilizado en instalaciones eléctricas. |
| `conector_electrico` | Categoría de conectores eléctricos. |
| `accesorio_electrico` | Categoría general de accesorios eléctricos. |
| `material_electrico` | Categoría superior que agrupa materiales eléctricos. |
| `producto_ferretero` | Categoría general de productos comercializados en una ferretería. |
| `control_stock` | Concepto que representa la necesidad de controlar existencias. |

Estos conceptos permiten construir relaciones jerárquicas y representar una propiedad general del inventario.

---

## 3. Modelado del conocimiento

### 3.1. Triples semánticos

Un triple semántico representa una relación entre dos conceptos mediante la estructura:

```text
(sujeto, relación, objeto)
```

Donde:

- **Sujeto:** concepto desde el que parte la relación.
- **Relación:** vínculo semántico entre conceptos.
- **Objeto:** concepto hacia el cual se dirige la relación.

Por ejemplo:

```text
(caja_5800, es_un, caja_electrica)
```

Este triple representa que una caja 5800 pertenece a la categoría de cajas eléctricas.

### 3.2. Relaciones utilizadas

Se implementaron dos relaciones principales:

| Relación | Significado |
|---|---|
| `es_un` | Representa pertenencia a una categoría o jerarquía de tipos. |
| `requiere` | Representa una propiedad o requisito asociado a un concepto. |

La relación `es_un` admite inferencia por transitividad.

La relación `requiere` permite heredar propiedades desde categorías superiores, según las reglas definidas en el prototipo.

No todas las relaciones se consideran transitivas o heredables automáticamente.

### 3.3. Triples registrados

Durante la ejecución se almacenaron los siguientes siete triples:

```text
(caja_5800, es_un, caja_electrica)

(caja_electrica, es_un, accesorio_electrico)

(conector_rapido, es_un, conector_electrico)

(conector_electrico, es_un, accesorio_electrico)

(accesorio_electrico, es_un, material_electrico)

(material_electrico, es_un, producto_ferretero)

(producto_ferretero, requiere, control_stock)
```

Los primeros seis triples representan relaciones jerárquicas.

El último establece una propiedad asociada con la categoría general `producto_ferretero`.

---

## 4. Interpretación de oraciones

### 4.1. Normalización lingüística

Antes de convertir una oración en un triple, el sistema realiza un proceso de normalización.

Este proceso busca reducir diferencias de escritura que puedan dificultar la identificación de los conceptos.

Entre las operaciones implementadas se encuentran:

- Conversión a minúsculas.
- Eliminación de tildes.
- Normalización de espacios y términos.
- Conversión de expresiones a identificadores consistentes.

Por ejemplo:

```text
"Caja Eléctrica" → "caja_electrica"
```

La normalización facilita las comparaciones entre conceptos dentro de la red.

### 4.2. Identificación de sujeto, relación y objeto

El sistema interpreta oraciones sencillas con estructuras previamente definidas.

Ejemplo:

```text
Una caja 5800 es una caja eléctrica.
```

Resultado:

```python
("caja_5800", "es_un", "caja_electrica")
```

Otro ejemplo:

```text
Un producto ferretero requiere control stock.
```

Resultado:

```python
("producto_ferretero", "requiere", "control_stock")
```

Estos resultados pueden almacenarse como relaciones dirigidas dentro de la red semántica.

### 4.3. Validación de oraciones

El sistema también identifica expresiones que no corresponden a los patrones admitidos.

Cuando una oración no puede interpretarse, se genera un error controlado mediante `ValueError`.

Durante la ejecución se obtuvo:

```text
ValueError: Oracion no admitida: use 'Un X es un Y' o 'Un X requiere Y'
```

Esto evita incorporar relaciones incorrectas cuando la estructura lingüística no puede interpretarse.

El sistema no comprende cualquier oración en español; solamente procesa las estructuras programadas.

---

## 5. Construcción de la red semántica

La red se implementó mediante nodos y aristas dirigidas.

Los nodos representan conceptos del inventario ferretero.

Las aristas representan las relaciones entre dichos conceptos.

Por ejemplo:

```text
caja_5800
    |
   es_un
    |
    v
caja_electrica
    |
   es_un
    |
    v
accesorio_electrico
    |
   es_un
    |
    v
material_electrico
    |
   es_un
    |
    v
producto_ferretero
    |
  requiere
    |
    v
control_stock
```

La dirección de las relaciones es importante, porque permite distinguir qué concepto pertenece a una categoría superior y qué propiedad está asociada con dicha categoría.

### 5.1. Consulta de relaciones explícitas

El sistema permite consultar las relaciones almacenadas directamente para un concepto.

Durante la ejecución se consultó:

```text
Relaciones de caja_5800:
[('es_un', 'caja_electrica')]
```

Este resultado indica que existe una relación explícita entre `caja_5800` y `caja_electrica`.

No es necesario realizar inferencia para obtener esta información, porque el triple fue registrado directamente.

---

## 6. Inferencia por jerarquía

### 6.1. Transitividad de `es_un`

La transitividad permite deducir una relación jerárquica indirecta a partir de varias relaciones existentes.

Por ejemplo, si:

```text
A es_un B
B es_un C
```

Entonces puede inferirse:

```text
A es_un C
```

En nuestro proyecto:

```text
caja_5800 es_un caja_electrica

caja_electrica es_un accesorio_electrico

accesorio_electrico es_un material_electrico

material_electrico es_un producto_ferretero
```

Por transitividad puede concluirse:

```text
caja_5800 es_un producto_ferretero
```

Esta relación no se almacenó directamente.

Fue obtenida mediante el recorrido de la jerarquía.

### 6.2. Resultado de ejecución

La consulta realizada fue:

```text
¿caja_5800 es_un producto_ferretero?: True
```

Y la traza generada fue:

```text
caja_5800
    -> caja_electrica
    -> accesorio_electrico
    -> material_electrico
    -> producto_ferretero
```

El resultado demuestra que existe un camino jerárquico entre ambos conceptos.

### 6.3. Diferencia entre conocimiento explícito e inferido

**Conocimiento explícito:**

```text
(caja_5800, es_un, caja_electrica)
```

Esta relación fue agregada directamente.

**Conocimiento inferido:**

```text
(caja_5800, es_un, producto_ferretero)
```

Esta relación se obtiene recorriendo varias conexiones jerárquicas.

La inferencia permite obtener conocimiento sin necesidad de almacenar directamente todas las relaciones posibles.

---

## 7. Herencia de propiedades

La herencia permite que un concepto específico reciba determinadas propiedades de una categoría superior.

En nuestro modelo se registró:

```text
(producto_ferretero, requiere, control_stock)
```

Esta relación representa que los productos ferreteros requieren control de existencias dentro del modelo definido.

Como `caja_5800` pertenece indirectamente a `producto_ferretero`, el sistema puede inferir que también requiere control de stock.

### 7.1. Resultado obtenido

La salida del programa fue:

```text
caja_5800 requiere control_stock:
heredada de producto_ferretero
```

La traza fue:

```text
caja_5800
    -> caja_electrica
    -> accesorio_electrico
    -> material_electrico
    -> producto_ferretero
    --requiere--> control_stock
```

La propiedad no estaba vinculada directamente con `caja_5800`.

Fue heredada desde una categoría superior de acuerdo con la regla de herencia definida en el programa.

### 7.2. Limitación de la herencia

No todas las propiedades de una categoría pueden heredarse automáticamente.

Algunas características pueden depender de productos específicos o presentar excepciones.

Por esta razón, la herencia debe aplicarse únicamente cuando la semántica de la relación lo permita.

---

## 8. Consultas sin evidencia

El sistema también permite comprobar relaciones que no pueden demostrarse con los triples disponibles.

Durante la ejecución se realizó la siguiente consulta:

```text
¿caja_5800 es_un conector_electrico?: False
```

El resultado fue `False` porque no existe un camino mediante relaciones `es_un` que conecte `caja_5800` con `conector_electrico`.

Sin embargo, es importante diferenciar la ausencia de evidencia de una negación universal.

En este caso, `False` significa que la relación no puede demostrarse con la información almacenada en la red.

No significa que el programa tenga conocimiento completo de todas las posibles relaciones del mundo real.

---

## 9. Prevención de ciclos infinitos

Para evitar ciclos infinitos durante las consultas, la implementación utiliza un conjunto de nodos visitados.

Cuando el algoritmo recorre una jerarquía, registra los conceptos que ya fueron procesados.

Si vuelve a encontrar un nodo visitado, evita procesarlo nuevamente.

Este mecanismo permite que las consultas terminen incluso cuando existan relaciones circulares.

Por ejemplo:

```text
A es_un B
B es_un C
C es_un A
```

Sin control de nodos visitados, un recorrido podría repetirse indefinidamente.

En nuestro programa, el conjunto `visitados` evita esta situación.

Aunque el algoritmo puede gestionar ciclos durante la búsqueda, una jerarquía circular puede representar un error conceptual del dominio y debería revisarse.

---

## 10. Resultados de la ejecución

Se ejecutó el archivo principal `main.py` para demostrar el funcionamiento de la red semántica.

### 10.1. Hechos explícitos

La ejecución convirtió siete oraciones relacionadas con el inventario ferretero en triples semánticos.

Ejemplo:

```text
Una caja 5800 es una caja eléctrica.
    -> ('caja_5800', 'es_un', 'caja_electrica')
```

### 10.2. Consultas e inferencias

| Operación | Resultado |
|---|---|
| Relaciones directas de `caja_5800` | `es_un caja_electrica` |
| Jerarquía de `caja_5800` hasta `producto_ferretero` | `True` |
| Propiedad heredada | `requiere control_stock` |
| Consulta `caja_5800 es_un conector_electrico` | `False` |
| Oración inválida | `ValueError` |

Los resultados muestran que la red permite distinguir entre relaciones almacenadas, conclusiones inferidas y consultas sin evidencia suficiente.

---

## 11. Pruebas unitarias

Se implementó el archivo:

```text
test_red_semantica.py
```

Para verificar el funcionamiento se utilizó `unittest`, incluido en la biblioteca estándar de Python.

### 11.1. Pruebas realizadas

| Prueba | Objetivo | Resultado |
|---|---|---|
| Ciclo no infinito | Verificar la terminación ante jerarquías circulares | OK |
| Concepto desconocido | Comprobar consultas sobre conceptos no registrados | OK |
| Herencia con traza | Comprobar propiedades heredadas y explicación del recorrido | OK |
| Triples duplicados | Evitar almacenar relaciones idénticas varias veces | OK |
| Normalización | Verificar conversión de términos a identificadores uniformes | OK |
| Oración inválida | Rechazar entradas fuera de los patrones admitidos | OK |
| Parser `es_un` | Interpretar correctamente relaciones jerárquicas | OK |
| Parser `requiere` | Interpretar correctamente relaciones de propiedades | OK |
| Relación inválida | Rechazar predicados no admitidos | OK |
| Relaciones no jerárquicas | Evitar tratar todas las relaciones como `es_un` | OK |
| Sin evidencia | Comprobar una relación que no puede demostrarse | OK |
| Transitividad con traza | Comprobar la inferencia jerárquica y su explicación | OK |
| Triple explícito y consulta | Verificar almacenamiento y recuperación de relaciones | OK |

### 11.2. Salida real de las pruebas

La ejecución proporcionó el siguiente resumen:

```text
Ran 13 tests in 0.010s

OK
```

Las trece pruebas finalizaron satisfactoriamente.

Esto permite verificar los comportamientos implementados en el prototipo, aunque no sustituye la validación conceptual de la taxonomía utilizada.

---

## 12. Relación con el proyecto semestral

La red semántica se relaciona con el Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero.

Durante las semanas anteriores se desarrollaron mecanismos para:

- Representar información mediante vectores y símbolos.
- Clasificar situaciones de inventario con redes neuronales.
- Procesar imágenes mediante algoritmos de visión artificial.
- Extraer características visuales.
- Comparar modelos de aprendizaje automático.
- Obtener conclusiones a partir de reglas lógicas.

La Semana 14 incorpora una representación jerárquica de conceptos y permite inferir relaciones entre categorías.

Por ejemplo, en una futura integración, el reconocimiento visual podría identificar un producto específico.

La red semántica podría utilizarse después para determinar su categoría general y consultar propiedades asociadas.

Esto ayudaría a organizar el conocimiento del sistema y facilitar consultas sobre distintos tipos de productos.

Actualmente, la red funciona como un prototipo independiente y todavía no está conectada automáticamente con el sistema de reconocimiento visual ni con la base de datos del inventario.

---

## 13. Limitaciones encontradas

### 13.1. Interpretación lingüística limitada

El programa reconoce únicamente ciertos patrones de oraciones sencillas.

No interpreta libremente cualquier expresión en español.

Tampoco procesa adecuadamente todas las posibles variaciones gramaticales, negaciones o ambigüedades.

### 13.2. Número limitado de conceptos

La red utiliza ocho conceptos principales del proyecto.

Una ferretería real puede manejar cientos o miles de productos y una taxonomía mucho más compleja.

### 13.3. Relaciones definidas manualmente

Las relaciones utilizadas fueron creadas explícitamente para la práctica.

El sistema no descubre automáticamente nuevas categorías ni aprende relaciones a partir de datos históricos.

### 13.4. Herencia simplificada

La propagación de propiedades sigue reglas establecidas para este prototipo.

En un sistema real sería necesario comprobar qué propiedades pueden heredarse y cuáles requieren condiciones adicionales.

### 13.5. Ausencia de integración automática

La red semántica no se encuentra conectada directamente con los demás componentes del proyecto.

Los triples utilizados son introducidos durante la ejecución de la demostración.

### 13.6. Validación del conocimiento

Las pruebas verifican el funcionamiento técnico de la red, pero no garantizan que todas las categorías y relaciones correspondan exactamente a la clasificación comercial utilizada por una ferretería real.

---

## 14. Aplicaciones futuras

La red semántica podría ampliarse mediante:

1. Integración con el catálogo real de productos.
2. Incorporación de categorías y subcategorías comerciales.
3. Relaciones con proveedores y tipos de materiales.
4. Consultas semánticas sobre productos.
5. Asociación con resultados del reconocimiento visual.
6. Ampliación de los patrones lingüísticos admitidos.
7. Validación de propiedades heredadas.
8. Integración con el motor de inferencia de la Semana 13.

Estas mejoras permitirían desarrollar un sistema de inventario con información más estructurada y relaciones interpretables.

---

## 15. Archivos desarrollados y ejecución

Los archivos de la práctica se encuentran organizados de la siguiente manera:

```text
src/
└── semana14/
    ├── red_semantica.py
    ├── main.py
    └── test_red_semantica.py

reports/
└── reporte_semana14.md
```

### 15.1. Ejecutar el programa principal

Desde la raíz del repositorio:

```bash
python src/semana14/main.py
```

Este comando permite:

- Cargar las oraciones.
- Generar y almacenar triples.
- Consultar relaciones explícitas.
- Demostrar inferencias jerárquicas.
- Obtener propiedades heredadas.
- Comprobar una consulta sin evidencia.
- Mostrar el manejo de una oración inválida.

### 15.2. Ejecutar pruebas automáticas

```bash
python -m unittest discover -s src/semana14 -p "test_red_semantica.py" -v
```

El resultado obtenido fue de trece pruebas correctas.

---

## 16. Conclusiones

La práctica de la Semana 14 permitió implementar una red semántica aplicada a conceptos relacionados con el inventario ferretero.

Se seleccionaron ocho conceptos y se representaron siete relaciones explícitas mediante triples de sujeto, relación y objeto.

La implementación permitió interpretar oraciones sencillas, normalizar expresiones y registrar relaciones dentro de un grafo dirigido.

Mediante la transitividad de `es_un`, se demostró que `caja_5800` pertenece indirectamente a la categoría `producto_ferretero`.

También se implementó herencia de propiedades, permitiendo concluir que `caja_5800` requiere control de stock a partir de una propiedad registrada en una categoría superior.

Las trece pruebas unitarias finalizaron correctamente y verificaron aspectos como normalización, interpretación, inferencia, manejo de ciclos, duplicados y entradas inválidas.

Finalmente, la actividad permitió diferenciar entre conocimiento explícito e inferido, demostrando que las redes semánticas pueden utilizarse para representar y consultar información estructurada dentro de un dominio específico.

Esta implementación constituye una base para integrar conocimiento jerárquico y razonamiento explicable en el proyecto de inventario ferretero.

---

## 17. Referencias

- Material docente: *Explicación de la Semana 14 – Inteligencia Artificial: Redes semánticas*.
- Material docente: *IA Semana 14 – Redes semánticas*.
- Código fuente del proyecto: `red_semantica.py`.
- Programa de demostración: `main.py`.
- Pruebas unitarias: `test_red_semantica.py`.
- Python Software Foundation: documentación de `re`, `unicodedata` y `unittest`.
