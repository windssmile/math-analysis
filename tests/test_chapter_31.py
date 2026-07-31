from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-31"
SOURCE = ROOT / "src" / "mathbook_examples" / "nonlinear.py"

EXPECTED_UNITS = [
    ("u-07-31-01", "Jacobian 可逆怎样产生局部反函数？", 1.50, 0.25, "inverse-function", 9, 11),
    ("u-07-31-02", "隐式方程什么时候能局部解出变量？", 1.50, 0.25, "implicit-function", 10, 12),
    ("u-07-31-03", "局部参数化怎样给出灵敏度并区分分支？", 1.25, 0.50, "local-parameterization", 9, 11),
    ("u-07-31-04", "Newton 法怎样可靠求解非线性方程组？", 1.00, 0.75, "newton-systems", 12, 15),
]

REQUIRED_MARKERS = {
    "u-07-31-01": ("反函数定理", "Jacobian 可逆", "局部", "全局"),
    "u-07-31-02": ("隐函数定理", "分块 Jacobian", "局部唯一", "导数公式"),
    "u-07-31-03": ("局部参数化", "灵敏度", "分支", "远处"),
    "u-07-31-04": ("问题来源", "数学转化", "算法思想", "误差与适用条件", "伪代码", "Python", "结果解释"),
}


def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"


class ChapterThirtyOneTests(unittest.TestCase):
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
        self.assertEqual([5.25, 1.75, 40, 49], totals)

    def test_theorem_order_and_local_global_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        inverse = guide.index("反函数定理")
        implicit = guide.index("隐函数定理")
        self.assertLess(inverse, implicit)
        for unit in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"))
        combined = "\n".join(self.required_text(unit_path(unit)) for unit in EXPECTED_UNITS[:3])
        for marker in ("局部可逆不等于全局一一对应", "隐函数局部存在", "远处可能存在其他分支"):
            self.assertIn(marker, combined)

    def test_newton_unit_reuses_source_and_keeps_stop_semantics(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[-1]))
        self.assertTrue(SOURCE.is_file())
        self.assertIn("mathbook_examples.nonlinear", text)
        self.assertNotIn("def newton_system(", text)
        for marker in ("residual", "step", "singular_jacobian", "ill_conditioned_jacobian", "max_iterations", "停止信号", "不是根误差证书"):
            self.assertIn(marker, text)

    def test_publication_reaches_chapter_31_only(self) -> None:
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-31/", config)
        self.assertNotIn("chapters/chapter-32/", config)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第七部第 31 章", readme)
        self.assertIn("141 个学习单元", readme)
        dependencies = self.required_text(ROOT / "docs" / "curriculum" / "part-07-dependencies.md")
        self.assertIn("当前发布边界：第 31 章", dependencies)


if __name__ == "__main__":
    unittest.main()
