from pathlib import Path
import re
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-09-dependencies.md"
COURSE_MAP = ROOT / "content" / "course-map.md"
APPENDIX = ROOT / "content" / "appendices" / "part-09-differential-forms.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

PART_09_UNITS = [
    ("u-09-37-01", "正则参数曲线怎样描述运动、方向与切向量？", 1.50, 0.00),
    ("u-09-37-02", "弧长与第一类曲线积分怎样由参数化定义？", 1.25, 0.25),
    ("u-09-37-03", "第二类曲线积分怎样表示功与环流？", 1.00, 0.50),
    ("u-09-37-04", "重新参数化、反向与保守场怎样改变积分？", 0.75, 0.75),
    ("u-09-38-01", "正则参数曲面怎样产生切平面、法向量与取向？", 1.50, 0.00),
    ("u-09-38-02", "曲面面积元为什么由叉积的模给出？", 1.25, 0.25),
    ("u-09-38-03", "第一类曲面积分怎样累积曲面上的标量分布？", 1.00, 0.50),
    ("u-09-38-04", "通量积分怎样依赖参数化与曲面取向？", 0.75, 0.75),
    ("u-09-39-01", "平面场的散度与旋度怎样描述局部变化？", 1.50, 0.00),
    ("u-09-39-02", "Green 公式怎样从简单区域上的微积分基本定理得到？", 1.25, 0.25),
    ("u-09-39-03", "分片区域、多连通区域与边界方向怎样处理？", 1.00, 0.50),
    ("u-09-39-04", "Green 公式怎样控制面积、环流、通量与路径无关？", 0.75, 0.75),
    ("u-09-40-01", "三维散度为什么表示局部源汇密度？", 1.50, 0.00),
    ("u-09-40-02", "Gauss 公式为什么先在长方体上成立？", 1.25, 0.25),
    ("u-09-40-03", "规则区域的分片与内部通量为什么会抵消？", 1.00, 0.50),
    ("u-09-40-04", "Gauss 公式怎样分析流量、电通量与奇点？", 0.75, 0.75),
    ("u-09-41-01", "三维旋度为什么表示局部环流密度？", 1.50, 0.00),
    ("u-09-41-02", "曲面取向怎样诱导边界曲线的正方向？", 1.25, 0.25),
    ("u-09-41-03", "Stokes 公式怎样在单个参数曲面片上证明？", 1.25, 0.25),
    ("u-09-41-04", "分片曲面上的内部边界为什么成对抵消？", 1.00, 0.50),
    ("u-09-41-05", "怎样选择并核验 Green、Gauss 与 Stokes 公式？", 1.00, 1.00),
]

CHAPTER_TITLES = ["[第 41 章：Stokes 公式与三大公式的统一](chapters/chapter-41/index.md)"]
UNIT_SLUGS = {
    "u-09-37-01": "regular-parametric-curves",
    "u-09-37-02": "arc-length-scalar-line-integral",
    "u-09-37-03": "work-circulation",
    "u-09-37-04": "reparameterization-conservative-fields",
    "u-09-38-01": "regular-parametric-surfaces",
    "u-09-38-02": "surface-area-element",
    "u-09-38-03": "scalar-surface-integral",
    "u-09-38-04": "flux-integral",
    "u-09-39-01": "planar-divergence-curl",
    "u-09-39-02": "green-theorem",
    "u-09-39-03": "multiply-connected-green",
    "u-09-39-04": "green-applications",
    "u-09-40-01": "spatial-divergence",
    "u-09-40-02": "gauss-box",
    "u-09-40-03": "gauss-piecewise-regions",
    "u-09-40-04": "gauss-applications-singularities",
    "u-09-41-01": "spatial-curl",
    "u-09-41-02": "induced-boundary-orientation",
    "u-09-41-03": "stokes-parametric-patch",
    "u-09-41-04": "stokes-piecewise-surfaces",
    "u-09-41-05": "vector-theorem-selection",
}
PAGE_COUNTS = {
    "u-09-37-01": (8, 10), "u-09-37-02": (9, 11), "u-09-37-03": (9, 11), "u-09-37-04": (10, 12),
    "u-09-38-01": (8, 10), "u-09-38-02": (9, 11), "u-09-38-03": (9, 11), "u-09-38-04": (10, 12),
    "u-09-39-01": (8, 10), "u-09-39-02": (10, 12), "u-09-39-03": (10, 12), "u-09-39-04": (11, 13),
    "u-09-40-01": (8, 10), "u-09-40-02": (10, 12), "u-09-40-03": (10, 12), "u-09-40-04": (11, 13),
    "u-09-41-01": (8, 10), "u-09-41-02": (9, 11), "u-09-41-03": (10, 12), "u-09-41-04": (10, 12), "u-09-41-05": (14, 20),
}


class PartNineConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def dependency_registry(self) -> list[tuple[str, str, float, float]]:
        text = self.required_text(DEPENDENCIES)
        rows = []
        for line in text.splitlines():
            if not line.startswith("| `u-09-"):
                continue
            fields = [field.strip() for field in line.strip("|").split("|")]
            self.assertGreaterEqual(len(fields), 6, f"incomplete registry row: {line}")
            rows.append(
                (fields[0].strip("`"), fields[1], float(fields[2]), float(fields[3]))
            )
            self.assertNotIn("微分形式", line)
        return rows

    def test_dependency_registry_and_actual_totals_are_locked(self) -> None:
        actual = self.dependency_registry()
        self.assertEqual(PART_09_UNITS, actual)
        theory = sum(unit[2] for unit in actual)
        applied = sum(unit[3] for unit in actual)
        self.assertEqual((21, 24.0, 8.0, 32.0), (len(actual), theory, applied, theory + applied))

    def test_blueprint_tracks_current_release_boundary(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 41 章", text)
        self.assertIn("21 个核心单元、32 学时", text)
        chapters = ROOT / "content" / "chapters"
        self.assertIn("chapters/chapter-37/", NAVIGATION)
        self.assertIn("chapters/chapter-38/", NAVIGATION)
        self.assertIn("chapters/chapter-39/", NAVIGATION)
        self.assertIn("chapters/chapter-40/", NAVIGATION)
        self.assertIn("chapters/chapter-41/", NAVIGATION)
        self.assertEqual(4, len(list((chapters / "chapter-37").glob("u-09-*.md"))))
        self.assertEqual(4, len(list((chapters / "chapter-38").glob("u-09-*.md"))))
        self.assertEqual(4, len(list((chapters / "chapter-39").glob("u-09-*.md"))))
        self.assertEqual(4, len(list((chapters / "chapter-40").glob("u-09-*.md"))))
        self.assertEqual(5, len(list((chapters / "chapter-41").glob("u-09-*.md"))))
        self.assertEqual(21, len(list(chapters.rglob("u-09-*.md"))))

    def test_optional_appendix_is_not_core(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("选读附录不计入核心学时", text)

    def test_optional_differential_forms_appendix_is_published_without_hours_metadata(self) -> None:
        text = self.required_text(APPENDIX)
        self.assertEqual(1, NAVIGATION.count("appendices/part-09-differential-forms.md"))
        self.assertNotRegex(text, r"(?m)^hours:")
        for marker in [
            "0-形式", "1-形式", "2-形式", "3-形式", "外微分", "拉回",
            "广义 Stokes", "不证明一般流形上的广义 Stokes 定理",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        self.assertIn("| Green", text)
        self.assertIn("| Gauss", text)
        self.assertIn("| Stokes", text)
        self.assertIn("一般流形", text)
        self.assertIn("切丛", text)
        self.assertIn("上同调", text)
        self.assertIn("完整外代数", text)

    def test_appendix_states_smoothness_contractions_and_euclidean_stokes_scope(self) -> None:
        text = self.required_text(APPENDIX)
        for marker in [
            r"C^k",
            r"C^2",
            "混合偏导交换",
            "有界分片光滑定向区域或曲面",
            "分片光滑且取向相容",
            r"(\iota_F\mathrm{vol})(u,v)=\mathrm{vol}(F,u,v)",
            r"P\,dy\wedge dz+Q\,dz\wedge dx+R\,dx\wedge dy",
            r"F\cdot(u\times v)",
            r"d\alpha=(R_y-Q_z)\,dy\wedge dz+(P_z-R_x)\,dz\wedge dx",
            r"d\beta=(A_x+B_y+C_z)\,dx\wedge dy\wedge dz",
            "足够光滑的 $\\omega$",
            "第 39–41 章",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_course_map_closes_part_nine_before_parts_ten_to_twelve(self) -> None:
        text = self.required_text(COURSE_MAP)
        self.assertIn("第九部已完成核心内容与选读附录的出版闭合", text)
        self.assertIn("第十至十二部继续覆盖", text)
        self.assertNotIn("第九至十二部继续覆盖", text)

    def test_course_map_locks_every_planned_unit(self) -> None:
        text = self.required_text(COURSE_MAP)
        self.assertEqual(1, text.count("[第 37 章：参数曲线与曲线积分](chapters/chapter-37/index.md)"))
        self.assertEqual(1, text.count("[第 38 章：参数曲面与曲面积分](chapters/chapter-38/index.md)"))
        self.assertEqual(1, text.count("[第 39 章：Green 公式与平面场](chapters/chapter-39/index.md)"))
        self.assertEqual(1, text.count("[第 40 章：Gauss 公式与通量](chapters/chapter-40/index.md)"))
        for heading in CHAPTER_TITLES:
            self.assertEqual(1, text.count(heading), heading)
        for unit_id, title, theory, applied in PART_09_UNITS[16:]:
            pattern = (
                rf"^\d+\. \[{re.escape(title)}\]\(chapters/chapter-41/[^)]+\)"
                rf"（理论 {theory:.2f}，应用 {applied:.2f}）$"
            )
            with self.subTest(unit=unit_id):
                self.assertEqual(1, len(re.findall(pattern, text, re.MULTILINE)))
        self.assertIn(
            "### [选读附录：从向量分析到微分形式](appendices/part-09-differential-forms.md)",
            text,
        )
        self.assertIn("第九部共 21 个核心单元、32 学时（理论 24，应用 8）", text)

    def test_every_registry_row_matches_page_guide_course_map_and_nav_once(self) -> None:
        course_map = self.required_text(COURSE_MAP)
        for unit_id, title, theory, applied in PART_09_UNITS:
            chapter = unit_id.split("-")[2]
            filename = f"{unit_id}-{UNIT_SLUGS[unit_id]}.md"
            page = ROOT / "content" / "chapters" / f"chapter-{chapter}" / filename
            metadata = yaml.safe_load(self.required_text(page).split("---\n", 2)[1])
            self.assertEqual((unit_id, title, theory, applied), (
                metadata["unit_id"], metadata["title"],
                float(metadata["hours"]["theory"]), float(metadata["hours"]["applied"]),
            ))
            guide = self.required_text(page.parent / "index.md")
            self.assertEqual(1, guide.count(f"[{title}]({filename})"))
            self.assertEqual(1, NAVIGATION.count(f"chapters/chapter-{chapter}/{filename}"))
            map_line = f"[{title}](chapters/chapter-{chapter}/{filename})（理论 {theory:.2f}，应用 {applied:.2f}）"
            self.assertEqual(1, course_map.count(map_line))

    def test_release_has_exact_core_guides_appendix_and_reviews(self) -> None:
        chapters = ROOT / "content" / "chapters"
        self.assertEqual(21, len(list(chapters.glob("chapter-*/u-09-*.md"))))
        self.assertEqual(5, sum((chapters / f"chapter-{chapter}" / "index.md").is_file() for chapter in range(37, 42)))
        self.assertTrue(APPENDIX.is_file())
        for chapter in range(37, 42):
            self.assertTrue((ROOT / "docs" / "reviews" / f"2026-07-31-chapter-{chapter}-consistency-review.md").is_file())
        review = ROOT / "docs" / "reviews" / "2026-07-31-part-09-consistency-review.md"
        self.assertTrue(review.is_file())

    def test_actual_page_counts_reconcile_with_registry_including_appendix(self) -> None:
        per_page = {}
        for unit_id, *_ in PART_09_UNITS:
            chapter = unit_id.split("-")[2]
            page = ROOT / "content" / "chapters" / f"chapter-{chapter}" / f"{unit_id}-{UNIT_SLUGS[unit_id]}.md"
            text = self.required_text(page)
            actual = (len(re.findall(r"\{#pr-u-09-[^}]+\}", text)), text.count('??? note "答案"'))
            self.assertEqual(PAGE_COUNTS[unit_id], actual, page.name)
            per_page[unit_id] = actual
        appendix = self.required_text(APPENDIX)
        per_page["appendix"] = (
            len(re.findall(r"\{#pr-appendix-part-09-[^}]+\}", appendix)),
            appendix.count('??? note "答案"'),
        )
        core = tuple(sum(per_page[unit_id][i] for unit_id, *_ in PART_09_UNITS) for i in range(2))
        self.assertEqual((201, 247), core)
        self.assertEqual((2, 5), per_page["appendix"])
        published = tuple(sum(values[i] for values in per_page.values()) for i in range(2))
        self.assertEqual((203, 252), published)

    def test_algorithms_have_one_source_one_call_each_and_are_not_certificates(self) -> None:
        source = self.required_text(ROOT / "src" / "mathbook_examples" / "vector_analysis.py")
        call_page = self.required_text(ROOT / "content" / "chapters" / "chapter-41" / "u-09-41-05-vector-theorem-selection.md")
        all_part_text = "\n".join(self.required_text(p) for p in sorted((ROOT / "content").glob("chapters/chapter-*/u-09-*.md")))
        for name in ("composite_midpoint_line_integral", "composite_midpoint_flux_integral"):
            self.assertEqual(1, len(re.findall(rf"^def {name}\(", source, re.MULTILINE)))
            self.assertEqual(1, call_page.count(f"{name}("))
            self.assertEqual(1, all_part_text.count(f"{name}("))
        for marker in ("数值结果不能证明", "不能证明正则性", "不是经过认证的上下界"):
            self.assertIn(marker, call_page)

    def test_historical_chapter_tests_do_not_lock_future_global_release_state(self) -> None:
        for chapter in range(37, 41):
            source = self.required_text(ROOT / "tests" / f"test_chapter_{chapter}.py")
            for global_fact in ("189 个学习单元", "337 学时", "当前发布边界：第 41 章"):
                self.assertNotIn(global_fact, source, f"chapter {chapter} owns a global fact")
            self.assertIn(f"chapter-{chapter}", source)

    def test_final_surfaces_record_release_totals_and_scope(self) -> None:
        readme = self.required_text(ROOT / "README.md")
        course_map = self.required_text(COURSE_MAP)
        dependencies = self.required_text(DEPENDENCIES)
        for text in (readme, course_map):
            self.assertIn("189 个学习单元", text)
            self.assertIn("337 学时", text)
        self.assertIn("第八部 18 个核心单元、32 学时已经历史闭合", readme)
        self.assertIn("第九部 21 个核心单元、32 学时已经完整发布", readme)
        self.assertIn("核心正文共 201 道稳定锚点习题和 247 个折叠答案", dependencies)
        self.assertIn("出版面合计 203 道稳定锚点练习和 252 个折叠答案", dependencies)
        self.assertIn("不自动形成数学证书", dependencies)

    def test_surface_area_cross_product_expansion_is_mobile_compact(self) -> None:
        text = self.required_text(
            ROOT / "content" / "chapters" / "chapter-38" / "u-09-38-02-surface-area-element.md"
        )
        self.assertIn(r"X_j:=Ae_j+\eta_j", text)
        self.assertIn(r"\Delta_T:=X_1\times X_2-Ae_1\times Ae_2", text)


if __name__ == "__main__":
    unittest.main()
