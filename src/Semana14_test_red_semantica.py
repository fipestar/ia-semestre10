"""Pruebas de redes semanticas del inventario ferretero."""

import unittest
from Semana14_red_semantica import RedSemantica, interpretar, normalizar
from Semana14_main import ORACIONES


class TestRedSemanticaFerretera(unittest.TestCase):
    def setUp(self) -> None:
        self.red = RedSemantica()
        for frase in ORACIONES:
            self.red.agregar(*interpretar(frase))

    def test_normalizacion(self) -> None:
        self.assertEqual(normalizar("  CAJA   ELÉCTRICA "), "caja electrica")

    def test_parser_es_un(self) -> None:
        self.assertEqual(
            interpretar("Una CAJA 5800 es una Caja Eléctrica."),
            ("caja_5800", "es_un", "caja_electrica"),
        )

    def test_parser_requiere(self) -> None:
        self.assertEqual(
            interpretar("Un producto ferretero requiere control stock."),
            ("producto_ferretero", "requiere", "control_stock"),
        )

    def test_oracion_invalida(self) -> None:
        with self.assertRaises(ValueError):
            interpretar("Las cajas eléctricas pesan mucho.")

    def test_concepto_desconocido(self) -> None:
        with self.assertRaises(ValueError):
            interpretar("Un perro es un producto ferretero.")

    def test_relacion_invalida(self) -> None:
        with self.assertRaises(ValueError):
            self.red.agregar("caja_5800", "se_come", "producto_ferretero")

    def test_triple_explicito_y_consulta(self) -> None:
        self.assertIn(("caja_5800", "es_un", "caja_electrica"), self.red.triples())
        self.assertIn(("es_un", "caja_electrica"), self.red.relacionados("caja_5800"))
        self.assertNotIn(("caja_5800", "es_un", "producto_ferretero"), self.red.triples())

    def test_transitividad_con_traza(self) -> None:
        self.assertEqual(self.red.ruta_es_un("caja_5800", "producto_ferretero"), [
            "caja_5800", "caja_electrica", "accesorio_electrico",
            "material_electrico", "producto_ferretero",
        ])

    def test_herencia_con_traza(self) -> None:
        self.assertEqual(self.red.propiedades("caja_5800"), [(
            "control_stock", "producto_ferretero",
            ["caja_5800", "caja_electrica", "accesorio_electrico",
             "material_electrico", "producto_ferretero"],
        )])

    def test_sin_evidencia(self) -> None:
        self.assertFalse(self.red.es_un("caja_5800", "conector_electrico"))
        self.assertIsNone(self.red.ruta_es_un("caja_5800", "conector_electrico"))

    def test_no_duplicar_triples(self) -> None:
        antes = len(self.red.triples())
        self.red.agregar("caja_5800", "es_un", "caja_electrica")
        self.assertEqual(len(self.red.triples()), antes)

    def test_ciclo_no_infinito(self) -> None:
        self.red.agregar("producto_ferretero", "es_un", "caja_5800")
        self.assertFalse(self.red.es_un("caja_5800", "conector_rapido"))
        self.assertEqual(len(self.red.propiedades("caja_5800")), 1)

    def test_relaciones_que_no_son_jerarquicas(self) -> None:
        self.assertFalse(self.red.es_un("producto_ferretero", "control_stock"))


if __name__ == "__main__":
    unittest.main()
