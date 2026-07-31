from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.vector_analysis import (
    FluxIntegralResult,
    LineIntegralResult,
    composite_midpoint_flux_integral,
    composite_midpoint_line_integral,
)


class LineIntegralTests(unittest.TestCase):
    def test_constant_field_on_parabola_and_metadata(self) -> None:
        result = composite_midpoint_line_integral(
            lambda point: (1.0, 0.0),
            curve=lambda t: (t, t * t),
            curve_derivative=lambda t: (1.0, 2.0 * t),
            bounds=(0.0, 1.0),
            n=7,
        )
        self.assertIsInstance(result, LineIntegralResult)
        self.assertAlmostEqual(1.0, result.value)
        self.assertEqual(((0.0, 1.0), 7, 7), (result.bounds, result.n, result.evaluations))
        with self.assertRaises(FrozenInstanceError):
            result.value = 0.0

    def test_reversing_curve_orientation_changes_sign(self) -> None:
        forward = composite_midpoint_line_integral(
            lambda point: (2.0, -1.0), curve=lambda t: (t, t * t),
            curve_derivative=lambda t: (1.0, 2.0 * t), bounds=(0.0, 1.0), n=8,
        )
        reverse = composite_midpoint_line_integral(
            lambda point: (2.0, -1.0), curve=lambda t: (1.0 - t, (1.0 - t) ** 2),
            curve_derivative=lambda t: (-1.0, -2.0 * (1.0 - t)), bounds=(0.0, 1.0), n=8,
        )
        self.assertAlmostEqual(forward.value, -reverse.value)

    def test_rejects_bad_input_and_callback_results(self) -> None:
        common = dict(field=lambda p: (1.0, 2.0), curve=lambda t: (t, t),
                      curve_derivative=lambda t: (1.0, 1.0), bounds=(0.0, 1.0), n=2)
        for replacement in (
            {"n": True}, {"bounds": (1.0, 0.0)}, {"bounds": (1.0, 1.0)},
            {"bounds": (0.0, math.inf)}, {"curve": lambda t: (t, t, t)},
            {"field": lambda p: (1.0,)}, {"curve_derivative": lambda t: (1.0, 1.0, 1.0)},
            {"field": lambda p: (math.nan, 1.0)},
            {"curve": lambda t: (t, t) if t < 0.5 else (t, t, t)},
            {"curve": lambda t: (_ for _ in ()).throw(RuntimeError("boom"))},
        ):
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                composite_midpoint_line_integral(**(common | replacement))

    def test_rejects_overflowing_accumulation(self) -> None:
        with self.assertRaises(ValueError):
            composite_midpoint_line_integral(
                lambda p: (1e308, 0.0), curve=lambda t: (t, 0.0),
                curve_derivative=lambda t: (1e308, 0.0), bounds=(0.0, 1.0), n=1,
            )

    def test_converts_dot_fsum_overflow_to_stage_specific_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "line dot product must be finite"):
            composite_midpoint_line_integral(
                lambda p: (1e308, 1e308), curve=lambda t: (t, t),
                curve_derivative=lambda t: (1.0, 1.0), bounds=(0.0, 1.0), n=1,
            )

    def test_converts_accumulation_fsum_overflow_to_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "integral accumulation must be finite"):
            composite_midpoint_line_integral(
                lambda p: (1e308, 0.0), curve=lambda t: (t, 0.0),
                curve_derivative=lambda t: (1.0, 0.0), bounds=(0.0, 1.0), n=2,
            )


class FluxIntegralTests(unittest.TestCase):
    def test_constant_vertical_field_through_unit_square(self) -> None:
        result = composite_midpoint_flux_integral(
            lambda point: (0.0, 0.0, 3.0), surface=lambda u, v: (u, v, 0.0),
            surface_u=lambda u, v: (1.0, 0.0, 0.0), surface_v=lambda u, v: (0.0, 1.0, 0.0),
            u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=4, nv=5,
        )
        self.assertIsInstance(result, FluxIntegralResult)
        self.assertAlmostEqual(3.0, result.value)
        self.assertEqual((4, 5, 20), (result.nu, result.nv, result.evaluations))
        with self.assertRaises(FrozenInstanceError):
            result.value = 0.0

    def test_reversing_surface_parameters_changes_sign(self) -> None:
        result = composite_midpoint_flux_integral(
            lambda point: (0.0, 0.0, 3.0), surface=lambda u, v: (v, u, 0.0),
            surface_u=lambda u, v: (0.0, 1.0, 0.0), surface_v=lambda u, v: (1.0, 0.0, 0.0),
            u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=3, nv=2,
        )
        self.assertAlmostEqual(-3.0, result.value)

    def test_rejects_bad_input_zero_normal_and_callback_errors(self) -> None:
        common = dict(field=lambda p: (0.0, 0.0, 1.0), surface=lambda u, v: (u, v, 0.0),
                      surface_u=lambda u, v: (1.0, 0.0, 0.0), surface_v=lambda u, v: (0.0, 1.0, 0.0),
                      u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=2, nv=2)
        for replacement in (
            {"nu": True}, {"nv": 0}, {"u_bounds": (1.0, 0.0)}, {"v_bounds": (0.0, math.nan)},
            {"surface": lambda u, v: (u, v)}, {"field": lambda p: (0.0, 1.0)},
            {"surface_u": lambda u, v: (1.0, 0.0)}, {"surface_v": lambda u, v: (math.inf, 1.0, 0.0)},
            {"surface_v": lambda u, v: (2.0, 0.0, 0.0)},
            {"field": lambda p: (0.0, 0.0, 1.0) if p[0] < 0.5 else (0.0, 1.0)},
            {"field": lambda p: (_ for _ in ()).throw(RuntimeError("boom"))},
        ):
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                composite_midpoint_flux_integral(**(common | replacement))

    def test_zero_normal_error_is_explicit(self) -> None:
        with self.assertRaisesRegex(ValueError, "nondegenerate normal"):
            composite_midpoint_flux_integral(
                lambda p: (0.0, 0.0, 1.0), surface=lambda u, v: (u, v, 0.0),
                surface_u=lambda u, v: (1.0, 0.0, 0.0), surface_v=lambda u, v: (2.0, 0.0, 0.0),
                u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=1, nv=1,
            )

    def test_rejects_overflowing_accumulation(self) -> None:
        with self.assertRaises(ValueError):
            composite_midpoint_flux_integral(
                lambda p: (0.0, 0.0, 1e308), surface=lambda u, v: (u, v, 0.0),
                surface_u=lambda u, v: (1e308, 0.0, 0.0), surface_v=lambda u, v: (0.0, 1e308, 0.0),
                u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=1, nv=1,
            )

    def test_converts_dot_fsum_overflow_to_stage_specific_value_error(self) -> None:
        common = dict(
            surface=lambda u, v: (u, v, 0.0),
            surface_u=lambda u, v: (1.0, 0.0, 0.0),
            surface_v=lambda u, v: (0.0, 1.0, 0.0),
            u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nv=1,
        )
        with self.assertRaisesRegex(ValueError, "flux dot product must be finite"):
            composite_midpoint_flux_integral(
                lambda p: (1e308, 0.0, 1e308),
                surface_u=lambda u, v: (1.0, 0.0, -1.0),
                surface_v=lambda u, v: (0.0, 1.0, 0.0), nu=1,
                **{key: value for key, value in common.items() if key not in ("surface_u", "surface_v")},
            )

    def test_converts_accumulation_fsum_overflow_to_value_error(self) -> None:
        common = dict(
            surface=lambda u, v: (u, v, 0.0),
            surface_u=lambda u, v: (1.0, 0.0, 0.0),
            surface_v=lambda u, v: (0.0, 1.0, 0.0),
            u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nv=1,
        )
        with self.assertRaisesRegex(ValueError, "integral accumulation must be finite"):
            composite_midpoint_flux_integral(
                lambda p: (0.0, 0.0, 1e308), nu=2, **common,
            )


if __name__ == "__main__":
    unittest.main()
