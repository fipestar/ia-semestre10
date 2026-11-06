
# Semana 13 – Ingeniería del conocimiento
## Sistemas lógicos y motor de inferencia

**Asignatura:** Inteligencia Artificial  
**Proyecto:** Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero  
**Modalidad:** Individual  
**Fecha:** 6 de noviembre de 2026

---

## 1. Introducción

Durante la Semana 13 se implementó un motor de inferencia basado en reglas lógicas, aplicado al proceso de reposición de inventario ferretero.

El objetivo de esta práctica fue representar conocimientos del dominio mediante hechos y reglas, permitiendo obtener conclusiones de manera automática y explicar cómo se llegó a ellas.

A diferencia de los modelos de aprendizaje automático desarrollados en semanas anteriores, este motor no necesita entrenarse con datos. Su funcionamiento depende de reglas explícitas y de los hechos disponibles en cada escenario.

La implementación se desarrolló en Python y utiliza encadenamiento hacia adelante, trazabilidad y pruebas unitarias mediante `unittest`.

---

## 2. Análisis del dominio

### 2.1. Problema identificado

En una ferretería es necesario identificar productos que podrían necesitar reposición prioritaria.

Sin embargo, tener un stock bajo no siempre es suficiente para recomendar inmediatamente una compra.

También pueden considerarse otras condiciones, como:

- Rotación del producto.
- Disponibilidad del proveedor.
- Confirmación del presupuesto para realizar el pedido.

Por esta razón, se propuso un motor lógico capaz de determinar si existe evidencia suficiente para recomendar un pedido prioritario.

### 2.2. Funcionalidad seleccionada

La funcionalidad implementada consiste en evaluar condiciones relacionadas con el inventario y derivar una recomendación de reposición.

El motor recibe un conjunto de hechos iniciales, consulta las reglas definidas y obtiene conclusiones mediante encadenamiento hacia adelante.

### 2.3. Conceptos principales

| Concepto | Descripción |
|---|---|
| Producto | Artículo comercializado en la ferretería. |
| Stock bajo | Condición que indica un nivel reducido de existencias. |
| Alta rotación | Condición que indica una demanda elevada del producto. |
| Proveedor disponible | Evidencia de que existe un proveedor disponible para el abastecimiento. |
| Presupuesto confirmado | Evidencia de que se dispone de un presupuesto confirmado para el pedido. |
| Reposición urgente | Conclusión que identifica una necesidad prioritaria de abastecimiento. |
| Abastecimiento viable | Conclusión que indica que existe una opción de suministro para una reposición urgente. |
| Pedido prioritario recomendado | Conclusión final que recomienda realizar una compra prioritaria. |

### 2.4. Hechos iniciales

Para el escenario principal se utilizaron cuatro hechos:

```python
hechos_iniciales = {
    "stock_bajo",
    "alta_rotacion",
    "proveedor_disponible",
    "presupuesto_confirmado"
}
```

Estos hechos representan las condiciones que el sistema considera disponibles al comenzar la inferencia.

No son conclusiones generadas automáticamente por el motor, sino información proporcionada para el escenario.

### 2.5. Conclusión esperada

La conclusión principal del experimento es:

```text
pedido_prioritario_recomendado
```

Esta conclusión debe demostrarse únicamente cuando las reglas y los hechos disponibles permiten derivarla.

---

## 3. Representación del conocimiento mediante reglas

Se implementaron cuatro reglas originales relacionadas con el proceso de inventario ferretero.

### 3.1. Regla R1 – Identificación de reposición urgente

**Premisas:**

- `stock_bajo`
- `alta_rotacion`

**Conclusión:**

- `reposicion_urgente`

Representación lógica:

```text
stock_bajo ∧ alta_rotacion → reposicion_urgente
```

Interpretación:

Si un producto tiene stock bajo y alta rotación, el sistema puede inferir que existe una necesidad de reposición urgente.

### 3.2. Regla R2 – Viabilidad del abastecimiento

**Premisas:**

- `reposicion_urgente`
- `proveedor_disponible`

**Conclusión:**

- `abastecimiento_viable`

Representación lógica:

```text
reposicion_urgente ∧ proveedor_disponible
    → abastecimiento_viable
```

Interpretación:

Si existe una reposición urgente y se tiene evidencia de un proveedor disponible, el sistema infiere que el abastecimiento es viable dentro de las condiciones simplificadas del prototipo.

### 3.3. Regla R3 – Recomendación de pedido prioritario

**Premisas:**

- `abastecimiento_viable`
- `presupuesto_confirmado`

**Conclusión:**

- `pedido_prioritario_recomendado`

Representación lógica:

```text
abastecimiento_viable ∧ presupuesto_confirmado
    → pedido_prioritario_recomendado
```

Interpretación:

Si el abastecimiento es viable y existe un presupuesto confirmado, el motor puede demostrar la recomendación de un pedido prioritario.

### 3.4. Regla R4 – Revisión de reposición programada

**Premisas:**

- `stock_bajo`
- `rotacion_baja`

**Conclusión:**

- `revision_reposicion_programada`

Representación lógica:

```text
stock_bajo ∧ rotacion_baja
    → revision_reposicion_programada
```

Interpretación:

Si un producto tiene stock bajo, pero presenta baja rotación, se genera una conclusión alternativa para revisar una posible reposición programada.

Esta regla no participa en la cadena principal R1–R3, pero demuestra que el motor puede producir conclusiones distintas según los hechos disponibles.

### 3.5. Resumen de las reglas

| Regla | Premisas | Conclusión |
|---|---|---|
| R1 | Stock bajo + alta rotación | Reposición urgente |
| R2 | Reposición urgente + proveedor disponible | Abastecimiento viable |
| R3 | Abastecimiento viable + presupuesto confirmado | Pedido prioritario recomendado |
| R4 | Stock bajo + rotación baja | Revisión de reposición programada |

Las reglas R1, R2 y R3 forman una cadena de inferencia, porque la conclusión de una regla se utiliza como premisa de la siguiente.

---

## 4. Implementación del motor de inferencia

El motor fue implementado en Python utilizando una estructura denominada `Regla` y una función principal llamada `inferir()`.

### 4.1. Estructura Regla

Cada regla contiene tres elementos:

- Nombre o identificador.
- Conjunto de premisas.
- Conclusión.

Las premisas se representan mediante `frozenset`, que permite almacenar hechos sin duplicados y evita modificar accidentalmente su contenido.

### 4.2. Función inferir()

La función `inferir()` recibe:

1. Un conjunto de hechos iniciales.
2. Una lista de reglas lógicas.

El procedimiento sigue estos pasos:

1. Crea una copia de los hechos iniciales.
2. Recorre las reglas disponibles.
3. Verifica si todas las premisas de una regla están presentes.
4. Comprueba que la conclusión todavía no exista.
5. Agrega la conclusión cuando se cumplen las condiciones.
6. Registra una traza de la regla ejecutada.
7. Repite el proceso mientras aparezcan conclusiones nuevas.

La función devuelve los hechos finales y el registro de inferencias realizadas.

### 4.3. Encadenamiento hacia adelante

La técnica utilizada fue el encadenamiento hacia adelante (*forward chaining*).

Este mecanismo comienza con hechos conocidos y aplica reglas que permiten obtener nuevos hechos.

Las nuevas conclusiones pueden activar otras reglas.

En nuestro proyecto, la cadena principal es:

```text
stock_bajo + alta_rotacion
              |
              v
             R1
              |
              v
      reposicion_urgente
              |
              + proveedor_disponible
              |
              v
             R2
              |
              v
      abastecimiento_viable
              |
              + presupuesto_confirmado
              |
              v
             R3
              |
              v
 pedido_prioritario_recomendado
```

El proceso termina cuando una pasada completa por las reglas no produce nuevas conclusiones.

### 4.4. Prevención de duplicados

El motor comprueba si la conclusión ya pertenece al conjunto de hechos.

Conceptualmente, utiliza la condición:

```python
regla.conclusion not in hechos
```

Esto impide agregar varias veces la misma conclusión.

Además, contribuye a evitar ciclos infinitos cuando existen reglas con dependencias circulares.

### 4.5. Conservación de los hechos originales

El motor trabaja con una copia de los hechos iniciales.

De esta manera, puede agregar hechos inferidos sin modificar el conjunto originalmente proporcionado.

---

## 5. Pruebas funcionales

Se ejecutaron dos escenarios principales para comprobar el funcionamiento del sistema.

### 5.1. Caso A – Evidencia completa

Se utilizaron los siguientes hechos iniciales:

```text
alta_rotacion
presupuesto_confirmado
proveedor_disponible
stock_bajo
```

La salida real del programa fue:

```text
=== CASO A: evidencia completa ===
Hechos iniciales: alta_rotacion, presupuesto_confirmado, proveedor_disponible, stock_bajo

Inferencia: R1: alta_rotacion, stock_bajo => reposicion_urgente
Inferencia: R2: proveedor_disponible, reposicion_urgente => abastecimiento_viable
Inferencia: R3: abastecimiento_viable, presupuesto_confirmado => pedido_prioritario_recomendado

Nuevos hechos: abastecimiento_viable, pedido_prioritario_recomendado, reposicion_urgente

Pedido prioritario: DEMOSTRADO (recomendación)
```

**Interpretación:**

El motor ejecutó correctamente las reglas R1, R2 y R3.

Primero identificó una reposición urgente.

Después determinó que el abastecimiento era viable.

Finalmente, al existir presupuesto confirmado, obtuvo la conclusión `pedido_prioritario_recomendado`.

Por tanto, la recomendación quedó demostrada con los hechos y reglas disponibles.

### 5.2. Caso B – Sin evidencia de presupuesto

En el segundo escenario se eliminó el hecho `presupuesto_confirmado`.

Los hechos iniciales fueron:

```text
alta_rotacion
proveedor_disponible
stock_bajo
```

La salida real del programa fue:

```text
=== CASO B: sin evidencia de presupuesto ===
Hechos iniciales: alta_rotacion, proveedor_disponible, stock_bajo

Inferencia: R1: alta_rotacion, stock_bajo => reposicion_urgente
Inferencia: R2: proveedor_disponible, reposicion_urgente => abastecimiento_viable

Nuevos hechos: abastecimiento_viable, reposicion_urgente

Pedido prioritario: NO DEMOSTRADO con la evidencia disponible
```

**Interpretación:**

El motor ejecutó R1 y R2, porque sus condiciones estaban satisfechas.

Sin embargo, R3 no se ejecutó porque faltaba `presupuesto_confirmado`.

Por esa razón, no se pudo demostrar la conclusión final.

Es importante aclarar que una conclusión no demostrada no significa que sea falsa.

En este caso, el motor no demuestra que el presupuesto sea insuficiente ni que el pedido esté prohibido. Solamente indica que falta evidencia para obtener la recomendación mediante las reglas implementadas.

### 5.3. Comparación de escenarios

| Característica | Caso A | Caso B |
|---|---|---|
| Stock bajo | Sí | Sí |
| Alta rotación | Sí | Sí |
| Proveedor disponible | Sí | Sí |
| Presupuesto confirmado | Sí | No disponible como hecho |
| Reglas ejecutadas | R1, R2, R3 | R1, R2 |
| Nuevas conclusiones | 3 | 2 |
| Pedido prioritario | Demostrado | No demostrado |

---

## 6. Trazabilidad de las conclusiones

La trazabilidad permite identificar qué reglas se ejecutaron y qué conclusiones produjeron.

Por ejemplo:

```text
R1: alta_rotacion, stock_bajo
    => reposicion_urgente

R2: proveedor_disponible, reposicion_urgente
    => abastecimiento_viable

R3: abastecimiento_viable, presupuesto_confirmado
    => pedido_prioritario_recomendado
```

Esta información permite explicar por qué el motor llegó a una conclusión específica.

También permite identificar qué premisa faltó cuando una conclusión no fue demostrada.

En el caso B, la traza muestra que el motor llegó hasta `abastecimiento_viable`, pero no pudo ejecutar R3.

Esto hace que el sistema sea interpretable y facilita la revisión de sus decisiones lógicas.

---

## 7. Pruebas unitarias con unittest

Para verificar el motor se implementó el archivo:

```text
test_motor_inferencia.py
```

Se utilizó el módulo `unittest`, incluido en la biblioteca estándar de Python.

Las pruebas verificaron distintos comportamientos del motor.

### 7.1. Resultados obtenidos

| Prueba | Objetivo | Resultado |
|---|---|---|
| Caso A | Demostrar la recomendación y registrar la traza | OK |
| Caso B | Comprobar que sin presupuesto no se demuestra la recomendación | OK |
| Ciclo | Verificar que las reglas circulares no produzcan ciclos infinitos | OK |
| Conservación de hechos | Comprobar que no se modifiquen los hechos iniciales | OK |
| Rama alternativa | Comprobar la reposición programada | OK |
| Regla repetida | Verificar que no se dupliquen conclusiones | OK |
| Orden inverso | Comprobar que el motor funcione aunque cambie el orden de las reglas | OK |
| Sin reglas | Verificar que no se generen inferencias sin reglas | OK |

### 7.2. Resultado de ejecución

La ejecución proporcionó:

```text
test_caso_a_demuestra_recomendacion_y_traza ... ok
test_caso_b_sin_presupuesto_no_demuestra_recomendacion ... ok
test_ciclo_termina_sin_duplicados ... ok
test_no_se_modifican_los_hechos_iniciales ... ok
test_rama_alternativa_reposicion_programada ... ok
test_regla_repetida_no_duplica_conclusion ... ok
test_reglas_en_orden_inverso_tambien_funcionan ... ok
test_sin_reglas_no_hay_inferencia ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.002s

OK
```

**Resultado general:** ocho pruebas ejecutadas satisfactoriamente.

Estas pruebas verifican los comportamientos implementados, aunque no garantizan que las reglas comerciales representen todos los escenarios reales de una ferretería.

---

## 8. Prevención de ciclos infinitos

Se implementó una prueba con reglas circulares.

Por ejemplo:

```text
a → b
b → a
```

Si el motor comienza con el hecho `a`, puede inferir `b`.

Sin embargo, cuando intenta volver a concluir `a`, identifica que ese hecho ya existe y evita incorporarlo nuevamente.

El encadenamiento termina cuando ninguna regla genera conclusiones nuevas.

Esto demuestra que el motor puede manejar dependencias circulares de este tipo sin quedar ejecutándose indefinidamente.

---

## 9. Relación con el proyecto semestral

El motor de inferencia complementa el Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero.

En semanas anteriores se desarrollaron mecanismos de:

- Representación numérica y simbólica.
- Clasificación mediante redes neuronales.
- Detección de bordes y segmentación de imágenes.
- Extracción de características visuales.
- Comparación de modelos de aprendizaje automático.

La Semana 13 incorpora una nueva capacidad: obtener recomendaciones explicables mediante reglas lógicas.

En una implementación futura, el sistema podría utilizar datos provenientes del inventario y de las ventas para generar hechos como:

```text
stock_bajo
alta_rotacion
proveedor_disponible
presupuesto_confirmado
```

Posteriormente, el motor analizaría estos hechos y determinaría si puede recomendar una reposición prioritaria.

Esto permitiría combinar componentes de reconocimiento con mecanismos explícitos de razonamiento.

La implementación actual es independiente y utiliza hechos proporcionados manualmente. Todavía no está conectada automáticamente con la base de datos ni con el reconocimiento visual de productos.

---

## 10. Limitaciones

### 10.1. Reglas definidas manualmente

El motor no aprende reglas automáticamente.

Las premisas y conclusiones deben definirse previamente.

### 10.2. Simplificación de las decisiones comerciales

Las reglas utilizadas representan un escenario simplificado.

Una decisión real de compra también puede depender de:

- Costos de adquisición.
- Cantidad mínima de pedido.
- Tiempo de entrega del proveedor.
- Demanda histórica.
- Rentabilidad.
- Disponibilidad de efectivo.
- Compromisos de pago existentes.

### 10.3. Ausencia de incertidumbre

El motor utiliza hechos considerados disponibles o no disponibles.

No maneja probabilidades ni niveles de confianza.

### 10.4. Ausencia de negación automática

Cuando una conclusión no se demuestra, el motor no infiere automáticamente su negación.

Por ejemplo, no demostrar `pedido_prioritario_recomendado` no equivale a demostrar que un pedido sea innecesario.

### 10.5. Falta de integración con datos reales

Los hechos de los escenarios fueron definidos para las pruebas.

En una versión futura podrían obtenerse desde las fuentes de información reales del inventario.

### 10.6. Validación del dominio

Aunque las pruebas unitarias verifican el funcionamiento técnico, las reglas deben contrastarse con los procesos comerciales reales antes de utilizarse para tomar decisiones operativas.

---

## 11. Posibles mejoras futuras

Entre las mejoras identificadas se encuentran:

1. Integrar el motor con los registros reales de inventario y ventas.
2. Generar automáticamente hechos a partir de condiciones numéricas.
3. Incorporar información de proveedores y tiempos de entrega.
4. Permitir configurar reglas desde una interfaz administrativa.
5. Conservar las trazas de inferencia para auditoría.
6. Incorporar nuevas reglas relacionadas con niveles de prioridad.
7. Integrar resultados del sistema de reconocimiento visual.
8. Validar las reglas con escenarios reales de la ferretería.

Estas mejoras permitirían ampliar la utilidad del motor sin modificar necesariamente su mecanismo básico de inferencia.

---

## 12. Archivos y ejecución

Los archivos principales de la práctica son:

```text
src/
├── motor_inferencia.py
└── test_motor_inferencia.py

reports/
└── reporte_semana13.md
```

Para ejecutar el motor desde la raíz del repositorio:

```bash
python src/motor_inferencia.py
```

Para ejecutar las pruebas:

```bash
python -m unittest discover -s src -p "test_motor_inferencia.py" -v
```

El motor y sus pruebas utilizan herramientas de la biblioteca estándar de Python, por lo que no necesitan instalar dependencias adicionales.

---

## 13. Conclusiones

La práctica de la Semana 13 permitió implementar un motor de inferencia basado en reglas lógicas, aplicado al proceso de reposición de inventario ferretero.

Se diseñaron cuatro reglas originales y se implementó encadenamiento hacia adelante para obtener conclusiones a partir de hechos iniciales.

El motor permitió demostrar una recomendación de pedido prioritario cuando estaban disponibles todas las condiciones necesarias.

También se comprobó que, al faltar una premisa, el sistema no deriva automáticamente la conclusión final.

Las pruebas unitarias verificaron la conservación de los hechos iniciales, la ausencia de conclusiones duplicadas y la terminación del motor ante dependencias circulares.

Los ocho casos de prueba finalizaron satisfactoriamente.

Finalmente, la trazabilidad permitió identificar cada regla ejecutada y comprender cómo se construyeron las conclusiones.

Esta implementación constituye una base para incorporar razonamiento lógico explicable al sistema inteligente de inventario ferretero, complementando las técnicas de reconocimiento y aprendizaje automático desarrolladas durante el semestre.

---

## 14. Referencias

- Material docente: *Explicación de la Semana 13 – Ingeniería del conocimiento*.
- Material docente: *IA Semana 13 – Ingeniería del conocimiento, tutorial de 15 diapositivas*.
- Código fuente del proyecto: `motor_inferencia.py`.
- Pruebas funcionales: `test_motor_inferencia.py`.
- Python Software Foundation: documentación oficial de `dataclasses` y `unittest`.
