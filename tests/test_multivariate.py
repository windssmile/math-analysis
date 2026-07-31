from dataclasses import FrozenInstanceError
from math import inf, nan
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.multivariate import JacobianCheck, check_jacobian


def sample_function(point):
    x, y = point
    return (x * x + y, x * y)


def sample_jacobian(point):
    x, y = point
    return ((2 * x, 1.0), (y, x))


class JacobianCheckTests(unittest.TestCase):
    def test_checks_a_smooth_square_system(self) -> None:
        result = check_jacobian(sample_function, sample_jacobian, (2.0, 3.0))

        self.assertIsInstance(result, JacobianCheck)
        self.assertEqual(((4.0, 1.0), (3.0, 2.0)), result.analytic)
        self.assertLess(result.max_abs_difference, 1e-5)
        self.assertEqual("checked", result.status)
        self.assertIsNotNone(result.condition_estimate)
        self.assertIn("finite_difference_is_diagnostic", result.assumptions)
        with self.assertRaisesRegex(FrozenInstanceError, "cannot assign to field"):
            result.status = "changed"  # type: ignore[misc]

    def test_reports_a_singular_analytic_jacobian(self) -> None:
        result = check_jacobian(
            lambda point: (point[0] + point[1], 2 * point[0] + 2 * point[1]),
            lambda _point: ((1.0, 1.0), (2.0, 2.0)),
            (0.0, 0.0),
        )

        self.assertEqual("singular", result.status)
        self.assertIsNone(result.condition_estimate)

    def test_reports_an_ill_conditioned_jacobian(self) -> None:
        result = check_jacobian(
            lambda point: (point[0], 1e-14 * point[1]),
            lambda _point: ((1.0, 0.0), (0.0, 1e-14)),
            (1.0, 1.0),
            condition_limit=1e12,
        )

        self.assertEqual("ill_conditioned", result.status)
        self.assertGreater(result.condition_estimate, 1e12)

    def test_supports_rectangular_jacobians_without_condition_estimate(self) -> None:
        result = check_jacobian(
            lambda point: (point[0] + point[1],),
            lambda _point: ((1.0, 1.0),),
            (2.0, 3.0),
        )

        self.assertEqual("checked", result.status)
        self.assertIsNone(result.condition_estimate)
        self.assertEqual(((1.0, 1.0),), result.analytic)

    def test_rejects_invalid_scalar_arguments(self) -> None:
        for point in ((nan,), (inf,), ()):
            with self.subTest(point=point):
                with self.assertRaises(ValueError):
                    check_jacobian(lambda value: value, lambda _value: ((1.0,),), point)
        for step in (0.0, -1.0, nan, inf):
            with self.subTest(step=step):
                with self.assertRaisesRegex(ValueError, "^step must be positive and finite$"):
                    check_jacobian(sample_function, sample_jacobian, (1.0, 2.0), step=step)
        for limit in (0.0, -1.0, nan, inf):
            with self.subTest(limit=limit):
                with self.assertRaisesRegex(ValueError, "^condition_limit must be positive and finite$"):
                    check_jacobian(
                        sample_function,
                        sample_jacobian,
                        (1.0, 2.0),
                        condition_limit=limit,
                    )

    def test_rejects_dimension_drift_and_malformed_matrices(self) -> None:
        with self.assertRaisesRegex(ValueError, "^function output dimension changed$"):
            check_jacobian(
                lambda point: (point[0],) if point[0] == 1.0 else (point[0], point[0]),
                lambda _point: ((1.0,),),
                (1.0,),
            )
        with self.assertRaisesRegex(ValueError, "^jacobian row count must match output dimension$"):
            check_jacobian(sample_function, lambda _point: ((1.0, 0.0),), (1.0, 2.0))
        with self.assertRaisesRegex(ValueError, "^jacobian column count must match point dimension$"):
            check_jacobian(sample_function, lambda _point: ((1.0,), (1.0,)), (1.0, 2.0))

    def test_rejects_nonfinite_function_or_jacobian_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "^function values must be finite$"):
            check_jacobian(lambda _point: (nan,), lambda _point: ((1.0,),), (1.0,))
        with self.assertRaisesRegex(ValueError, "^jacobian values must be finite$"):
            check_jacobian(lambda point: point, lambda _point: ((inf,),), (1.0,))


if __name__ == "__main__":
    unittest.main()
