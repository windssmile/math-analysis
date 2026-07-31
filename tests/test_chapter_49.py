from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-49"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-11-49-01", "简单函数的积分怎样由水平集测度定义？", 1.25, 0.50, "simple-function-integral",
     ["u-11-47-04", "u-11-48-03"], ["simple_function_integral", "representation_independence", "finite_partition_integral"]),
    ("u-11-49-02", "非负可测函数的积分怎样由下逼近定义？", 1.50, 0.25, "nonnegative-integral",
     ["u-11-49-01"], ["nonnegative_integral", "lower_simple_supremum", "zero_integral_criterion"]),
    ("u-11-49-03", "积分的单调性、齐次性与可加性怎样证明？", 1.50, 0.25, "integral-properties",
     ["u-11-49-01", "u-11-49-02"], ["integral_monotonicity", "integral_homogeneity", "integral_additivity"]),
    ("u-11-49-04", "正部、负部怎样定义一般函数的积分？", 1.25, 0.25, "signed-integral",
     ["u-11-48-02", "u-11-49-02", "u-11-49-03"], ["positive_negative_parts", "signed_lebesgue_integral", "infinity_minus_infinity_boundary"]),
    ("u-11-49-05", "绝对可积、零测集修改与积分估计怎样统一？", 1.00, 0.25, "absolute-integrability",
     ["u-11-47-05", "u-11-49-04"], ["absolute_integrability", "null_set_invariance", "integral_absolute_bound"]),
]
MARKERS = {
    "u-11-49-01": ("共同加细", "表示无关", "simple_integral"),
    "u-11-49-02": ("下方简单函数", "上确界", "非负可测"),
    "u-11-49-03": ("递增简单函数引理", "单调性", "可加性"),
    "u-11-49-04": ("正部", "负部", r"\infty-\infty"),
    "u-11-49-05": ("绝对可积", "零测集", r"\left|\int f\right|"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row): return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFortyNineTests(unittest.TestCase):
    def text(self, target):
        self.assertTrue(target.is_file(), f"missing {target.relative_to(ROOT)}")
        return target.read_text(encoding="utf-8") if target.is_file() else ""

    def test_units_have_locked_contracts(self):
        totals = [0.0, 0.0, 0, 0]
        for row in EXPECTED:
            uid, title, theory, applied, _, prereqs, caps = row
            text = self.text(path(row)); meta = yaml.safe_load(text.split("---\n", 2)[1])
            self.assertEqual((uid, title, 2), (meta["unit_id"], meta["title"], meta["content_standard"]))
            self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
            self.assertEqual(prereqs, meta["prerequisites"]["book"]); self.assertEqual(caps, meta["capabilities"])
            self.assertEqual(3, len(meta["learning_goals"])); self.assertIn(f"# {title} {{#{uid}}}", text)
            pos = [text.index(f"## {h}") for h in HEADINGS]; self.assertEqual(sorted(pos), pos)
            self.assertGreaterEqual(text.count("{#ex-"), 2); self.assertGreaterEqual(text.count("### 即时检验"), 2)
            self.assertEqual(10, text.count(f"{{#pr-{uid}-")); self.assertGreaterEqual(text.count('??? note "答案"'), 12)
            for marker in MARKERS[uid]: self.assertIn(marker, text)
            totals = [totals[0]+theory, totals[1]+applied, totals[2]+text.count(f"{{#pr-{uid}-"), totals[3]+text.count('??? note "答案"')]
        self.assertEqual([6.5, 1.5, 50, 60], totals)

    def test_integral_definition_and_anti_circularity(self):
        simple = self.text(path(EXPECTED[0])); nonnegative = self.text(path(EXPECTED[1]))
        properties = self.text(path(EXPECTED[2])); signed = self.text(path(EXPECTED[3]))
        self.assertIn(r"\int \phi\,dm=\sum_{k=1}^m a_km(E_k)", simple)
        self.assertEqual(1, simple.count("simple_integral"))
        self.assertIn(r"\sup\left\{\int\phi\,dm:0\le\phi\le f", nonnegative)
        core = "\n".join(self.text(path(r)).split("## 常见误区与后续", 1)[0] for r in EXPECTED)
        self.assertIn("递增简单函数引理", properties)
        self.assertNotIn("u-11-50-01", core)
        self.assertNotIn("由单调收敛定理", core)
        self.assertIn("至少一个为有限值", signed)

    def test_navigation_hours_and_future_boundary(self):
        guide = self.text(CHAPTER / "index.md"); self.assertIn("8 学时（理论 6.50，应用 1.50）", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-49/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-50/", NAVIGATION)

if __name__ == "__main__": unittest.main()
