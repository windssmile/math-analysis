from pathlib import Path
import re
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
        self.assertIn("chapters/chapter-38/", nav)
        course_map = self.text(ROOT / "content" / "course-map.md")
        self.assertIn("第 37 章：参数曲线与曲线积分](chapters/chapter-37/index.md)", course_map)
        self.assertIn("第 38 章：参数曲面与曲面积分](chapters/chapter-38/index.md)", course_map)

    def test_consistency_review_records_evidence(self):
        review = self.text(ROOT / "docs" / "reviews" / "2026-07-31-chapter-37-consistency-review.md")
        for marker in ("元数据", "依赖", "取向", "重新参数化", "路径无关"):
            self.assertIn(marker, review)

    def test_arc_length_and_reparameterization_proofs_are_complete(self):
        scalar = self.text(path(EXPECTED[1]))
        reparameterization = self.text(path(EXPECTED[3]))
        for marker in ("### 证明障碍", "### 证明路线", "### 逐步证明", "### 假设位置",
                       "### 边界", "### 迁移"):
            self.assertIn(marker, scalar)
        for marker in ("折线和上界", "一致连续", "分割逼近", "保向情形", "反向情形",
                       "换元公式只要求", "保持正则参数化还要求", "每个光滑段", "不为零"):
            self.assertIn(marker, scalar)
        for marker in ("保持正则参数化还要求", "每个光滑段", "不为零", "递增", "递减"):
            self.assertIn(marker, reparameterization)

    def test_review_records_green_gates(self):
        review = self.text(ROOT / "docs" / "reviews" / "2026-07-31-chapter-37-consistency-review.md")
        for marker in ("章级测试", "part_09", "test_zensical_structure", "check_content.py",
                       "zensical build --strict", "check_site.py", "git diff --check", "通过"):
            self.assertIn(marker, review)

    def test_path_independence_converse_states_continuous_field_hypothesis(self):
        text = self.text(path(EXPECTED[3]))
        theorem_window = re.search(
            r"反过来，设(?P<statement>.{0,260})固定.*?定义",
            text,
            re.DOTALL,
        )
        self.assertIsNotNone(theorem_window, "missing path-independence converse statement")
        statement = theorem_window.group("statement")
        self.assertRegex(statement, r"F:D\\to\\mathbb\{R\}\^n")
        self.assertIn("连续", statement)
        assumptions = re.search(
            r"### 假设位置(?P<body>.*?)(?=\n### |\n## )",
            text,
            re.DOTALL,
        )
        self.assertIsNotNone(assumptions, "missing assumptions section")
        self.assertRegex(
            assumptions.group("body"),
            r"连续性[\s\S]*坐标线段[\s\S]*平均[\s\S]*趋于[\s\S]*F_i\(x\)",
        )


if __name__ == "__main__":
    unittest.main()
