from pathlib import Path
import re
import unittest


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
        self.assertNotIn("chapters/chapter-42/", NAVIGATION)
        self.assertFalse((chapters / "chapter-42").exists())
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


if __name__ == "__main__":
    unittest.main()
