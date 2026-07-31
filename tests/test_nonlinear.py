from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.nonlinear import SystemNewtonResult, newton_system


class SystemNewtonTests(unittest.TestCase):
    @staticmethod
    def circle_line(point):
        x, y = point
        return (x * x + y * y - 1.0, x - y)

    @staticmethod
    def circle_line_jacobian(point):
        x, y = point
        return ((2.0 * x, 2.0 * y), (1.0, -1.0))

    def test_converges_to_circle_line_root_by_residual(self) -> None:
        result = newton_system(self.circle_line, self.circle_line_jacobian, (0.8, 0.6))
        target = math.sqrt(0.5)
        self.assertIsInstance(result, SystemNewtonResult)
        self.assertTrue(result.converged)
        self.assertEqual("residual", result.reason)
        self.assertAlmostEqual(target, result.point[0], places=9)
        self.assertAlmostEqual(target, result.point[1], places=9)
        self.assertLessEqual(result.residual_norm, 1e-10)
        self.assertEqual(result.iterations + 1, len(result.trace))
        with self.assertRaises(FrozenInstanceError):
            result.reason = "changed"

    def test_initial_root_and_step_stop_are_explicit(self) -> None:
        root = math.sqrt(0.5)
        initial = newton_system(self.circle_line, self.circle_line_jacobian, (root, root))
        self.assertEqual(("residual", 0, None), (initial.reason, initial.iterations, initial.last_step_norm))

        step = newton_system(
            lambda p: (p[0] + 1.0,),
            lambda _p: ((1e16,),),
            (0.0,),
            residual_tolerance=1e-30,
            step_tolerance=1e-10,
            condition_limit=1e20,
        )
        self.assertTrue(step.converged)
        self.assertEqual("step", step.reason)
        self.assertGreater(step.residual_norm, 0.5)

    def test_reports_singular_and_ill_conditioned_jacobians(self) -> None:
        singular = newton_system(lambda p: (p[0] + 1.0, p[1] + 1.0), lambda _p: ((1.0, 1.0), (2.0, 2.0)), (0.0, 0.0))
        self.assertEqual("singular_jacobian", singular.reason)
        self.assertFalse(singular.converged)
        ill = newton_system(
            lambda p: (p[0] + 1.0, p[1] + 1.0),
            lambda _p: ((1.0, 0.0), (0.0, 1e-10)),
            (0.0, 0.0),
            condition_limit=1e8,
        )
        self.assertEqual("ill_conditioned_jacobian", ill.reason)
        self.assertGreater(ill.jacobian_condition, 1e8)

    def test_nonfinite_value_preserves_last_finite_point(self) -> None:
        result = newton_system(
            lambda p: (1.0,) if p[0] == 0.0 else (math.inf,),
            lambda _p: ((1.0,),),
            (0.0,),
        )
        self.assertEqual("nonfinite_value", result.reason)
        self.assertEqual((0.0,), result.point)
        self.assertEqual(((0.0,),), result.trace)

    def test_max_iterations_records_every_accepted_iterate(self) -> None:
        result = newton_system(
            lambda p: (p[0] * p[0] + 1.0,),
            lambda p: ((2.0 * p[0],),),
            (1.0,),
            residual_tolerance=1e-30,
            step_tolerance=1e-30,
            max_iterations=1,
        )
        self.assertEqual("max_iterations", result.reason)
        self.assertEqual(1, result.iterations)
        self.assertEqual(2, len(result.trace))

    def test_rejects_invalid_arguments_and_dimensions(self) -> None:
        cases = [
            ({"initial": ()}, "initial"),
            ({"initial": (math.inf,)}, "initial"),
            ({"residual_tolerance": 0.0}, "residual_tolerance"),
            ({"step_tolerance": math.inf}, "step_tolerance"),
            ({"condition_limit": -1.0}, "condition_limit"),
            ({"max_iterations": 0}, "max_iterations"),
            ({"max_iterations": True}, "max_iterations"),
        ]
        for kwargs, marker in cases:
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, marker):
                initial = kwargs.pop("initial", (1.0,))
                newton_system(lambda p: (p[0],), lambda _p: ((1.0,),), initial, **kwargs)
        with self.assertRaisesRegex(ValueError, "function output"):
            newton_system(lambda _p: (1.0, 2.0), lambda _p: ((1.0,),), (1.0,))
        with self.assertRaisesRegex(ValueError, "jacobian"):
            newton_system(lambda p: (p[0],), lambda _p: ((1.0, 2.0),), (1.0,))


if __name__ == "__main__":
    unittest.main()
