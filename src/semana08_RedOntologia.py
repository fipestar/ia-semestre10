from pathlib import Path
from datetime import datetime
import pickle
import sqlite3

import networkx as nx

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


# ============================================================
# 1. RUTAS DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"

ARTIFACTS.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. DATOS DEL PROYECTO
# ============================================================

# Cada registro representa:
# [stock_actual, stock_minimo, ventas_semanales]

X = [
    # STOCK NORMAL
    [20, 10, 8],
    [18, 10, 6],
    [15, 8, 5],
    [25, 12, 10],
    [14, 7, 4],

    # REPOSICIÓN
    [8, 10, 7],
    [6, 10, 8],
    [5, 10, 6],
    [7, 12, 9],
    [4, 8, 5],

    # PRIORIDAD
    [4, 10, 25],
    [3, 10, 30],
    [2, 8, 20],
    [5, 12, 28],
    [3, 9, 24],

    # AGOTADO
    [0, 10, 12],
    [0, 8, 20],
    [0, 5, 7],
    [0, 12, 25],
    [0, 9, 15],
]

y = [
    "stock_normal",
    "stock_normal",
    "stock_normal",
    "stock_normal",
    "stock_normal",

    "reposicion",
    "reposicion",
    "reposicion",
    "reposicion",
    "reposicion",

    "prioridad",
    "prioridad",
    "prioridad",
    "prioridad",
    "prioridad",

    "agotado",
    "agotado",
    "agotado",
    "agotado",
    "agotado",
]


# ============================================================
# 3. DIVISIÓN ENTRE ENTRENAMIENTO Y PRUEBA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# ============================================================
# 4. RED NEURONAL
# ============================================================

model = MLPClassifier(
    hidden_layer_sizes=(16,),
    max_iter=1000,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("=== RED NEURONAL ===")
print("Datos de entrenamiento:", len(X_train))
print("Datos de prueba:", len(X_test))
print("Accuracy:", round(accuracy, 4))


# ============================================================
# 5. MOSTRAR PREDICCIONES DE PRUEBA
# ============================================================

print("\n=== PREDICCIONES ===")

for entrada, real, prediccion in zip(X_test, y_test, pred):
    print(
        "Entrada:",
        entrada,
        "| Real:",
        real,
        "| Predicción:",
        prediccion
    )


# ============================================================
# 6. GUARDAR MODELO ENTRENADO
# ============================================================

with (ARTIFACTS / "modelo_inventario_mlp.pkl").open("wb") as file:
    pickle.dump(model, file)


# ============================================================
# 7. BASE DE DATOS SQLITE
# ============================================================

with sqlite3.connect(
    ARTIFACTS / "inventario_reconocimiento.db"
) as con:

    con.execute("""
        CREATE TABLE IF NOT EXISTS predicciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_actual REAL,
            stock_minimo REAL,
            ventas_semanales REAL,
            categoria_real TEXT,
            prediccion TEXT,
            fecha TEXT
        )
    """)

    # Limpiamos la tabla para no duplicar registros
    # cada vez que se ejecute la práctica.
    con.execute("DELETE FROM predicciones")

    fecha_actual = datetime.now().isoformat(
        timespec="seconds"
    )

    for entrada, real, prediccion in zip(
        X_test,
        y_test,
        pred
    ):
        con.execute(
            """
            INSERT INTO predicciones(
                stock_actual,
                stock_minimo,
                ventas_semanales,
                categoria_real,
                prediccion,
                fecha
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entrada[0],
                entrada[1],
                entrada[2],
                real,
                prediccion,
                fecha_actual
            )
        )

    con.commit()


print(
    "\nBase de datos creada:",
    ARTIFACTS / "inventario_reconocimiento.db"
)


# ============================================================
# 8. ONTOLOGÍA DEL PROYECTO
# ============================================================

G = nx.DiGraph()

G.add_edges_from([
    (
        "producto",
        "estado_inventario",
        {"rel": "tiene_estado"}
    ),
    (
        "observacion_inventario",
        "producto",
        {"rel": "describe"}
    ),
    (
        "modelo_mlp",
        "observacion_inventario",
        {"rel": "analiza"}
    ),
    (
        "modelo_mlp",
        "prediccion_inventario",
        {"rel": "produce"}
    ),
    (
        "prediccion_inventario",
        "estado_inventario",
        {"rel": "asigna_estado"}
    ),
    (
        "estado_inventario",
        "reposicion",
        {"rel": "puede_requerir"}
    ),
])


# ============================================================
# 9. ENLAZAR UNA PREDICCIÓN REAL CON LA ONTOLOGÍA
# ============================================================

ejemplo = [4, 10, 25]

estado_predicho = model.predict([ejemplo])[0]

G.add_edge(
    "observacion_1",
    "prediccion_1",
    rel="genera"
)

G.add_edge(
    "prediccion_1",
    f"estado_{estado_predicho}",
    rel="asigna_estado"
)

G.add_edge(
    "observacion_1",
    "producto",
    rel="describe"
)


# ============================================================
# 10. GUARDAR ONTOLOGÍA
# ============================================================

nx.write_graphml(
    G,
    ARTIFACTS / "ontologia_inventario.graphml"
)


# ============================================================
# 11. RESULTADO FINAL
# ============================================================

print("\n=== ONTOLOGÍA ===")
print(
    "Relaciones de ontología:",
    G.number_of_edges()
)

print("\n=== EJEMPLO DE INTEGRACIÓN ===")
print("Entrada:", ejemplo)
print("Predicción:", estado_predicho)

print(
    "Relación:",
    f"prediccion_1 -> asigna_estado -> "
    f"estado_{estado_predicho}"
)