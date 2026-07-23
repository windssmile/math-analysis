"""Regression tests for the complete Chapter 9 function-limit foundation."""

from __future__ import annotations

from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
QUARTO = ROOT / "_quarto.yml"
CHAPTER = ROOT / "book" / "part-03" / "chapter-09"

EXPECTED = (
    (
        "u-03-09-01",
        "函数在一点附近意味着什么？",
        1.50,
        0.50,
        "book/part-03/chapter-09/u-03-09-01-local-neighborhoods.qmd",
    ),
    (
        "u-03-09-02",
        "“任意接近”怎样定义函数极限？",
        1.75,
        0.25,
        "book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.qmd",
    ),
    (
        "u-03-09-05",
        "极限证明怎样从目标误差反推局部范围？",
        1.50,
        0.50,
        "book/part-03/chapter-09/u-03-09-05-epsilon-delta-workshop.qmd",
    ),
    (
        "u-03-09-06",
        "左右极限怎样共同决定双侧极限？",
        1.50,
        0.50,
        "book/part-03/chapter-09/u-03-09-06-one-sided-limits.qmd",
    ),
    (
        "u-03-09-07",
        "函数怎样在有限点附近趋于无穷？",
        1.75,
        0.25,
        "book/part-03/chapter-09/u-03-09-07-infinite-limits-at-point.qmd",
    ),
    (
        "u-03-09-08",
        "自变量趋于无穷时怎样定义函数极限？",
        1.50,
        0.50,
        "book/part-03/chapter-09/u-03-09-08-limits-at-infinity.qmd",
    ),
    (
        "u-03-09-03",
        "局部估计怎样传递极限？",
        1.75,
        0.25,
        "book/part-03/chapter-09/u-03-09-03-function-limit-laws.qmd",
    ),
    (
        "u-03-09-04",
        "用点列靠近能否判别函数极限？",
        1.75,
        0.25,
        "book/part-03/chapter-09/u-03-09-04-sequential-function-limits.qmd",
    ),
)

EXPECTED_METADATA = {
    "u-03-09-01": (
        2,
        ["chapter-01", "chapter-03"],
        ["绝对值与不等式"],
        ["实轴上的区间"],
    ),
    "u-03-09-02": (
        3,
        ["chapter-05", "chapter-09"],
        ["绝对值不等式"],
        ["实轴距离"],
    ),
    "u-03-09-05": (
        3,
        ["chapter-09"],
        ["因式分解", "根式与分式恒等变形", "绝对值不等式"],
        ["实轴距离"],
    ),
    "u-03-09-06": (
        3,
        ["chapter-09"],
        ["分段函数与不等式"],
        ["实轴上的半区间"],
    ),
    "u-03-09-07": (
        3,
        ["chapter-05", "chapter-09"],
        ["绝对值不等式", "倒数不等式"],
        ["实轴距离"],
    ),
    "u-03-09-08": (
        3,
        ["chapter-05", "chapter-09"],
        ["多项式与有理式", "绝对值不等式"],
        ["实轴上的射线"],
    ),
    "u-03-09-03": (
        4,
        ["chapter-06", "chapter-09"],
        ["分式运算", "绝对值不等式"],
        ["实轴距离"],
    ),
    "u-03-09-04": (
        4,
        ["chapter-08", "chapter-09"],
        ["量词否定"],
        ["实轴距离"],
    ),
}


class Chapter09Tests(unittest.TestCase):
    def chapter_units(self) -> list[dict]:
        with UNITS.open("rb") as handle:
            units = tomllib.load(handle)["units"]
        return [unit for unit in units if unit["chapter_id"] == "chapter-09"]

    def read_page(self, relative_path: str) -> str:
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"missing Chapter 9 page: {relative_path}")
        return path.read_text(encoding="utf-8")

    def test_registry_closes_exact_hours_paths_and_reading_order(self) -> None:
        chapter_units = self.chapter_units()
        self.assertEqual(
            [unit["id"] for unit in chapter_units],
            [row[0] for row in EXPECTED],
        )
        for unit, (unit_id, title, theory, applied, path) in zip(
            chapter_units, EXPECTED, strict=True
        ):
            with self.subTest(unit_id=unit_id):
                self.assertEqual(unit["id"], unit_id)
                self.assertEqual(unit["title"], title)
                self.assertEqual(
                    (unit["theory_hours"], unit["applied_hours"]),
                    (theory, applied),
                )
                self.assertEqual(unit["path"], path)
                self.assertEqual(unit["content_standard"], 2)
        self.assertEqual(sum(unit["theory_hours"] for unit in chapter_units), 13.0)
        self.assertEqual(sum(unit["applied_hours"] for unit in chapter_units), 3.0)

    def test_registry_prerequisites_and_capabilities_are_concrete(self) -> None:
        by_id = {unit["id"]: unit for unit in self.chapter_units()}
        for unit_id, (
            difficulty,
            book_prerequisites,
            algebra_prerequisites,
            geometry_prerequisites,
        ) in EXPECTED_METADATA.items():
            with self.subTest(unit_id=unit_id):
                self.assertIn(unit_id, by_id)
                unit = by_id[unit_id]
                self.assertEqual(unit["difficulty"], difficulty)
                self.assertEqual(unit["book_prerequisites"], book_prerequisites)
                self.assertEqual(
                    unit["higher_algebra_prerequisites"], algebra_prerequisites
                )
                self.assertEqual(
                    unit["analytic_geometry_prerequisites"],
                    geometry_prerequisites,
                )
                self.assertIn("concepts", unit["capabilities"])
                self.assertIn("proof", unit["capabilities"])
                self.assertIn("mathematical_expression", unit["capabilities"])
                self.assertGreaterEqual(len(unit["learning_goals"]), 3)

    def test_quarto_registers_exact_render_and_sidebar_order(self) -> None:
        config = QUARTO.read_text(encoding="utf-8")
        expected_paths = [row[4] for row in EXPECTED]
        render_paths = [
            line.strip().removeprefix("- ")
            for line in config.splitlines()
            if line.strip().startswith("- book/part-03/chapter-09/")
        ]
        self.assertEqual(render_paths, expected_paths)

        sidebar_items = re.findall(
            r'^\s+- text: "([^"]+)"\n'
            r"\s+href: (book/part-03/chapter-09/[^\n]+)$",
            config,
            flags=re.MULTILINE,
        )
        self.assertEqual(
            sidebar_items,
            [
                (f"9.{index} {title}", path)
                for index, (_, title, _, _, path) in enumerate(EXPECTED, start=1)
            ],
        )

    def test_all_pages_keep_the_complete_self_study_structure(self) -> None:
        required_headings = [
            "## 先备知识",
            "## 学习目标",
            "## 牵引问题",
            "## 探索与猜想",
            "## 概念与理论",
            "## 例题与迁移",
            "## 即时检验与回望",
            "## 习题与答案",
            "## 常见误区与后续",
        ]
        by_id = {unit["id"]: unit for unit in self.chapter_units()}
        for unit_id, title, _, _, relative_path in EXPECTED:
            with self.subTest(unit_id=unit_id):
                content = self.read_page(relative_path)
                lines = content.splitlines()
                self.assertEqual(lines[0], f"# {title} {{#{unit_id}}}")
                self.assertIn("::: {.unit-meta}", content)
                self.assertTrue(
                    all(heading in lines for heading in required_headings),
                    f"{unit_id} is missing one or more required headings",
                )
                heading_positions = [lines.index(heading) for heading in required_headings]
                self.assertEqual(heading_positions, sorted(heading_positions))
                self.assertGreaterEqual(
                    len(
                        re.findall(
                            rf"^### .+ \{{#ex-{re.escape(unit_id)}-[^}}]+\}}$",
                            content,
                            flags=re.MULTILINE,
                        )
                    ),
                    2,
                )
                self.assertGreaterEqual(
                    len(
                        re.findall(
                            rf"^### .+ \{{#pr-{re.escape(unit_id)}-[^}}]+\}}$",
                            content,
                            flags=re.MULTILINE,
                        )
                    ),
                    5,
                )
                self.assertGreaterEqual(
                    len(re.findall(r"^### 即时检验 [12]：", content, re.MULTILINE)),
                    2,
                )
                self.assertGreaterEqual(
                    content.count('::: {.callout-note collapse="true"}'),
                    7,
                )
                unit = by_id[unit_id]
                for prerequisite in (
                    unit["higher_algebra_prerequisites"]
                    + unit["analytic_geometry_prerequisites"]
                ):
                    self.assertIn(prerequisite, content)

    def test_local_neighborhoods_define_domain_relative_approach(self) -> None:
        content = self.read_page(EXPECTED[0][4])
        for marker in (
            "{#def-u-03-09-01-accumulation-point}",
            "{#def-u-03-09-01-neighborhood}",
            "{#def-u-03-09-01-deleted-neighborhood}",
            "左邻域",
            "右邻域",
            r"D\cap N_r^*(a)",
            "定义域的聚点",
            "端点",
            r"f(a)",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        self.assertIn("有限采样", content)
        self.assertIn("不能替代证明", content)
        self.assertIn(
            "### 定义：相对定义域与单侧邻域 "
            "{#def-u-03-09-01-deleted-neighborhood}",
            content,
        )
        self.assertNotIn("保留旧的稳定锚点", content)
        self.assertIn("第 3 章", content)

    def test_epsilon_delta_definition_and_uniqueness_fix_all_quantifiers(self) -> None:
        content = self.read_page(EXPECTED[1][4])
        for marker in (
            "{#def-u-03-09-02-function-limit}",
            "{#thm-u-03-09-02-uniqueness}",
            r"\forall\varepsilon>0\;\exists\delta>0\;\forall x\in D",
            r"0<|x-a|<\delta",
            r"|f(x)-L|<\varepsilon",
            r"\varepsilon=\frac{|L_1-L_2|}{3}",
            r"\delta=\min\{\delta_1,\delta_2\}",
            "聚点",
            "去心",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_workshop_runs_backward_design_then_forward_verification(self) -> None:
        content = self.read_page(EXPECTED[2][4])
        for marker in (
            "{#def-u-03-09-05-proof-certificate}",
            "{#ex-u-03-09-05-linear}",
            "{#ex-u-03-09-05-quadratic}",
            "反向设计",
            "正向验证",
            r"|x-a|<1",
            r"C>0",
            "根式",
            "有理式",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_one_sided_limits_prove_the_two_sided_criterion(self) -> None:
        content = self.read_page(EXPECTED[3][4])
        for marker in (
            "{#def-u-03-09-06-left-limit}",
            "{#def-u-03-09-06-right-limit}",
            "{#thm-u-03-09-06-two-sided-criterion}",
            r"a-\delta<x<a",
            r"a<x<a+\delta",
            r"\delta=\min\{\delta_-,\delta_+\}",
            r"D=[a,b],\qquad a<b",
            "当且仅当",
            "端点",
            "分段函数",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        exercise = content.split(
            "### 习题 2：由两侧证书合并双侧证书",
            1,
        )[1].split("### 习题 3：", 1)[0]
        self.assertIn(r"f:D\to\mathbb R", exercise)
        necessity = content.split("**必要性。**", 1)[1].split("**充分性。**", 1)[0]
        self.assertIn(
            r"若 \(x\in D\) 且 \(a-\delta<x<a\)",
            necessity,
        )
        self.assertIn(
            r"若 \(x\in D\) 且 \(a<x<a+\delta\)",
            necessity,
        )

    def test_infinite_limits_at_a_point_use_m_quantifiers_and_side_data(self) -> None:
        content = self.read_page(EXPECTED[4][4])
        for marker in (
            "{#def-u-03-09-07-positive-infinite-limit}",
            "{#def-u-03-09-07-negative-infinite-limit}",
            r"\forall M>0\;\exists\delta>0\;\forall x\in D",
            r"a\in\mathbb R",
            r"f(x)>M",
            r"f(x)<-M",
            r"\lim_{x\to0^+}\frac1x=+\infty",
            r"\lim_{x\to0^-}\frac1x=-\infty",
            r"\lim_{x\to0}\frac1{x^2}=+\infty",
            "竖直渐近线",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        self.assertIn("不是实数", content)

        one_sided = content.split(
            "{#def-u-03-09-07-one-sided-infinite-limits}",
            1,
        )[1].split(
            "{#thm-u-03-09-07-two-sided-criterion}",
            1,
        )[0]
        for marker in (
            "{#def-u-03-09-07-right-positive-infinite-limit}",
            "{#def-u-03-09-07-right-negative-infinite-limit}",
            "{#def-u-03-09-07-left-positive-infinite-limit}",
            "{#def-u-03-09-07-left-negative-infinite-limit}",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, one_sided)
        self.assertEqual(
            4,
            one_sided.count(
                r"\forall M>0\;\exists\delta>0\;\forall x\in D"
            ),
        )

        necessity = content.split("**证明。**", 1)[1].split("反过来", 1)[0]
        self.assertIn(
            r"任取 \(x\in D\)。若 \(0<x-a<\delta\)",
            necessity,
        )
        self.assertIn(
            r"若 \(0<a-x<\delta\)",
            necessity,
        )
        negative_necessity = content.split(
            "对负无穷，若双侧极限为",
            1,
        )[1].split("反之", 1)[0]
        self.assertIn(r"任取 \(x\in D\)", negative_necessity)
        self.assertIn("- **Python 先备：** 无", content)

    def test_limits_at_infinity_cover_all_approach_and_target_types(self) -> None:
        content = self.read_page(EXPECTED[5][4])
        for marker in (
            "{#def-u-03-09-08-finite-limit-at-infinity}",
            "{#def-u-03-09-08-infinite-limit-at-infinity}",
            r"x\to+\infty",
            r"x\to-\infty",
            r"f(x)\to+\infty",
            r"f(x)\to-\infty",
            r"\forall\varepsilon>0\;\exists R>0\;\forall x\in D",
            r"\forall M>0\;\exists R>0\;\forall x\in D",
            "水平",
            "有理函数",
            "增长",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        self.assertIn("不是实数", content)
        self.assertIn("- **Python 先备：** 无", content)

    def test_limit_laws_prove_local_hypotheses_before_algebra(self) -> None:
        content = self.read_page(EXPECTED[6][4])
        for marker in (
            "{#lem-u-03-09-03-local-boundedness}",
            "{#lem-u-03-09-03-eventual-sign}",
            "{#thm-u-03-09-03-order}",
            "{#thm-u-03-09-03-squeeze}",
            "{#thm-u-03-09-03-sum-product}",
            "{#thm-u-03-09-03-quotient}",
            "{#thm-u-03-09-03-composition}",
            r"|g(x)|\ge\frac{|B|}{2}",
            "定义域",
            "未定式",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

        order_section = content.split(
            "{#thm-u-03-09-03-order}",
            1,
        )[1].split("{#thm-u-03-09-03-squeeze}", 1)[0]
        self.assertIn(r"f,g:D\to\mathbb R", order_section)
        self.assertIn(
            r"\delta=\min\{\delta_0,\delta_f,\delta_g\}",
            order_section,
        )
        self.assertIn("由聚点条件选取", order_section)

        squeeze_section = content.split(
            "{#thm-u-03-09-03-squeeze}",
            1,
        )[1].split("{#thm-u-03-09-03-sum-product}", 1)[0]
        self.assertIn(r"p,h,q:D\to\mathbb R", squeeze_section)

        composition_exercise = content.split(
            "{#pr-u-03-09-03-composition-boundary}",
            1,
        )[1].split("## 常见误区与后续", 1)[0]
        for marker in (
            r"D=E=\mathbb R",
            r"a=0",
            r"\lim_{\substack{x\to0\\x\in D}}f(x)=0",
            r"\lim_{\substack{y\to0\\y\in E}}g(y)=0",
            r"\lim_{\substack{x\to0\\x\in D}}g(f(x))=1",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, composition_exercise)

    def test_heine_criterion_proves_both_directions_from_the_definition(self) -> None:
        content = self.read_page(EXPECTED[7][4])
        for marker in (
            "{#thm-u-03-09-04-sequential-criterion}",
            "充分性",
            "必要性",
            r"\exists\varepsilon_0>0\;\forall\delta>0\;\exists x\in D",
            r"0<|x_n-a|<\frac1n",
            r"|f(x_n)-L|\ge\varepsilon_0",
            "反例",
            "等价判别",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_chapter_avoids_calculus_dependencies_placeholders_and_corrupt_tex(self) -> None:
        contents = "\n".join(
            self.read_page(relative_path)
            for _, _, _, _, relative_path in EXPECTED
        )
        forbidden = (
            "导数",
            "中值定理",
            "Taylor",
            "泰勒",
            "L'Hôpital",
            "L'Hopital",
            "洛必达",
            "Newton",
            "牛顿",
            "积分",
            r"\int",
        )
        for fragment in forbidden:
            with self.subTest(forbidden=fragment):
                self.assertNotIn(fragment.casefold(), contents.casefold())

        for pattern in (
            r"度量空间",
            r"\bmetric\s+spaces?\b",
        ):
            with self.subTest(prohibited_scope=pattern):
                self.assertIsNone(
                    re.search(pattern, contents, flags=re.IGNORECASE),
                )

        incomplete_or_corrupt = (
            "TODO",
            "TBD",
            "待补充",
            "证明略",
            "留作练习",
            "显然可取",
            "由图可知",
            "|,|",
            "\to",
            "+infty",
            "=lim ",
        )
        for fragment in incomplete_or_corrupt:
            with self.subTest(fragment=repr(fragment)):
                self.assertNotIn(fragment, contents)


if __name__ == "__main__":
    unittest.main()
