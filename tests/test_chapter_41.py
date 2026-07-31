from pathlib import Path
import re
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-41"
EXPECTED = [
    ("u-09-41-01", "三维旋度为什么表示局部环流密度？", 1.50, 0.00,
     "spatial-curl", 8, 10, ["第 29 章偏导与叉积", "u-09-37-03"],
     ["spatial_curl", "local_circulation_density", "small_rectangle_remainder"]),
    ("u-09-41-02", "曲面取向怎样诱导边界曲线的正方向？", 1.25, 0.25,
     "induced-boundary-orientation", 9, 11, ["u-09-37-01", "u-09-38-01", "右手规则"],
     ["induced_boundary_orientation", "right_hand_rule", "boundary_branches"]),
    ("u-09-41-03", "Stokes 公式怎样在单个参数曲面片上证明？", 1.25, 0.25,
     "stokes-parametric-patch", 10, 12, ["u-09-39-02", "u-09-41-01", "u-09-41-02"],
     ["stokes_patch", "pullback_calculation", "green_reduction"]),
    ("u-09-41-04", "分片曲面上的内部边界为什么成对抵消？", 1.00, 0.50,
     "stokes-piecewise-surfaces", 10, 12, ["u-09-39-03", "u-09-41-03"],
     ["piecewise_stokes", "internal_boundary_cancellation", "compatible_patches"]),
    ("u-09-41-05", "怎样选择并核验 Green、Gauss 与 Stokes 公式？", 1.00, 1.00,
     "vector-theorem-selection", 12, 15, ["u-09-39-04", "u-09-40-04", "u-09-41-04"],
     ["vector_theorem_selection", "line_integral_check", "flux_integral_check"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]
MARKERS = {
    "u-09-41-01": ("三维旋度", "局部环流密度", "右手规则", "取向", "{#def-u-09-41-01-curl}"),
    "u-09-41-02": ("诱导边界方向", "曲面取向", "右手规则", "边界分支", "{#def-u-09-41-02-induced-orientation}", "### 取向检查"),
    "u-09-41-03": ("Stokes", "参数域", "Green", "拉回计算", "{#thm-u-09-41-03-stokes-patch}", "### 取向检查"),
    "u-09-41-04": ("分片光滑曲面", "内部边界抵消", "相反方向", "拼接", "{#thm-u-09-41-04-stokes}", "### 取向检查"),
    "u-09-41-05": ("Green", "Gauss", "Stokes", "数值结果不能证明", "{#workflow-u-09-41-05-selection}", "### 取向检查"),
}


def unit_path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterFortyOneTests(unittest.TestCase):
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
        self.assertEqual([6.0, 2.0, 49, 60], totals)

    def test_local_curl_comes_from_oriented_small_rectangle_with_remainder(self):
        text = self.text(unit_path(EXPECTED[0]))
        for marker in ("小坐标矩形", "一阶展开", "余项", "面积", "除以", "趋于",
                       "Q_x-P_y", "R_y-Q_z", "P_z-R_x", "正向", "右手规则"):
            self.assertIn(marker, text)
        self.assertRegex(text, r"环流[\s\S]{0,2200}Q_x-P_y")
        self.assertRegex(text, r"除以[\s\S]{0,600}面积[\s\S]{0,600}趋于")

    def test_induced_orientation_matches_parameter_domain_and_left_side_rule(self):
        text = self.text(unit_path(EXPECTED[1]))
        block = re.search(r"### 诱导边界方向 \{#def-u-09-41-02-induced-orientation\}(?P<body>.*?)\n### 迁移", text, re.S)
        self.assertIsNotNone(block)
        body = block.group("body")
        for marker in ("r_u\\times r_v", "参数域", "逆时针", "保向", "沿边界行进时曲面在左侧",
                       "右手", "拇指", "四指", "每个边界分支", "内边界"):
            self.assertIn(marker, body)

    def test_patch_proof_expands_pullback_and_uses_green(self):
        text = self.text(unit_path(EXPECTED[2]))
        proof = re.search(r"### 单参数片上的 Stokes 公式 \{#thm-u-09-41-03-stokes-patch\}(?P<body>.*?)\n### 迁移", text, re.S)
        self.assertIsNotNone(proof)
        body = proof.group("body")
        for marker in ("C^1", "邻域", "C^2", "正则", "分片光滑边界", "参数域", "Green 公式",
                       "F(r)\\cdot dr", "F(r)\\cdot r_u", "F(r)\\cdot r_v", "链式法则",
                       "\\operatorname{curl}F(r)\\cdot(r_u\\times r_v)", "### 证明障碍", "### 证明路线",
                       "### 逐步证明", "### 假设位置", "### 边界"):
            self.assertIn(marker, body)

    def test_piecewise_stokes_is_finite_and_honest_about_seams(self):
        text = self.text(unit_path(EXPECTED[3]))
        theorem = re.search(r"### 有限兼容分片 Stokes 公式 \{#thm-u-09-41-04-stokes\}(?P<body>.*?)\n### 迁移", text, re.S)
        self.assertIsNotNone(theorem)
        body = theorem.group("body")
        for marker in ("有限个", "兼容", "正则参数片", "接缝", "相反方向", "成对抵消", "外边界保留", "奇点"):
            self.assertIn(marker, body)
        for forbidden in ("任意分片光滑曲面显然", "无限分片", "微分形式"):
            self.assertNotIn(forbidden, body)

    def test_selection_page_uses_both_algorithms_once_and_states_certificate_boundary(self):
        text = self.text(unit_path(EXPECTED[4]))
        self.assertEqual(1, text.count("from src.mathbook_examples.vector_analysis import"))
        self.assertEqual(1, text.count("composite_midpoint_line_integral("))
        self.assertEqual(1, text.count("composite_midpoint_flux_integral("))
        for marker in ("内部微分算子", "定向对象", "诱导边界", "正则性", "奇点",
                       "参数化无关", "误差证书", "采样", "不能证明 Green", "不能证明 Gauss", "不能证明 Stokes"):
            self.assertIn(marker, text)

    def test_all_tex_is_explicitly_delimited(self):
        suspicious = re.compile(r"(?<!\\)\((?:[^()\n]*(?:\\[A-Za-z]+|[_^])[^()\n]*)\)")
        for row in EXPECTED:
            text = self.text(unit_path(row))
            outside_math = re.sub(r"\\\[[\s\S]*?\\\]", "", text)
            outside_math = re.sub(r"\\\(.*?\\\)", "", outside_math)
            self.assertEqual([], [m.group(0) for m in suspicious.finditer(outside_math)])

    def test_release_surfaces_and_no_chapter_42_body(self):
        guide = self.text(CHAPTER / "index.md")
        nav = self.text(ROOT / "mkdocs.yml")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
            self.assertEqual(1, nav.count(f"chapters/chapter-41/{row[0]}-{row[4]}.md"))
        self.assertFalse((ROOT / "content" / "chapters" / "chapter-42").exists())
        self.assertNotIn("chapters/chapter-42/", nav)
        self.assertIn("第九部第 41 章，共 186 个学习单元、337 学时", self.text(ROOT / "README.md"))
        course_map = self.text(ROOT / "content" / "course-map.md")
        self.assertIn("第 41 章：Stokes 公式与三大公式的统一](chapters/chapter-41/index.md)", course_map)
        self.assertIn("当前发布第 37–41 章；第九部核心正文已全部发布", course_map)
        self.assertIn("选读附录：从向量分析到微分形式（规划中）", course_map)

    def test_dependency_review_and_representative_html(self):
        dependencies = self.text(ROOT / "docs" / "curriculum" / "part-09-dependencies.md")
        for marker in ("当前发布边界：第 41 章", "第 37–41 章已经发布", "第九部核心正文已全部发布"):
            self.assertIn(marker, dependencies)
        review = self.text(ROOT / "docs" / "reviews" / "2026-07-31-chapter-41-consistency-review.md")
        for marker in ("元数据", "Stokes", "取向", "拉回", "有限分片", "算法唯一调用点", "390", "arithmatex",
                       "make verify", "check_content.py", "zensical build --strict", "check_site.py", "git diff --check", "通过"):
            self.assertIn(marker, review)


if __name__ == "__main__":
    unittest.main()
