from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-35"
EXPECTED = [
    ("u-08-35-01", "Jacobian 行列式为什么描述局部面积与体积伸缩？", 1.50, 0.25, "jacobian-scaling", 9, 11),
    ("u-08-35-02", "重积分换元公式需要哪些条件？", 1.50, 0.25, "change-of-variables", 10, 12),
    ("u-08-35-03", "极坐标怎样处理圆形与径向对称区域？", 1.50, 0.25, "polar-coordinates", 10, 12),
    ("u-08-35-04", "柱面、球面坐标怎样处理三维区域？", 1.50, 0.25, "cylindrical-spherical", 11, 13),
]
MARKERS = {
    "u-08-35-01": ("线性变换", "行列式绝对值", "局部伸缩", "取向"),
    "u-08-35-02": ("一一对应", "连续可微", "Jacobian 不退化", "边界分片", "thm-u-08-35-02-change-of-variables"),
    "u-08-35-03": ("极坐标", "Jacobian", "det", "r"),
    "u-08-35-04": ("柱面坐标", "球面坐标", "rho^2", "sin", "det"),
}

def path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"

class ChapterThirtyFiveTests(unittest.TestCase):
    def text(self, file):
        self.assertTrue(file.is_file(), f"missing {file}")
        return file.read_text(encoding="utf-8") if file.is_file() else ""

    def test_contract(self):
        totals = [0.0, 0.0, 0, 0]
        for row in EXPECTED:
            uid, title, theory, applied, _suffix, exercises, answers = row
            text = self.text(path(row))
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(uid=uid):
                self.assertEqual((uid, title), (meta["unit_id"], meta["title"]))
                self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
                self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
                self.assertEqual(answers, text.count('??? note "答案"'))
                self.assertGreaterEqual(text.count("{#ex-"), 2)
                for marker in MARKERS[uid]:
                    self.assertIn(marker, text)
                self.assertNotIn("由公式可得面积元", text)
            totals = [totals[0]+theory, totals[1]+applied, totals[2]+exercises, totals[3]+answers]
        self.assertEqual([6.0, 1.0, 40, 48], totals)

    def test_guide_and_release(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
        nav = self.text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-35/", nav)

if __name__ == "__main__":
    unittest.main()
