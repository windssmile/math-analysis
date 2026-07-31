from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.optimization import (
    EqualityCandidateCheck,
    OptimizationResult,
    check_equality_candidate,
    gradient_descent,
    newton_optimize,
)


class OptimizationTests(unittest.TestCase):
    @staticmethod
    def objective(point):
        x, y = point
        return 0.5 * (x * x + 4.0 * y * y)

    @staticmethod
    def gradient(point):
        x, y = point
        return (x, 4.0 * y)

    @staticmethod
    def hessian(_point):
        return ((1.0, 0.0), (0.0, 4.0))

    def test_gradient_descent_reaches_quadratic_stationarity(self) -> None:
        result = gradient_descent(self.objective, self.gradient, (2.0, -1.0))
        self.assertIsInstance(result, OptimizationResult)
        self.assertTrue(result.converged)
        self.assertEqual("gradient", result.reason)
        self.assertLessEqual(result.gradient_norm, 1e-8)
        self.assertEqual(result.iterations + 1, len(result.trace))
        with self.assertRaises(FrozenInstanceError):
            result.reason = "changed"

    def test_newton_reaches_quadratic_stationarity(self) -> None:
        result = newton_optimize(self.objective, self.gradient, self.hessian, (2.0, -1.0))
        self.assertTrue(result.converged)
        self.assertEqual("gradient", result.reason)
        self.assertEqual("positive_definite", result.hessian_status)
        self.assertAlmostEqual(0.0, result.objective)

    def test_step_and_budget_reasons_are_explicit(self) -> None:
        step = gradient_descent(
            lambda p: p[0],
            lambda _p: (1.0,),
            (0.0,),
            initial_step=1e-12,
            gradient_tolerance=1e-30,
            step_tolerance=1e-10,
        )
        self.assertEqual("step", step.reason)
        budget = gradient_descent(
            self.objective,
            self.gradient,
            (2.0, -1.0),
            gradient_tolerance=1e-30,
            step_tolerance=1e-30,
            max_iterations=1,
        )
        self.assertEqual("max_iterations", budget.reason)
        self.assertFalse(budget.converged)

    def test_newton_reports_hessian_failures(self) -> None:
        singular = newton_optimize(
            self.objective, self.gradient, lambda _p: ((1.0, 0.0), (0.0, 0.0)), (1.0, 1.0)
        )
        self.assertEqual("singular_hessian", singular.reason)
        indefinite = newton_optimize(
            self.objective, self.gradient, lambda _p: ((1.0, 0.0), (0.0, -1.0)), (1.0, 1.0)
        )
        self.assertEqual("indefinite_hessian", indefinite.reason)
        non_descent = newton_optimize(
            lambda p: p[0],
            lambda _p: (1.0,),
            lambda _p: ((-1.0,),),
            (0.0,),
            require_positive_definite=False,
        )
        self.assertEqual("non_descent_direction", non_descent.reason)

    def test_nonfinite_value_preserves_last_finite_point(self) -> None:
        result = gradient_descent(
            lambda p: 0.0 if p[0] == 0.0 else math.inf,
            lambda _p: (1.0,),
            (0.0,),
        )
        self.assertEqual("nonfinite_value", result.reason)
        self.assertEqual((0.0,), result.point)
        self.assertEqual(((0.0,),), result.trace)

    def test_equality_candidate_returns_residuals_not_optimality(self) -> None:
        check = check_equality_candidate(
            lambda p: (2.0 * p[0], 2.0 * p[1]),
            lambda _p: ((1.0, 1.0),),
            (0.5, 0.5),
            (-1.0,),
            constraints=lambda p: (p[0] + p[1] - 1.0,),
        )
        self.assertIsInstance(check, EqualityCandidateCheck)
        self.assertEqual((0.0, 0.0), check.stationarity_residual)
        self.assertEqual((0.0,), check.constraint_residual)
        self.assertFalse(hasattr(check, "optimal"))

    def test_rejects_invalid_arguments_and_dimension_drift(self) -> None:
        with self.assertRaisesRegex(ValueError, "initial"):
            gradient_descent(self.objective, self.gradient, (), max_iterations=2)
        with self.assertRaisesRegex(ValueError, "gradient"):
            gradient_descent(self.objective, lambda _p: (1.0,), (1.0, 1.0))
        with self.assertRaisesRegex(ValueError, "max_iterations"):
            gradient_descent(self.objective, self.gradient, (1.0, 1.0), max_iterations=0)
        with self.assertRaisesRegex(ValueError, "hessian"):
            newton_optimize(self.objective, self.gradient, lambda _p: ((1.0,),), (1.0, 1.0))
        with self.assertRaisesRegex(ValueError, "constraint_jacobian"):
            check_equality_candidate(
                self.gradient,
                lambda _p: ((1.0, 1.0),),
                (1.0, 1.0),
                (1.0, 2.0),
            )


if __name__ == "__main__":
    unittest.main()
