from pathlib import Path
import re
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-38"
EXPECTED = [
    ("u-09-38-01", "正则参数曲面怎样产生切平面、法向量与取向？", 1.50, 0.00,
     "regular-parametric-surfaces", 8, 10, ["向量函数微分", "局部参数化", "叉积"],
     ["regular_parametric_surface", "tangent_plane", "surface_orientation"]),
    ("u-09-38-02", "曲面面积元为什么由叉积的模给出？", 1.25, 0.25,
     "surface-area-element", 9, 11, ["u-09-38-01", "局部面积伸缩"],
     ["surface_area_element", "local_linearization", "area_reparameterization"]),
    ("u-09-38-03", "第一类曲面积分怎样累积曲面上的标量分布？", 1.00, 0.50,
     "scalar-surface-integral", 9, 11, ["u-09-38-02", "Riemann 重积分"],
     ["scalar_surface_integral", "surface_density", "unoriented_invariance"]),
    ("u-09-38-04", "通量积分怎样依赖参数化与曲面取向？", 0.75, 0.75,
     "flux-integral", 10, 12, ["u-09-38-01", "u-09-38-02", "u-09-38-03", "向量场"],
     ["flux_integral", "oriented_area_element", "orientation_reversal"]),
]
MARKERS = {
    "u-09-38-01": ("正则参数曲面", "切平面", "法向量", "### 取向检查",
                     "{#def-u-09-38-01-regular-surface}"),
    "u-09-38-02": ("叉积", "局部线性化", "面积元", "重新参数化",
                     "{#thm-u-09-38-02-area-element}"),
    "u-09-38-03": ("第一类曲面积分", "曲面密度", "薄膜质量", "无向",
                     "{#def-u-09-38-03-scalar-surface-integral}"),
    "u-09-38-04": ("通量", "有向面积元", "取向反转", "图形曲面", "### 取向检查",
                     "{#def-u-09-38-04-flux-integral}"),
}
HEADINGS = [
    "先备知识", "学习目标", "牵引问题", "探索与猜想", "概念与理论", "例题与迁移",
    "即时检验与回望", "常见误区与后续", "习题与答案",
]


def path(row):
    return CHAPTER / f"{row[0]}-{row[4]}.md"


class ChapterThirtyEightTests(unittest.TestCase):
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
        for forbidden in ("由 Green 公式", "由 Gauss 公式", "由 Stokes 公式", "一般流形"):
            self.assertNotIn(forbidden, all_text)

    def test_area_element_has_classical_riemann_proof_contract(self):
        text = self.text(path(EXPECTED[1]))
        for marker in ("### 证明障碍", "### 证明路线", "### 逐步证明", "### 假设位置",
                       "### 边界", "### 迁移", "Fréchet", "第 35 章", "一致连续",
                       "参数矩形", "关键估计", "Jacobian 的绝对值", "取向符号"):
            self.assertIn(marker, text)

    def test_area_element_proof_uses_non_circular_inscribed_triangulations(self):
        text = self.text(path(EXPECTED[1]))
        window = re.search(
            r"### 面积元定理 \{#thm-u-09-38-02-area-element\}"
            r"(?P<body>.*?)\n### 迁移",
            text,
            re.DOTALL,
        )
        self.assertIsNotNone(window, "missing anchored area-element proof window")
        body = window.group("body")
        for marker in (
            "形状正则三角剖分", "内接平面三角形", "定义曲面面积", "有限覆盖",
            "边向量", "Dr(a)", "余项", "\\omega(h)", "叉积的双线性",
            "单三角形面积差", "\\operatorname{area}(T)", "求和", "Riemann 和",
        ):
            self.assertIn(marker, body)
        self.assertRegex(body, r"C[^\n]{0,100}\\sup_D\\lVert Dr\\rVert[^\n]{0,100}\\omega\(h\)")
        self.assertNotIn("曲面片面积与此值之差", body)

    def test_zero_area_parameter_boundary_extension_is_explicit(self):
        area = self.text(path(EXPECTED[1]))
        extension = re.search(
            r"### 零面积边界扩展 \{#prop-u-09-38-02-zero-area-boundary\}"
            r"(?P<body>.*?)\n### 迁移",
            area,
            re.DOTALL,
        )
        self.assertIsNotNone(extension, "missing zero-area parameter-boundary extension")
        body = extension.group("body")
        for marker in (
            "内部一一正则", "有限接缝重复", "边界退化", "边界遗漏",
            "零面积", "闭子域穷竭", "有限正则片", "连续有界",
            "边界贡献趋于零", "与穷竭无关", "与分片无关",
        ):
            self.assertIn(marker, body)

        sphere = re.search(
            r"### 例 2：球带面积 \{#ex-u-09-38-02-sphere\}"
            r"(?P<body>.*?)\n## 即时检验与回望",
            area,
            re.DOTALL,
        )
        self.assertIsNotNone(sphere)
        for marker in (
            "R>0", "0\\le\\alpha\\le\\beta\\le\\pi", "零面积边界扩展",
            "\\theta=0", "\\theta=2\\pi", "接缝", "极点",
        ):
            self.assertIn(marker, sphere.group("body"))

    def test_spherical_integral_examples_invoke_boundary_extension(self):
        scalar = self.text(path(EXPECTED[2]))
        half_sphere = re.search(
            r"### 例 2：半球上的标量分布 \{#ex-u-09-38-03-sphere\}"
            r"(?P<body>.*?)\n## 即时检验与回望",
            scalar,
            re.DOTALL,
        )
        self.assertIsNotNone(half_sphere)
        for marker in ("R>0", "零面积边界扩展", "接缝", "极点"):
            self.assertIn(marker, half_sphere.group("body"))

        flux = self.text(path(EXPECTED[3]))
        sphere_flux = re.search(
            r"### 例 2：球面径向场 \{#ex-u-09-38-04-sphere\}"
            r"(?P<body>.*?)\n### 例 3",
            flux,
            re.DOTALL,
        )
        self.assertIsNotNone(sphere_flux)
        for marker in ("零面积边界扩展", "接缝", "两个极点"):
            self.assertIn(marker, sphere_flux.group("body"))

    def test_reparameterization_and_orientation_contract(self):
        scalar = self.text(path(EXPECTED[2]))
        flux = self.text(path(EXPECTED[3]))
        for marker in ("合法参数变换", "Jacobian 的绝对值", "不变"):
            self.assertIn(marker, scalar)
        for marker in ("合法参数变换", "Jacobian 的绝对值", "取向符号", "保向", "反向",
                       "取向反转", "变号", "参数范围", "法向"):
            self.assertIn(marker, flux)

    def test_examples_cover_graph_sphere_and_piecewise_surface(self):
        combined = "\n".join(self.text(path(row)) for row in EXPECTED)
        for marker in ("图形曲面", "球面", "分片曲面", "参数范围", "法向"):
            self.assertIn(marker, combined)
        self.assertIn("非零梯度", combined)
        self.assertIn("局部法向", combined)
        self.assertIn("全局可定向", combined)

    def test_piecewise_cylinder_flux_checks_each_patch_orientation(self):
        text = self.text(path(EXPECTED[3]))
        window = re.search(
            r"### 例 3：分片曲面的逐片核验 \{#ex-u-09-38-04-piecewise\}"
            r"(?P<body>.*?)\n## 即时检验与回望",
            text,
            re.DOTALL,
        )
        self.assertIsNotNone(window, "missing anchored piecewise-cylinder example")
        body = window.group("body")
        for marker in (
            "侧面参数化", "0\\le\\theta\\le2\\pi", "0\\le z\\le1",
            "s_\\theta\\times s_z", "(\\cos\\theta,\\sin\\theta,0)",
            "上盘参数化", "0\\le\\rho\\le1", "t_\\rho\\times t_\\theta",
            "下盘参数化", "b_\\theta\\times b_\\rho", "外法向",
            "侧面通量", "上盘通量", "下盘通量",
        ):
            self.assertIn(marker, body)
        self.assertIn("边界曲面", body)
        self.assertIn(r"\partial\{x^2+y^2\le1,\ 0\le z\le1\}", body)

    def test_guide_and_release_surfaces(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
        nav = self.text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-38/", nav)
        self.assertIn("chapters/chapter-41/", nav)
        readme = self.text(ROOT / "README.md")
        self.assertIn("第九部第 41 章，共 186 个学习单元、337 学时", readme)
        course_map = self.text(ROOT / "content" / "course-map.md")
        self.assertIn("第 38 章：参数曲面与曲面积分](chapters/chapter-38/index.md)", course_map)
        self.assertIn("第 39 章：Green 公式与平面场](chapters/chapter-39/index.md)", course_map)

    def test_dependency_map_and_review_record_release_boundary(self):
        dependencies = self.text(ROOT / "docs" / "curriculum" / "part-09-dependencies.md")
        for marker in ("当前发布边界：第 41 章", "第 37–41 章已经发布", "第九部核心正文已全部发布"):
            self.assertIn(marker, dependencies)
        review = self.text(ROOT / "docs" / "reviews" / "2026-07-31-chapter-38-consistency-review.md")
        for marker in ("元数据", "依赖", "取向", "面积元", "重新参数化", "章级测试",
                       "make verify", "check_content.py", "zensical build --strict", "check_site.py",
                       "git diff --check", "通过"):
            self.assertIn(marker, review)


if __name__ == "__main__":
    unittest.main()
