from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-44"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-10-44-01", "含参反常积分的一致收敛应怎样定义？", 1.25, 0.00, "uniform-improper-definition", 10, 12,
     ["第 22 章", "第 25 章", "u-10-42-01"], ["uniform_improper_integral", "infinite_tail", "singular_endpoint"]),
    ("u-10-44-02", "一致 Cauchy 判据怎样把尾部转化为可检查条件？", 1.50, 0.25, "uniform-cauchy-criterion", 10, 12,
     ["u-10-44-01", "第 8 章"], ["uniform_cauchy_criterion", "tail_control", "necessity_sufficiency"]),
    ("u-10-44-03", "Weierstrass、Dirichlet 与 Abel 型判据怎样控制参数族？", 1.25, 0.50, "uniform-convergence-tests", 10, 12,
     ["u-10-44-02", "第 24–25 章"], ["weierstrass_test", "dirichlet_test", "abel_test"]),
    ("u-10-44-04", "连续性、极限与参数积分何时可同反常积分交换？", 1.00, 0.50, "improper-exchange", 10, 12,
     ["u-10-42-02", "u-10-42-03", "u-10-44-02"], ["improper_continuity", "improper_limit_exchange", "parameter_integral_exchange"]),
    ("u-10-44-05", "积分号下求导何时成立，反例揭示哪些条件缺口？", 1.00, 0.75, "improper-differentiation", 11, 13,
     ["u-10-43-02", "u-10-44-02", "u-10-44-04"], ["improper_differentiation", "basepoint_convergence", "nonuniform_counterexample"]),
]
MARKERS = {
    "u-10-44-01": ("一致收敛", "无穷区间", "有限端点奇性", "统一截断"),
    "u-10-44-02": ("一致 Cauchy", "对所有参数", "统一尾项", "充要性"),
    "u-10-44-03": ("Weierstrass", "Dirichlet", "Abel", "单调"),
    "u-10-44-04": ("连续性", "极限", "参数积分", "统一尾项"),
    "u-10-44-05": ("积分号下求导", "导数积分一致收敛", "基点收敛", "反例"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFortyFourTests(unittest.TestCase):
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
            positions = [text.index(f"## {h}") for h in HEADINGS]
            self.assertEqual(sorted(positions), positions)
            self.assertGreaterEqual(text.count("{#ex-"), 2)
            self.assertGreaterEqual(text.count("### 即时检验"), 2)
            self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
            self.assertEqual(answers, text.count('??? note "答案"'))
            for marker in MARKERS[uid]:
                self.assertIn(marker, text)
            self.assertEqual(text.count(r"\["), text.count(r"\]"))
            totals = [totals[0] + theory, totals[1] + applied, totals[2] + exercises, totals[3] + answers]
        self.assertEqual([6.0, 2.0, 51, 61], totals)

    def test_quantifiers_and_endpoint_types_are_explicit(self):
        definition = self.text(path(EXPECTED[0]))
        cauchy = self.text(path(EXPECTED[1]))
        self.assertIn(r"\forall\varepsilon>0\ \exists A_0", definition)
        self.assertIn(r"\forall t\in T\ \forall A\ge A_0", definition)
        self.assertIn(r"\forall\varepsilon>0\ \exists\delta_0>0", definition)
        self.assertIn(r"0<\delta\le\delta_0", definition)
        self.assertIn(r"\forall\varepsilon>0\ \exists A_0", cauchy)
        self.assertIn(r"\forall B>A\ge A_0\ \forall t\in T", cauchy)
        self.assertIn("充分性", cauchy)
        self.assertIn("必要性", cauchy)

    def test_proof_and_scope_boundaries(self):
        tests = self.text(path(EXPECTED[2]))
        exchange = self.text(path(EXPECTED[3]))
        diff = self.text(path(EXPECTED[4]))
        for heading in ("### Weierstrass 型判据", "### Dirichlet 型判据", "### Abel 型判据"):
            self.assertIn(heading, tests)
        self.assertIn("统一截断", exchange)
        self.assertIn("统一尾项", exchange)
        self.assertIn("每个紧参数区间", diff)
        self.assertIn("有限截断上的数值稳定不能证明一致收敛", diff)
        self.assertIn("每个参数", diff)

    def test_guide_navigation_and_boundary(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-44/{row[0]}-{row[4]}.md"))
        self.assertIn("8 学时（理论 6.00，应用 2.00）", guide)
        self.assertNotIn("chapters/chapter-45/", NAVIGATION)

if __name__ == "__main__":
    unittest.main()
