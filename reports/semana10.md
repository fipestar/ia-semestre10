# Semana 10 – Reconocimiento de imágenes: histogramas, regiones y texturas LBP

## 1. Objetivo

Aplicar técnicas de procesamiento de imágenes a fotografías reales de productos de ferretería, utilizando segmentación con Otsu, etiquetado de regiones e histogramas de intensidad y textura LBP.

## 2. Imágenes utilizadas

Se analizaron dos fotografías relacionadas con el proyecto de monitoreo visual de inventario ferretero:

- **Imagen A:** ocho accesorios plásticos de ferretería.
- **Imagen B:** conjunto de cajas metálicas 5800 utilizadas en instalaciones eléctricas.

Se seleccionaron estos productos para comparar superficies, formas, intensidades y patrones de textura diferentes.

## 3. Segmentación mediante Otsu

Las imágenes se convirtieron a escala de grises y se segmentaron mediante el método automático de Otsu.

Los umbrales obtenidos fueron:

- Accesorios plásticos: **146**.
- Cajas metálicas: **113**.

Estos valores permitieron generar máscaras binarias diferenciando píxeles según su intensidad. Sin embargo, los reflejos, las perforaciones y el fondo impidieron una separación perfecta de cada producto.

## 4. Etiquetado y medición de regiones

| Característica | Accesorios plásticos | Cajas metálicas |
|---|---:|---:|
| Regiones iniciales | 275 | 1565 |
| Regiones mayores a 50 píxeles | 36 | 214 |
| Área promedio | 10382.03 | 3072.09 |
| Desviación del área | 59052.52 | 13040.08 |

Se utilizó un filtro de área mayor a 50 píxeles para descartar regiones pequeñas que podían corresponder a ruido.

La imagen de las cajas metálicas generó más regiones conectadas, posiblemente debido a sus perforaciones, relieves y variaciones de iluminación. Las regiones obtenidas no representan necesariamente productos individuales.

## 5. Comparación de histogramas

El histograma de intensidad de los accesorios plásticos presentó una concentración importante en valores relativamente altos, mientras que el de las cajas metálicas mostró una mayor distribución en intensidades medias.

Esto demuestra diferencias en la distribución de tonos entre ambas fotografías.

## 6. Análisis de texturas LBP

Se aplicó `local_binary_pattern()` con radio 2 y 16 puntos de vecindad para describir patrones locales.

Los histogramas LBP presentaron semejanzas generales, pero también diferencias en las frecuencias de ciertos patrones.

Estas diferencias pueden estar relacionadas con las características de las superficies, sus bordes y relieves. Sin embargo, también influyen el fondo, las sombras y las condiciones de iluminación.

Por tanto, los resultados permiten comparar descriptores de textura, pero todavía no identificar automáticamente los tipos de productos.

## 7. Vector de características

Mediante `np.concatenate()` se combinaron tres características de regiones, 32 valores del histograma de intensidad y 18 valores del histograma LBP.

Se obtuvo un vector de **53 características por imagen**, almacenando ambos en `artifacts/semana10_features.npy`.

La forma final del arreglo fue `(2, 53)`.

## 8. Limitaciones

- La segmentación por intensidad puede confundir partes del fondo con productos.
- Los reflejos sobre las superficies metálicas generan regiones adicionales.
- Las perforaciones internas pueden dividir visualmente los objetos.
- El filtro de área no garantiza una correspondencia entre regiones y productos.
- Los histogramas globales incluyen información del fondo.
- Dos fotografías son insuficientes para evaluar un clasificador confiable.

## 9. Aplicación futura al proyecto

Los vectores de características podrán utilizarse como entradas para modelos de aprendizaje automático que busquen diferenciar referencias de productos.

A futuro se podría mejorar la segmentación, extraer las características únicamente de los productos y desarrollar un sistema capaz de reconocer y contar unidades visibles.

Esta etapa aporta información numérica al proyecto de monitoreo visual y reposición de inventario ferretero.

## 10. Evidencias

- `src/semana10_texturas.py`
- `artifacts/semana10_features.npy`
- `artifacts/semana10_histograma.png`
- Fotografías propias en `data/`
