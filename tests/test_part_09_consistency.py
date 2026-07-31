from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-09-dependencies.md"
COURSE_MAP = ROOT / "content" / "course-map.md"
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

CHAPTER_TITLES = [
    "第 37 章：参数曲线与曲线积分（规划中）",
    "第 38 章：参数曲面与曲面积分（规划中）",
    "第 39 章：Green 公式与平面场（规划中）",
    "第 40 章：Gauss 公式与通量（规划中）",
    "第 41 章：Stokes 公式与三大公式的统一（规划中）",
]


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
        self.assertIn("当前发布边界：第 36 章", text)
        self.assertIn("21 个核心单元、32 学时", text)
        self.assertNotIn("chapters/chapter-37/", NAVIGATION)

    def test_optional_appendix_is_not_core(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("选读附录不计入核心学时", text)

    def test_course_map_locks_every_planned_unit(self) -> None:
        text = self.required_text(COURSE_MAP)
        for heading in CHAPTER_TITLES:
            self.assertEqual(1, text.count(heading), heading)
        for unit_id, title, theory, applied in PART_09_UNITS:
            pattern = (
                rf"^\d+\. `{re.escape(unit_id)}` {re.escape(title)}"
                rf"（理论 {theory:.2f}，应用 {applied:.2f}）$"
            )
            with self.subTest(unit=unit_id):
                self.assertEqual(1, len(re.findall(pattern, text, re.MULTILINE)))
        self.assertIn("### 选读附录：从向量分析到微分形式（规划中）", text)
        self.assertIn("第九部规划 21 个核心单元、32 学时（理论 24，应用 8）", text)


if __name__ == "__main__":
    unittest.main()
