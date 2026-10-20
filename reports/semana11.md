# ADR – Semana 11: Selección de modelo para clasificación de inventario

**Proyecto:** Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero

**Estado:** Decisión provisional

## 1. Contexto

El proyecto busca apoyar el monitoreo de inventario de una ferretería mediante técnicas de inteligencia artificial.

Uno de sus componentes consiste en clasificar situaciones de inventario utilizando tres características numéricas:

- Stock actual.
- Stock mínimo.
- Ventas semanales.

Las categorías posibles son `stock_normal`, `reposicion`, `prioridad` y `agotado`.

Para elegir una técnica apropiada, se compararon tres modelos de clasificación considerando exactitud, tiempo de entrenamiento, complejidad y explicabilidad.

## 2. Modelos evaluados

**Logistic Regression:** modelo lineal utilizado como referencia inicial. Ofrece un entrenamiento rápido y una interpretación relativamente sencilla.

**Random Forest:** conjunto de árboles de decisión capaz de representar relaciones no lineales entre las variables.

**MLPClassifier:** red neuronal multicapa que puede aprender relaciones complejas, aunque requiere escalado y mayor atención al entrenamiento.

## 3. Metodología

Se utilizó el conjunto de 20 ejemplos etiquetados del proyecto, distribuidos en cuatro categorías.

Se realizaron tres repeticiones utilizando diferentes semillas para la división de los datos. En cada repetición, los tres modelos recibieron los mismos datos de entrenamiento y prueba.

La división utilizada fue del 75 % para entrenamiento y 25 % para evaluación, con estratificación por clase.

Se registraron accuracy y tiempo de entrenamiento en `artifacts/benchmark.csv`.

## 4. Resultados obtenidos

| Modelo | Accuracy promedio | Desviación | Tiempo promedio |
|---|---:|---:|---:|
| Logistic Regression | 0.8000 | 0.0000 | 0.0061 s |
| Random Forest | 0.8667 | 0.1155 | 0.3795 s |
| MLPClassifier | 0.8000 | 0.0000 | 0.2421 s |

Random Forest consiguió el mayor accuracy promedio, alcanzando un resultado perfecto durante la primera repetición.

Logistic Regression obtuvo el menor tiempo de entrenamiento y mantuvo un accuracy de 0.80 en las tres repeticiones.

MLPClassifier obtuvo el mismo accuracy que Logistic Regression, pero necesitó más tiempo para entrenar.

## 5. Decisión técnica

Se selecciona provisionalmente **Logistic Regression** como línea base del componente de clasificación numérica de inventario.

Aunque Random Forest obtuvo un accuracy promedio superior, la diferencia fue de 6.67 puntos porcentuales y el conjunto de evaluación fue demasiado pequeño para demostrar una ventaja consistente.

Logistic Regression presentó un desempeño estable, menor tiempo de entrenamiento y mayor facilidad de interpretación.

Random Forest se conservará como alternativa para evaluaciones posteriores con un conjunto de datos más representativo.

## 6. Ventajas y limitaciones

### Ventajas

- Entrenamiento rápido.
- Implementación sencilla mediante scikit-learn.
- Menor complejidad que una red neuronal.
- Facilidad para integrarse posteriormente con una API.
- Mayor interpretabilidad de sus parámetros.

### Limitaciones

- Puede presentar dificultades para representar relaciones no lineales complejas.
- El conjunto actual contiene únicamente 20 ejemplos.
- Cada prueba utiliza cinco observaciones.
- Los datos empleados son ejemplos académicos, no una muestra representativa del inventario real.
- La estabilidad observada no garantiza un desempeño similar con datos nuevos.
- No se midieron todavía el tiempo de inferencia ni la exactitud del reconocimiento visual.

## 7. Aplicación al proyecto final

El modelo seleccionado podría recibir información como stock actual, stock mínimo y ventas semanales para clasificar el estado de un producto.

Posteriormente, un sistema de reglas podría transformar esa clasificación en recomendaciones de reposición explicables para el usuario.

El componente visual deberá desarrollarse y evaluarse por separado para identificar productos y estimar unidades visibles.

## 8. Consecuencias y próximos pasos

Se mantendrá Logistic Regression como referencia inicial.

En futuras evaluaciones se recomienda ampliar el conjunto de datos con registros reales, comparar nuevas particiones y analizar otras métricas como precisión por clase, recall y matriz de confusión.

Si Random Forest demuestra una mejora consistente con datos representativos, podrá reconsiderarse la decisión.

## 9. Conclusión

El benchmark permitió comparar tres alternativas bajo condiciones equivalentes.

La decisión no se basó exclusivamente en el mayor accuracy, sino en el equilibrio entre rendimiento, tiempo, explicabilidad y necesidades del proyecto.

La selección es provisional y deberá validarse con información real antes de utilizarse para decisiones operativas de inventario.