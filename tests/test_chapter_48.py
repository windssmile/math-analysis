from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-48"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-11-48-01", "可测函数为何可由水平集的可测性刻画？", 1.25, 0.25, "measurable-functions",
     ["u-11-47-03"], ["measurable_function_definition", "level_set_criteria", "extended_real_values"]),
    ("u-11-48-02", "运算、上确界与逐点极限怎样保持可测性？", 1.25, 0.25, "measurable-operations-limits",
     ["u-11-48-01"], ["measurable_arithmetic", "measurable_suprema", "measurable_pointwise_limits"]),
    ("u-11-48-03", "非负可测函数怎样由递增简单函数逼近？", 1.50, 0.50, "simple-function-approximation",
     ["u-11-48-01", "u-11-48-02"], ["simple_functions", "dyadic_lower_approximation", "monotone_pointwise_approximation"]),
    ("u-11-48-04", "逐点、一致与几乎处处收敛怎样区分？", 1.00, 0.25, "pointwise-uniform-ae",
     ["u-11-46-05", "第 25 章"], ["pointwise_convergence", "uniform_convergence", "almost_everywhere_convergence"]),
    ("u-11-48-05", "依测度收敛与其他收敛方式有什么关系？", 1.00, 0.25, "convergence-in-measure",
     ["u-11-47-04", "u-11-48-04"], ["convergence_in_measure", "finite_measure_implication", "convergence_counterexamples"]),
]
MARKERS = {
    "u-11-48-01": ("水平集", "扩展实值", "可测函数"),
    "u-11-48-02": ("上确界", "下确界", "逐点极限"),
    "u-11-48-03": ("简单函数", "二进", "递增"),
    "u-11-48-04": ("逐点收敛", "一致收敛", "几乎处处"),
    "u-11-48-05": ("依测度收敛", "有限测度", "反例"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row): return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFortyEightTests(unittest.TestCase):
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
        self.assertEqual([6.0, 1.5, 50, 60], totals)

    def test_simple_approximation_and_convergence_boundaries(self):
        simple = self.text(path(EXPECTED[2])); measure = self.text(path(EXPECTED[4]))
        for marker in (r"2^{-n}\lfloor 2^n f(x)\rfloor", r"f(x)<n", r"f(x)\ge n", r"\phi_n(x)\uparrow f(x)"):
            self.assertIn(marker, simple)
        self.assertIn(r"m(\{|f_n-f|>\varepsilon\})", measure)
        self.assertIn("打字机序列", measure)
        core = "\n".join(self.text(path(r)).split("## 常见误区与后续", 1)[0] for r in EXPECTED)
        for forbidden in ("单调收敛定理", "Fatou", "控制收敛定理", "Egorov", "Riesz 子列", "L^p"):
            self.assertNotIn(forbidden, core)

    def test_navigation_hours_and_future_boundary(self):
        guide = self.text(CHAPTER / "index.md"); self.assertIn("7.5 学时（理论 6.00，应用 1.50）", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-48/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-49/", NAVIGATION)

if __name__ == "__main__": unittest.main()
