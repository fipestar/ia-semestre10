from pathlib import Path
from importlib import import_module

import matplotlib.pyplot as plt


# Carga diferida para evitar falsos diagnósticos del analizador cuando
# `scikit-image` está instalado en un intérprete distinto al seleccionado.
skimage = import_module("skimage")
feature = skimage.feature
filters = skimage.filters
io = skimage.io
label = import_module("skimage.measure").label


# ============================================================
# 1. RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTIFACTS = ROOT / "artifacts"

ARTIFACTS.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. CARGAR IMAGEN DEL PROYECTO
# ============================================================

image = io.imread(
    DATA / "imagen_proyecto2.png",
    as_gray=True
)


# ============================================================
# 3. DETECCIÓN DE BORDES - CANNY
# ============================================================

edges_sigma_1 = feature.canny(
    image,
    sigma=1.0
)

edges_sigma_2 = feature.canny(
    image,
    sigma=2.0
)

edges_sigma_4 = feature.canny(
    image,
    sigma=4.0
)


# ============================================================
# 4. SEGMENTACIÓN MEDIANTE OTSU
# ============================================================

threshold = filters.threshold_otsu(image)

mask = image > threshold


# ============================================================
# 5. REGIONES CONECTADAS
# ============================================================

labels = label(mask)

numero_regiones = labels.max()

print("Umbral Otsu:", round(float(threshold), 4))
print("Regiones conectadas:", numero_regiones)


# ============================================================
# 6. EVIDENCIA VISUAL
# ============================================================

fig, axes = plt.subplots(
    1,
    5,
    figsize=(18, 4)
)

axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original")

axes[1].imshow(edges_sigma_1, cmap="gray")
axes[1].set_title("Canny sigma=1")

axes[2].imshow(edges_sigma_2, cmap="gray")
axes[2].set_title("Canny sigma=2")

axes[3].imshow(edges_sigma_4, cmap="gray")
axes[3].set_title("Canny sigma=4")

axes[4].imshow(mask, cmap="gray")
axes[4].set_title("Otsu")


for ax in axes:
    ax.axis("off")


fig.tight_layout()

fig.savefig(
    ARTIFACTS / "semana09_vision.png",
    dpi=160
)

print(
    "Guardado:",
    ARTIFACTS / "semana09_vision.png"
)