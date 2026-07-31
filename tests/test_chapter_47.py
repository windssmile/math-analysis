from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-47"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
EXPECTED = [
    ("u-11-47-01", "为什么集合运算必须对可数过程封闭？", 1.25, 0.25, "sigma-algebras",
     ["第 1 章", "u-11-46-05"], ["sigma_algebra_definition", "countable_set_operations", "generated_sigma_algebra"]),
    ("u-11-47-02", "Carathéodory 判据怎样定义可测集合？", 1.50, 0.25, "caratheodory-criterion",
     ["u-11-46-03", "u-11-47-01"], ["caratheodory_criterion", "test_set_splitting", "measurability_boundary"]),
    ("u-11-47-03", "可测集合为何构成 σ-代数？", 1.50, 0.25, "measurable-sigma-algebra",
     ["u-11-47-02"], ["measurable_complements", "measurable_countable_unions", "caratheodory_sigma_algebra"]),
    ("u-11-47-04", "外测度在可测集上为何成为可数可加的测度？", 1.25, 0.25, "countable-additivity",
     ["u-11-47-03"], ["finite_additivity_measure", "countable_additivity_measure", "continuity_from_below"]),
    ("u-11-47-05", "Borel 集、零测集及其子集怎样进入 Lebesgue 可测世界？", 1.00, 0.50, "borel-lebesgue-completion",
     ["u-11-46-04", "u-11-46-05", "u-11-47-03", "u-11-47-04"], ["borel_sets", "lebesgue_measurable_sets", "measure_completeness"]),
]
MARKERS = {
    "u-11-47-01": ("σ-代数", "可数并", "补集"),
    "u-11-47-02": ("Carathéodory", "任意测试集", "分裂"),
    "u-11-47-03": ("补集封闭", "可数并封闭", "σ-代数"),
    "u-11-47-04": ("有限可加", "可数可加", "从下连续"),
    "u-11-47-05": ("Borel", "Lebesgue", "完备"),
}
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]

def path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterFortySevenTests(unittest.TestCase):
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
            for marker in MARKERS[uid]:
                self.assertIn(marker, text)
            totals = [totals[0] + theory, totals[1] + applied,
                      totals[2] + text.count(f"{{#pr-{uid}-"), totals[3] + text.count('??? note "答案"')]
        self.assertEqual([6.5, 1.5, 50, 60], totals)

    def test_proof_chain_is_explicit_and_no_extension_black_box(self) -> None:
        criterion = self.text(path(EXPECTED[1]))
        closure = self.text(path(EXPECTED[2]))
        measure = self.text(path(EXPECTED[3]))
        completion = self.text(path(EXPECTED[4]))
        self.assertIn(r"m^*(T)=m^*(T\cap E)+m^*(T\setminus E)", criterion)
        self.assertIn("两两不交化", closure)
        self.assertIn("余项", measure)
        self.assertIn("零测集的任意子集", completion)
        core = "\n".join(self.text(path(row)).split("## 常见误区与后续", 1)[0] for row in EXPECTED)
        for forbidden in ("测度扩张定理", "Carathéodory 扩张定理", "Tonelli", "Radon–Nikodym"):
            self.assertNotIn(forbidden, core)

    def test_navigation_hours_and_future_boundary(self) -> None:
        guide = self.text(CHAPTER / "index.md")
        self.assertIn("8 学时（理论 6.50，应用 1.50）", guide)
        for row in EXPECTED:
            self.assertIn(f"{row[0]}-{row[4]}.md", guide)
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-47/{row[0]}-{row[4]}.md"))
        if "chapters/chapter-48/" in NAVIGATION:
            self.assertLess(NAVIGATION.index("chapters/chapter-47/"), NAVIGATION.index("chapters/chapter-48/"))

if __name__ == "__main__":
    unittest.main()
