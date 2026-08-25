from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix


RANDOM_STATE = 42

ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "data" / "inventario_semana02.csv"


# Cargar el dataset simulado del proyecto
data = pd.read_csv(CSV_FILE)


# X representa la información disponible que utilizará el modelo
X = data[
    [
        "stock_actual",
        "stock_minimo",
        "ventas_30_dias",
        "dias_sin_venta"
    ]
]


# y representa lo que queremos que el modelo aprenda a predecir
# 0 = No necesita reposición
# 1 = Necesita reposición
y = data["necesita_reposicion"]


# Dividir los datos:
# 75% para entrenamiento y 25% para prueba
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=RANDOM_STATE,
    stratify=y
)


# Construcción del modelo
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE
    )
)


# Entrenamiento
model.fit(X_train, y_train)


# Predicciones sobre los datos de prueba
pred = model.predict(X_test)


# Evaluación
print(f"Muestras entrenamiento: {len(X_train)}")
print(f"Muestras prueba: {len(X_test)}")
print(f"Accuracy: {accuracy_score(y_test, pred):.3f}")

print("Matriz de confusión:")
print(confusion_matrix(y_test, pred))