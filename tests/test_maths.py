import math
import unittest

from maths import (
    advertising_model,
    budget_parts,
    future_value,
    integrated_product,
    linear_break_even,
    marginal_model,
    optimal_quantity,
    quadratic_analysis,
)


class MathsTestCase(unittest.TestCase):
    def test_budget_parts(self):
        r = budget_parts(250_000, .15, .42)
        self.assertEqual(r["communication"], 37_500)
        self.assertEqual(r["digital"], 15_750)
        self.assertEqual(r["reste"], 212_500)

    def test_future_value(self):
        self.assertTrue(math.isclose(future_value(10_000, .04, 8), 13_685.690504, rel_tol=1e-8))

    def test_linear_break_even(self):
        self.assertEqual(linear_break_even(5_000, 25, 15), 500)

    def test_quadratic_analysis(self):
        r = quadratic_analysis(-1, 10, -16)
        self.assertEqual(r.discriminant, 36)
        self.assertEqual(r.roots, (2, 8))
        self.assertEqual(r.vertex_x, 5)
        self.assertEqual(r.vertex_y, 9)

    def test_marginal_model(self):
        r = marginal_model(500, 30, .5, 100, .8, 20)
        self.assertEqual(r["marginal_cost"], 50)
        self.assertEqual(r["marginal_revenue"], 68)
        self.assertEqual(r["marginal_profit"], 18)

    def test_optimal_quantity(self):
        self.assertTrue(math.isclose(optimal_quantity(30, .5, 100, .8), 70 / 2.6))

    def test_advertising_model(self):
        r = advertising_model(1_200, 20_000, 80, 15_000)
        self.assertTrue(math.isclose(r["sales"], 1_200 * 15_000 / 35_000))

    def test_integrated_product_capacity(self):
        r = integrated_product(1_000, 10, 5_000, 20, 30, 600)
        self.assertEqual(r["demand"], 700)
        self.assertEqual(r["quantity"], 600)
        self.assertEqual(r["profit"], 1_000)


if __name__ == "__main__":
    unittest.main()
