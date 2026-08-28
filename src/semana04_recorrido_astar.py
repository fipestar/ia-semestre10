from heapq import heappush, heappop


# Mapa de ejemplo de la ferretería
# 0 = espacio transitable
# 1 = obstáculo / estantería que no se puede atravesar
MAPA = [
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [1, 1, 0, 0, 0, 0],
]


def heuristica_manhattan(actual, meta):
    """
    Calcula la distancia Manhattan entre la posición actual
    y la meta.

    Se utiliza porque el movimiento permitido es:
    arriba, abajo, izquierda y derecha.
    """

    fila_actual, columna_actual = actual
    fila_meta, columna_meta = meta

    return (
        abs(fila_actual - fila_meta)
        + abs(columna_actual - columna_meta)
    )


def obtener_sucesores(posicion, mapa):
    """
    Genera los estados sucesores válidos desde una posición.

    Cada sucesor corresponde a moverse una casilla:
    arriba, abajo, izquierda o derecha.
    """

    fila, columna = posicion

    movimientos = [
        (-1, 0),  # arriba
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (0, 1),   # derecha
    ]

    sucesores = []

    for movimiento_fila, movimiento_columna in movimientos:

        nueva_fila = fila + movimiento_fila
        nueva_columna = columna + movimiento_columna

        # Verificar que la nueva posición esté dentro del mapa
        if (
            0 <= nueva_fila < len(mapa)
            and 0 <= nueva_columna < len(mapa[0])
        ):

            # Verificar que no sea un obstáculo
            if mapa[nueva_fila][nueva_columna] == 0:
                sucesores.append(
                    (nueva_fila, nueva_columna)
                )

    return sucesores


def reconstruir_camino(origenes, actual):
    """
    Reconstruye la ruta encontrada desde la meta
    hasta el estado inicial.
    """

    camino = [actual]

    while actual in origenes:
        actual = origenes[actual]
        camino.append(actual)

    camino.reverse()

    return camino


def astar(mapa, inicio, meta):
    """
    Implementación del algoritmo A*.

    f(n) = g(n) + h(n)

    g(n): costo acumulado desde el inicio.
    h(n): estimación del costo restante.
    """

    # Cola de prioridad
    frontera = []

    # En Python heapq siempre extrae el menor valor.
    # Guardamos:
    # (f, posición)
    heappush(
        frontera,
        (
            heuristica_manhattan(inicio, meta),
            inicio
        )
    )

    # Guarda desde qué estado llegamos a cada posición
    origenes = {}

    # Costo real acumulado g(n)
    costos = {
        inicio: 0
    }

    while frontera:

        _, actual = heappop(frontera)

        # Si llegamos a la meta, terminamos
        if actual == meta:

            camino = reconstruir_camino(
                origenes,
                actual
            )

            return camino, costos[actual]

        # Explorar estados sucesores
        for sucesor in obtener_sucesores(
            actual,
            mapa
        ):

            # Cada movimiento tiene costo 1
            nuevo_costo = costos[actual] + 1

            # Si nunca habíamos visitado el estado
            # o encontramos una ruta más barata
            if (
                sucesor not in costos
                or nuevo_costo < costos[sucesor]
            ):

                costos[sucesor] = nuevo_costo

                h = heuristica_manhattan(
                    sucesor,
                    meta
                )

                f = nuevo_costo + h

                heappush(
                    frontera,
                    (
                        f,
                        sucesor
                    )
                )

                origenes[sucesor] = actual

    # Si no existe camino posible
    return None, None


def mostrar_mapa(
    mapa,
    camino=None,
    inicio=None,
    meta=None
):

    camino = camino or []

    print()

    for fila in range(len(mapa)):

        linea = ""

        for columna in range(len(mapa[0])):

            posicion = (
                fila,
                columna
            )

            if posicion == inicio:
                linea += "S "

            elif posicion == meta:
                linea += "M "

            elif posicion in camino:
                linea += "* "

            elif mapa[fila][columna] == 1:
                linea += "# "

            else:
                linea += ". "

        print(linea)

    print()


def ejecutar_caso(
    numero,
    mapa,
    inicio,
    meta
):

    print("=" * 60)
    print(
        f"CASO DE PRUEBA {numero}"
    )
    print("=" * 60)

    print(
        f"Estado inicial: {inicio}"
    )

    print(
        f"Meta: {meta}"
    )

    camino, costo = astar(
        mapa,
        inicio,
        meta
    )

    if camino is None:

        print(
            "No existe una ruta posible."
        )

        mostrar_mapa(
            mapa,
            inicio=inicio,
            meta=meta
        )

        return

    print(
        f"Camino encontrado: {camino}"
    )

    print(
        f"Costo total: {costo}"
    )

    mostrar_mapa(
        mapa,
        camino,
        inicio,
        meta
    )


def main():

    # Caso 1:
    # recorrido base hacia un estante
    ejecutar_caso(
        numero=1,
        mapa=MAPA,
        inicio=(0, 0),
        meta=(4, 5)
    )

    # Caso 2:
    # misma ferretería, pero diferente producto/meta
    ejecutar_caso(
        numero=2,
        mapa=MAPA,
        inicio=(0, 0),
        meta=(2, 4)
    )

    # Caso 3:
    # cambia la ubicación inicial
    ejecutar_caso(
        numero=3,
        mapa=MAPA,
        inicio=(4, 2),
        meta=(0, 5)
    )


if __name__ == "__main__":
    main()