from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-46"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-11-46-01", "区间长度应满足哪些基本性质？", 1.25, 0.00, "interval-length-axioms",
     ["第 1 章", "第 19 章"], ["interval_length_contract", "translation_invariance", "finite_additivity"]),
    ("u-11-46-02", "可数区间覆盖怎样定义 Lebesgue 外测度？", 1.25, 0.25, "outer-measure-definition",
     ["u-11-46-01", "第 3 章"], ["countable_interval_covers", "outer_measure_definition", "infimum_audit"]),
    ("u-11-46-03", "外测度为何单调并满足可数次可加性？", 1.25, 0.25, "outer-measure-properties",
     ["u-11-46-02"], ["outer_measure_monotonicity", "countable_subadditivity", "epsilon_budget"]),
    ("u-11-46-04", "区间的外测度为何恰好等于区间长度？", 1.25, 0.50, "interval-outer-measure",
     ["u-11-46-03", "第 11 章"], ["interval_outer_measure", "finite_subcover", "cover_length_lower_bound"]),
    ("u-11-46-05", "可数集为何是零测集，Jordan 理论的边界在哪里？", 1.00, 0.50, "null-countable-sets",
     ["u-11-46-03", "u-11-46-04", "第八部 Jordan 附录"], ["countable_null_sets", "dense_null_set", "jordan_boundary"]),
]
MARKERS = {
    "u-11-46-01": ("平移不变", "有限可加", "区间长度"),
    "u-11-46-02": ("可数开区间覆盖", "下确界", "外测度"),
    "u-11-46-03": ("单调性", "可数次可加性", r"\varepsilon/2^n"),
    "u-11-46-04": ("有限子覆盖", "紧致性", "区间长度"),
    "u-11-46-05": ("可数集", "零测集", "Jordan"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]


def path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterFortySixTests(unittest.TestCase):
    def text(self, target: Path) -> str:
        self.assertTrue(target.is_file(), f"missing {target.relative_to(ROOT)}")
        return target.read_text(encoding="utf-8") if target.is_file() else ""

    def test_units_have_locked_metadata_training_and_markers(self) -> None:
        totals = [0.0, 0.0, 0, 0]
        for row in EXPECTED:
            uid, title, theory, applied, _, prereqs, capabilities = row
            text = self.text(path(row))
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            self.assertEqual((uid, title, 2), (meta["unit_id"], meta["title"], meta["content_standard"]))
            self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
            self.assertEqual(prereqs, meta["prerequisites"]["book"])
            self.assertEqual(capabilities, meta["capabilities"])
            self.assertEqual(3, len(meta["learning_goals"]))
            self.assertIn(f"# {title} {{#{uid}}}", text)
            positions = [text.index(f"## {heading}") for heading in HEADINGS]
            self.assertEqual(sorted(positions), positions)
            self.assertGreaterEqual(text.count("{#ex-"), 2)
            self.assertGreaterEqual(text.count("### 即时检验"), 2)
            self.assertEqual(10, text.count(f"{{#pr-{uid}-"))
            self.assertGreaterEqual(text.count('??? note "答案"'), 12)
            self.assertEqual(text.count(r"\["), text.count(r"\]"))
            for marker in MARKERS[uid]:
                self.assertIn(marker, text)
            totals = [totals[0] + theory, totals[1] + applied,
                      totals[2] + text.count(f"{{#pr-{uid}-"),
                      totals[3] + text.count('??? note "答案"')]
        self.assertEqual([6.0, 1.5, 50, 60], totals)

    def test_introduction_opens_the_four_questions_without_using_mct(self) -> None:
        guide = self.text(CHAPTER / "index.md")
        for marker in ("q_n", "f_n", "Riemann", "可数集", "可数并", "可测性", "积分与极限"):
            self.assertIn(marker, guide)
        self.assertNotIn("由单调收敛定理", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-46/{row[0]}-{row[4]}.md"))

    def test_proof_and_computation_boundaries_are_explicit(self) -> None:
        interval = self.text(path(EXPECTED[3]))
        application = self.text(path(EXPECTED[4]))
        self.assertIn("反证", interval)
        self.assertIn("有限覆盖长度引理", interval)
        self.assertIn("from mathbook_examples.lebesgue_approximation import finite_cover_upper_bound", application)
        self.assertIn("finite_cover_only", application)
        self.assertNotIn("def finite_cover_upper_bound", application)
        self.assertNotIn("外测度的精确值", application)

    def test_navigation_hours_and_future_boundary(self) -> None:
        guide = self.text(CHAPTER / "index.md")
        self.assertIn("7.5 学时（理论 6.00，应用 1.50）", guide)
        self.assertNotIn("chapters/chapter-47/", NAVIGATION)


if __name__ == "__main__":
    unittest.main()
