from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-26"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-06-dependencies.md"

EXPECTED_UNITS = [
    ("u-06-26-01", "系数怎样决定收敛半径？", 1.25, 0.25, "radius", 8, 10),
    ("u-06-26-02", "幂级数为什么在收敛区间内部表现稳定？", 1.25, 0.25, "interior-uniformity", 8, 10),
    ("u-06-26-03", "为什么幂级数可以逐项积分与微分？", 1.25, 0.25, "termwise-operations", 9, 11),
    ("u-06-26-04", "Taylor 级数什么时候真的等于原函数？", 1.25, 0.50, "taylor-analytic", 9, 11),
    ("u-06-26-05", "常用展开怎样形成可靠计算工具？", 1.00, 0.75, "standard-expansions", 12, 15),
]

REQUIRED_ANCHORS = {
    "u-06-26-01": ("def-u-06-26-01-power-series", "thm-u-06-26-01-radius-dichotomy", "thm-u-06-26-01-cauchy-hadamard"),
    "u-06-26-02": ("thm-u-06-26-02-interior-uniform", "cor-u-06-26-02-continuity", "ex-u-06-26-02-full-open-failure"),
    "u-06-26-03": ("thm-u-06-26-03-same-radius", "thm-u-06-26-03-termwise-operations", "thm-u-06-26-03-coefficient-uniqueness"),
    "u-06-26-04": ("def-u-06-26-04-analytic", "thm-u-06-26-04-remainder-criterion", "ex-u-06-26-04-smooth-not-analytic"),
    "u-06-26-05": ("thm-u-06-26-05-abel-endpoint", "tbl-u-06-26-05-expansions", "alg-u-06-26-05-reliable-use"),
}

FORBIDDEN_CORE_TERMS = ("Bernstein 多项式", "Weierstrass 逼近定理", "Fourier 级数", "Lebesgue 积分", "复分析")


def unit_path(unit):
    unit_id, _title, _th, _ap, suffix, _ex, _ans = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n", 2)[1]), text


class ChapterTwentySixTests(unittest.TestCase):
    def required_text(self, path):
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_registry_anchors_and_training(self):
        theory = applied = exercises_total = answers_total = 0
        for unit in EXPECTED_UNITS:
            unit_id, title, th, ap, _suffix, exercises, answers = unit
            metadata, text = read_unit(unit_path(unit))
            with self.subTest(unit=unit_id):
                self.assertEqual(unit_id, metadata["unit_id"])
                self.assertEqual(title, metadata["title"])
                self.assertEqual(th, metadata["hours"]["theory"])
                self.assertEqual(ap, metadata["hours"]["applied"])
                self.assertEqual(2, metadata["content_standard"])
                self.assertIn(f"{{#{unit_id}}}", text)
                for anchor in REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(f"{{#{anchor}}}", text)
                self.assertGreaterEqual(text.count("### 例 "), 2)
                checks = 3 if unit_id == "u-06-26-05" else 2
                self.assertGreaterEqual(text.count("### 即时检验 "), checks)
                actual_exercises = text.count(f"{{#pr-{unit_id}-")
                actual_answers = text.count('??? note "答案"')
                self.assertEqual(exercises, actual_exercises)
                self.assertEqual(answers, actual_answers)
                theory += metadata["hours"]["theory"]
                applied += metadata["hours"]["applied"]
                exercises_total += actual_exercises
                answers_total += actual_answers
        self.assertEqual((6.0, 2.0, 46, 57), (theory, applied, exercises_total, answers_total))

    def test_guide_keeps_inside_endpoint_route(self):
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，8学时（理论6，应用2）。", guide)
        for marker in ("收敛半径", "内闭区间", "逐项积分", "逐项微分", "Taylor", "解析", "端点", "第 25 章", "第 27 章"):
            self.assertIn(marker, guide)
        for unit_id, title, _th, _ap, suffix, _ex, _ans in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_radius_requires_inside_outside_and_separate_endpoints(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in ("Cauchy–Hadamard", "上极限", "绝对收敛", "发散", "两个端点", "单独代回"):
            self.assertIn(marker, text)

    def test_interior_uniformity_does_not_claim_full_open_interval(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in ("0<r<R", "M 判别", "一致绝对收敛", "内闭区间", "整个开区间", "端点"):
            self.assertIn(marker, text)

    def test_operations_prove_radius_and_coefficient_uniqueness(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in ("相同收敛半径", "逐项积分", "逐项微分", "系数唯一", "任意阶可微"):
            self.assertIn(marker, text)

    def test_analytic_unit_separates_polynomial_series_and_function(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in ("有限 Taylor 多项式", "Taylor 级数", "函数本身", "余项趋于零", "光滑不推出解析", "e^{-1/x^2}"):
            self.assertIn(marker, text)

    def test_standard_expansions_keep_domains_endpoints_and_errors(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        for marker in ("指数", "正弦", "余弦", "几何", "对数", "二项式", "Abel 端点", "收敛域", "误差界"):
            self.assertIn(marker, text)

    def test_core_avoids_later_or_out_of_scope_theory(self):
        for unit in EXPECTED_UNITS:
            core = self.required_text(unit_path(unit)).split("## 常见误区与后续", 1)[0]
            for forbidden in FORBIDDEN_CORE_TERMS:
                self.assertNotIn(forbidden, core)

    def test_publication_reaches_chapter_26_only(self):
        dependencies = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 27 章", dependencies)
        self.assertIn("24 个核心单元、42 学时", dependencies)
        self.assertIn("第六部第 27 章，共 125 个学习单元", self.required_text(ROOT / "README.md"))
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("第 26 章：幂级数与解析表示", config)
        self.assertIn("chapters/chapter-27/", config)
