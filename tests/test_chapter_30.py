from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-30"

EXPECTED_UNITS = [
    ("u-07-30-01", "二阶微分和 Hessian 为什么是双线性对象？", 1.50, 0.25, "second-derivative", 9, 11),
    ("u-07-30-02", "高阶微分和多重指标怎样组织混合偏导？", 1.25, 0.25, "higher-derivatives", 8, 10),
    ("u-07-30-03", "多元 Taylor 公式怎样给出可证明的余项？", 1.50, 0.25, "multivariable-taylor", 10, 12),
    ("u-07-30-04", "二次模型怎样支持误差界和敏感性分析？", 1.25, 0.75, "quadratic-models", 11, 14),
]

REQUIRED_MARKERS = {
    "u-07-30-01": ("双线性映射", "Hessian", "混合偏导", "连续"),
    "u-07-30-02": ("多重指标", "高阶微分", "对称多线性"),
    "u-07-30-03": ("线段完全位于定义域", "一元 Taylor", "余项"),
    "u-07-30-04": ("二次模型", "理论误差界", "敏感性", "不作极值判定"),
}


def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"


class ChapterThirtyTests(unittest.TestCase):
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
                self.assertNotIn("Hessian 正定所以是极小值", text)
                totals[0] += theory
                totals[1] += applied
                totals[2] += exercises
                totals[3] += answers
        self.assertEqual([5.5, 1.5, 38, 47], totals)

    def test_guide_lists_four_units_and_the_proof_route(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共4个核心单元，7学时（理论5.5，应用1.5）。", guide)
        for unit in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"))
        for marker in ("Hessian", "多重指标", "沿线段", "第 31 章", "不作极值判定"):
            self.assertIn(marker, guide)

    def test_taylor_proof_checks_domain_and_remainder_conditions(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in ("g(t)=f(a+th)", "[a,a+h]", "线段完全位于定义域", "Lagrange 余项", "Peano 余项"):
            self.assertIn(marker, text)

    def test_chapter_30_remains_on_the_publication_surfaces(self) -> None:
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-30/", config)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第七部已经完整发布", readme)
        dependencies = self.required_text(ROOT / "docs" / "curriculum" / "part-07-dependencies.md")
        self.assertIn("| 第 30 章 | 4 | 5.50 | 1.50 | 7.00 | 已发布 |", dependencies)


if __name__ == "__main__":
    unittest.main()
