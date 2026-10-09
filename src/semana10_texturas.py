
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, filters, measure, img_as_ubyte
from skimage.feature import local_binary_pattern

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

imagenes = [
    ("Accesorios plasticos", "semana10_terminales.png"),
    ("Cajas metalicas 5800", "semana10_cajas.png"),
]

radius = 2
points = 8 * radius
features_total = []

fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for i, (nombre, archivo) in enumerate(imagenes):
    # 1. Cargar imagen y convertir a escala de grises (0-255).
    image = io.imread(DATA / archivo)

    if image.ndim == 3:
        image = color.rgb2gray(image[:, :, :3])

    image = img_as_ubyte(image)

    # 2. Segmentar mediante Otsu.
    threshold = filters.threshold_otsu(image)
    mask = image > threshold

    # 3. Etiquetar regiones y filtrar las pequenas.
    labels = measure.label(mask)
    regiones_total = measure.regionprops(labels)
    regions = [r for r in regiones_total if r.area > 50]

    areas = np.array([r.area for r in regions], dtype=float)
    area_mean = float(areas.mean()) if len(areas) else 0.0
    area_std = float(areas.std()) if len(areas) else 0.0

    # 4. Histograma de intensidad.
    intensity_hist, intensity_bins = np.histogram(
        image.ravel(), bins=32, range=(0, 256), density=True
    )

    # 5. Descriptor e histograma de textura LBP.
    lbp = local_binary_pattern(
        image, points, radius, method="uniform"
    )
    lbp_hist, _ = np.histogram(
        lbp.ravel(),
        bins=np.arange(0, points + 3),
        density=True
    )

    # 6. Unir las caracteristicas de esta imagen.
    features = np.concatenate([
        [area_mean, area_std, len(regions)],
        intensity_hist,
        lbp_hist
    ])
    features_total.append(features)

    print(f"\n=== {nombre} ===")
    print("Umbral Otsu:", threshold)
    print("Regiones antes del filtro:", len(regiones_total))
    print("Regiones mayores a 50 px:", len(regions))
    print("Area promedio:", round(area_mean, 2))
    print("Desviacion del area:", round(area_std, 2))
    print("Dimension del vector:", len(features))

    # 7. Evidencia visual.
    axes[i, 0].imshow(image, cmap="gray")
    axes[i, 0].set_title(nombre)
    axes[i, 0].axis("off")

    axes[i, 1].imshow(mask, cmap="gray")
    axes[i, 1].set_title(f"Otsu: {threshold}")
    axes[i, 1].axis("off")

    centers = (intensity_bins[:-1] + intensity_bins[1:]) / 2
    axes[i, 2].plot(centers, intensity_hist)
    axes[i, 2].set_title("Histograma intensidad")
    axes[i, 2].set_xlabel("Intensidad")

    axes[i, 3].bar(
        np.arange(len(lbp_hist)), lbp_hist
    )
    axes[i, 3].set_title("Histograma LBP")
    axes[i, 3].set_xlabel("Patron LBP")

# 8. Guardar los vectores de ambas imagenes.
features_total = np.array(features_total)

np.save(
    ARTIFACTS / "semana10_features.npy",
    features_total
)

fig.tight_layout()
fig.savefig(
    ARTIFACTS / "semana10_histograma.png",
    dpi=160
)
plt.close(fig)

print("\nForma del arreglo:", features_total.shape)
print("Guardado: artifacts/semana10_features.npy")
print("Guardado: artifacts/semana10_histograma.png")
