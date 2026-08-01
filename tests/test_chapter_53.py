from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-53"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-12-53-01", "Bessel 不等式怎样限制 Fourier 系数的能量？", 1.25, 0.25, "bessel-inequality", ["u-12-51-03"], ["bessel_inequality", "finite_energy_bound", "coefficient_control"]),
    ("u-12-53-02", "均方误差为何等于总能量减去投影能量？", 1.25, 0.25, "mean-square-error", ["u-12-51-03", "u-12-53-01"], ["mean_square_error", "finite_error_identity", "best_square_approximation"]),
    ("u-12-53-03", "Parseval 等式在什么条件下成立？", 1.50, 0.25, "parseval-identity", ["u-12-53-02", "第 50 章"], ["parseval_identity", "mean_square_limit", "energy_equality"]),
    ("u-12-53-04", "Parseval 等式怎样用于经典数项级数求和？", 1.00, 0.75, "parseval-series-sums", ["u-12-52-02", "u-12-53-03"], ["parseval_series_sums", "normalization_check", "exact_reciprocal_sums"]),
    ("u-12-53-05", "均方收敛与逐点、一致收敛有什么区别？", 1.00, 0.50, "convergence-comparison", ["u-12-52-05", "u-12-53-03", "第 25 章"], ["convergence_modes", "counterexamples", "implication_boundaries"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移", "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row): return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFiftyThreeTests(unittest.TestCase):
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
        self.assertEqual([6.0, 2.0, 50, 60], totals)

    def test_proof_order_and_energy_contracts(self):
        bessel = self.text(path(EXPECTED[0])); error = self.text(path(EXPECTED[1])); parseval = self.text(path(EXPECTED[2]))
        bessel_core = bessel[bessel.index("### 逐步证明"):bessel.index("### 假设用在何处")]
        self.assertNotIn("由 Parseval", bessel_core); self.assertIn("非负", bessel_core)
        self.assertIn("有限阶误差恒等式", error); self.assertIn("最佳平方逼近", error)
        for marker in ("均方收敛", "逼近输入", "第 50 章", "不能只由 Bessel 推出"):
            self.assertIn(marker, parseval)

    def test_series_sums_and_convergence_modes(self):
        sums = self.text(path(EXPECTED[3])); modes = self.text(path(EXPECTED[4]))
        self.assertIn("先验证", sums)
        for marker in (r"\sum_{n=1}^{\infty}\frac1{n^2}=\frac{\pi^2}{6}", r"\sum_{n=1}^{\infty}\frac1{n^4}=\frac{\pi^4}{90}", "归一化"):
            self.assertIn(marker, sums)
        for marker in ("均方收敛", "逐点收敛", "一致收敛", "互不推出", "反例"):
            self.assertIn(marker, modes)

    def test_scope_navigation_and_release_boundary(self):
        joined = "\n".join(self.text(path(row)) for row in EXPECTED)
        for forbidden in ("Hilbert 空间投影", "Riesz–Fischer", "一般 L^p"):
            self.assertNotIn(forbidden, joined)
        guide = self.text(CHAPTER / "index.md"); self.assertIn("8 学时", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-53/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-54/", NAVIGATION)

if __name__ == "__main__": unittest.main()
