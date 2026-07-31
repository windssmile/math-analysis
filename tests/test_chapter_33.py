from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-33"
EXPECTED_UNITS = [
    ("u-08-33-01", "小矩形上的局部贡献怎样累积成二重积分？", 1.50, 0.25, "riemann-double-integral", 8, 10),
    ("u-08-33-02", "连续函数为什么在闭矩形上可积？", 1.75, 0.00, "continuous-integrability", 9, 11),
    ("u-08-33-03", "线性、序关系与区域可加性怎样成立？", 1.50, 0.25, "integral-properties", 8, 10),
    ("u-08-33-04", "怎样在常用有界区域上定义重积分？", 1.50, 0.25, "bounded-regions", 9, 11),
]
REQUIRED_MARKERS = {
    "u-08-33-01": ("分割", "小矩形直径", "Riemann 和", "取样无关"),
    "u-08-33-02": ("一致连续", "振幅", "连续函数", "可积"),
    "u-08-33-03": ("线性", "单调性", "绝对值估计", "区域可加性"),
    "u-08-33-04": ("区域外补零", "分片光滑边界", "三重积分", "不发展 Jordan 测度"),
}
REQUIRED_ANCHORS = {
    "u-08-33-01": ("def-u-08-33-01-riemann-double-integral",),
    "u-08-33-02": ("thm-u-08-33-02-continuous-integrable",),
    "u-08-33-03": ("thm-u-08-33-03-integral-properties",),
    "u-08-33-04": ("def-u-08-33-04-region-integral",),
}


def unit_path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"


class ChapterThirtyThreeTests(unittest.TestCase):
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
                for marker in REQUIRED_MARKERS[unit_id] + REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(marker, text)
                totals[0] += theory
                totals[1] += applied
                totals[2] += exercises
                totals[3] += answers
        self.assertEqual([6.25, 0.75, 34, 42], totals)

    def test_guide_and_release_boundary_are_consistent(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        for unit in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{unit[1]}]({unit[0]}-{unit[4]}.md)"))
        navigation = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-33/", navigation)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第八部已发布", readme)
        dependencies = self.required_text(ROOT / "docs" / "curriculum" / "part-08-dependencies.md")
        self.assertIn("| 第 33 章 | 4 | 6.25 | 0.75 | 7.00 | 已发布 |", dependencies)


if __name__ == "__main__":
    unittest.main()
