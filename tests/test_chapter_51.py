from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-51"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-12-51-01", "周期函数与三角函数系怎样构成正交族？", 1.25, 0.25, "trig-orthogonality",
     ["第 19 章", "三角恒等式"], ["trigonometric_orthogonality", "period_normalization", "orthogonal_family"]),
    ("u-12-51-02", "Fourier 系数为什么来自正交投影？", 1.25, 0.25, "fourier-projection",
     ["u-12-51-01"], ["fourier_coefficients", "orthogonal_projection", "coefficient_normalization"]),
    ("u-12-51-03", "三角多项式怎样给出最佳平方逼近？", 1.50, 0.25, "best-square-approximation",
     ["u-12-51-02"], ["best_square_approximation", "finite_pythagoras", "error_decomposition"]),
    ("u-12-51-04", "复指数形式怎样统一正弦与余弦形式？", 1.00, 0.25, "complex-form",
     ["u-12-51-01", "u-12-51-02"], ["complex_fourier_form", "real_complex_conversion", "conjugate_symmetry"]),
    ("u-12-51-05", "有限维投影计算怎样验证最佳逼近？", 1.00, 0.50, "finite-projection-check",
     ["u-12-51-03", "u-12-51-04"], ["finite_fourier_check", "quadrature_boundary", "truncation_boundary"]),
]
MARKERS = {
    "u-12-51-01": ("正交", "周期", r"\int"),
    "u-12-51-02": ("正交投影", "Fourier 系数", "归一化"),
    "u-12-51-03": ("最佳平方逼近", "Pythagoras", "有限维"),
    "u-12-51-04": ("复指数", "共轭对称", "双向换算"),
    "u-12-51-05": ("finite_quadrature_only", "有限截断", "误差"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row): return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFiftyOneTests(unittest.TestCase):
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
            for marker in MARKERS[uid]: self.assertIn(marker, text)
            totals = [totals[0]+theory, totals[1]+applied, totals[2]+text.count(f"{{#pr-{uid}-"), totals[3]+text.count('??? note "答案"')]
        self.assertEqual([6.0, 1.5, 50, 60], totals)

    def test_guide_motivation_navigation_and_scope(self):
        guide = self.text(CHAPTER / "index.md")
        for marker in ("方波", "连续点", "跳跃点", "Gibbs"):
            self.assertIn(marker, guide)
        self.assertEqual(4, guide.count("?"))
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-51/{row[0]}-{row[4]}.md"))
        if "chapters/chapter-52/" in NAVIGATION:
            self.assertLess(NAVIGATION.index("chapters/chapter-51/"),
                            NAVIGATION.index("chapters/chapter-52/"))

    def test_proof_core_avoids_later_theorems(self):
        first_four = "\n".join(self.text(path(row)).split("## 常见误区与后续", 1)[0] for row in EXPECTED[:4])
        self.assertNotIn("由 Parseval", first_four)
        self.assertNotIn("由 Fejér", first_four)
        self.assertNotIn("Hilbert 空间投影定理", first_four)

if __name__ == "__main__": unittest.main()
