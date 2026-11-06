"""Semana 14: red semantica de productos de una ferreteria (biblioteca estandar)."""

from __future__ import annotations

import re
import unicodedata
from collections import deque


# Ocho conceptos pertenecientes al dominio de inventario ferretero.
CONCEPTOS = frozenset({
    "producto_ferretero",
    "material_electrico",
    "accesorio_electrico",
    "caja_electrica",
    "caja_5800",
    "conector_electrico",
    "conector_rapido",
    "control_stock",
})
RELACIONES = frozenset({"es_un", "requiere"})


def normalizar(texto: str) -> str:
    """Unifica espacios, mayusculas y tildes; no intenta entender lenguaje libre."""
    if not isinstance(texto, str):
        raise ValueError("La entrada debe ser texto")
    base = unicodedata.normalize("NFD", texto.casefold().strip())
    sin_tildes = "".join(c for c in base if unicodedata.category(c) != "Mn")
    return " ".join(sin_tildes.split())


def _concepto(texto: str) -> str:
    clave = normalizar(texto).replace(" ", "_")
    if clave not in CONCEPTOS:
        raise ValueError(f"Concepto no admitido: {texto!r}")
    return clave


def interpretar(oracion: str) -> tuple[str, str, str]:
    """Acepta exclusivamente: 'Un X es un Y' y 'Un X requiere Y'."""
    texto = normalizar(oracion).strip(" .!?")
    patrones = (
        (r"(?:un|una|el|la) (.+?) es (?:un|una) (.+)", "es_un"),
        (r"(?:un|una|el|la) (.+?) requiere (.+)", "requiere"),
    )
    for patron, relacion in patrones:
        coincidencia = re.fullmatch(patron, texto)
        if coincidencia:
            sujeto, objeto = coincidencia.groups()
            return _concepto(sujeto), relacion, _concepto(objeto)
    raise ValueError("Oracion no admitida: use 'Un X es un Y' o 'Un X requiere Y'")


class RedSemantica:
    """Grafo dirigido de triples explicitos y consultas inferidas por jerarquia."""

    def __init__(self) -> None:
        self._triples: set[tuple[str, str, str]] = set()
        self._aristas: dict[str, set[tuple[str, str]]] = {}

    def agregar(self, sujeto: str, relacion: str, objeto: str) -> None:
        sujeto = _concepto(sujeto)
        objeto = _concepto(objeto)
        relacion = normalizar(relacion)
        if relacion not in RELACIONES:
            raise ValueError(f"Relacion no admitida: {relacion}")
        if relacion == "es_un" and sujeto == objeto:
            raise ValueError("Una categoria no se declara como subtipo directo de si misma")
        triple = (sujeto, relacion, objeto)
        self._triples.add(triple)
        self._aristas.setdefault(sujeto, set()).add((relacion, objeto))

    def triples(self) -> list[tuple[str, str, str]]:
        return sorted(self._triples)

    def relacionados(self, sujeto: str) -> list[tuple[str, str]]:
        """Lista solo las relaciones explicitas salientes del concepto."""
        sujeto = _concepto(sujeto)
        return sorted(self._aristas.get(sujeto, set()))

    def ruta_es_un(self, origen: str, categoria: str) -> list[str] | None:
        """Camino BFS de subtipos; None = no demostrado en esta red."""
        origen, categoria = _concepto(origen), _concepto(categoria)
        pendientes = deque([(origen, [origen])])
        visitados: set[str] = set()
        while pendientes:
            actual, ruta = pendientes.popleft()
            if actual == categoria:
                return ruta
            if actual in visitados:
                continue
            visitados.add(actual)
            for relacion, destino in sorted(self._aristas.get(actual, set())):
                if relacion == "es_un" and destino not in visitados:
                    pendientes.append((destino, ruta + [destino]))
        return None

    def es_un(self, origen: str, categoria: str) -> bool:
        return self.ruta_es_un(origen, categoria) is not None

    def propiedades(self, concepto: str, relacion: str = "requiere") -> list[tuple[str, str, list[str]]]:
        """Devuelve (propiedad, origen, camino) de propiedades directas/heredadas.

        Solo 'requiere' se hereda desde las categorias superiores: no cualquier arista.
        """
        concepto = _concepto(concepto)
        if relacion != "requiere":
            raise ValueError("Solo la relacion 'requiere' se hereda en este prototipo")
        pendientes = deque([(concepto, [concepto])])
        visitados: set[str] = set()
        resultados: dict[str, tuple[str, str, list[str]]] = {}
        while pendientes:
            actual, ruta = pendientes.popleft()
            if actual in visitados:
                continue
            visitados.add(actual)
            for tipo, destino in sorted(self._aristas.get(actual, set())):
                if tipo == "es_un" and destino not in visitados:
                    pendientes.append((destino, ruta + [destino]))
                elif tipo == relacion and destino not in resultados:
                    resultados[destino] = (destino, actual, ruta)
        return [resultados[clave] for clave in sorted(resultados)]
