from pathlib import Path
import re
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-39"
EXPECTED = [
    ("u-09-39-01", "平面场的散度与旋度怎样描述局部变化？", 1.50, 0.00,
     "planar-divergence-curl", 8, 10, ["偏导", "Jacobian"],
     ["planar_divergence", "scalar_curl", "local_circulation_flux"]),
    ("u-09-39-02", "Green 公式怎样从简单区域上的微积分基本定理得到？", 1.25, 0.25,
     "green-theorem", 10, 12, ["u-09-37-03", "u-09-39-01", "微积分基本定理", "累次积分"],
     ["green_theorem", "simple_region_proof", "boundary_cancellation"]),
    ("u-09-39-03", "分片区域、多连通区域与边界方向怎样处理？", 1.00, 0.50,
     "multiply-connected-green", 10, 12, ["u-09-39-02", "区域分片"],
     ["piecewise_green", "multiply_connected_region", "boundary_orientation"]),
    ("u-09-39-04", "Green 公式怎样控制面积、环流、通量与路径无关？", 0.75, 0.75,
     "green-applications", 11, 13, ["u-09-37-04", "u-09-39-01", "u-09-39-02", "u-09-39-03"],
     ["area_by_green", "path_independence", "planar_incompressibility"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]
MARKERS = {
    "u-09-39-01": ("平面散度", "标量旋度", "局部环流", "局部通量", "{#def-u-09-39-01-planar-div-curl}"),
    "u-09-39-02": ("Green 公式", "微积分基本定理", "简单区域", "内部边界抵消", "{#thm-u-09-39-02-green}", "### 取向检查"),
    "u-09-39-03": ("多连通", "外边界", "内边界", "### 取向检查", "{#thm-u-09-39-03-multiply-connected-green}"),
    "u-09-39-04": ("面积公式", "路径无关", "环流", "不可压缩", "{#thm-u-09-39-04-path-independence}", "### 取向检查"),
}


def unit_path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterThirtyNineTests(unittest.TestCase):
    def text(self, path):
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_unit_contract(self):
        totals = [0.0, 0.0, 0, 0]
        for row in EXPECTED:
            uid, title, theory, applied, _, exercises, answers, prereqs, capabilities = row
            text = self.text(unit_path(row))
            meta = yaml.safe_load(text.split("---\n", 2)[1])
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
            totals = [totals[0] + theory, totals[1] + applied, totals[2] + exercises, totals[3] + answers]
        self.assertEqual([4.5, 1.5, 39, 47], totals)

    def test_local_rectangle_derivations_fix_signs(self):
        text = self.text(unit_path(EXPECTED[0]))
        for marker in ("小矩形", "Q_x-P_y", "P_x+Q_y", "逆时针", "净外通量", "除以", "趋于"):
            self.assertIn(marker, text)
        self.assertRegex(text, r"局部环流[\s\S]{0,500}Q_x-P_y")
        self.assertRegex(text, r"局部通量[\s\S]{0,500}P_x\+Q_y")

    def test_green_proof_is_ftc_based_and_non_circular(self):
        text = self.text(unit_path(EXPECTED[1]))
        proof = re.search(r"### Green 公式 \{#thm-u-09-39-02-green\}(?P<body>.*?)\n### 迁移", text, re.S)
        self.assertIsNotNone(proof)
        body = proof.group("body")
        for marker in ("C^1", "邻域", "同时", "x-简单", "y-简单", "一元微积分基本定理",
                       "逐项", "P_y", "Q_x", "逆时针", "内部边界抵消", "### 证明障碍",
                       "### 证明路线", "### 逐步证明", "### 假设位置", "### 边界"):
            self.assertIn(marker, body)
        for forbidden in ("Gauss 公式", "Stokes 公式", "微分形式"):
            self.assertNotIn(forbidden, body)

    def test_normal_form_has_explicit_tangent_normal_sign(self):
        text = self.text(unit_path(EXPECTED[1]))
        for marker in ("正外法向", "正向单位切向", "n=(T_y,-T_x)",
                       "P n_x+Q n_y", "P_x+Q_y", "切向形式推出"):
            self.assertIn(marker, text)

    def test_multiply_connected_orientation_and_cancellation(self):
        text = self.text(unit_path(EXPECTED[2]))
        for marker in ("有限分片", "相反方向", "成对抵消", "外边界逆时针", "洞边界顺时针"):
            self.assertIn(marker, text)
        annulus = re.search(r"### 例 1：环域(?P<body>.*?)\n### 例 2", text, re.S)
        self.assertIsNotNone(annulus)
        self.assertIn("2\\pi", annulus.group("body"))
        self.assertIn("-2\\pi", annulus.group("body"))

    def test_path_independence_conditions_and_punctured_counterexample(self):
        text = self.text(unit_path(EXPECTED[3]))
        theorem = re.search(r"### 路径无关判据 \{#thm-u-09-39-04-path-independence\}(?P<body>.*?)\n###", text, re.S)
        self.assertIsNotNone(theorem)
        for marker in ("单连通", "每条分片光滑闭路", "curl", "势函数"):
            self.assertIn(marker, theorem.group("body"))
        for marker in ("穿孔域", "(-y/(x^2+y^2),x/(x^2+y^2))", "奇点", "不在域", "2\\pi", "不能保证势函数"):
            self.assertIn(marker, text)

    def test_guide_and_release_surfaces(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
        nav = self.text(ROOT / "mkdocs.yml")
        for row in EXPECTED:
            self.assertEqual(1, nav.count(f"chapters/chapter-39/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-40/", nav)
        self.assertNotIn("chapters/chapter-41/", nav)
        readme = self.text(ROOT / "README.md")
        self.assertIn("第九部第 39 章，共 177 个学习单元、323 学时", readme)
        course_map = self.text(ROOT / "content" / "course-map.md")
        self.assertIn("第 39 章：Green 公式与平面场](chapters/chapter-39/index.md)", course_map)
        self.assertIn("第 40 章：Gauss 公式与通量（规划中）", course_map)

    def test_dependency_map_and_review_record_release_boundary(self):
        dependencies = self.text(ROOT / "docs" / "curriculum" / "part-09-dependencies.md")
        for marker in ("当前发布边界：第 39 章", "第 37–39 章已经发布", "第 40–41 章仍在规划中"):
            self.assertIn(marker, dependencies)
        review = self.text(ROOT / "docs" / "reviews" / "2026-07-31-chapter-39-consistency-review.md")
        for marker in ("元数据", "Green", "取向", "多连通", "路径无关", "make verify",
                       "check_content.py", "zensical build --strict", "check_site.py", "git diff --check", "通过"):
            self.assertIn(marker, review)


if __name__ == "__main__":
    unittest.main()
