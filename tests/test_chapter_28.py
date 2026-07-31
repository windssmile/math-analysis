from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-28"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-07-dependencies.md"

EXPECTED_UNITS = [
    ("u-07-28-01", "向量、内积、范数和距离怎样描述多维几何？", 1.25, 0.50, "euclidean-geometry", 8, 10),
    ("u-07-28-02", "邻域、开集、闭集、内部与边界怎样组织局部和整体？", 1.50, 0.25, "open-closed-sets", 8, 10),
    ("u-07-28-03", "向量序列怎样收敛，有限维空间为什么完备？", 1.50, 0.25, "sequences-completeness", 9, 11),
    ("u-07-28-04", "紧致性为什么等价于闭且有界？", 1.50, 0.25, "compactness", 9, 11),
    ("u-07-28-05", "多元极限、连续与连通性怎样给出存在性结论？", 1.50, 0.50, "limits-continuity", 10, 12),
]

REQUIRED_ANCHORS = {
    "u-07-28-01": (
        "thm-u-07-28-01-cauchy-schwarz",
        "thm-u-07-28-01-norm-equivalence",
    ),
    "u-07-28-02": (
        "def-u-07-28-02-open-closed",
        "thm-u-07-28-02-sequential-closed",
    ),
    "u-07-28-03": (
        "thm-u-07-28-03-coordinate-convergence",
        "thm-u-07-28-03-completeness",
    ),
    "u-07-28-04": (
        "thm-u-07-28-04-bolzano-weierstrass",
        "thm-u-07-28-04-heine-borel",
    ),
    "u-07-28-05": (
        "def-u-07-28-05-multivariable-limit",
        "thm-u-07-28-05-continuous-image-connected",
    ),
}


def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"


class ChapterTwentyEightTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_locked_metadata_anchors_and_training(self) -> None:
        totals = [0.0, 0.0, 0, 0]
        for unit in EXPECTED_UNITS:
            unit_id, title, theory, applied, _suffix, exercises, answers = unit
            text = self.required_text(unit_path(unit))
            metadata = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(unit=unit_id):
                self.assertEqual(unit_id, metadata["unit_id"])
                self.assertEqual(title, metadata["title"])
                self.assertEqual(theory, metadata["hours"]["theory"])
                self.assertEqual(applied, metadata["hours"]["applied"])
                self.assertEqual(2, metadata["content_standard"])
                self.assertIn(f"{{#{unit_id}}}", text)
                for anchor in REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(f"{{#{anchor}}}", text)
                self.assertGreaterEqual(text.count("### 例 "), 2)
                self.assertGreaterEqual(text.count("### 即时检验 "), 2)
                actual_exercises = text.count(f"{{#pr-{unit_id}-")
                actual_answers = text.count('??? note "答案"')
                self.assertEqual(exercises, actual_exercises)
                self.assertEqual(answers, actual_answers)
                totals[0] += theory
                totals[1] += applied
                totals[2] += actual_exercises
                totals[3] += actual_answers
        self.assertEqual([7.25, 1.75, 44, 54], totals)

    def test_guide_lists_the_route_and_exact_links(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，9学时（理论7.25，应用1.75）。", guide)
        for marker in ("Euclid", "范数", "完备性", "紧致性", "多元极限", "连通", "第 29 章"):
            self.assertIn(marker, guide)
        for unit in EXPECTED_UNITS:
            self.assertEqual(
                1,
                guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"),
            )

    def test_geometry_unit_proves_finite_dimensional_norm_contracts(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in ("Cauchy–Schwarz", "三角不等式", "等价范数", "有限维", "坐标"):
            self.assertIn(marker, text)

    def test_topology_unit_uses_sequential_closedness(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in ("开集", "闭集", "内部", "边界", "序列刻画", "补集"):
            self.assertIn(marker, text)

    def test_completeness_unit_reduces_to_coordinates(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in ("逐坐标收敛", "Cauchy", "完备", "有限个坐标"):
            self.assertIn(marker, text)

    def test_compactness_unit_keeps_finite_dimensional_boundary(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in ("Bolzano–Weierstrass", "Heine–Borel", "闭且有界", "有限维", "不能无条件推广到无限维"):
            self.assertIn(marker, text)

    def test_limit_unit_keeps_path_and_connectedness_boundaries(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        for marker in ("\\varepsilon", "\\delta", "序列刻画", "不同路径", "有限条路径不能证明极限存在", "连续像", "连通"):
            self.assertIn(marker, text)

    def test_chapter_28_remains_on_the_publication_surfaces(self) -> None:
        dependencies = self.required_text(DEPENDENCIES)
        self.assertIn("| 第 28 章 | 5 | 7.25 | 1.75 | 9.00 | 已发布 |", dependencies)
        self.assertIn("第 28 章", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("第七部第 29 章", readme)


if __name__ == "__main__":
    unittest.main()
