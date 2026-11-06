"""Semana 13: motor de inferencia proposicional para reposición ferretera.

Python >= 3.10, únicamente biblioteca estándar.
Los hechos son evidencias simbólicas verificadas externamente; el motor no
calcula stock, no consulta proveedores y no ejecuta compras.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Regla:
    """Una implicación: TODAS las premisas permiten inferir una conclusión."""

    nombre: str
    premisas: frozenset[str]
    conclusion: str


def inferir(
    hechos_iniciales: set[str], reglas: list[Regla]
) -> tuple[set[str], list[str]]:
    """Encadenamiento hacia adelante hasta alcanzar un punto fijo.

    Devuelve una nueva base de hechos y una traza por cada conclusión nueva.
    No altera el conjunto recibido ni infiere negaciones por ausencia.
    """
    hechos = set(hechos_iniciales)
    trazas: list[str] = []
    cambios = True

    while cambios:
        cambios = False
        for regla in reglas:
            if regla.premisas.issubset(hechos) and regla.conclusion not in hechos:
                hechos.add(regla.conclusion)
                detalle = ", ".join(sorted(regla.premisas))
                trazas.append(f"{regla.nombre}: {detalle} => {regla.conclusion}")
                cambios = True

    return hechos, trazas


def construir_reglas() -> list[Regla]:
    """Reglas didácticas originales del dominio ferretero.

    'Confirmado' significa evidencia positiva, no ausencia de una alerta.
    El resultado es una recomendación, nunca la creación automática de compra.
    """
    return [
        Regla(
            "R1",
            frozenset({"stock_bajo", "alta_rotacion"}),
            "reposicion_urgente",
        ),
        Regla(
            "R2",
            frozenset({"reposicion_urgente", "proveedor_disponible"}),
            "abastecimiento_viable",
        ),
        Regla(
            "R3",
            frozenset({"abastecimiento_viable", "presupuesto_confirmado"}),
            "pedido_prioritario_recomendado",
        ),
        Regla(
            "R4",
            frozenset({"stock_bajo", "rotacion_baja"}),
            "revision_reposicion_programada",
        ),
    ]


def mostrar_escenario(nombre: str, hechos_iniciales: set[str]) -> None:
    objetivo = "pedido_prioritario_recomendado"
    hechos_finales, trazas = inferir(hechos_iniciales, construir_reglas())
    print(f"\n=== {nombre} ===")
    print("Hechos iniciales:", ", ".join(sorted(hechos_iniciales)))
    for traza in trazas:
        print("Inferencia:", traza)
    nuevos = hechos_finales - hechos_iniciales
    print("Nuevos hechos:", ", ".join(sorted(nuevos)) if nuevos else "ninguno")
    print(
        "Pedido prioritario:",
        "DEMOSTRADO (recomendación)"
        if objetivo in hechos_finales
        else "NO DEMOSTRADO con la evidencia disponible",
    )


def main() -> None:
    hechos_completos = {
        "stock_bajo",
        "alta_rotacion",
        "proveedor_disponible",
        "presupuesto_confirmado",
    }
    hechos_sin_presupuesto = hechos_completos - {"presupuesto_confirmado"}
    mostrar_escenario("CASO A: evidencia completa", hechos_completos)
    mostrar_escenario("CASO B: sin evidencia de presupuesto", hechos_sin_presupuesto)


if __name__ == "__main__":
    main()
