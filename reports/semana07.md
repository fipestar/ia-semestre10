# Semana 07 - Representaciones del reconocimiento

## Proyecto

**Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero**

## Objetivo

Aplicar diferentes formas de representación del reconocimiento al contexto de un sistema de inventario ferretero.

Durante la práctica se trabajaron tres formas de representación:

- Representación numérica.
- Representación simbólica.
- Reconocimiento mediante autómatas.

Cada representación permite describir una misma situación desde una perspectiva diferente y determina qué tipo de operaciones pueden realizarse sobre la información.

---

# 1. Representación numérica

La representación numérica permite describir una situación mediante un vector de características.

Para el proyecto se representa el estado de inventario de un producto mediante:

```text
[stock_actual, stock_minimo, ventas_semanales]
```

Se definió como muestra observada:

```text
[4, 10, 25]
```

Esto representa:

- Stock actual: 4 unidades.
- Stock mínimo: 10 unidades.
- Ventas semanales: 25 unidades.

También se definió un vector de referencia asociado a una situación de reposición:

```text
[3, 10, 28]
```

Para comparar ambos vectores se utiliza la distancia euclidiana:

```python
distance = np.linalg.norm(sample - reference)
```

La diferencia entre los vectores es:

```text
[4, 10, 25] - [3, 10, 28]

= [1, 0, -3]
```

Por lo tanto:

```text
distancia = √(1² + 0² + (-3)²)

distancia = √10

distancia ≈ 3.162
```

### Resultado

```text
Distancia numérica: 3.162
```

Una distancia menor indica que las dos situaciones presentan características numéricas más similares.

En el contexto del proyecto, esta representación permite comparar el estado actual de un producto con una situación de referencia utilizando características cuantitativas del inventario.

### Información que puede perderse

Aunque se conservan cantidades exactas, esta representación no expresa directamente conceptos como `stock_bajo` o `alta_rotacion`, tampoco describe cómo ha evolucionado el producto a través del tiempo.

---

# 2. Representación simbólica

La representación simbólica utiliza conceptos, hechos y reglas en lugar de trabajar directamente con valores numéricos.

Para el producto analizado se definieron los siguientes hechos:

```text
stock_bajo
alta_rotacion
producto_critico
```

Estos hechos representan conocimiento sobre la situación actual del producto.

Se estableció la siguiente regla:

```text
SI stock_bajo
Y alta_rotacion
ENTONCES prioridad_reposicion
```

En Python se representa mediante:

```python
facts = {
    "stock_bajo",
    "alta_rotacion",
    "producto_critico"
}

if {"stock_bajo", "alta_rotacion"}.issubset(facts):
    print("Conclusión simbólica: prioridad_reposicion")
```

El método `issubset()` verifica que todos los hechos requeridos por la regla se encuentren dentro del conjunto de hechos conocidos.

Como `stock_bajo` y `alta_rotacion` están presentes, la regla se cumple.

### Resultado

```text
Conclusión simbólica: prioridad_reposicion
```

Por lo tanto, el sistema determina que el producto debe recibir prioridad de reposición.

### Información que puede perderse

La representación simbólica facilita la interpretación de la situación, pero pierde precisión numérica.

Por ejemplo, el hecho:

```text
stock_bajo
```

indica que existe poco inventario, pero no permite conocer directamente si quedan 4, 3 o 2 unidades.

---

# 3. Reconocimiento mediante autómata

Para representar la evolución del inventario se diseñó un autómata finito.

El objetivo del autómata es reconocer una secuencia en la cual un producto presenta bajo stock y posteriormente llega a estar agotado.

## Alfabeto

Se definió el siguiente alfabeto:

```text
Σ = {N, B, A}
```

donde:

```text
N = Stock normal
B = Stock bajo
A = Producto agotado
```

## Estados

El autómata utiliza los siguientes estados:

```text
Q = {q0, q1, q2}
```

Su significado es:

```text
q0 = No se ha detectado previamente bajo stock.
q1 = Se ha detectado bajo stock.
q2 = Después de presentar bajo stock, el producto llegó a agotado.
```

## Estado inicial

El estado inicial es:

```text
q0
```

## Estado de aceptación

El estado de aceptación es:

```text
q2
```

Llegar a `q2` significa que el sistema reconoció el patrón de interés: el producto presentó bajo stock y posteriormente llegó a agotado.

## Función de transición

Las transiciones utilizadas son:

| Estado actual | N | B | A |
|---|---|---|---|
| `q0` | `q0` | `q1` | `q0` |
| `q1` | `q0` | `q1` | `q2` |
| `q2` | `q0` | `q1` | `q2` |

El autómata lee cada símbolo de la secuencia y cambia de estado según esta tabla.

Por ejemplo, para:

```text
NNBBA
```

se realiza el siguiente recorrido:

```text
q0
 ↓ N
q0
 ↓ N
q0
 ↓ B
q1
 ↓ B
q1
 ↓ A
q2
```

Como la secuencia termina en `q2`, es aceptada.

## Casos de prueba

| Secuencia | Interpretación | Resultado |
|---|---|---|
| `NNBBA` | Normal → Normal → Bajo → Bajo → Agotado | Aceptada |
| `NNBN` | Normal → Normal → Bajo → Normal | Rechazada |
| `BA` | Bajo → Agotado | Aceptada |
| `NNA` | Normal → Normal → Agotado | Rechazada |

Los resultados esperados durante la ejecución son:

```text
NNBBA aceptada: True
NNBN aceptada: False
BA aceptada: True
NNA aceptada: False
```

El caso `NNA` es rechazado porque el producto llega directamente al estado agotado sin que previamente se haya reconocido un estado de bajo stock.

### Información que puede perderse

El autómata conserva la evolución de los estados del producto, pero cada observación se reduce a uno de tres símbolos.

Por ejemplo:

```text
B
```

permite conocer que el producto tiene bajo stock, pero no indica cuántas unidades quedan, cuál es su stock mínimo o cuántas unidades se venden semanalmente.

---

# 4. Comparación de las representaciones

| Representación | Información utilizada | Qué puede reconocer | Ventajas | Limitaciones | Información que puede perderse |
|---|---|---|---|---|---|
| **Numérica** | Stock actual, stock mínimo y ventas semanales | Similitud entre una situación observada y una situación de referencia | Permite realizar comparaciones matemáticas y conserva valores cuantitativos | Si las características utilizan escalas muy diferentes puede ser necesario normalizarlas | Contexto cualitativo, reglas del negocio y evolución temporal |
| **Simbólica** | Hechos como `stock_bajo`, `alta_rotacion` y `producto_critico` | Situaciones que cumplen reglas definidas previamente | Es interpretable y permite explicar claramente por qué se genera una conclusión | Depende de reglas creadas manualmente y no contempla automáticamente situaciones nuevas | Valores numéricos exactos como cantidad disponible o ventas |
| **Autómata** | Secuencias de símbolos `N`, `B` y `A` | Patrones en la evolución del estado del inventario | Permite analizar información secuencial mediante estados y transiciones claramente definidos | La situación real debe simplificarse a un conjunto limitado de símbolos y estados | Cantidades exactas, ventas, demanda, precio y otras características del producto |

---

# 5. Relación entre las tres representaciones

Las tres representaciones pueden describir diferentes aspectos relacionados con un mismo producto.

Una observación inicialmente puede contener información numérica:

```text
Stock actual = 4
Stock mínimo = 10
Ventas semanales = 25
```

Esta información puede representarse mediante el vector:

```text
[4, 10, 25]
```

A partir de la interpretación de estos datos también pueden generarse conceptos simbólicos:

```text
stock_bajo
alta_rotacion
```

Los hechos permiten aplicar la regla:

```text
SI stock_bajo
Y alta_rotacion
ENTONCES prioridad_reposicion
```

Por otra parte, al realizar diferentes observaciones a través del tiempo, el estado del producto puede representarse mediante una secuencia:

```text
N → N → B → B → A
```

Esta secuencia puede ser procesada por el autómata para reconocer que el producto presentó bajo stock antes de llegar a estar agotado.

Por lo tanto, una misma situación puede representarse de diferentes maneras:

```text
Producto de la ferretería
        │
        ├── Representación numérica
        │       [4, 10, 25]
        │
        ├── Representación simbólica
        │       stock_bajo
        │       alta_rotacion
        │       ↓
        │       prioridad_reposicion
        │
        └── Representación secuencial
                N → N → B → B → A
                ↓
              Autómata
```

Cada representación permite realizar operaciones diferentes y conserva distintos aspectos de la información original.

---

# 6. Conclusión

La práctica permitió aplicar tres formas de representación del reconocimiento al proyecto de monitoreo y reposición de inventario ferretero.

La **representación numérica** permitió describir el estado de un producto mediante características cuantitativas y compararlo con una situación de referencia utilizando distancia euclidiana.

La **representación simbólica** permitió convertir la situación del inventario en hechos y aplicar una regla explícita para determinar una prioridad de reposición.

El **autómata** permitió representar el comportamiento del inventario como una secuencia de estados y reconocer el patrón en el que un producto presenta bajo stock antes de llegar a estar agotado.

Se observa que ninguna representación conserva toda la información disponible. La representación numérica conserva valores exactos, la simbólica facilita el razonamiento mediante conceptos y el autómata permite analizar patrones secuenciales.

Por esta razón, las diferentes representaciones pueden complementarse dentro del Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero.