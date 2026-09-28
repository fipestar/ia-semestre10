# Semana 08 - Representaciones del reconocimiento

## Proyecto

**Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero**

## Objetivo

Implementar un flujo completo de reconocimiento aplicado al proyecto de inventario ferretero mediante tres componentes:

1. Una red neuronal artificial encargada de realizar una clasificación.
2. Una base de datos encargada de registrar evidencia de las predicciones.
3. Una ontología encargada de representar el significado de los resultados dentro del dominio del inventario.

El flujo implementado es:

```text
Entrada
  ↓
Modelo de reconocimiento
  ↓
Predicción
  ↓
Registro de evidencia
  ↓
Ontología / significado
```

La intención no es solamente obtener una predicción, sino conservar evidencia del proceso y relacionar el resultado con conceptos propios del proyecto.

---

# 1. Modelo de reconocimiento

Para el reconocimiento se utilizó una red neuronal artificial mediante `MLPClassifier`.

El objetivo del modelo es clasificar el estado de inventario de un producto utilizando tres características numéricas:

```text
[stock_actual, stock_minimo, ventas_semanales]
```

Las clases utilizadas fueron:

```text
stock_normal
reposicion
prioridad
agotado
```

Por ejemplo:

```text
[20, 10, 8] → stock_normal
[7, 12, 9]  → reposicion
[4, 10, 25] → prioridad
[0, 5, 7]   → agotado
```

El modelo recibe las características numéricas del producto y aprende patrones asociados con cada una de las categorías.

---

# 2. Datos utilizados

Se utilizaron 20 ejemplos relacionados con situaciones de inventario.

Cada registro contiene:

```text
stock_actual
stock_minimo
ventas_semanales
```

Se utilizaron cinco ejemplos para cada categoría:

- 5 ejemplos de `stock_normal`.
- 5 ejemplos de `reposicion`.
- 5 ejemplos de `prioridad`.
- 5 ejemplos de `agotado`.

Los datos fueron separados utilizando:

```python
train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)
```

La distribución obtenida fue:

```text
Datos totales:          20
Datos de entrenamiento: 15
Datos de prueba:         5
```

Esto permite que el modelo aprenda utilizando una parte de los datos y posteriormente sea evaluado con ejemplos que no utilizó durante el entrenamiento.

El uso de `stratify=y` ayuda a mantener representación de las distintas clases durante la división de los datos.

---

# 3. Red neuronal utilizada

El modelo fue definido mediante:

```python
model = MLPClassifier(
    hidden_layer_sizes=(16,),
    max_iter=1000,
    random_state=42
)
```

La red utiliza una capa oculta de 16 neuronas.

El proceso general es:

```text
stock_actual
stock_minimo
ventas_semanales
        ↓
  RED NEURONAL MLP
        ↓
estado de inventario
```

El entrenamiento se realiza mediante:

```python
model.fit(X_train, y_train)
```

Después del entrenamiento se generan predicciones utilizando:

```python
pred = model.predict(X_test)
```

La red no recibe reglas escritas manualmente como:

```text
SI stock = 0 ENTONCES agotado
```

En cambio, recibe ejemplos con su categoría correcta e intenta aprender patrones a partir de ellos.

---

# 4. Validación del modelo

Para evaluar el modelo se utilizó la métrica `accuracy`.

El resultado obtenido fue:

```text
Accuracy: 1.0
```

Esto equivale a:

```text
100 % de predicciones correctas
```

sobre los cinco ejemplos utilizados en la prueba.

Las predicciones obtenidas fueron:

| Entrada | Categoría real | Predicción |
|---|---|---|
| `[0, 5, 7]` | agotado | agotado |
| `[15, 8, 5]` | stock_normal | stock_normal |
| `[7, 12, 9]` | reposicion | reposicion |
| `[5, 10, 6]` | reposicion | reposicion |
| `[3, 10, 30]` | prioridad | prioridad |

En este experimento el modelo clasificó correctamente los cinco ejemplos reservados para prueba.

Sin embargo, un accuracy de `1.0` no significa que el sistema sea perfecto, ya que el conjunto utilizado es pequeño y únicamente contiene 20 ejemplos.

El resultado demuestra que el modelo logró reconocer correctamente los patrones incluidos en este experimento, pero serían necesarios más datos reales para evaluar su comportamiento en situaciones de inventario más variadas.

---

# 5. Modelo entrenado

Después del entrenamiento, el modelo se guarda utilizando `pickle`.

El archivo generado es:

```text
artifacts/modelo_inventario_mlp.pkl
```

Este archivo contiene el modelo entrenado y permite conservarlo para reutilizarlo posteriormente sin necesidad de volver a entrenarlo desde cero.

---

# 6. Registro de evidencia mediante SQLite

Para que las predicciones no existan únicamente durante la ejecución del programa, se creó una base de datos SQLite.

El archivo generado es:

```text
artifacts/inventario_reconocimiento.db
```

La tabla utilizada se llama:

```text
predicciones
```

y contiene los siguientes campos:

| Campo | Descripción |
|---|---|
| `id` | Identificador del registro |
| `stock_actual` | Cantidad actual de unidades |
| `stock_minimo` | Cantidad mínima definida |
| `ventas_semanales` | Cantidad de unidades vendidas semanalmente |
| `categoria_real` | Categoría correcta del ejemplo |
| `prediccion` | Resultado generado por la red neuronal |
| `fecha` | Fecha y hora de registro |

La base de datos permite conservar evidencia de:

```text
Entrada analizada
        ↓
Categoría real
        ↓
Predicción generada
        ↓
Fecha del proceso
```

Por ejemplo, un registro puede representar:

```text
stock_actual = 7
stock_minimo = 12
ventas_semanales = 9
categoria_real = reposicion
prediccion = reposicion
```

Esto permite revisar posteriormente qué información fue procesada y cuál fue el resultado generado por el modelo.

---

# 7. Ontología del proyecto

También se creó una representación del conocimiento mediante una ontología implementada como un grafo dirigido utilizando NetworkX.

El archivo generado es:

```text
artifacts/ontologia_inventario.graphml
```

La ontología utiliza conceptos directamente relacionados con el proyecto.

Entre los conceptos definidos se encuentran:

```text
producto
observacion_inventario
modelo_mlp
prediccion_inventario
estado_inventario
reposicion
```

Estos conceptos representan diferentes elementos relacionados con el proceso de reconocimiento y reposición de inventario.

---

# 8. Relaciones de la ontología

Se definieron relaciones con significado dentro del dominio.

Entre las relaciones principales se encuentran:

```text
producto
    → tiene_estado
    → estado_inventario
```

```text
observacion_inventario
    → describe
    → producto
```

```text
modelo_mlp
    → analiza
    → observacion_inventario
```

```text
modelo_mlp
    → produce
    → prediccion_inventario
```

```text
prediccion_inventario
    → asigna_estado
    → estado_inventario
```

```text
estado_inventario
    → puede_requerir
    → reposicion
```

Estas relaciones pueden leerse como frases:

- Un producto tiene un estado de inventario.
- Una observación de inventario describe un producto.
- El modelo MLP analiza una observación de inventario.
- El modelo MLP produce una predicción de inventario.
- Una predicción asigna un estado de inventario.
- Un estado de inventario puede requerir reposición.

Esto permite que el resultado del modelo tenga un significado dentro del contexto del proyecto.

---

# 9. Integración de una predicción con la ontología

Para demostrar la integración completa se utilizó la siguiente entrada:

```text
[4, 10, 25]
```

Esto representa:

```text
Stock actual: 4
Stock mínimo: 10
Ventas semanales: 25
```

La red neuronal realizó la siguiente predicción:

```text
prioridad
```

Después, esta predicción fue relacionada con la ontología.

Se generaron las relaciones:

```text
observacion_1
    → genera
    → prediccion_1
```

```text
prediccion_1
    → asigna_estado
    → estado_prioridad
```

```text
observacion_1
    → describe
    → producto
```

Por lo tanto, el flujo completo puede representarse de la siguiente forma:

```text
Observación
[4, 10, 25]
      ↓
Modelo MLP
      ↓
Predicción
prioridad
      ↓
Registro en base de datos
      ↓
Ontología
prediccion_1
      ↓ asigna_estado
estado_prioridad
```

Esto permite pasar de una entrada puramente numérica a un resultado con significado dentro del dominio del inventario.

---

# 10. Relaciones generadas

Después de agregar las relaciones generales y las correspondientes al ejemplo de integración, la ontología quedó con:

```text
Relaciones de ontología: 9
```

Estas relaciones representan tanto conocimiento general del dominio como información asociada con una predicción concreta.

---

# 11. Flujo completo del sistema

El desarrollo de la Semana 8 puede resumirse de la siguiente manera:

```text
1. Se definen 20 ejemplos de inventario.
        ↓
2. Se dividen entre entrenamiento y prueba.
        ↓
3. La red neuronal aprende los patrones.
        ↓
4. El modelo clasifica los datos de prueba.
        ↓
5. Se calcula el accuracy.
        ↓
6. Se guarda el modelo entrenado.
        ↓
7. SQLite registra evidencia de las predicciones.
        ↓
8. Se construye una ontología del inventario.
        ↓
9. Una predicción concreta se relaciona con la ontología.
        ↓
10. El resultado queda representado como conocimiento del dominio.
```

En forma resumida:

```text
MODELO
reconoce

BASE DE DATOS
registra

ONTOLOGÍA
interpreta
```

---

# 12. Limitaciones

La implementación realizada tiene varias limitaciones.

## Cantidad de datos

El modelo únicamente fue entrenado utilizando 20 ejemplos.

Aunque el resultado obtenido fue un accuracy de `1.0`, el conjunto de prueba solamente contiene cinco observaciones.

Por esta razón, el resultado no puede interpretarse como evidencia de que el modelo clasificará correctamente cualquier producto real de la ferretería.

## Datos definidos manualmente

Los ejemplos utilizados fueron construidos para la práctica y todavía no provienen directamente de datos históricos reales del sistema de inventario.

En una versión futura sería conveniente utilizar información real de productos, ventas y movimientos de inventario.

## Características limitadas

Actualmente el modelo utiliza únicamente:

```text
stock_actual
stock_minimo
ventas_semanales
```

En un sistema más completo podrían considerarse otras características como:

- Rotación histórica.
- Tiempo desde la última compra.
- Demanda promedio.
- Proveedor.
- Criticidad del producto.
- Tiempo de entrega del proveedor.
- Stock objetivo.

## Clasificación simplificada

Las categorías:

```text
stock_normal
reposicion
prioridad
agotado
```

simplifican situaciones reales que pueden ser más complejas.

## Ontología básica

La ontología construida representa los conceptos principales necesarios para la práctica, pero podría ampliarse incluyendo productos específicos, proveedores, categorías, niveles de prioridad y decisiones de reposición.

---

# 13. Archivos generados

Al ejecutar:

```text
python src/semana08_RedOntologia.py
```

se generan los siguientes artefactos:

```text
artifacts/
├── modelo_inventario_mlp.pkl
├── inventario_reconocimiento.db
└── ontologia_inventario.graphml
```

Además, el proyecto contiene:

```text
src/
└── semana08_RedOntologia.py

reports/
└── semana08.md
```

---

# 14. Resultado obtenido

La ejecución realizada produjo:

```text
=== RED NEURONAL ===
Datos de entrenamiento: 15
Datos de prueba: 5
Accuracy: 1.0

=== PREDICCIONES ===
Entrada: [0, 5, 7] | Real: agotado | Predicción: agotado
Entrada: [15, 8, 5] | Real: stock_normal | Predicción: stock_normal
Entrada: [7, 12, 9] | Real: reposicion | Predicción: reposicion
Entrada: [5, 10, 6] | Real: reposicion | Predicción: reposicion
Entrada: [3, 10, 30] | Real: prioridad | Predicción: prioridad

=== ONTOLOGÍA ===
Relaciones de ontología: 9

=== EJEMPLO DE INTEGRACIÓN ===
Entrada: [4, 10, 25]
Predicción: prioridad
Relación: prediccion_1 -> asigna_estado -> estado_prioridad
```

El modelo clasificó correctamente los cinco ejemplos utilizados durante la prueba.

---

# 15. Conclusión

La actividad permitió implementar un sistema de reconocimiento relacionado directamente con el proyecto de inventario ferretero.

La red neuronal MLP aprendió a clasificar productos en los estados `stock_normal`, `reposicion`, `prioridad` y `agotado` utilizando como entrada el stock actual, stock mínimo y ventas semanales.

La base de datos SQLite permitió conservar evidencia de las entradas procesadas, su categoría real y la predicción generada.

Finalmente, la ontología permitió representar conceptos y relaciones del dominio, conectando una predicción concreta con un estado de inventario interpretable.

De esta forma se logró implementar el flujo solicitado:

```text
Reconocimiento
      +
Evidencia
      +
Interpretación
```

La práctica demuestra que una predicción puede convertirse en información verificable y posteriormente en conocimiento relacionado con el dominio del proyecto.