from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-11-dependencies.md"
COURSE_MAP = ROOT / "content" / "course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

PART_11_UNITS = [
    ("u-11-46-01", "区间长度应满足哪些基本性质？", 1.25, 0.00),
    ("u-11-46-02", "可数区间覆盖怎样定义 Lebesgue 外测度？", 1.25, 0.25),
    ("u-11-46-03", "外测度为何单调并满足可数次可加性？", 1.25, 0.25),
    ("u-11-46-04", "区间的外测度为何恰好等于区间长度？", 1.25, 0.50),
    ("u-11-46-05", "可数集为何是零测集，Jordan 理论的边界在哪里？", 1.00, 0.50),
    ("u-11-47-01", "为什么集合运算必须对可数过程封闭？", 1.25, 0.25),
    ("u-11-47-02", "Carathéodory 判据怎样定义可测集合？", 1.50, 0.25),
    ("u-11-47-03", "可测集合为何构成 σ-代数？", 1.50, 0.25),
    ("u-11-47-04", "外测度在可测集上为何成为可数可加的测度？", 1.25, 0.25),
    ("u-11-47-05", "Borel 集、零测集及其子集怎样进入 Lebesgue 可测世界？", 1.00, 0.50),
    ("u-11-48-01", "可测函数为何可由水平集的可测性刻画？", 1.25, 0.25),
    ("u-11-48-02", "运算、上确界与逐点极限怎样保持可测性？", 1.25, 0.25),
    ("u-11-48-03", "非负可测函数怎样由递增简单函数逼近？", 1.50, 0.50),
    ("u-11-48-04", "逐点、一致与几乎处处收敛怎样区分？", 1.00, 0.25),
    ("u-11-48-05", "依测度收敛与其他收敛方式有什么关系？", 1.00, 0.25),
    ("u-11-49-01", "简单函数的积分怎样由水平集测度定义？", 1.25, 0.50),
    ("u-11-49-02", "非负可测函数的积分怎样由下逼近定义？", 1.50, 0.25),
    ("u-11-49-03", "积分的单调性、齐次性与可加性怎样证明？", 1.50, 0.25),
    ("u-11-49-04", "正部、负部怎样定义一般函数的积分？", 1.25, 0.25),
    ("u-11-49-05", "绝对可积、零测集修改与积分估计怎样统一？", 1.00, 0.25),
    ("u-11-50-01", "单调收敛定理怎样闭合递增逼近？", 1.25, 0.25),
    ("u-11-50-02", "Fatou 引理怎样给出下极限不等式？", 1.25, 0.00),
    ("u-11-50-03", "控制收敛定理为何需要可积控制函数？", 1.50, 0.25),
    ("u-11-50-04", "Riemann 可积函数与 Lebesgue 积分怎样兼容？", 1.25, 0.25),
    ("u-11-50-05", "序章失败序列怎样被新理论完整解释？", 0.75, 0.25),
]


class PartElevenConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def dependency_registry(self) -> list[tuple[str, str, float, float]]:
        text = self.required_text(DEPENDENCIES)
        rows = []
        for line in text.splitlines():
            if not line.startswith("| `u-11-"):
                continue
            fields = [field.strip() for field in line.strip("|").split("|")]
            self.assertGreaterEqual(len(fields), 6, f"incomplete row: {line}")
            rows.append((fields[0].strip("`"), fields[1], float(fields[2]), float(fields[3])))
        return rows

    def test_locked_part_totals_and_registry(self) -> None:
        actual = self.dependency_registry()
        self.assertEqual(PART_11_UNITS, actual)
        theory = sum(row[2] for row in actual)
        applied = sum(row[3] for row in actual)
        self.assertEqual((25, 31.0, 7.0, 38.0),
                         (len(actual), theory, applied, theory + applied))

    def test_blueprint_starts_after_part_ten(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 50 章", text)
        self.assertIn("25 个核心单元、38 学时", text)
        self.assertIn("chapters/chapter-46/", NAVIGATION)

    def test_course_map_records_planned_part(self) -> None:
        text = self.required_text(COURSE_MAP)
        self.assertIn("## 第十一部：测度与 Lebesgue 积分", text)
        self.assertIn("第 46–50 章规划已锁定", text)
        for unit_id, title, _, _ in PART_11_UNITS:
            with self.subTest(unit_id=unit_id):
                self.assertIn(title, text)

    def test_motivation_proof_order_and_scope_are_explicit(self) -> None:
        text = self.required_text(DEPENDENCIES)
        for marker in (
            "有理数", "Riemann", "外测度", "Carathéodory", "简单函数",
            "单调收敛", "Fatou", "控制收敛", "finite_cover_only", "第十二部",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_part_twelve_is_not_created(self) -> None:
        self.assertFalse((ROOT / "content" / "chapters" / "chapter-51").exists())
        self.assertNotIn("chapters/chapter-51/", NAVIGATION)

    def test_final_release_has_exact_pages_hours_navigation_and_reviews(self) -> None:
        pages = sorted((ROOT / "content" / "chapters").glob("chapter-4[6-9]/u-11-*.md"))
        pages += sorted((ROOT / "content" / "chapters" / "chapter-50").glob("u-11-*.md"))
        self.assertEqual(25, len(pages))
        ids, theory, applied = [], 0.0, 0.0
        for page in pages:
            text = page.read_text(encoding="utf-8")
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            ids.append(meta["unit_id"]); theory += meta["hours"]["theory"]; applied += meta["hours"]["applied"]
            self.assertEqual(1, NAVIGATION.count(f"chapters/{page.parent.name}/{page.name}"))
        self.assertEqual((25, 25, 31.0, 7.0), (len(ids), len(set(ids)), theory, applied))
        for chapter in range(46, 51):
            self.assertTrue((ROOT / "docs" / "reviews" / f"2026-08-01-chapter-{chapter}-consistency-review.md").is_file())
            guide = self.required_text(ROOT / "content" / "chapters" / f"chapter-{chapter}" / "index.md")
            self.assertIn("序章", guide)

    def test_computation_sources_and_cross_part_handoffs_are_unique(self) -> None:
        sources = list((ROOT / "src").rglob("*.py"))
        joined = "\n".join(path.read_text(encoding="utf-8") for path in sources)
        self.assertEqual(1, joined.count("def simple_integral("))
        self.assertEqual(1, joined.count("def finite_cover_upper_bound("))
        handoffs = {
            "part-05-dependencies.md": "u-11-50-04",
            "part-06-dependencies.md": "u-11-48-04",
            "part-08-dependencies.md": "u-11-46-05",
            "part-10-dependencies.md": "第 46–50 章现已发布",
        }
        for name, marker in handoffs.items():
            self.assertIn(marker, self.required_text(ROOT / "docs" / "curriculum" / name))


if __name__ == "__main__":
    unittest.main()
