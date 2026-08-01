from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-54"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-12-54-01", "有限 Fourier 部分和怎样重建周期信号？", 1.00, 0.50, "periodic-reconstruction", ["u-12-52-02", "u-12-52-06"], ["finite_reconstruction", "truncation_status", "periodic_signal_model"]),
    ("u-12-54-02", "Gibbs 现象为何不会因增加项数而消失？", 1.25, 0.50, "gibbs-phenomenon", ["u-12-52-04", "u-12-52-06", "u-12-54-01"], ["gibbs_phenomenon", "overshoot_limit", "jump_neighborhood"]),
    ("u-12-54-03", "Fejér 平均为何比普通部分和更稳定？", 1.50, 0.25, "fejer-means", ["u-12-52-04", "u-12-54-02"], ["fejer_kernel", "cesaro_mean", "uniform_convergence"]),
    ("u-12-54-04", "截断阶数、误差指标与采样分辨率怎样选择？", 0.75, 0.75, "truncation-error", ["u-12-53-02", "u-12-54-01", "u-12-54-03"], ["truncation_error", "sampled_metrics", "resolution_limits"]),
    ("u-12-54-05", "一个周期模型怎样完成“建模—展开—误差—解释”闭环？", 1.00, 0.50, "periodic-model-closure", ["u-12-53-05", "u-12-54-02", "u-12-54-04"], ["periodic_model_closure", "square_wave_closure", "conclusion_boundaries"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移", "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row): return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFiftyFourTests(unittest.TestCase):
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
        self.assertEqual([5.5, 2.5, 50, 60], totals)

    def test_gibbs_and_fejer_claims_are_distinct(self):
        gibbs = self.text(path(EXPECTED[1])); fejer = self.text(path(EXPECTED[2]))
        for marker in ("跳跃点半和", "相对超调", "不趋于零", "邻域宽度", "趋于零"):
            self.assertIn(marker, gibbs)
        for marker in ("非负", "单位质量", "集中性", "算术平均", "连续周期函数", "一致收敛"):
            self.assertIn(marker, fejer)

    def test_finite_computation_and_model_contract(self):
        reconstruction = self.text(path(EXPECTED[0])); error = self.text(path(EXPECTED[3])); model = self.text(path(EXPECTED[4]))
        self.assertIn("finite_truncation_only", reconstruction); self.assertIn("finite_truncation_only", error)
        for marker in ("采样最大误差", "不是一致误差证书", "均方误差", "解析系数"):
            self.assertIn(marker, error)
        steps = ["问题定义", "周期归一化", "解析系数", "有限重建", "误差指标", "结论边界"]
        closure = model[model.index("最终模型严格按六步完成") :]
        positions = [closure.index(step) for step in steps]; self.assertEqual(sorted(positions), positions)
        for chapter in ("第 51 章", "第 52 章", "第 53 章", "第 54 章", "方波"):
            self.assertIn(chapter, model)

    def test_scope_navigation_and_final_boundary(self):
        joined = "\n".join(self.text(path(row)) for row in EXPECTED)
        for forbidden in ("FFT", "DFT", "采样定理", "Fourier 变换", "多维 Fourier", "PDE"):
            self.assertNotIn(forbidden, joined)
        guide = self.text(CHAPTER / "index.md"); self.assertIn("8 学时", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-54/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-55/", NAVIGATION)

if __name__ == "__main__": unittest.main()
