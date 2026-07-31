import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "content" / "chapters"
MATRIX = ROOT / "docs" / "reviews" / "2026-07-31-parts-01-09-interface-matrix.md"

# Stable chapter-level witnesses selected from actual prerequisites.book declarations.
# These are deliberately semantic witnesses, not a brittle equality check over prose.
CHAPTER_CONTRACT = {
    1: (), 2: (), 3: ("chapter-02",), 4: ("chapter-03",),
    5: ("chapter-04",), 6: ("chapter-05",), 7: ("chapter-03", "chapter-05"),
    8: ("chapter-05", "chapter-07"), 9: ("chapter-05",), 10: ("chapter-09",),
    11: ("u-02-08-02", "u-03-10-01"), 12: ("u-02-07-03", "u-03-10-01"),
    13: ("u-03-09-02", "u-03-10-01"), 14: ("u-04-13-03",),
    15: ("u-03-11-02", "u-04-13-02"), 16: ("u-04-14-04", "u-04-15-01"),
    17: ("u-04-15-02", "u-04-16-02"), 18: ("u-04-14-05",),
    19: ("u-01-03-02", "u-02-05-02"), 20: ("u-05-19-04",),
    21: ("u-05-19-04", "u-05-20-03"), 22: ("u-05-19-04", "u-05-20-03"),
    23: ("数列极限",), 24: ("Cauchy 尾部",), 25: ("上确界", "一致收敛"),
    26: ("根值判别", "上极限"), 27: ("一致连续", "一致收敛"),
    28: ("邻域",), 29: ("Fréchet 微分", "多元极限与连续"),
    30: ("Fréchet 微分", "链式法则"), 31: ("Fréchet 微分", "Jacobian"),
    32: ("紧致性", "隐函数定理"), 33: ("Riemann 积分", "紧致性"),
    34: ("一元 Riemann 积分",), 35: ("Fréchet 微分", "Jacobian"),
    36: ("反常积分", "累次积分"), 37: ("Riemann 积分", "向量函数微分"),
    38: ("局部参数化", "叉积"), 39: ("Jacobian", "u-09-37-03"),
    40: ("u-09-38-04", "u-09-39-01"), 41: ("u-09-37-03", "u-09-38-01"),
}

# One semantic token per required interface field, for every chapter.  This
# makes the matrix an executable chapter contract rather than a row-count test.
FIELD_CONTRACT = {
    1: ("集合", "无", "第 2–41 章", "公理集合论", "\\forall"),
    2: ("Dedekind", "无", "第 3、5、7 章", "Cauchy 列", "\\mathbb R"),
    3: ("确界原理", "chapter-02", "第 5、7、19、25、28 章", "数列极限", "\\sup"),
    4: ("区间套", "chapter-03", "第 5、7、12 章", "介值定理", "误差预算"),
    5: ("epsilon-N", "chapter-04", "第 6–9、23、25 章", "数值稳定", "\\varepsilon"),
    6: ("极限代数", "chapter-05", "第 8、9、19、23 章", "无条件交换", "夹逼"),
    7: ("单调收敛", "chapter-03", "第 8、11、12 章", "介值定理", "单调有界"),
    8: ("Cauchy", "chapter-05", "第 11、12、26、28、31 章", "函数连续性", "\\limsup"),
    9: ("函数极限", "chapter-05", "第 10、13 章", "导数", "\\delta"),
    10: ("连续性", "chapter-09", "第 11、12、15、19、25、28 章", "闭区间整体定理", "间断"),
    11: ("闭区间", "u-02-08-02", "第 12、15、19、28 章", "开覆盖紧致性", "Heine–Cantor"),
    12: ("三类求根证书", "u-02-07-03", "第 17、31 章", "Newton", "IVT"),
    13: ("局部线性化", "u-03-09-02", "第 14–18、29 章", "导数法则反证", "o(h)"),
    14: ("求导", "u-04-13-03", "第 15–18、29–31 章", "隐函数定理", "链式法则"),
    15: ("中值定理", "u-03-11-02", "第 16–19、30 章", "数值图像", "Rolle"),
    16: ("Taylor", "u-04-14-04", "第 17、22、26、30 章", "无穷级数", "余项"),
    17: ("凸性", "u-04-15-02", "第 18、31、32 章", "KKT", "Newton"),
    18: ("原函数", "u-04-14-05", "第 20–22 章", "Riemann 积分", "分部积分"),
    19: ("Darboux", "u-01-03-02", "第 20、22、33、34、37 章", "基本定理定义积分", "Riemann 和"),
    20: ("微积分基本定理", "u-05-19-04", "第 21、22、34、39、40 章", "数值求积", "Newton–Leibniz"),
    21: ("面积", "u-05-19-04", "第 33、36–38 章", "重积分", "弧长"),
    22: ("反常积分", "u-05-19-04", "第 23、26、36 章", "网格误差", "Simpson"),
    23: ("数项级数", "数列极限", "第 24–26 章", "符号抵消", "部分和"),
    24: ("一般项级数", "Cauchy 尾部", "第 25、26 章", "条件收敛当绝对", "Dirichlet"),
    25: ("一致收敛", "上确界", "第 26、27 章", "不反向依赖", "M 判别"),
    26: ("收敛半径", "根值判别", "可选解析对照", "端点须另判", "Cauchy–Hadamard"),
    27: ("多项式逼近", "一致连续", "后续数值分析", "网格最大误差", "Bernstein"),
    28: ("Euclid", "邻域", "第 29、32–35 章", "一般拓扑", "Heine–Borel"),
    29: ("Fréchet", "多元极限与连续", "第 31、35、38 章", "偏导存在不推出可微", "Jacobian"),
    30: ("高阶 Fréchet", "链式法则", "第 31、32 章", "全局误差", "Hessian"),
    31: ("反函数", "Jacobian", "第 32、35、38 章", "局部而非全局", "IFT"),
    32: ("Lagrange", "紧致性", "后续应用", "KKT", "约束资格"),
    33: ("Riemann 重积分", "Riemann 积分", "第 34–41 章", "Lebesgue", "矩形分割"),
    34: ("累次积分", "一元 Riemann 积分", "第 35–41 章", "换序前先合法化", "换序"),
    35: ("变量代换", "Fréchet 微分", "第 36–41 章", "非退化", "Jacobian 行列式"),
    36: ("反常重积分", "反常积分", "第 40 章", "截断数值", "概率密度"),
    37: ("参数曲线", "Riemann 积分", "第 39–41 章", "先定义再应用", "ds"),
    38: ("参数曲面", "局部参数化", "第 39–41 章", "测度论", "dS"),
    39: ("Green", "u-09-37-03", "第 41 章", "先简单区域", "正向边界"),
    40: ("Gauss", "u-09-38-04", "第 41 章", "不依赖第 41 章", "外法向"),
    41: ("Stokes", "u-09-37-03", "后续物理/几何", "微分形式", "右手规则"),
}

DIRECT_PREREQUISITES = {
    1: set(), 2: {1}, 3: {2}, 4: {3}, 5: {3, 4}, 6: {5},
    7: {3, 5}, 8: {3, 5, 6, 7}, 9: {1, 3, 5, 6}, 10: {9},
    11: {8, 10}, 12: {7, 8, 10}, 13: {9, 10}, 14: {10, 13},
    15: {11, 13, 14}, 16: {13, 14, 15}, 17: {12, 14, 15, 16},
    18: {14, 15, 17}, 19: {3, 5, 6, 10, 11}, 20: {10, 13, 18, 19},
    21: {14, 19, 20}, 22: {5, 6, 15, 16, 19, 20},
    23: {5, 6, 8, 19}, 24: {23}, 25: {3, 5, 10, 11, 19, 20, 24},
    26: {8, 16, 24, 25}, 27: {10, 11, 25},
    28: {3, 5, 8, 9, 10, 11}, 29: {13, 14, 28},
    30: {14, 16, 29}, 31: {8, 12, 14, 17, 29, 30},
    32: {11, 15, 17, 28, 29, 30, 31},
    33: {3, 5, 10, 11, 19, 28}, 34: {19, 20, 33},
    35: {29, 31, 33, 34}, 36: {21, 22, 33, 34, 35},
    37: {19, 29}, 38: {29, 31, 33, 34, 35},
    39: {20, 29, 34, 37}, 40: {20, 34, 36, 38, 39},
    41: {29, 37, 38, 39, 40},
}

BACKGROUND_INTERFACES = {
    n: ({"bg-algebra", "bg-geometry", "bg-python"}
        - ({"bg-python"} if n in {1, 2, 3, 9, 10, 11, 28, 30, 33, 35, 37, 38, 39, 40} else set())
        - ({"bg-geometry"} if n in {2, 3, 4, 5, 6} else set())
        - ({"bg-algebra"} if n in {33, 34, 36} else set()))
    for n in range(1, 42)
}

PREREQUISITE_NAME_MAP = {
    "数列极限": 5, "上确界": 3, "一致连续": 11, "Riemann 积分": 19,
    "微积分基本定理": 20, "Fréchet 微分": 29, "Jacobian": 29,
    "反函数定理": 31, "隐函数定理": 31, "累次积分": 34,
}


def metadata(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---\n", 2)[1])


def matrix_rows() -> list[list[str]]:
    text = MATRIX.read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if re.match(r"^\|\s*\d+\s*\|", line):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def chapter_slice(course_map: str, chapter: int) -> str:
    start = course_map.index(f"{{#chapter-{chapter:02d}}}")
    if chapter == 41:
        return course_map[start:]
    end = course_map.index(f"{{#chapter-{chapter + 1:02d}}}", start)
    return course_map[start:end]


class Parts0109CrossConsistencyTests(unittest.TestCase):
    def test_chapter_26_output_is_optional_context_for_chapter_27(self):
        rows = {int(row[0]): row for row in matrix_rows()}
        self.assertIn("可选解析对照", rows[26][5])
        self.assertNotIn("→ 第 27 章", rows[26][5])
        self.assertEqual({10, 11, 25}, DIRECT_PREREQUISITES[27])

    def test_matrix_covers_each_real_chapter_once_with_complete_contract_fields(self):
        guides = sorted(CHAPTERS.glob("chapter-*/index.md"))
        self.assertEqual(41, len(guides))
        rows = matrix_rows()
        self.assertEqual(list(range(1, 42)), [int(row[0]) for row in rows])
        self.assertTrue(all(len(row) == 9 for row in rows))
        for row in rows:
            self.assertTrue(all(row[i] and row[i] != "—" for i in range(2, 7)), row)

    def test_every_matrix_row_satisfies_its_semantic_contract_and_cites_evidence(self):
        rows = {int(row[0]): row for row in matrix_rows()}
        for chapter, tokens in FIELD_CONTRACT.items():
            for column, token in zip((2, 5, 6, 7), (tokens[0], tokens[2], tokens[3], tokens[4])):
                self.assertIn(token, rows[chapter][column], f"chapter {chapter}, column {column}")
            evidence = rows[chapter][8]
            self.assertIn(f"chapter-{chapter:02d}/index.md", evidence)
            self.assertRegex(evidence, r"docs/(curriculum|superpowers/specs)/")

    def test_real_core_pages_ids_counts_and_publication_order_match_matrix(self):
        pages = sorted(CHAPTERS.glob("chapter-*/u-*.md"))
        ids = [metadata(page)["unit_id"] for page in pages]
        # Parse every physical core-unit front matter; appendices live outside
        # chapter directories and are deliberately excluded from this inventory.
        self.assertEqual(189, len(pages))
        self.assertEqual(189, len(set(ids)))
        total_hours = sum(sum(metadata(page)["hours"].values()) for page in pages)
        self.assertEqual(337, total_hours)
        part_ranges = ((1, 4), (5, 8), (9, 12), (13, 17), (18, 22),
                       (23, 27), (28, 32), (33, 36), (37, 41))
        self.assertEqual([14, 21, 20, 21, 25, 24, 25, 18, 21], [
            sum(len(list((CHAPTERS / f"chapter-{n:02d}").glob("u-*.md"))) for n in range(a, b + 1))
            for a, b in part_ranges
        ])
        self.assertIn("189 个学习单元、337 学时", (ROOT / "README.md").read_text(encoding="utf-8"))

        matrix_order = [int(row[0]) for row in matrix_rows()]
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        map_order = [int(n) for n in re.findall(r"\{#chapter-(\d{2})\}", course_map)]
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        nav_order = [int(n) for n in re.findall(r"chapters/chapter-(\d{2})/index\.md", nav)]
        self.assertEqual(matrix_order, map_order)
        self.assertEqual(matrix_order, nav_order)

    def test_guides_physical_pages_course_map_and_nav_have_identical_unit_routes(self):
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for chapter in range(1, 42):
            directory = CHAPTERS / f"chapter-{chapter:02d}"
            guide = (directory / "index.md").read_text(encoding="utf-8")
            guide_routes = re.findall(r"\]\((u-[^)]+\.md)\)", guide)
            physical = [page.name for page in sorted(directory.glob("u-*.md"))]
            map_routes = [Path(route).name for route in re.findall(
                rf"\]\(chapters/chapter-{chapter:02d}/(u-[^)]+\.md)\)", course_map
            )]
            nav_routes = [Path(route).name for route in re.findall(
                rf"chapters/chapter-{chapter:02d}/(u-[^\s]+\.md)", nav
            )]
            self.assertEqual(set(physical), set(guide_routes), f"chapter {chapter} guide inventory")
            self.assertEqual(guide_routes, map_routes, f"chapter {chapter} course map order")
            self.assertEqual(guide_routes, nav_routes, f"chapter {chapter} nav order")
            section = chapter_slice(course_map, chapter)
            for route in guide_routes:
                unit = metadata(directory / route)
                expected = f"[{unit['title']}](chapters/chapter-{chapter:02d}/{route})"
                self.assertIn(expected, section)
            chapter_hours = sum(sum(metadata(directory / route)["hours"].values()) for route in guide_routes)
            self.assertRegex(section, rf"本章学时：{chapter_hours:g} 小时")

    def test_chapter_hour_check_is_scoped_and_rejects_neighbor_substitution(self):
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        chapter_19 = chapter_slice(course_map, 19)
        self.assertIn("本章学时：7.5 小时", chapter_19)
        mutated = course_map.replace(chapter_19, chapter_19.replace("本章学时：7.5 小时", "本章学时：8 小时"))
        self.assertNotIn("本章学时：7.5 小时", chapter_slice(mutated, 19))

    def test_current_publication_surfaces_use_authoritative_189_total(self):
        surfaces = (
            ROOT / "README.md",
            ROOT / "content" / "course-map.md",
            ROOT / "docs" / "curriculum" / "part-09-dependencies.md",
            ROOT / "docs" / "reviews" / "2026-07-31-part-09-consistency-review.md",
            MATRIX,
        )
        for surface in surfaces:
            text = surface.read_text(encoding="utf-8")
            self.assertIn("189", text, surface)
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        self.assertIn("当前已完整发布第一至第九部", course_map)
        self.assertNotIn("当前已完整发布第一至第八部", course_map)

    def test_historical_release_snapshots_match_physical_chapter_totals(self):
        through_27 = list(CHAPTERS.glob("chapter-[01][0-9]/u-*.md"))
        through_27 += list(CHAPTERS.glob("chapter-2[0-7]/u-*.md"))
        through_32 = through_27 + list(CHAPTERS.glob("chapter-2[89]/u-*.md"))
        through_32 += list(CHAPTERS.glob("chapter-3[0-2]/u-*.md"))
        self.assertEqual(125, len(through_27))
        self.assertEqual(150, len(through_32))

        surfaces_125 = (
            ROOT / "README.md",
            ROOT / "content" / "course-map.md",
            ROOT / "docs" / "curriculum" / "part-06-dependencies.md",
            ROOT / "docs" / "superpowers" / "specs" / "2026-07-30-part-06-series-approximation-design.md",
            ROOT / "docs" / "reviews" / "2026-07-30-part-06-consistency-review.md",
            ROOT / "docs" / "reviews" / "2026-07-30-chapter-27-consistency-review.md",
        )
        surfaces_150 = (
            ROOT / "README.md",
            ROOT / "content" / "course-map.md",
            ROOT / "docs" / "curriculum" / "part-07-dependencies.md",
            ROOT / "docs" / "superpowers" / "specs" / "2026-07-31-part-07-multivariable-differentiation-design.md",
            ROOT / "docs" / "reviews" / "2026-07-31-part-07-consistency-review.md",
            ROOT / "docs" / "reviews" / "2026-07-31-chapter-32-consistency-review.md",
        )
        for surface in surfaces_125:
            self.assertIn("125 个学习单元", surface.read_text(encoding="utf-8"), surface)
        for surface in surfaces_150:
            self.assertIn("150 个学习单元", surface.read_text(encoding="utf-8"), surface)

    def test_chapter_contract_witnesses_are_declared_and_recorded(self):
        rows = {int(row[0]): row for row in matrix_rows()}
        for chapter, witnesses in CHAPTER_CONTRACT.items():
            declared = []
            for page in (CHAPTERS / f"chapter-{chapter:02d}").glob("u-*.md"):
                declared.extend(str(x) for x in metadata(page)["prerequisites"]["book"])
            if not witnesses:
                self.assertFalse(declared, f"chapter {chapter} unexpectedly declares book prerequisites")
            for witness in witnesses:
                self.assertIn(witness, declared, f"chapter {chapter}: registry drift")

    def test_direct_prerequisites_and_background_interfaces_are_exact(self):
        rows = {int(row[0]): row for row in matrix_rows()}
        for chapter in range(1, 42):
            direct = {int(n) for n in re.findall(r"`ch-(\d{2})`", rows[chapter][3])}
            background = set(re.findall(r"`(bg-[a-z]+)`", rows[chapter][4]))
            self.assertEqual(DIRECT_PREREQUISITES[chapter], direct, f"chapter {chapter} direct")
            self.assertEqual(BACKGROUND_INTERFACES[chapter], background, f"chapter {chapter} background")
            declared_background = set()
            for page in (CHAPTERS / f"chapter-{chapter:02d}").glob("u-*.md"):
                prerequisites = metadata(page)["prerequisites"]
                for key, tag in (("higher_algebra", "bg-algebra"),
                                 ("analytic_geometry", "bg-geometry"), ("python", "bg-python")):
                    if prerequisites[key]:
                        declared_background.add(tag)
            self.assertEqual(BACKGROUND_INTERFACES[chapter], declared_background)
        self.assertEqual(19, PREREQUISITE_NAME_MAP["Riemann 积分"])
        self.assertEqual(29, PREREQUISITE_NAME_MAP["Jacobian"])

    def test_locked_cross_part_interfaces_and_boundaries(self):
        rows = {int(row[0]): row for row in matrix_rows()}
        self.assertIn("第 5、7、19、25、28 章", rows[3][5])
        self.assertIn("第 12、15、19、28 章", rows[11][5])
        self.assertIn("第 20、22、33、34、37 章", rows[19][5])
        self.assertIn("第 26、27 章", rows[25][5])
        self.assertTrue({26, 27}.isdisjoint(DIRECT_PREREQUISITES[25]))
        self.assertIn("第 31、35、38 章", rows[29][5])
        self.assertEqual({19, 29}, DIRECT_PREREQUISITES[37])
        self.assertNotIn(38, DIRECT_PREREQUISITES[39])
        self.assertTrue({20, 29, 34, 37}.issubset(DIRECT_PREREQUISITES[39]))
        self.assertIn(39, DIRECT_PREREQUISITES[41])
        self.assertNotIn(41, DIRECT_PREREQUISITES[40])

        text = MATRIX.read_text(encoding="utf-8")
        self.assertIn("附录不作为任何核心章节或单元的前置", text)
        self.assertNotRegex(text, r"第\s*42\s*章|chapter-42|u-\d{2}-42-")


if __name__ == "__main__":
    unittest.main()
