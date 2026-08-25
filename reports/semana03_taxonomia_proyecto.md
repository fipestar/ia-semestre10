# Semana 03 - Taxonomía aplicada al Sistema Inteligente Híbrido de Inventario Ferretero

## Resultado automático frente a clasificación manual de referencia

| Caso | Categoría automática principal | Categorías detectadas | Manual | Estado |
|---:|---|---|---|---|
| 1 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 2 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 3 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 4 | Visión por computador | Visión por computador | Visión por computador | Coincide |
| 5 | Requiere análisis | Requiere análisis | Visión por computador | Revisar |
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
| 20 | Aprendizaje automático predictivo | Aprendizaje automático predictivo, Visión por computador, Sistemas expertos | Visión por computador | Revisar |

Coincidencia con la referencia: **90.00%** (18/20).

## Reglas específicas del dominio ferretero

Reemplaza o amplía las cinco reglas de ejemplo de `CUSTOM_RULES` y explica aquí por qué son pertinentes para tu dominio.

## Discrepancias y análisis

Para cada discrepancia explica: (1) qué palabra o frase activó la regla, (2) por qué la clasificación manual difiere y (3) qué regla modificarías.

## Nota técnica

Un problema real puede pertenecer a varias áreas de IA. La columna 'principal' usa la categoría con mayor cantidad de coincidencias; las demás coincidencias se conservan como categorías secundarias.

## Discrepancias y análisis

Se identificaron dos discrepancias respecto a la clasificación manual.

### Caso 5

El sistema devolvió `Requiere análisis`, aunque manualmente se clasificó como `Visión por computador`. Esto ocurrió porque la descripción no contenía ninguna de las palabras o frases definidas actualmente para esa categoría.

Como mejora se puede agregar una regla específica como `clasificar visualmente` o `reconocer productos`, ya que representa tareas propias de visión por computador dentro del proyecto.

### Caso 20

El sistema detectó correctamente tres áreas: `Aprendizaje automático predictivo`, `Visión por computador` y `Sistemas expertos`. Sin embargo, seleccionó `Aprendizaje automático predictivo` como categoría principal, mientras que la referencia manual define `Visión por computador`.

Esto ocurre porque el clasificador utiliza como categoría principal aquella con mayor cantidad de coincidencias. Como el proyecto tiene como componente central el reconocimiento visual mediante cámara, se pueden reforzar las reglas de Visión por computador para reflejar mejor esta prioridad.

Este caso también evidencia que el sistema es híbrido y que una misma necesidad puede pertenecer simultáneamente a varias áreas de Inteligencia Artificial.

Elaborado por Juan David Barbosa & Juan Camilo Gonzalez