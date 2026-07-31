from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-36"
EXPECTED = [
    ("u-08-36-01", "无界区域上的重积分怎样由极限定义？", 1.50, 0.25, "unbounded-regions", 9, 11),
    ("u-08-36-02", "被积函数有奇点时怎样判断收敛？", 1.50, 0.25, "singular-integrands", 10, 12),
    ("u-08-36-03", "密度怎样产生质量、质心与转动惯量？", 1.00, 0.75, "mass-centroid-inertia", 10, 12),
    ("u-08-36-04", "联合密度怎样产生边缘密度、期望与协方差？", 0.75, 1.00, "joint-density", 10, 12),
    ("u-08-36-05", "怎样为空间累积模型选择区域、坐标与核验方法？", 1.00, 1.00, "spatial-modeling", 12, 15),
]
MARKERS = {
    "u-08-36-01": ("无界区域", "区域穷竭", "非负函数", "极限方式"),
    "u-08-36-02": ("奇点", "挖去邻域", "绝对收敛", "路径风险"),
    "u-08-36-03": ("质量", "质心", "转动惯量", "单位"),
    "u-08-36-04": ("联合密度", "非负", "归一化", "边缘密度", "协方差"),
    "u-08-36-05": ("区域", "坐标", "量纲", "独立核验", "Monte Carlo 选读"),
}

def path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"

class ChapterThirtySixTests(unittest.TestCase):
    def text(self, file):
        self.assertTrue(file.is_file(), f"missing {file}")
        return file.read_text(encoding="utf-8") if file.is_file() else ""

    def test_contract(self):
        totals = [0.0, 0.0, 0, 0]
        all_text = []
        for row in EXPECTED:
            uid, title, theory, applied, _suffix, exercises, answers = row
            text = self.text(path(row))
            all_text.append(text)
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(uid=uid):
                self.assertEqual((uid, title), (meta["unit_id"], meta["title"]))
                self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
                self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
                self.assertEqual(answers, text.count('??? note "答案"'))
                self.assertGreaterEqual(text.count("{#ex-"), 2)
                for marker in MARKERS[uid]:
                    self.assertIn(marker, text)
            totals = [totals[0]+theory, totals[1]+applied, totals[2]+exercises, totals[3]+answers]
        self.assertEqual([5.75, 3.25, 51, 62], totals)
        combined = "\n".join(all_text)
        for forbidden in ("## 条件密度", "σ-代数", "def monte_carlo"):
            self.assertNotIn(forbidden, combined)

    def test_guide_and_release(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
        nav = self.text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-36/", nav)

if __name__ == "__main__":
    unittest.main()
