from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-34"
SOURCE = ROOT / "src" / "mathbook_examples" / "multiple_integration.py"
EXPECTED_UNITS = [
    ("u-08-34-01", "矩形上的二重积分为什么可以逐次计算？", 1.50, 0.25, "iterated-integral-theorem", 9, 11),
    ("u-08-34-02", "x-型与 y-型区域怎样写出积分限？", 1.25, 0.50, "type-i-ii-regions", 10, 12),
    ("u-08-34-03", "改变积分次序怎样化简区域与被积函数？", 1.00, 0.75, "change-order", 10, 12),
    ("u-08-34-04", "三重积分怎样按截面或投影逐层计算？", 1.25, 0.50, "triple-integrals", 9, 11),
    ("u-08-34-05", "二维张量积中点法能保证什么、不能保证什么？", 1.00, 1.00, "tensor-midpoint", 12, 15),
]
MARKERS = {
    "u-08-34-01": ("累次积分", "连续", "闭矩形", "完整证明"),
    "u-08-34-02": ("x-型区域", "y-型区域", "投影", "积分限"),
    "u-08-34-03": ("重新描述区域", "改变次序", "分片", "不能机械交换"),
    "u-08-34-04": ("三重积分", "截面", "投影", "积分次序"),
    "u-08-34-05": ("mathbook_examples.multiple_integration", "张量积中点法", "误差前提", "不能证明可积性"),
}

def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"

class ChapterThirtyFourTests(unittest.TestCase):
    def required_text(self, path):
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_locked_units_and_training(self):
        totals = [0.0, 0.0, 0, 0]
        for unit in EXPECTED_UNITS:
            uid, title, theory, applied, _suffix, exercises, answers = unit
            text = self.required_text(unit_path(unit))
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(unit=uid):
                self.assertEqual((uid, title), (meta["unit_id"], meta["title"]))
                self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
                self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
                self.assertEqual(answers, text.count('??? note "答案"'))
                self.assertGreaterEqual(text.count("{#ex-"), 2)
                for marker in MARKERS[uid]:
                    self.assertIn(marker, text)
            totals = [totals[0] + theory, totals[1] + applied, totals[2] + exercises, totals[3] + answers]
        self.assertEqual([6.0, 3.0, 50, 61], totals)

    def test_guide_algorithm_and_release(self):
        guide = self.required_text(CHAPTER / "index.md")
        for unit in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"))
        algorithm = self.required_text(unit_path(EXPECTED_UNITS[-1]))
        self.assertTrue(SOURCE.is_file())
        self.assertIn("tensor_midpoint_2d", algorithm)
        self.assertNotIn("def tensor_midpoint_2d(", algorithm)
        for heading in ("问题来源", "数学转化", "算法思想", "误差与适用条件", "伪代码", "Python", "结果解释"):
            self.assertIn(heading, algorithm)
        nav = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-34/", nav)

if __name__ == "__main__":
    unittest.main()
