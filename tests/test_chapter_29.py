from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-29"
SOURCE = ROOT / "src" / "mathbook_examples" / "multivariate.py"

EXPECTED_UNITS = [
    ("u-07-29-01", "偏导数和方向导数能否保证函数可微？", 1.25, 0.25, "partial-directional", 8, 10),
    ("u-07-29-02", "Fréchet 微分怎样刻画最佳线性近似？", 1.50, 0.25, "frechet-derivative", 9, 11),
    ("u-07-29-03", "连续偏导为什么足以推出可微？", 1.50, 0.25, "continuous-partials", 9, 11),
    ("u-07-29-04", "导数映射怎样满足代数规则和链式法则？", 1.50, 0.25, "chain-rule", 9, 11),
    ("u-07-29-05", "Jacobian、梯度与条件数怎样描述敏感性？", 1.25, 0.50, "jacobian-conditioning", 10, 12),
    ("u-07-29-06", "怎样计算并可靠核验多元线性化？", 0.75, 0.75, "linearization-check", 12, 15),
]

REQUIRED_MARKERS = {
    "u-07-29-01": ("偏导数", "方向导数", "不连续", "不能推出可微"),
    "u-07-29-02": ("Fréchet", "线性映射", "余项", "唯一"),
    "u-07-29-03": ("连续偏导", "充分条件", "不是必要条件", "线段"),
    "u-07-29-04": ("链式法则", "定义域", "值域", "矩阵乘法"),
    "u-07-29-05": ("Jacobian", "梯度", "条件数", "问题敏感性", "算法稳定性"),
    "u-07-29-06": ("问题来源", "数学转化", "算法思想", "误差与适用条件", "伪代码", "Python", "结果解释"),
}


def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"


class ChapterTwentyNineTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_locked_metadata_training_and_markers(self) -> None:
        totals = [0.0, 0.0, 0, 0]
        for unit in EXPECTED_UNITS:
            unit_id, title, theory, applied, _suffix, exercises, answers = unit
            text = self.required_text(unit_path(unit))
            metadata = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(unit=unit_id):
                self.assertEqual((unit_id, title), (metadata["unit_id"], metadata["title"]))
                self.assertEqual((theory, applied), (metadata["hours"]["theory"], metadata["hours"]["applied"]))
                self.assertEqual(2, metadata["content_standard"])
                self.assertIn(f"{{#{unit_id}}}", text)
                self.assertGreaterEqual(text.count("{#ex-"), 2)
                self.assertGreaterEqual(text.count("### 即时检验 "), 2)
                self.assertEqual(exercises, text.count(f"{{#pr-{unit_id}-"))
                self.assertEqual(answers, text.count('??? note "答案"'))
                for marker in REQUIRED_MARKERS[unit_id]:
                    self.assertIn(marker, text)
                totals[0] += theory
                totals[1] += applied
                totals[2] += exercises
                totals[3] += answers
        self.assertEqual([7.75, 2.25, 57, 70], totals)

    def test_guide_lists_six_units_and_route(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共6个核心单元，10学时（理论7.75，应用2.25）。", guide)
        for unit in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"))
        for marker in ("方向导数", "Fréchet", "链式法则", "Jacobian", "第 30 章"):
            self.assertIn(marker, guide)

    def test_application_unit_reuses_unique_source(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[-1]))
        self.assertTrue(SOURCE.is_file())
        self.assertIn("mathbook_examples.multivariate", text)
        self.assertNotIn("def check_jacobian(", text)
        for marker in ("截断误差", "舍入误差", "数值吻合", "不能证明 Fréchet 可微"):
            self.assertIn(marker, text)

    def test_chapter_29_remains_on_the_publication_surfaces(self) -> None:
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-29/", config)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第七部已经完整发布", readme)
        dependencies = self.required_text(ROOT / "docs" / "curriculum" / "part-07-dependencies.md")
        self.assertIn("| 第 29 章 | 6 | 7.75 | 2.25 | 10.00 | 已发布 |", dependencies)


if __name__ == "__main__":
    unittest.main()
