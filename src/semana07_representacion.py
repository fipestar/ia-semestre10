import numpy as np

# ============================================================
# 1) REPRESENTACIÓN NUMÉRICA
# ============================================================

# Vector del producto observado:
# [stock_actual, stock_minimo, ventas_semanales]
sample = np.array([4.0, 10.0, 25.0])

# Vector de referencia de una situación de reposición
reference = np.array([3.0, 10.0, 28.0])

# Distancia euclidiana entre ambos vectores
distance = np.linalg.norm(sample - reference)

print("=== REPRESENTACIÓN NUMÉRICA ===")
print("Producto observado:", sample)
print("Referencia de reposición:", reference)
print("Distancia numérica:", round(float(distance), 3))

# ============================================================
# 2) REPRESENTACIÓN SIMBÓLICA
# ============================================================

# Hechos conocidos sobre el producto
facts = {
    "stock_bajo",
    "alta_rotacion",
    "producto_critico"
}

print("\n=== REPRESENTACIÓN SIMBÓLICA ===")
print("Hechos:", facts)

# Regla:
# SI stock_bajo Y alta_rotacion
# ENTONCES prioridad_reposicion
if {"stock_bajo", "alta_rotacion"}.issubset(facts):
    print("Hechos:", facts)

# ============================================================
# 3) RECONOCIMIENTO MEDIANTE AUTÓMATA
# ============================================================

# Alfabeto:
# N = stock normal
# B = stock bajo
# A = agotado
#
# q0 = no se ha detectado bajo stock
# q1 = se detectó bajo stock
# q2 = después de bajo stock, el producto llegó a agotado
#
# Estado inicial: q0
# Estado de aceptación: q2

def acepta_agotamiento(text):
    state = "q0"

    transitions = {
        ("q0", "N"): "q0",
        ("q0", "B"): "q1",
        ("q0", "A"): "q0",

        ("q1", "N"): "q0",
        ("q1", "B"): "q1",
        ("q1", "A"): "q2",

        ("q2", "N"): "q0",
        ("q2", "B"): "q1",
        ("q2", "A"): "q2",
    }
    for symbol in text:
        state = transitions[(state, symbol)]

    return state == "q2"

print("\n=== RECONOCIMIENTO MEDIANTE AUTÓMATA ===")

for seq in ("NNBBA", "NNBN", "BA", "NNA"):
    print(seq, "aceptada:", acepta_agotamiento(seq))    