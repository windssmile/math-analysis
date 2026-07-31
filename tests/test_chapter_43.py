from pathlib import Path
import re
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-43"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-10-43-01", "什么条件允许对含参积分求导？", 1.25, 0.00,
     "differentiation-under-integral", 10, 12, ["u-10-42-03", "第 14 章", "第 29 章"],
     ["differentiate_under_integral", "continuous_partial", "fixed_endpoint_rule"]),
    ("u-10-43-02", "差商与偏导的一致控制怎样完成 Leibniz 公式证明？", 1.50, 0.25,
     "difference-quotient-control", 10, 12, ["u-10-43-01", "第 15 章"],
     ["difference_quotient_control", "mean_value_bridge", "leibniz_proof"]),
    ("u-10-43-03", "积分端点随参数变化时，边界项从哪里产生？", 1.25, 0.50,
     "variable-endpoints-leibniz", 10, 12, ["u-10-43-02", "第 20 章"],
     ["variable_endpoint_rule", "boundary_terms", "sign_audit"]),
    ("u-10-43-04", "对参数再积分时，怎样通过经典 Fubini 交换次序？", 1.00, 0.50,
     "parameter-integration-fubini", 10, 12, ["u-10-42-02", "第 34 章"],
     ["parameter_integration", "classical_fubini", "order_exchange"]),
    ("u-10-43-05", "可固定化的移动区域怎样化为固定区域问题？", 1.00, 0.75,
     "fixed-domain-transform", 10, 12, ["u-10-43-03", "第 35 章"],
     ["fixed_reference_domain", "moving_domain_transform", "jacobian_sensitivity"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]
MARKERS = {
    "u-10-43-01": ("偏导数", "连续", "积分号下求导", "充分条件", "{#thm-u-10-43-01-fixed}"),
    "u-10-43-02": ("差商", "中值定理", "一致控制", "极限交换", "{#thm-u-10-43-02-proof}"),
    "u-10-43-03": ("上端点", "下端点", "边界项", "链式法则", "{#thm-u-10-43-03-variable}"),
    "u-10-43-04": ("参数再积分", "经典 Fubini", "固定区域", "交换次序", "{#thm-u-10-43-04-fubini}"),
    "u-10-43-05": ("固定参考域", "Jacobian", "换元", "后续去向", "{#workflow-u-10-43-05-fixed-domain}"),
}


def unit_path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterFortyThreeTests(unittest.TestCase):
    def text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_unit_contract(self) -> None:
        totals = [0.0, 0.0, 0, 0]
        for row in EXPECTED:
            uid, title, theory, applied, _, exercises, answers, prereqs, capabilities = row
            text = self.text(unit_path(row))
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            self.assertEqual(2, meta["content_standard"])
            self.assertEqual((uid, title), (meta["unit_id"], meta["title"]))
            self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
            self.assertEqual(prereqs, meta["prerequisites"]["book"])
            self.assertEqual(capabilities, meta["capabilities"])
            self.assertEqual(3, len(meta["learning_goals"]))
            self.assertIn(f"# {title} {{#{uid}}}", text)
            positions = [text.index(f"## {heading}") for heading in HEADINGS]
            self.assertEqual(sorted(positions), positions)
            self.assertGreaterEqual(text.count("{#ex-"), 2)
            self.assertGreaterEqual(text.count("### 即时检验"), 2)
            self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
            self.assertEqual(answers, text.count('??? note "答案"'))
            for marker in MARKERS[uid]:
                self.assertIn(marker, text)
            totals = [totals[0] + theory, totals[1] + applied, totals[2] + exercises, totals[3] + answers]
        self.assertEqual([6.0, 2.0, 50, 60], totals)

    def test_fixed_endpoint_rule_and_proof_are_explicit(self) -> None:
        statement = self.text(unit_path(EXPECTED[0]))
        proof = self.text(unit_path(EXPECTED[1]))
        self.assertIn(r"F'(t)=\int_a^b\partial_t f(x,t)\,dx", statement)
        for marker in ("### 交换对象", "### 定理条件", "### 证明路线", "### 条件用在何处", "### 失败边界"):
            self.assertIn(marker, proof)
        self.assertIn(r"q_h(x)=\frac{f(x,t+h)-f(x,t)}{h}", proof)
        self.assertIn(r"q_h(x)-\partial_t f(x,t)", proof)
        self.assertIn("对所有", proof)

    def test_variable_endpoint_formula_has_both_signed_boundary_terms(self) -> None:
        text = self.text(unit_path(EXPECTED[2]))
        formula = (
            r"F'(t)=f(b(t),t)b'(t)-f(a(t),t)a'(t)"
            "\n"
            r"+\int_{a(t)}^{b(t)}\partial_t f(x,t)\,dx."
        )
        self.assertIn(formula, text)
        self.assertIn("上端点贡献为正", text)
        self.assertIn("下端点贡献为负", text)

    def test_fubini_stays_classical_and_fixed(self) -> None:
        text = self.text(unit_path(EXPECTED[3]))
        for marker in ("闭矩形", "连续", "Riemann", "经典 Fubini", "两次累次积分"):
            self.assertIn(marker, text)
        self.assertNotIn("测度", text)

    def test_moving_domain_scope_is_only_fixedizable(self) -> None:
        text = self.text(unit_path(EXPECTED[4]))
        self.assertIn(r"D_t=\Phi_t(U)", text)
        self.assertIn(r"|\det D_u\Phi_t(u)|", text)
        self.assertIn("Reynolds 输运定理", text)
        self.assertIn("形状导数", text)
        exercises = text.split("## 习题与答案", 1)[1]
        self.assertNotIn("Reynolds", exercises)
        self.assertNotIn("形状导数", exercises)
        self.assertNotRegex(text, r"### (Reynolds|形状导数)")

    def test_guide_navigation_latex_and_release_boundary(self) -> None:
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-43/{row[0]}-{row[4]}.md"))
            text = self.text(unit_path(row))
            self.assertEqual(text.count(r"\["), text.count(r"\]"), row[0])
            for body in re.findall(r"\\\[(?P<body>[\s\S]*?)\\\]", text):
                self.assertNotIn(r"\(", body)
                self.assertNotIn(r"\)", body)
        self.assertIn("8 学时（理论 6.00，应用 2.00）", guide)


if __name__ == "__main__":
    unittest.main()
