
from pathlib import Path
from time import perf_counter

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

# Datos de inventario utilizados en la Semana 8.
# Caracteristicas: stock_actual, stock_minimo, ventas_semanales.
X = [
    [20, 10, 8], [18, 10, 6], [15, 8, 5],
    [25, 12, 10], [14, 7, 4],
    [8, 10, 7], [6, 10, 8], [5, 10, 6],
    [7, 12, 9], [4, 8, 5],
    [4, 10, 25], [3, 10, 30], [2, 8, 20],
    [5, 12, 28], [3, 9, 24],
    [0, 10, 12], [0, 8, 20], [0, 5, 7],
    [0, 12, 25], [0, 9, 15],
]

y = (
    ["stock_normal"] * 5
    + ["reposicion"] * 5
    + ["prioridad"] * 5
    + ["agotado"] * 5
)

rows = []

# Tres pruebas con diferentes divisiones reproducibles.
for repeticion in range(1, 4):
    semilla = 41 + repeticion

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=semilla,
        stratify=y
    )

    # Los tres modelos usan el mismo split en cada repeticion.
    models = {
        "Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1500)
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=250,
            random_state=42,
            n_jobs=-1
        ),
        "MLPClassifier": make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(16,),
                max_iter=1000,
                random_state=42
            )
        ),
    }

    print(f"\n=== REPETICION {repeticion} ===")
    print("Entrenamiento:", len(X_train))
    print("Prueba:", len(X_test))

    for nombre, modelo in models.items():
        inicio = perf_counter()

        modelo.fit(X_train, y_train)

        tiempo = perf_counter() - inicio
        predicciones = modelo.predict(X_test)
        accuracy = accuracy_score(y_test, predicciones)

        rows.append({
            "repeticion": repeticion,
            "semilla": semilla,
            "modelo": nombre,
            "accuracy": accuracy,
            "fit_seconds": tiempo,
        })

        print(
            f"{nombre}: "
            f"accuracy={accuracy:.4f} | "
            f"tiempo={tiempo:.4f}s"
        )

# Crear tabla con las nueve mediciones.
df = pd.DataFrame(rows)
df.to_csv(ARTIFACTS / "benchmark.csv", index=False)

# Resumen para facilitar la decision tecnica.
resumen = df.groupby("modelo").agg(
    accuracy_promedio=("accuracy", "mean"),
    accuracy_desviacion=("accuracy", "std"),
    tiempo_promedio=("fit_seconds", "mean")
).sort_values("accuracy_promedio", ascending=False)

print("\n=== RESUMEN DE LOS TRES MODELOS ===")
print(resumen.round(4).to_string())

print("\nGuardado: artifacts/benchmark.csv")
