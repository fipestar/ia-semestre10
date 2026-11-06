"""Pruebas automáticas para motor lógico de Semana 13."""

import unittest

from Semana13motor_inferencia import Regla, construir_reglas, inferir


class TestMotorInferenciaFerretero(unittest.TestCase):
    def setUp(self) -> None:
        self.hechos_base = {
            "stock_bajo",
            "alta_rotacion",
            "proveedor_disponible",
            "presupuesto_confirmado",
        }
        self.objetivo = "pedido_prioritario_recomendado"

    def test_caso_a_demuestra_recomendacion_y_traza(self) -> None:
        hechos, trazas = inferir(self.hechos_base, construir_reglas())
        self.assertIn(self.objetivo, hechos)
        self.assertEqual(len(trazas), 3)
        self.assertTrue(trazas[0].startswith("R1:"))
        self.assertTrue(trazas[1].startswith("R2:"))
        self.assertTrue(trazas[2].startswith("R3:"))

    def test_caso_b_sin_presupuesto_no_demuestra_recomendacion(self) -> None:
        iniciales = self.hechos_base - {"presupuesto_confirmado"}
        hechos, trazas = inferir(iniciales, construir_reglas())
        self.assertNotIn(self.objetivo, hechos)
        self.assertIn("abastecimiento_viable", hechos)
        self.assertEqual(len(trazas), 2)

    def test_no_se_modifican_los_hechos_iniciales(self) -> None:
        originales = set(self.hechos_base)
        finales, _ = inferir(self.hechos_base, construir_reglas())
        self.assertEqual(self.hechos_base, originales)
        self.assertTrue(originales.issubset(finales))

    def test_ciclo_termina_sin_duplicados(self) -> None:
        reglas = [
            Regla("C1", frozenset({"a"}), "b"),
            Regla("C2", frozenset({"b"}), "a"),
        ]
        hechos, trazas = inferir({"a"}, reglas)
        self.assertEqual(hechos, {"a", "b"})
        self.assertEqual(len(trazas), 1)

    def test_reglas_en_orden_inverso_tambien_funcionan(self) -> None:
        hechos, trazas = inferir(self.hechos_base, list(reversed(construir_reglas())))
        self.assertIn(self.objetivo, hechos)
        self.assertEqual(len(trazas), 3)

    def test_regla_repetida_no_duplica_conclusion(self) -> None:
        reglas = construir_reglas()
        hechos, trazas = inferir(self.hechos_base, reglas + [reglas[0]])
        self.assertIn(self.objetivo, hechos)
        self.assertEqual(len(trazas), 3)

    def test_rama_alternativa_reposicion_programada(self) -> None:
        iniciales = {"stock_bajo", "rotacion_baja"}
        hechos, trazas = inferir(iniciales, construir_reglas())
        self.assertIn("revision_reposicion_programada", hechos)
        self.assertNotIn(self.objetivo, hechos)
        self.assertEqual(len(trazas), 1)
        self.assertTrue(trazas[0].startswith("R4:"))

    def test_sin_reglas_no_hay_inferencia(self) -> None:
        hechos, trazas = inferir(self.hechos_base, [])
        self.assertEqual(hechos, self.hechos_base)
        self.assertEqual(trazas, [])


if __name__ == "__main__":
    unittest.main()
