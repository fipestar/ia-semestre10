from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"

KB_PATH = DATA_DIR / "base_conocimiento.txt"
REPORT_PATH = REPORTS_DIR / "semana05.md"


# -------------------------------------------------------------------
# 1. SISTEMA EXPERTO
# -------------------------------------------------------------------
# Cada regla contiene:
# - una condición que revisa palabras o frases en la consulta
# - una acción o recomendación asociada

RULES = [
    (
        lambda q: "agotado" in q or "sin unidades" in q or "stock cero" in q,
        "reponer_inmediatamente"
    ),
    (
        lambda q: (
            "stock bajo" in q
            or "debajo del minimo" in q
            or "por debajo del minimo" in q
        ),
        "revisar_reposicion"
    ),
    (
        lambda q: (
            "alta rotacion" in q
            or "se vende mucho" in q
            or "mucha demanda" in q
        ),
        "aumentar_prioridad"
    ),
    (
        lambda q: "stock suficiente" in q or "buen stock" in q,
        "no_reponer"
    ),
    (
        lambda q: (
            "diferencia" in q
            and (
                "stock" in q
                or "inventario" in q
                or "conteo" in q
            )
        ),
        "revisar_inventario"
    ),
]


# -------------------------------------------------------------------
# 2. EJEMPLOS ETIQUETADOS PARA EL CLASIFICADOR
# -------------------------------------------------------------------
# La práctica exige mínimo 15 ejemplos etiquetados.
# Todos estos ejemplos están adaptados al dominio del inventario.

TRAIN_X = [
    "el producto esta agotado",
    "no quedan unidades disponibles",
    "el stock llego a cero",

    "el stock esta por debajo del minimo",
    "quedan muy pocas unidades",
    "el producto necesita reposicion",

    "el producto tiene suficiente inventario",
    "hay buen stock disponible",
    "no es necesario reponer este producto",

    "este producto se vende mucho",
    "es un producto de alta rotacion",
    "quedan pocas unidades y tiene mucha demanda",

    "hay diferencia entre el stock registrado y el visible",
    "el conteo fisico no coincide con el inventario",
    "debe revisarse la diferencia de inventario"
]

TRAIN_Y = [
    "agotado",
    "agotado",
    "agotado",

    "reposicion",
    "reposicion",
    "reposicion",

    "stock_normal",
    "stock_normal",
    "stock_normal",

    "prioridad",
    "prioridad",
    "prioridad",

    "revision",
    "revision",
    "revision"
]


# -------------------------------------------------------------------
# 3. CONSULTAS DE PRUEBA
# -------------------------------------------------------------------
TEST_QUERIES = [
    "El producto está por debajo del mínimo y quedan pocas unidades",
    "No quedan unidades visibles, el producto está agotado",
    "Este producto se vende mucho y debería tener prioridad de reposición",
]


def normalize_text(text: str) -> str:
    """
    Normalización básica para facilitar la comparación por reglas.
    """
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
    }

    normalized = text.lower().strip()

    for original, replacement in replacements.items():
        normalized = normalized.replace(original, replacement)

    return normalized


def load_documents() -> list[str]:
    """
    Carga la base de conocimiento desde data/base_conocimiento.txt.
    Valida que existan al menos 8 entradas.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not KB_PATH.exists():
        raise FileNotFoundError(
            f"No existe {KB_PATH}. "
            "Crea data/base_conocimiento.txt antes de ejecutar."
        )

    docs = [
        line.strip()
        for line in KB_PATH.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(docs) < 8:
        raise ValueError(
            "data/base_conocimiento.txt debe contener "
            "al menos 8 entradas."
        )

    return docs


def build_retrieval_system(documents: list[str]):
    """
    Crea la representación TF-IDF de la base de conocimiento.
    """

    vectorizer = TfidfVectorizer()
    doc_matrix = vectorizer.fit_transform(documents)

    return vectorizer, doc_matrix


def build_classifier():
    """
    Entrena un clasificador de texto usando:
    - TF-IDF
    - Regresión logística
    """

    classifier = make_pipeline(
        TfidfVectorizer(),
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )

    classifier.fit(
        TRAIN_X,
        TRAIN_Y
    )

    return classifier


def apply_rules(query: str) -> list[str]:
    """
    Evalúa las reglas expertas y devuelve
    las acciones cuyas condiciones se cumplen.
    """

    q = normalize_text(query)

    fired_rules = [
        action
        for condition, action in RULES
        if condition(q)
    ]

    return fired_rules


def retrieve_information(
    query: str,
    documents: list[str],
    vectorizer: TfidfVectorizer,
    doc_matrix
) -> tuple[str, float]:
    """
    Busca la entrada de la base de conocimiento
    más parecida a la consulta mediante:
    TF-IDF + similitud coseno.
    """

    q = normalize_text(query)

    query_vector = vectorizer.transform([q])

    similarities = cosine_similarity(
        query_vector,
        doc_matrix
    )[0]

    best_index = int(
        similarities.argmax()
    )

    best_document = documents[best_index]
    best_similarity = float(
        similarities[best_index]
    )

    return (
        best_document,
        best_similarity
    )


def answer(
    query: str,
    documents: list[str],
    vectorizer: TfidfVectorizer,
    doc_matrix,
    classifier
) -> dict:
    """
    Procesa una consulta utilizando:
    1. Reglas expertas
    2. Recuperación de información
    3. Clasificación
    """

    fired_rules = apply_rules(query)

    evidence, similarity = retrieve_information(
        query,
        documents,
        vectorizer,
        doc_matrix
    )

    predicted_class = str(
        classifier.predict([query])[0]
    )

    return {
        "reglas": fired_rules,
        "evidencia": evidence,
        "similitud": similarity,
        "clase": predicted_class,
    }


def write_report(
    rows: list[tuple[str, dict]]
) -> None:
    """
    Genera reports/semana05.md con la trazabilidad
    de las consultas ejecutadas.
    """

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    lines = [
        "# Semana 05 - Sistema híbrido aplicado al inventario ferretero",
        "",
        "El sistema combina reglas expertas, recuperación de información "
        "mediante TF-IDF y similitud coseno, y clasificación de texto.",
        "",
    ]

    for i, (query, result) in enumerate(
        rows,
        start=1
    ):
        reglas = (
            ", ".join(result["reglas"])
            if result["reglas"]
            else "ninguna"
        )

        lines += [
            f"## Consulta {i}",
            "",
            f"- **Consulta:** {query}",
            f"- **Regla activada:** {reglas}",
            f"- **Evidencia recuperada:** {result['evidencia']}",
            f"- **Similitud:** {result['similitud']:.3f}",
            f"- **Clasificación:** {result['clase']}",
            "",
        ]

    lines += [
        "## Limitaciones",
        "",
        "- Las reglas expertas dependen de palabras o frases definidas manualmente.",
        "- La recuperación TF-IDF depende de los términos presentes en la base de conocimiento.",
        "- El clasificador se entrena con pocos ejemplos, por lo que puede equivocarse ante consultas muy diferentes.",
        "- El sistema todavía no utiliza datos reales del ERP ni imágenes capturadas por cámara.",
        "",
    ]

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


def main() -> None:
    """
    Ejecuta las tres consultas de prueba,
    imprime resultados y genera el reporte.
    """

    documents = load_documents()

    vectorizer, doc_matrix = (
        build_retrieval_system(
            documents
        )
    )

    classifier = build_classifier()

    results = []

    print("=" * 80)
    print(
        "SEMANA 05 - SISTEMA HÍBRIDO "
        "DE INVENTARIO FERRETERO"
    )
    print("=" * 80)

    for i, query in enumerate(
        TEST_QUERIES,
        start=1
    ):
        result = answer(
            query,
            documents,
            vectorizer,
            doc_matrix,
            classifier
        )

        results.append(
            (query, result)
        )

        print(
            f"\nCONSULTA {i}"
        )
        print(
            f"Entrada: {query}"
        )

        print(
            "Reglas activadas:",
            ", ".join(result["reglas"])
            if result["reglas"]
            else "ninguna"
        )

        print(
            f"Evidencia recuperada: "
            f"{result['evidencia']}"
        )

        print(
            f"Similitud: "
            f"{result['similitud']:.3f}"
        )

        print(
            f"Clasificación: "
            f"{result['clase']}"
        )

    write_report(results)

    print(
        f"\nReporte generado: "
        f"{REPORT_PATH}"
    )


if __name__ == "__main__":
    main()
