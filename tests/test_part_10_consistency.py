from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-10-dependencies.md"
COURSE_MAP = ROOT / "content" / "course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

PART_10_UNITS = [
    ("u-10-42-01", "含参积分怎样定义函数，参数与积分变量怎样分工？", 1.25, 0.00),
    ("u-10-42-02", "被积函数联合连续时，积分为什么连续依赖参数？", 1.25, 0.25),
    ("u-10-42-03", "一致收敛为什么允许极限进入积分号？", 1.25, 0.25),
    ("u-10-42-04", "哪些逐点收敛反例说明一致控制不可省略？", 1.00, 0.50),
    ("u-10-42-05", "怎样为连续性与极限交换建立条件检查表？", 0.75, 0.50),
    ("u-10-43-01", "什么条件允许对含参积分求导？", 1.25, 0.00),
    ("u-10-43-02", "差商与偏导的一致控制怎样完成 Leibniz 公式证明？", 1.50, 0.25),
    ("u-10-43-03", "积分端点随参数变化时，边界项从哪里产生？", 1.25, 0.50),
    ("u-10-43-04", "对参数再积分时，怎样通过经典 Fubini 交换次序？", 1.00, 0.50),
    ("u-10-43-05", "可固定化的移动区域怎样化为固定区域问题？", 1.00, 0.75),
    ("u-10-44-01", "含参反常积分的一致收敛应怎样定义？", 1.25, 0.00),
    ("u-10-44-02", "一致 Cauchy 判据怎样把尾部转化为可检查条件？", 1.50, 0.25),
    ("u-10-44-03", "Weierstrass、Dirichlet 与 Abel 型判据怎样控制参数族？", 1.25, 0.50),
    ("u-10-44-04", "连续性、极限与参数积分何时可同反常积分交换？", 1.00, 0.50),
    ("u-10-44-05", "积分号下求导何时成立，反例揭示哪些条件缺口？", 1.00, 0.75),
    ("u-10-45-01", "Gamma 积分在哪些参数上收敛，递推公式怎样得到？", 1.00, 0.25),
    ("u-10-45-02", "Beta 积分的端点奇性怎样控制？", 1.00, 0.25),
    ("u-10-45-03", "Beta–Gamma 关系怎样由重积分与换元推出？", 1.25, 0.25),
    ("u-10-45-04", "参数求导怎样产生含对数因子的积分与敏感性公式？", 0.75, 0.75),
    ("u-10-45-05", "怎样对 Gamma、Beta 积分作带状态的可靠近似？", 0.50, 1.00),
]


class PartTenConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def dependency_registry(self) -> list[tuple[str, str, float, float]]:
        text = self.required_text(DEPENDENCIES)
        rows = []
        for line in text.splitlines():
            if not line.startswith("| `u-10-"):
                continue
            fields = [field.strip() for field in line.strip("|").split("|")]
            self.assertGreaterEqual(len(fields), 6, f"incomplete registry row: {line}")
            rows.append((fields[0].strip("`"), fields[1], float(fields[2]), float(fields[3])))
        return rows

    def test_locked_part_totals_and_registry(self) -> None:
        actual = self.dependency_registry()
        self.assertEqual(PART_10_UNITS, actual)
        theory = sum(row[2] for row in actual)
        applied = sum(row[3] for row in actual)
        self.assertEqual((20, 22.0, 8.0, 30.0), (len(actual), theory, applied, theory + applied))

    def test_blueprint_starts_after_part_nine(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 43 章", text)
        self.assertIn("20 个核心单元、30 学时", text)
        self.assertIn("chapters/chapter-42/", NAVIGATION)

    def test_course_map_records_planned_part(self) -> None:
        text = self.required_text(COURSE_MAP)
        self.assertIn("## 第十部：含参变量积分", text)
        self.assertIn("第 42–43 章已发布，第 44–45 章规划中", text)
        for unit_id, title, _, _ in PART_10_UNITS:
            with self.subTest(unit_id=unit_id):
                self.assertIn(title, text)

    def test_scope_and_status_contracts_are_explicit(self) -> None:
        text = self.required_text(DEPENDENCIES)
        for marker in (
            "固定区域", "一致控制", "一致 Cauchy", "target_met",
            "budget_exhausted", "uncertified", "第十一部",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_part_eleven_is_not_created(self) -> None:
        self.assertFalse((ROOT / "content" / "chapters" / "chapter-46").exists())
        self.assertNotIn("chapters/chapter-46/", NAVIGATION)


if __name__ == "__main__":
    unittest.main()
