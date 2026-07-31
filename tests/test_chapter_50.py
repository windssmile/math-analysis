from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-50"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-11-50-01", "单调收敛定理怎样闭合递增逼近？", 1.25, 0.25, "monotone-convergence",
     ["u-11-48-03", "u-11-49-02", "u-11-49-03"], ["monotone_convergence_theorem", "integral_limit_exchange", "mct_hypotheses"]),
    ("u-11-50-02", "Fatou 引理怎样给出下极限不等式？", 1.25, 0.00, "fatou-lemma",
     ["u-11-48-02", "u-11-50-01"], ["fatou_lemma", "tail_infimum", "liminf_integral_bound"]),
    ("u-11-50-03", "控制收敛定理为何需要可积控制函数？", 1.50, 0.25, "dominated-convergence",
     ["u-11-49-05", "u-11-50-02"], ["dominated_convergence_theorem", "integrable_dominator", "dct_failure_modes"]),
    ("u-11-50-04", "Riemann 可积函数与 Lebesgue 积分怎样兼容？", 1.25, 0.25, "riemann-lebesgue-comparison",
     ["第 19 章", "u-11-47-05", "u-11-49-03"], ["riemann_lebesgue_compatibility", "lebesgue_criterion", "oscillation_sets"]),
    ("u-11-50-05", "序章失败序列怎样被新理论完整解释？", 0.75, 0.25, "intro-sequence-closure",
     ["u-11-46-05", "u-11-48-02", "u-11-49-01", "u-11-50-01"], ["dirichlet_sequence_closure", "limit_integral_exchange", "part_eleven_synthesis"]),
]
MARKERS = {
    "u-11-50-01": ("单调收敛定理", "简单函数", "递增"),
    "u-11-50-02": ("Fatou", "尾部下确界", r"\liminf"),
    "u-11-50-03": ("控制收敛定理", r"g+f_n", r"g-f_n"),
    "u-11-50-04": ("一维", "振幅集合", "不连续点"),
    "u-11-50-05": (r"q_1,q_2,\ldots", r"f_n=\mathbf1_{\{q_1,\ldots,q_n\}}", "Dirichlet"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row): return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFiftyTests(unittest.TestCase):
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
        self.assertEqual([6.0, 1.0, 50, 60], totals)

    def test_proof_routes_and_scope(self):
        fatou = self.text(path(EXPECTED[1])); dct = self.text(path(EXPECTED[2])); comparison = self.text(path(EXPECTED[3]))
        self.assertIn(r"h_n=\inf_{k\ge n}f_k", fatou)
        self.assertIn("分别应用 Fatou", dct)
        for forbidden in ("乘积测度", "Tonelli", "Fubini"):
            self.assertNotIn(forbidden, comparison.split("## 常见误区与后续", 1)[0])

    def test_navigation_hours_and_final_boundary(self):
        guide = self.text(CHAPTER / "index.md"); self.assertIn("7 学时（理论 6.00，应用 1.00）", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-50/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-51/", NAVIGATION)

if __name__ == "__main__": unittest.main()
