# Semana 04 - Marco tecnológico de la Inteligencia Artificial

## Aplicación de A* al Sistema Inteligente Híbrido de Inventario Ferretero

## A. Descripción del problema

El proyecto consiste en un Sistema Inteligente Híbrido para el monitoreo visual y la reposición de inventario ferretero. Uno de sus componentes principales busca utilizar la cámara de un dispositivo móvil para inspeccionar productos ubicados en estanterías y posteriormente determinar si estos requieren reposición.

Para aplicar los conceptos de búsqueda estudiados durante la Semana 4, se planteó un problema relacionado con el recorrido necesario para llegar hasta un estante que debe ser inspeccionado.

La zona de la ferretería se representa mediante una cuadrícula. Algunas posiciones representan espacios transitables y otras representan obstáculos o estanterías que no pueden atravesarse.

El objetivo consiste en encontrar un recorrido de costo mínimo desde una posición inicial hasta la ubicación del estante o producto que se desea inspeccionar.

Para resolver este problema se utilizó el algoritmo A*, debido a que permite encontrar caminos de costo mínimo combinando el costo acumulado del recorrido con una estimación de la distancia restante hasta la meta.

---

## B. Representación del problema

El problema se representa mediante un espacio de estados.

### Estado

Un estado corresponde a la posición actual dentro del mapa de la ferretería y se representa mediante una tupla:

`(fila, columna)`

Por ejemplo:

`(2, 3)`

representa una posición ubicada en la fila 2 y columna 3.

### Estado inicial

El estado inicial representa la posición desde la cual comienza el recorrido.

Por ejemplo:

`(0, 0)`

### Estados posibles

Los estados posibles corresponden a todas las posiciones transitables dentro del mapa.

En la representación utilizada:

- `0` representa una posición transitable.
- `1` representa un obstáculo o una zona que no puede atravesarse.

### Acciones u operadores

Desde una posición se permiten cuatro movimientos:

- Arriba.
- Abajo.
- Izquierda.
- Derecha.

No se permiten movimientos diagonales.

### Transiciones y sucesores

Una transición ocurre cuando el sistema pasa desde la posición actual hacia una posición vecina válida.

Por ejemplo:

`(2, 2) → (2, 3)`

representa un movimiento hacia la derecha.

La función `obtener_sucesores()` genera las posiciones a las cuales es posible desplazarse desde el estado actual, verificando que:

1. La posición se encuentre dentro de los límites del mapa.
2. La posición no corresponda a un obstáculo.

### Meta

La meta corresponde a la ubicación del estante o producto que se desea inspeccionar.

El algoritmo finaliza cuando la posición actual coincide con la posición definida como meta.

### Costo del camino

Para esta implementación se asignó un costo de `1` a cada movimiento.

Por lo tanto, el costo total corresponde al número de desplazamientos necesarios para llegar desde el estado inicial hasta la meta.

Este costo representa `g(n)` dentro del algoritmo A*.

### Heurística

Se utilizó la distancia Manhattan como función heurística:

`h(n) = |fila_actual - fila_meta| + |columna_actual - columna_meta|`

Esta heurística es apropiada porque solamente se permiten desplazamientos horizontales y verticales.

La heurística estima cuántos movimientos serían necesarios para alcanzar la meta si no existieran obstáculos.

### Función de evaluación

A* utiliza:

`f(n) = g(n) + h(n)`

donde:

- `g(n)` representa el costo real acumulado desde el estado inicial.
- `h(n)` representa una estimación del costo restante hasta la meta.
- `f(n)` representa el costo total estimado de alcanzar la meta pasando por el estado actual.

El algoritmo selecciona para explorar los estados con menor valor de `f(n)`.

### Criterio para seleccionar la solución

La solución seleccionada corresponde a una ruta válida de costo mínimo entre la posición inicial y la meta, evitando las posiciones identificadas como obstáculos.

---

## C. Implementación

Para la Semana 4 se creó el archivo:

`src/semana04_recorrido_astar.py`

En este archivo se implementó el algoritmo A* aplicado al recorrido de una zona simplificada de la ferretería.

El mapa utilizado inicialmente fue:

```text
. . . # . .
. # . # . #
. # . . . .
. . . # # .
# # . . . .

Elaborado por Juan David Barbosa & Juan Camilo Gonzalez