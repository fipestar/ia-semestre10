"""Ejecutar desde la raiz: python src/semana14/main.py"""

from Semana14_red_semantica import RedSemantica, interpretar


ORACIONES = [
    "Una caja 5800 es una caja eléctrica.",
    "Una caja eléctrica es un accesorio eléctrico.",
    "Un conector rápido es un conector eléctrico.",
    "Un conector eléctrico es un accesorio eléctrico.",
    "Un accesorio eléctrico es un material eléctrico.",
    "Un material eléctrico es un producto ferretero.",
    "Un producto ferretero requiere control stock.",
]


def main() -> None:
    red = RedSemantica()
    print("=== HECHOS EXPLICITOS: ORACION -> TRIPLE ===")
    for oracion in ORACIONES:
        triple = interpretar(oracion)
        red.agregar(*triple)
        print(f"{oracion} -> {triple}")

    print("\n=== CONSULTA DIRECTA ===")
    print("Relaciones de caja_5800:", red.relacionados("caja_5800"))

    print("\n=== INFERENCIA DE JERARQUIA (NO EXPLICITA) ===")
    ruta = red.ruta_es_un("caja_5800", "producto_ferretero")
    print("¿caja_5800 es_un producto_ferretero?:", bool(ruta))
    print("Traza jerarquica:", " -> ".join(ruta) if ruta else "sin evidencia")

    print("\n=== HERENCIA DE PROPIEDAD ===")
    for propiedad, desde, ruta in red.propiedades("caja_5800"):
        print(f"caja_5800 requiere {propiedad}: heredada de {desde}")
        print("Traza:", " -> ".join(ruta), f"--requiere--> {propiedad}")

    print("\n=== CONSULTA SIN EVIDENCIA ===")
    print("¿caja_5800 es_un conector_electrico?:", red.es_un("caja_5800", "conector_electrico"))
    print("Interpretacion: no demostrada en esta red; no prueba falsedad universal.")

    print("\n=== ORACION INVALIDA ===")
    try:
        interpretar("Las cajas eléctricas pesan mucho.")
    except ValueError as exc:
        print(type(exc).__name__ + ":", exc)


if __name__ == "__main__":
    main()
