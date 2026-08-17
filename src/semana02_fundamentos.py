from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
RANDOM_STATE = 42
X, y = load_iris(return_X_y=True) # x es la info disponible, y es lo que queremos que el modelo aprenda a predecir
X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y #se reserva el 25% para entrenar el modelo
)
model = make_pipeline(
 StandardScaler(),
 LogisticRegression(max_iter=1000, random_state=RANDOM_STATE) #se construye el modelo de regresión logística con un máximo de 1000 iteraciones y una semilla aleatoria para reproducibilidad
)
model.fit(X_train, y_train) #se entrena el modelo con los datos de entrenamiento
pred = model.predict(X_test) #Respuesta del modelo
print(f"Muestras entrenamiento: {len(X_train)}")
print(f"Muestras prueba: {len(X_test)}")
print(f"Accuracy: {accuracy_score(y_test, pred):.3f}") #Evaluación del modelo con la métrica de precisión
print("Matriz de confusión:")
print(confusion_matrix(y_test, pred))