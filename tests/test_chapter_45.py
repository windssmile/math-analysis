from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-45"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-10-45-01", "Gamma 积分在哪些参数上收敛，递推公式怎样得到？", 1.00, 0.25, "gamma-convergence-recurrence", 10, 12,
     ["第 22 章", "u-10-44-03"], ["gamma_convergence", "gamma_recurrence", "boundary_term_audit"]),
    ("u-10-45-02", "Beta 积分的端点奇性怎样控制？", 1.00, 0.25, "beta-endpoint-singularities", 10, 12,
     ["第 22 章", "u-10-44-03"], ["beta_convergence", "two_endpoint_control", "beta_symmetry"]),
    ("u-10-45-03", "Beta–Gamma 关系怎样由重积分与换元推出？", 1.25, 0.25, "beta-gamma-relation", 10, 13,
     ["u-10-45-01", "u-10-45-02", "第 34–35 章"], ["beta_gamma_relation", "first_quadrant_transform", "polar_jacobian"]),
    ("u-10-45-04", "参数求导怎样产生含对数因子的积分与敏感性公式？", 0.75, 0.75, "logarithmic-parameter-derivatives", 10, 12,
     ["u-10-44-05", "u-10-45-01", "u-10-45-02"], ["logarithmic_integrals", "parameter_sensitivity", "derivative_hypothesis_audit"]),
    ("u-10-45-05", "怎样对 Gamma、Beta 积分作带状态的可靠近似？", 0.50, 1.00, "certified-gamma-beta", 10, 13,
     ["第 22 章", "u-10-45-01", "u-10-45-02", "u-10-45-03", "u-10-45-04"], ["gamma_beta_quadrature", "certificate_status", "endpoint_error_budget"]),
]
MARKERS = {
    "u-10-45-01": ("Gamma", "参数大于 0", "分部积分", "递推公式"),
    "u-10-45-02": ("Beta", "两个参数大于 0", "端点奇性", "收敛"),
    "u-10-45-03": ("Beta–Gamma", "第一象限", "极坐标", "Jacobian"),
    "u-10-45-04": ("对数因子", "参数求导", "一致收敛", "敏感性"),
    "u-10-45-05": ("endpoint_error_bound", "total_error_bound", "budget_exhausted", "uncertified"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFortyFiveTests(unittest.TestCase):
    def text(self, p):
        self.assertTrue(p.is_file(), f"missing {p.relative_to(ROOT)}")
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    def test_unit_contract(self):
        totals = [0.0, 0.0, 0, 0]
        for row in EXPECTED:
            uid, title, theory, applied, _, exercises, answers, prereqs, caps = row
            text = self.text(path(row))
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            self.assertEqual((uid, title, 2), (meta["unit_id"], meta["title"], meta["content_standard"]))
            self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
            self.assertEqual(prereqs, meta["prerequisites"]["book"])
            self.assertEqual(caps, meta["capabilities"])
            self.assertEqual(3, len(meta["learning_goals"]))
            self.assertIn(f"# {title} {{#{uid}}}", text)
            self.assertEqual(sorted(text.index(f"## {h}") for h in HEADINGS), [text.index(f"## {h}") for h in HEADINGS])
            self.assertGreaterEqual(text.count("{#ex-"), 2)
            self.assertGreaterEqual(text.count("### 即时检验"), 2)
            self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
            self.assertEqual(answers, text.count('??? note "答案"'))
            self.assertEqual(text.count(r"\["), text.count(r"\]"))
            for marker in MARKERS[uid]:
                self.assertIn(marker, text)
            totals = [totals[0] + theory, totals[1] + applied, totals[2] + exercises, totals[3] + answers]
        self.assertEqual([4.5, 2.5, 50, 62], totals)

    def test_proofs_and_numerical_source_are_explicit(self):
        gamma = self.text(path(EXPECTED[0]))
        relation = self.text(path(EXPECTED[2]))
        numeric = self.text(path(EXPECTED[4]))
        self.assertIn("在 1 处分拆", gamma)
        self.assertIn("边界项", gamma)
        self.assertIn(r"B(p,q)=\frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}", relation)
        self.assertIn("from mathbook_examples.parametric_integrals import beta_integral, gamma_integral", numeric)
        self.assertNotIn("def gamma_integral", numeric)
        for status in ("target_met", "budget_exhausted", "uncertified"):
            self.assertIn(status, numeric)
        self.assertIn("数学输入", numeric)

    def test_scope_navigation_and_release(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-45/{row[0]}-{row[4]}.md"))
            core = self.text(path(row)).split("## 常见误区与后续", 1)[0]
            self.assertNotIn("解析延拓", core)
            self.assertNotIn("复参数", core)
        self.assertIn("7 学时（理论 4.50，应用 2.50）", guide)
        if "chapters/chapter-46/" in NAVIGATION:
            self.assertLess(NAVIGATION.index("chapters/chapter-45/"),
                            NAVIGATION.index("chapters/chapter-46/"))

if __name__ == "__main__":
    unittest.main()
