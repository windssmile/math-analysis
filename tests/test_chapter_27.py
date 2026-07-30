from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-27"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-06-dependencies.md"
SOURCE = ROOT / "src" / "mathbook_examples" / "approximation.py"

EXPECTED_UNITS = [
    ("u-06-27-01", "函数逼近问题应怎样衡量误差？", 0.75, 0.75, "approximation-error", 8, 10),
    ("u-06-27-02", "Bernstein 多项式怎样逼近连续函数？", 1.50, 0.25, "bernstein-weierstrass", 9, 11),
    ("u-06-27-03", "连续性模怎样给出显式误差界？", 1.00, 0.75, "modulus-error", 9, 11),
    ("u-06-27-04", "怎样可靠构造并评价逼近多项式？", 0.25, 1.75, "reliable-bernstein", 12, 15),
]

ANCHORS = {
    "u-06-27-01": ("def-u-06-27-01-uniform-error", "def-u-06-27-01-best-error", "ex-u-06-27-01-runge"),
    "u-06-27-02": ("def-u-06-27-02-bernstein", "lem-u-06-27-02-moments", "thm-u-06-27-02-weierstrass"),
    "u-06-27-03": ("def-u-06-27-03-modulus", "thm-u-06-27-03-quantitative-bound", "cor-u-06-27-03-lipschitz-budget"),
    "u-06-27-04": ("alg-u-06-27-04-stable-evaluation", "tbl-u-06-27-04-output-semantics", "ex-u-06-27-04-method-comparison"),
}


def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"


class ChapterTwentySevenTests(unittest.TestCase):
    def required_text(self, path):
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_registry_anchors_and_training(self):
        totals = [0.0, 0.0, 0, 0]
        for unit in EXPECTED_UNITS:
            unit_id, title, th, ap, _suffix, exercises, answers = unit
            text = self.required_text(unit_path(unit))
            metadata = yaml.safe_load(text.split("---\n", 2)[1])
            self.assertEqual((unit_id, title, th, ap, 2), (metadata["unit_id"], metadata["title"], metadata["hours"]["theory"], metadata["hours"]["applied"], metadata["content_standard"]))
            self.assertIn(f"{{#{unit_id}}}", text)
            for anchor in ANCHORS[unit_id]:
                self.assertIn(f"{{#{anchor}}}", text)
            self.assertGreaterEqual(text.count("### 例 "), 2)
            checks = 3 if unit_id == "u-06-27-04" else 2
            self.assertGreaterEqual(text.count("### 即时检验 "), checks)
            actual_exercises = text.count(f"{{#pr-{unit_id}-")
            actual_answers = text.count('??? note "答案"')
            self.assertEqual((exercises, answers), (actual_exercises, actual_answers))
            totals[0] += th; totals[1] += ap; totals[2] += actual_exercises; totals[3] += actual_answers
        self.assertEqual([3.5, 3.5, 38, 47], totals)

    def test_guide_closes_part_six(self):
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共4个核心单元，7学时（理论3.5，应用3.5）。", guide)
        for marker in ("一致误差", "Bernstein", "Weierstrass", "连续性模", "可靠实现", "第 26 章", "第六部"):
            self.assertIn(marker, guide)
        for unit in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"))

    def test_error_unit_keeps_method_boundaries(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in ("最佳误差下确界", "不保证取得", "插值", "最小二乘", "逐点逼近", "一致逼近", "Runge", "仿射变换"):
            self.assertIn(marker, text)

    def test_bernstein_proof_is_constructive_and_nonprobabilistic(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in ("权重非负", "权重和为 1", "保持常数", "保持线性", "二阶中心矩", "近点", "远点", "一致连续"):
            self.assertIn(marker, text)
        self.assertIn("证明不依赖概率论", text)

    def test_modulus_unit_separates_bounds_from_observations(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in ("连续性模", "Lipschitz", "次数预算", "二阶导数", "理论上界", "网格最大误差", "未知真实上确界"):
            self.assertIn(marker, text)

    def test_application_unit_reuses_source_and_required_sequence(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in ("问题来源", "数学转化", "算法思想", "误差与适用条件", "伪代码", "Python", "结果解释", "de Casteljau", "理论误差界", "网格观测误差"):
            self.assertIn(marker, text)
        self.assertIn("mathbook_examples.approximation", text)
        self.assertNotIn("def bernstein_approximation(", text)
        self.assertTrue(SOURCE.is_file())

    def test_publication_closes_part_six(self):
        dependencies = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 27 章", dependencies)
        self.assertIn("24 个核心单元、42 学时", dependencies)
        self.assertIn("第六部第 27 章，共 122 个学习单元", self.required_text(ROOT / "README.md"))
        self.assertIn("第 27 章：多项式逼近与误差控制", self.required_text(ROOT / "mkdocs.yml"))

