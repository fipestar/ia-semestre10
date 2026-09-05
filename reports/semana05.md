# Semana 05 - Sistema híbrido aplicado al inventario ferretero

El sistema combina reglas expertas, recuperación de información mediante TF-IDF y similitud coseno, y clasificación de texto.

## Consulta 1

- **Consulta:** El producto está por debajo del mínimo y quedan pocas unidades
- **Regla activada:** revisar_reposicion
- **Evidencia recuperada:** Cuando el stock actual está por debajo del stock mínimo, el producto debe ser considerado para reposición.
- **Similitud:** 0.460
- **Clasificación:** reposicion

## Consulta 2

- **Consulta:** No quedan unidades visibles, el producto está agotado
- **Regla activada:** reponer_inmediatamente
- **Evidencia recuperada:** Cuando un producto no tiene unidades disponibles, su estado se considera agotado y requiere reposición inmediata.
- **Similitud:** 0.346
- **Clasificación:** agotado

## Consulta 3

- **Consulta:** Este producto se vende mucho y debería tener prioridad de reposición
- **Regla activada:** aumentar_prioridad
- **Evidencia recuperada:** Los productos con bajo stock pero poca rotación pueden tener una prioridad menor que los productos de alta demanda.
- **Similitud:** 0.275
- **Clasificación:** prioridad

## Limitaciones

- Las reglas expertas dependen de palabras o frases definidas manualmente.
- La recuperación TF-IDF depende de los términos presentes en la base de conocimiento.
- El clasificador se entrena con pocos ejemplos, por lo que puede equivocarse ante consultas muy diferentes.
- El sistema todavía no utiliza datos reales del ERP ni imágenes capturadas por cámara.

Elaborado por Juan Camilo Gonzalez & Juan David Barbosa