from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-11"

EXPECTED_UNITS = [
    (
        "u-03-11-01",
        "为什么闭区间中的数列总有收敛子列？",
        1.75,
        0.25,
        "compact-intervals",
    ),
    (
        "u-03-11-02",
        "连续函数为何一定有界并取得最值？",
        1.75,
        0.25,
        "extreme-value-theorem",
    ),
    (
        "u-03-11-03",
        "局部连续何时升级为全局一致控制？",
        1.50,
        0.50,
        "uniform-continuity",
    ),
]

REQUIRED_ANCHORS = {
    "u-03-11-01": (
        "def-u-03-11-01-sequential-compactness",
        "thm-u-03-11-01-closed-interval-sequentially-compact",
    ),
    "u-03-11-02": (
        "thm-u-03-11-02-boundedness",
        "thm-u-03-11-02-extreme-value",
    ),
    "u-03-11-03": (
        "def-u-03-11-03-uniform-continuity",
        "thm-u-03-11-03-uniform-continuity",
    ),
}


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterElevenTests(unittest.TestCase):
    def test_units_have_final_metadata_hours_and_anchors(self) -> None:
        theory = 0.0
        applied = 0.0
        for unit_id, title, theory_hours, applied_hours, suffix in EXPECTED_UNITS:
            path = CHAPTER / f"{unit_id}-{suffix}.md"
            with self.subTest(unit=unit_id):
                metadata, text = read_unit(path)
                self.assertEqual(unit_id, metadata["unit_id"])
                self.assertEqual(title, metadata["title"])
                self.assertEqual(theory_hours, metadata["hours"]["theory"])
                self.assertEqual(applied_hours, metadata["hours"]["applied"])
                self.assertEqual(2, metadata["content_standard"])
                for anchor in REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(f"{{#{anchor}}}", text)
                theory += metadata["hours"]["theory"]
                applied += metadata["hours"]["applied"]
        self.assertEqual(5.0, theory)
        self.assertEqual(1.0, applied)

    def test_unit_one_uses_sequential_compactness_as_the_core_route(self) -> None:
        text = (
            CHAPTER / "u-03-11-01-compact-intervals.md"
        ).read_text(encoding="utf-8")
        preview_heading = "### 选读前瞻：第七部的开覆盖语言"
        core = text.split(preview_heading, 1)[0]
        self.assertIn("Bolzano–Weierstrass", core)
        self.assertIn("两个端点都包含在区间中", core)
        self.assertIn("极限保序性", core)
        self.assertNotIn("开覆盖", core)
        for removed_anchor in (
            "def-u-03-11-01-open-cover",
            "def-u-03-11-01-compactness",
            "thm-u-03-11-01-heine-borel",
        ):
            self.assertNotIn(removed_anchor, text)

    def test_unit_one_keeps_general_closed_set_theory_out_of_the_core(self) -> None:
        text = (
            CHAPTER / "u-03-11-01-compact-intervals.md"
        ).read_text(encoding="utf-8")
        core = text.split("### 选读前瞻：第七部的开覆盖语言", 1)[0]
        for later_generalization in (
            "lem-u-03-11-01-closed-limit",
            "prop-u-03-11-01-closed-bounded",
            "闭集的补集",
            "序列紧致集必有界且闭",
        ):
            self.assertNotIn(later_generalization, core)
        for order_step in (
            "a\\le x_{n_k}\\le b",
            "极限的保序性",
            "a\\le x\\le b",
        ):
            self.assertIn(order_step, core)

    def test_open_interval_counterexample_is_indexed_inside_the_set(self) -> None:
        text = (
            CHAPTER / "u-03-11-01-compact-intervals.md"
        ).read_text(encoding="utf-8")
        example = text.split(
            "### 例题 1：开区间为什么失败", 1
        )[1].split("### 例题 2：", 1)[0]
        self.assertIn(r"x_n=1/(n+1)\in(0,1)", example)
        self.assertNotIn(r"x_n=1/n\in(0,1)", example)
        self.assertNotIn("从 \\(n\\ge2\\) 开始", example)

    def test_navigation_and_course_map_use_final_order_and_hours(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        chapter_start = course_map.index("### [第 11 章")
        chapter_end = course_map.index("### [第 12 章")
        chapter = course_map[chapter_start:chapter_end]
        self.assertIn("本章学时：6 小时（理论 5，应用 1）。", chapter)

        nav_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-11/{unit_id}-{suffix}.md"
            nav_marker = f"{title}: {path}"
            map_marker = f"[{title}]({path})"
            self.assertEqual(1, config.count(nav_marker))
            self.assertEqual(1, chapter.count(map_marker))
            nav_positions.append(config.index(nav_marker))
            map_positions.append(chapter.index(map_marker))
        self.assertEqual(sorted(nav_positions), nav_positions)
        self.assertEqual(sorted(map_positions), map_positions)

    def test_core_proofs_do_not_use_later_results(self) -> None:
        forbidden = ("介值定理", "导数", "中值定理", "Taylor", "积分")
        for _unit_id, _title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = next(CHAPTER.glob(f"*-{suffix}.md"))
            text = path.read_text(encoding="utf-8")
            core = text.split("## 常见误区与后续", 1)[0]
            with self.subTest(page=path.name):
                for term in forbidden:
                    self.assertNotIn(term, core)


if __name__ == "__main__":
    unittest.main()
