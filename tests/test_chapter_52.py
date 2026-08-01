from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-52"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-12-52-01", "Fourier 系数有哪些平移、伸缩与对称性质？", 1.00, 0.50, "symmetry-transformations",
     ["u-12-51-02"], ["coefficient_transformations", "parity_rules", "period_scaling"]),
    ("u-12-52-02", "奇偶性和分段积分怎样简化系数计算？", 1.00, 0.75, "coefficient-calculation",
     ["u-12-52-01", "第 18 章"], ["analytic_coefficients", "piecewise_integration", "symmetry_reduction"]),
    ("u-12-52-03", "半区间正弦展开与余弦展开怎样选择？", 1.00, 0.75, "half-range-expansions",
     ["u-12-52-02"], ["odd_extension", "even_extension", "half_range_series"]),
    ("u-12-52-04", "Fourier 部分和怎样写成 Dirichlet 核卷积？", 1.25, 0.25, "dirichlet-kernel",
     ["u-12-51-01", "u-12-51-02"], ["dirichlet_kernel", "partial_sum_convolution", "kernel_normalization"]),
    ("u-12-52-05", "Dirichlet 判别条件怎样保证逐点收敛？", 1.50, 0.25, "dirichlet-convergence",
     ["u-12-52-04", "第 44 章"], ["dirichlet_convergence", "oscillatory_cancellation", "one_sided_limits"]),
    ("u-12-52-06", "连续点与跳跃点的展开值应怎样判断？", 0.75, 0.50, "pointwise-values",
     ["u-12-52-02", "u-12-52-03", "u-12-52-05"], ["pointwise_values", "jump_half_sum", "endpoint_identification"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row): return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFiftyTwoTests(unittest.TestCase):
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
            positions = [text.index(f"## {heading}") for heading in HEADINGS]; self.assertEqual(sorted(positions), positions)
            self.assertGreaterEqual(text.count("{#ex-"), 2); self.assertGreaterEqual(text.count("### 即时检验"), 2)
            self.assertEqual(10, text.count(f"{{#pr-{uid}-")); self.assertGreaterEqual(text.count('??? note "答案"'), 12)
            totals = [totals[0]+theory, totals[1]+applied, totals[2]+text.count(f"{{#pr-{uid}-"), totals[3]+text.count('??? note "答案"')]
        self.assertEqual([6.5, 3.0, 60, 72], totals)

    def test_analytic_expansions_are_complete(self):
        joined = "\n".join(self.text(path(row)) for row in (EXPECTED[1], EXPECTED[2], EXPECTED[5]))
        for marker in ("方波", "锯齿波", "三角波", r"|x|", "分段积分", "最终展开式", "逐点收敛值"):
            self.assertIn(marker, joined)
        for marker in (r"\int", "a_n", "b_n", r"\sum"):
            self.assertGreaterEqual(joined.count(marker), 4)

    def test_kernel_convergence_and_jump_contract(self):
        kernel = self.text(path(EXPECTED[3])); theorem = self.text(path(EXPECTED[4])); values = self.text(path(EXPECTED[5]))
        for marker in ("Dirichlet 核", "卷积", "归一化", r"\sin((N+\frac12)t)"):
            self.assertIn(marker, kernel)
        for marker in ("分段光滑", "左右极限", "振荡", "周期端点"):
            self.assertIn(marker, theorem)
        self.assertIn(r"\frac{f(x-)+f(x+)}2", values)
        self.assertIn("不一定等于原函数赋值", values)

    def test_navigation_and_release_boundary(self):
        guide = self.text(CHAPTER / "index.md"); self.assertIn("9.5 学时", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-52/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-53/", NAVIGATION)

if __name__ == "__main__": unittest.main()
