from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-32"
SOURCE = ROOT / "src" / "mathbook_examples" / "optimization.py"

EXPECTED_UNITS = [
    ("u-07-32-01", "多元极值什么时候存在，模型定义域怎样影响答案？", 1.25, 0.25, "extrema-existence", 8, 10),
    ("u-07-32-02", "无约束极值为什么满足一阶必要条件？", 1.50, 0.25, "first-order-extrema", 9, 11),
    ("u-07-32-03", "Hessian 怎样给出二阶必要与充分条件？", 1.50, 0.25, "second-order-tests", 10, 12),
    ("u-07-32-04", "Lagrange 乘子怎样处理正则等式约束？", 1.50, 0.50, "lagrange-multipliers", 10, 12),
    ("u-07-32-05", "多个约束、几何解释和异常点怎样处理？", 1.25, 0.50, "multiple-constraints", 10, 12),
    ("u-07-32-06", "梯度法、Newton 法和约束候选怎样可靠核验？", 1.00, 1.25, "optimization-check", 13, 16),
]

REQUIRED_MARKERS = {
    "u-07-32-01": ("紧致", "连续", "极值存在", "定义域"),
    "u-07-32-02": ("一阶必要条件", "内点", "驻点", "边界"),
    "u-07-32-03": ("二阶必要条件", "二阶充分条件", "半正定", "不能判定"),
    "u-07-32-04": ("正则", "Lagrange 乘子", "约束资格", "必要条件"),
    "u-07-32-05": ("多个约束", "梯度线性无关", "异常点", "直接检查"),
    "u-07-32-06": ("问题来源", "数学转化", "算法思想", "误差与适用条件", "伪代码", "Python", "结果解释"),
}


def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"


class ChapterThirtyTwoTests(unittest.TestCase):
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
        self.assertEqual([8.0, 3.0, 60, 73], totals)

    def test_dependency_order_and_scope_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        for unit in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"))
        combined = "\n".join(self.required_text(unit_path(unit)) for unit in EXPECTED_UNITS)
        for marker in ("先证明极值存在", "再检查一阶必要条件", "半正定不能判定", "不覆盖不等式约束", "不建立一般 KKT 理论"):
            self.assertIn(marker, combined)

    def test_computational_unit_reuses_source_without_optimal_claim(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[-1]))
        self.assertTrue(SOURCE.is_file())
        self.assertIn("mathbook_examples.optimization", text)
        self.assertNotIn("def gradient_descent(", text)
        self.assertNotIn("def newton_optimize(", text)
        for marker in ("gradient", "step", "non_descent_direction", "singular_hessian", "indefinite_hessian", "max_iterations", "不声明候选点最优"):
            self.assertIn(marker, text)

    def test_part_remains_fully_published_after_later_parts_advance(self) -> None:
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-32/", config)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第七部已经完整发布", readme)
        self.assertIn("147 个学习单元", readme)
        dependencies = self.required_text(ROOT / "docs" / "curriculum" / "part-07-dependencies.md")
        self.assertIn("当前发布边界：第 32 章", dependencies)
        self.assertIn("25 个核心单元、44 学时", dependencies)


if __name__ == "__main__":
    unittest.main()
