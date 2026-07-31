from pathlib import Path
import re
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-42"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-10-42-01", "含参积分怎样定义函数，参数与积分变量怎样分工？", 1.25, 0.00,
     "parametric-integral-functions", 8, 10, ["第 19 章", "第 28 章"],
     ["parametric_integral", "variable_roles", "fixed_domain"]),
    ("u-10-42-02", "被积函数联合连续时，积分为什么连续依赖参数？", 1.25, 0.25,
     "continuity-under-integral", 9, 11, ["u-10-42-01", "第 11 章", "第 28 章"],
     ["parameter_continuity", "compact_uniform_continuity", "supremum_estimate"]),
    ("u-10-42-03", "一致收敛为什么允许极限进入积分号？", 1.25, 0.25,
     "uniform-limit-interchange", 9, 11, ["u-10-42-01", "第 25 章"],
     ["uniform_integral_interchange", "integral_error_bound", "limit_exchange"]),
    ("u-10-42-04", "哪些逐点收敛反例说明一致控制不可省略？", 1.00, 0.50,
     "pointwise-failure", 10, 12, ["u-10-42-03"],
     ["moving_spike", "pointwise_failure", "hypothesis_diagnosis"]),
    ("u-10-42-05", "怎样为连续性与极限交换建立条件检查表？", 0.75, 0.50,
     "exchange-checklist", 10, 12, ["u-10-42-02", "u-10-42-03", "u-10-42-04"],
     ["exchange_checklist", "assumption_audit", "counterexample_selection"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]
MARKERS = {
    "u-10-42-01": ("积分变量", "参数变量", "固定紧区间", "Riemann", "{#def-u-10-42-01-parametric}"),
    "u-10-42-02": ("联合连续", "一致连续", "上确界估计", "连续依赖", "{#thm-u-10-42-02-continuity}"),
    "u-10-42-03": ("一致收敛", "极限进入积分号", "积分区间长度", "误差界", "{#thm-u-10-42-03-interchange}"),
    "u-10-42-04": ("逐点收敛", "移动尖峰", "不能交换", "失败边界", "{#ex-u-10-42-04-moving-spike}"),
    "u-10-42-05": ("交换对象", "定理条件", "条件用在何处", "条件检查表", "{#workflow-u-10-42-05-checklist}"),
}
FORBIDDEN = ("控制收敛定理", "几乎处处", "Reynolds 输运", "形状导数")


def unit_path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterFortyTwoTests(unittest.TestCase):
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
            for forbidden in FORBIDDEN:
                self.assertNotIn(forbidden, text)
            totals = [totals[0] + theory, totals[1] + applied, totals[2] + exercises, totals[3] + answers]
        self.assertEqual([5.5, 1.5, 46, 56], totals)

    def test_guide_navigation_and_release_boundary(self) -> None:
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-42/{row[0]}-{row[4]}.md"))
        self.assertIn("第 42 章：正常含参变量积分", guide)
        self.assertIn("7 学时（理论 5.50，应用 1.50）", guide)

    def test_continuity_proof_exposes_uniform_estimate(self) -> None:
        text = self.text(unit_path(EXPECTED[1]))
        for marker in ("### 交换对象", "### 定理条件", "### 证明路线", "### 条件用在何处", "### 失败边界"):
            self.assertIn(marker, text)
        self.assertIn(r"\left|F(t)-F(t_0)\right|", text)
        self.assertIn(r"(b-a)\sup_{x\in[a,b]}|f(x,t)-f(x,t_0)|", text)

    def test_uniform_limit_proof_has_exact_error_bound(self) -> None:
        text = self.text(unit_path(EXPECTED[2]))
        self.assertIn(r"\left|\int_a^b f_n-\int_a^b f\right|", text)
        self.assertIn(r"\le (b-a)\lVert f_n-f\rVert_\infty", text)
        self.assertRegex(text, r"任意.*\\varepsilon[\s\S]{0,1000}N")

    def test_moving_spike_is_continuous_pointwise_zero_with_constant_integral(self) -> None:
        text = self.text(unit_path(EXPECTED[3]))
        for marker in (r"f_n(0)=0", r"x=\frac{1}{n}", r"高度为 \(n\)", "连续", "逐点趋于", r"\int_0^1 f_n(x)\,dx"):
            self.assertIn(marker, text)
        self.assertIn("积分极限是 1", text)
        self.assertIn("极限函数的积分是 0", text)

    def test_display_math_delimiters_are_not_nested_or_unbalanced(self) -> None:
        for row in EXPECTED:
            text = self.text(unit_path(row))
            self.assertEqual(text.count(r"\["), text.count(r"\]"), row[0])
            for body in re.findall(r"\[(?P<body>[\s\S]*?)\]", text):
                self.assertNotIn(r"\(", body, row[0])
                self.assertNotIn(r"\)", body, row[0])


if __name__ == "__main__":
    unittest.main()
