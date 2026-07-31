from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-37"
EXPECTED = [
    ("u-09-37-01", "正则参数曲线怎样描述运动、方向与切向量？", 1.50, 0.00,
     "regular-parametric-curves", 8, 10, ["向量函数微分", "空间解析几何"],
     ["regular_parametric_curve", "curve_orientation", "unit_tangent"]),
    ("u-09-37-02", "弧长与第一类曲线积分怎样由参数化定义？", 1.25, 0.25,
     "arc-length-scalar-line-integral", 9, 11, ["u-09-37-01", "Riemann 积分"],
     ["arc_length", "scalar_line_integral", "reparameterization_invariance"]),
    ("u-09-37-03", "第二类曲线积分怎样表示功与环流？", 1.00, 0.50,
     "work-circulation", 9, 11, ["u-09-37-01", "u-09-37-02", "内积"],
     ["vector_line_integral", "work", "circulation"]),
    ("u-09-37-04", "重新参数化、反向与保守场怎样改变积分？", 0.75, 0.75,
     "reparameterization-conservative-fields", 10, 12,
     ["u-09-37-02", "u-09-37-03", "梯度"],
     ["oriented_reparameterization", "potential_function", "path_independence"]),
]
MARKERS = {
    "u-09-37-01": ("分段光滑", "正则", "切向量", "方向", "{#def-u-09-37-01-regular-curve}"),
    "u-09-37-02": ("弧长", "第一类曲线积分", "参数分割", "重新参数化", "{#def-u-09-37-02-scalar-line-integral}"),
    "u-09-37-03": ("第二类曲线积分", "功", "环流", "### 取向检查", "{#def-u-09-37-03-vector-line-integral}"),
    "u-09-37-04": ("保向", "反向", "势函数", "路径无关", "### 取向检查", "{#thm-u-09-37-04-reparameterization}"),
}
HEADINGS = [
    "先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
    "即时检验与回望", "常见误区与后续", "习题与答案",
]


def path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterThirtySevenTests(unittest.TestCase):
    def text(self, file):
        self.assertTrue(file.is_file(), f"missing {file}")
        return file.read_text(encoding="utf-8") if file.is_file() else ""

    def test_unit_contract(self):
        totals = [0.0, 0.0, 0, 0]
        combined = []
        for row in EXPECTED:
            uid, title, theory, applied, _suffix, exercises, answers, prereqs, capabilities = row
            text = self.text(path(row))
            combined.append(text)
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(uid=uid):
                self.assertEqual(2, meta["content_standard"])
                self.assertEqual((uid, title), (meta["unit_id"], meta["title"]))
                self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
                self.assertEqual(prereqs, meta["prerequisites"]["book"])
                self.assertEqual(capabilities, meta["capabilities"])
                self.assertEqual(3, len(meta["learning_goals"]))
                self.assertIn(f"# {title} {{#{uid}}}", text)
                positions = [text.index(f"## {heading}") for heading in HEADINGS]
                self.assertEqual(sorted(positions), positions)
                self.assertGreaterEqual(text.count("{#ex-"), 2)
                self.assertGreaterEqual(text.count("### 即时检验"), 2)
                self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
                self.assertEqual(answers, text.count('??? note "答案"'))
                for marker in MARKERS[uid]:
                    self.assertIn(marker, text)
            totals = [totals[0] + theory, totals[1] + applied,
                      totals[2] + exercises, totals[3] + answers]
        self.assertEqual([4.5, 1.5, 36, 44], totals)
        all_text = "\n".join(combined)
        for forbidden in ("Green 公式可得", "Gauss 公式可得", "Stokes 公式可得"):
            self.assertNotIn(forbidden, all_text)

    def test_guide_and_release_surfaces(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
        nav = self.text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-37/", nav)
        for chapter in range(38, 42):
            self.assertNotIn(f"chapters/chapter-{chapter}/", nav)
        readme = self.text(ROOT / "README.md")
        self.assertIn("第九部第 37 章，共 169 个学习单元、311 学时", readme)
        course_map = self.text(ROOT / "content" / "course-map.md")
        self.assertIn("第 37 章：参数曲线与曲线积分](chapters/chapter-37/index.md)", course_map)
        self.assertIn("第 38 章：参数曲面与曲面积分（规划中）", course_map)

    def test_consistency_review_records_evidence(self):
        review = self.text(ROOT / "docs" / "reviews" / "2026-07-31-chapter-37-consistency-review.md")
        for marker in ("元数据", "依赖", "取向", "重新参数化", "路径无关", "第 38–41 章"):
            self.assertIn(marker, review)


if __name__ == "__main__":
    unittest.main()
