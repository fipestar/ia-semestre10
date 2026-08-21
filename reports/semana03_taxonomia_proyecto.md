# Semana 03 - Taxonomía aplicada al Sistema Inteligente Híbrido de Inventario Ferretero

## Resultado automático frente a clasificación manual de referencia

| Caso | Categoría automática principal | Categorías detectadas | Manual | Estado |
|---:|---|---|---|---|
| 1 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 2 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 3 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 4 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 5 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 6 | Sistemas expertos | Sistemas expertos | Sistemas expertos | Coincide |
| 7 | Sistemas expertos | Sistemas expertos | Sistemas expertos | Coincide |
| 8 | Sistemas expertos | Sistemas expertos | Sistemas expertos | Coincide |
| 9 | Sistemas expertos | Sistemas expertos | Sistemas expertos | Coincide |
| 10 | Sistemas expertos | Sistemas expertos | Sistemas expertos | Coincide |
| 11 | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Coincide |
| 12 | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Coincide |
| 13 | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Coincide |
| 14 | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Aprendizaje automático predictivo | Coincide |
| 15 | Búsqueda y optimización | Búsqueda y optimización | Búsqueda y optimización | Coincide |
| 16 | Búsqueda y optimización | Búsqueda y optimización | Búsqueda y optimización | Coincide |
| 17 | Búsqueda y optimización | Búsqueda y optimización | Búsqueda y optimización | Coincide |
| 18 | Búsqueda y optimización | Búsqueda y optimización | Búsqueda y optimización | Coincide |
| 19 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 20 | Visión por computador | Visión por computador, Aprendizaje automático predictivo, Sistemas expertos | Visión por computador | Coincide |

Coincidencia con la referencia: **100.00%** (20/20).

## Reglas específicas del dominio ferretero

Reemplaza o amplía las cinco reglas de ejemplo de `CUSTOM_RULES` y explica aquí por qué son pertinentes para tu dominio.

## Discrepancias y análisis

Para cada discrepancia explica: (1) qué palabra o frase activó la regla, (2) por qué la clasificación manual difiere y (3) qué regla modificarías.

## Nota técnica

Un problema real puede pertenecer a varias áreas de IA. La columna 'principal' usa la categoría con mayor cantidad de coincidencias; las demás coincidencias se conservan como categorías secundarias.

## Conclusión de la taxonomía del proyecto

El Sistema Inteligente Híbrido para Monitoreo Visual y Reposición de Inventario Ferretero pertenece principalmente al área de **Visión por computador**, ya que el sistema deberá reconocer productos y estimar cantidades visibles mediante imágenes capturadas con la cámara de un dispositivo móvil.

Sin embargo, el sistema también incorpora otras áreas de Inteligencia Artificial:

- **Sistemas expertos:** para aplicar reglas relacionadas con stock mínimo, stock objetivo y decisiones de reposición.
- **Aprendizaje automático predictivo:** para estimar demanda futura o riesgo de agotamiento a partir de datos históricos.
- **Búsqueda y optimización:** para priorizar productos y tomar decisiones de reposición bajo restricciones como presupuesto o capacidad.

La clasificación automática obtuvo una coincidencia del **100%** frente a la clasificación manual de referencia en los 20 casos definidos para el dominio.

Este resultado valida las reglas actuales para este conjunto de casos, pero no garantiza que el clasificador pueda generalizar correctamente ante cualquier descripción nueva, ya que depende de palabras y frases definidas manualmente.

Elaborado por Juan David Barbosa & Camilo Gonzalez