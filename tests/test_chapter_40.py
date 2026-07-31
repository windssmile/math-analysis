from pathlib import Path
import re
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-40"
EXPECTED = [
    ("u-09-40-01", "三维散度为什么表示局部源汇密度？", 1.50, 0.00,
     "spatial-divergence", 8, 10, ["u-09-39-01", "三维偏导"],
     ["spatial_divergence", "source_density", "small_box_flux"]),
    ("u-09-40-02", "Gauss 公式为什么先在长方体上成立？", 1.25, 0.25,
     "gauss-box", 10, 12, ["u-09-38-04", "u-09-40-01", "微积分基本定理", "累次积分"],
     ["gauss_box", "coordinate_ftc_proof", "outward_normal_signs"]),
    ("u-09-40-03", "规则区域的分片与内部通量为什么会抵消？", 1.00, 0.50,
     "gauss-piecewise-regions", 10, 12, ["u-09-40-02", "第 36 章规则区域"],
     ["piecewise_gauss", "internal_flux_cancellation", "regular_region"]),
    ("u-09-40-04", "Gauss 公式怎样分析流量、电通量与奇点？", 0.75, 0.75,
     "gauss-applications-singularities", 11, 13, ["u-09-40-01", "u-09-40-02", "u-09-40-03", "第 36 章奇点处理"],
     ["incompressible_flow", "electric_flux", "punctured_domain"]),
]
HEADINGS = ["先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
            "即时检验与回望", "常见误区与后续", "习题与答案"]
MARKERS = {
    "u-09-40-01": ("三维散度", "源汇", "净流出", "小长方体", "{#def-u-09-40-01-divergence}"),
    "u-09-40-02": ("Gauss 公式", "长方体", "外法向", "FTC", "{#thm-u-09-40-02-gauss-box}", "### 取向检查"),
    "u-09-40-03": ("分片光滑", "内部通量抵消", "规则区域", "### 取向检查", "{#thm-u-09-40-03-gauss}"),
    "u-09-40-04": ("不可压缩", "电通量", "奇点", "挖孔", "{#ex-u-09-40-04-punctured-flux}", "### 取向检查"),
}


def unit_path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterFortyTests(unittest.TestCase):
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

    def test_small_box_flux_has_remainder_and_normalized_limit(self):
        text = self.text(unit_path(EXPECTED[0]))
        for marker in ("一阶展开", "余项", "体积", "除以", "趋于", "P_x+Q_y+R_z", "正外法向"):
            self.assertIn(marker, text)
        self.assertRegex(text, r"净流出[\s\S]{0,1800}P_x\+Q_y\+R_z")
        self.assertRegex(text, r"除以[\s\S]{0,500}体积[\s\S]{0,500}趋于")

    def test_box_proof_uses_coordinate_ftc_and_all_face_signs(self):
        text = self.text(unit_path(EXPECTED[1]))
        proof = re.search(r"### 长方体上的 Gauss 公式 \{#thm-u-09-40-02-gauss-box\}(?P<body>.*?)\n### 迁移", text, re.S)
        self.assertIsNotNone(proof)
        body = proof.group("body")
        for marker in ("C^1", "邻域", "一元微积分基本定理", "逐坐标", "x=a", "x=b",
                       "y=c", "y=d", "z=e", "z=f", "(-1,0,0)", "(1,0,0)",
                       "(0,-1,0)", "(0,1,0)", "(0,0,-1)", "(0,0,1)",
                       "### 证明障碍", "### 证明路线", "### 逐步证明", "### 假设位置", "### 边界"):
            self.assertIn(marker, body)
        for forbidden in ("Stokes 公式", "微分形式"):
            self.assertNotIn(forbidden, body)

    def test_piecewise_theorem_is_honestly_finite(self):
        text = self.text(unit_path(EXPECTED[2]))
        theorem = re.search(r"### 有限分片 Gauss 公式 \{#thm-u-09-40-03-gauss\}(?P<body>.*?)\n### 迁移", text, re.S)
        self.assertIsNotNone(theorem)
        body = theorem.group("body")
        for marker in ("有限个", "轴对齐长方体", "长方体复形", "阶梯状", "分片光滑", "相反外法向", "成对抵消", "外边界保留"):
            self.assertIn(marker, body)
        for forbidden in ("长方体型正则块", "C^1 双射坐标图", "任意光滑区域都可网格逼近", "显然推广到任意", "Stokes 公式", "微分形式"):
            self.assertNotIn(forbidden, body)

    def test_punctured_domain_checks_inner_normal_and_limit(self):
        text = self.text(unit_path(EXPECTED[3]))
        example = re.search(r"### 例 2：点源与挖孔 \{#ex-u-09-40-04-punctured-flux\}(?P<body>.*?)\n## 即时检验", text, re.S)
        self.assertIsNotNone(example)
        body = example.group("body")
        for marker in ("立方壳", "穿孔域", "正则", "内边界", "相对小立方体", "负", "六面", "单独", "极限"):
            self.assertIn(marker, body)
        self.assertIn(r"F(x)=\frac{x}{\lVert x\rVert^3}", body)
        self.assertIn(r"4\arctan\frac1{\sqrt3}=\frac{2\pi}{3}", body)
        self.assertIn("球面通量只由曲面积分定义直接计算", body)
        self.assertNotIn("在包含原点的球上直接使用", body)
        self.assertIn("若把内边界误取小立方体自身外法向", text)
        self.assertNotIn(r"若把内边界误取 \(e_r\)", text)

    def test_all_tex_is_explicitly_delimited(self):
        suspicious = re.compile(r"(?<!\\)\((?:[^()\n]*(?:\\[A-Za-z]+|[_^])[^()\n]*)\)")
        for row in EXPECTED:
            text = self.text(unit_path(row))
            outside_math = re.sub(r"\\\[[\s\S]*?\\\]", "", text)
            outside_math = re.sub(r"\\\(.*?\\\)", "", outside_math)
            self.assertEqual([], [m.group(0) for m in suspicious.finditer(outside_math)])

    def test_release_surfaces(self):
        guide = self.text(CHAPTER / "index.md")
        nav = self.text(ROOT / "mkdocs.yml")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
            self.assertEqual(1, nav.count(f"chapters/chapter-40/{row[0]}-{row[4]}.md"))
        self.assertNotIn("chapters/chapter-41/", nav)
        self.assertIn("第九部第 40 章，共 181 个学习单元、329 学时", self.text(ROOT / "README.md"))
        course_map = self.text(ROOT / "content" / "course-map.md")
        self.assertIn("第 40 章：Gauss 公式与通量](chapters/chapter-40/index.md)", course_map)
        self.assertIn("第 41 章：Stokes 公式与三大公式的统一（规划中）", course_map)
        self.assertIn("当前发布第 37–40 章；\n第 41 章仍为规划中，不创建正文页面或导航入口。", course_map)
        self.assertNotIn("当前发布第 37–39 章", course_map)
        self.assertNotIn("第 40–41 章仍为规划中", course_map)

    def test_dependency_review_and_representative_html(self):
        dependencies = self.text(ROOT / "docs" / "curriculum" / "part-09-dependencies.md")
        for marker in ("当前发布边界：第 40 章", "第 37–40 章已经发布", "第 41 章仍在规划中"):
            self.assertIn(marker, dependencies)
        review = self.text(ROOT / "docs" / "reviews" / "2026-07-31-chapter-40-consistency-review.md")
        for marker in ("元数据", "Gauss", "取向", "有限分片", "奇点", "390", "arithmatex",
                       "make verify", "check_content.py", "zensical build --strict", "check_site.py", "git diff --check", "通过"):
            self.assertIn(marker, review)


if __name__ == "__main__":
    unittest.main()
