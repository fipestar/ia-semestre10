import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

RANDOM_STATE = 42

#cargar el dataset de inventario
data = pd.read_csv("data/inventario_semana02.csv")

#X contiene las caracteristicas que usara el modelo
X = data[
    [
        "stock_actual",
        "stock_minimo",
        "ventas_30_dias",
        "dias_sin_venta"
    ]
]

#y contiene lo que queremos predecir
y = data["necesita_reposicion"]

#Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.25,
    random_state=RANDOM_STATE,
    stratify=y
)

#crear el modelo
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(
        max_iter=1000, 
        random_state=RANDOM_STATE
        )
)

#entrenar el modelo
model.fit(X_train, y_train)

#predecir
pred = model.predict(X_test)

#evaluar el modelo
print(f"Muestras entrenamiento: {len(X_train)}")
print(f"Muestras prueba: {len(X_test)}")
print(f"Accuracy: {accuracy_score(y_test, pred):.3f}") 
print("Matriz de confusión:")
print(confusion_matrix(y_test, pred))