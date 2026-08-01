from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-12-dependencies.md"
COURSE_MAP = ROOT / "content" / "course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

PART_12_UNITS = [
    ("u-12-51-01", "周期函数与三角函数系怎样构成正交族？", 1.25, 0.25, "trig-orthogonality"),
    ("u-12-51-02", "Fourier 系数为什么来自正交投影？", 1.25, 0.25, "fourier-projection"),
    ("u-12-51-03", "三角多项式怎样给出最佳平方逼近？", 1.50, 0.25, "best-square-approximation"),
    ("u-12-51-04", "复指数形式怎样统一正弦与余弦形式？", 1.00, 0.25, "complex-form"),
    ("u-12-51-05", "有限维投影计算怎样验证最佳逼近？", 1.00, 0.50, "finite-projection-check"),
    ("u-12-52-01", "Fourier 系数有哪些平移、伸缩与对称性质？", 1.00, 0.50, "symmetry-transformations"),
    ("u-12-52-02", "奇偶性和分段积分怎样简化系数计算？", 1.00, 0.75, "coefficient-calculation"),
    ("u-12-52-03", "半区间正弦展开与余弦展开怎样选择？", 1.00, 0.75, "half-range-expansions"),
    ("u-12-52-04", "Fourier 部分和怎样写成 Dirichlet 核卷积？", 1.25, 0.25, "dirichlet-kernel"),
    ("u-12-52-05", "Dirichlet 判别条件怎样保证逐点收敛？", 1.50, 0.25, "dirichlet-convergence"),
    ("u-12-52-06", "连续点与跳跃点的展开值应怎样判断？", 0.75, 0.50, "pointwise-values"),
    ("u-12-53-01", "Bessel 不等式怎样限制 Fourier 系数的能量？", 1.25, 0.25, "bessel-inequality"),
    ("u-12-53-02", "均方误差为何等于总能量减去投影能量？", 1.25, 0.25, "mean-square-error"),
    ("u-12-53-03", "Parseval 等式在什么条件下成立？", 1.50, 0.25, "parseval-identity"),
    ("u-12-53-04", "Parseval 等式怎样用于经典数项级数求和？", 1.00, 0.75, "parseval-series-sums"),
    ("u-12-53-05", "均方收敛与逐点、一致收敛有什么区别？", 1.00, 0.50, "convergence-comparison"),
    ("u-12-54-01", "有限 Fourier 部分和怎样重建周期信号？", 1.00, 0.50, "periodic-reconstruction"),
    ("u-12-54-02", "Gibbs 现象为何不会因增加项数而消失？", 1.25, 0.50, "gibbs-phenomenon"),
    ("u-12-54-03", "Fejér 平均为何比普通部分和更稳定？", 1.50, 0.25, "fejer-means"),
    ("u-12-54-04", "截断阶数、误差指标与采样分辨率怎样选择？", 0.75, 0.75, "truncation-error"),
    ("u-12-54-05", "一个周期模型怎样完成“建模—展开—误差—解释”闭环？", 1.00, 0.50, "periodic-model-closure"),
]


class PartTwelveConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def dependency_registry(self) -> list[tuple[str, str, float, float, str]]:
        text = self.required_text(DEPENDENCIES)
        rows = []
        for line in text.splitlines():
            if not line.startswith("| `u-12-"):
                continue
            fields = [field.strip() for field in line.strip("|").split("|")]
            self.assertGreaterEqual(len(fields), 7, f"incomplete row: {line}")
            rows.append((fields[0].strip("`"), fields[1], float(fields[2]),
                         float(fields[3]), fields[4].strip("`")))
        return rows

    def test_locked_part_totals_and_registry(self) -> None:
        actual = self.dependency_registry()
        self.assertEqual(PART_12_UNITS, actual)
        theory = sum(row[2] for row in actual)
        applied = sum(row[3] for row in actual)
        self.assertEqual((21, 24.0, 9.0, 33.0),
                         (len(actual), theory, applied, theory + applied))

    def test_blueprint_starts_after_current_release(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 51 章", text)
        self.assertIn("21 个核心单元、33 学时", text)
        self.assertIn("255 个学习单元、438 学时", text)
        self.assertIn("不超过 34 学时", text)

    def test_course_map_records_planned_part(self) -> None:
        text = self.required_text(COURSE_MAP)
        self.assertIn("## 第十二部：Fourier 级数", text)
        self.assertIn("第 51–54 章规划已锁定", text)
        for unit_id, title, _, _, _ in PART_12_UNITS:
            with self.subTest(unit_id=unit_id):
                self.assertIn(title, text)

    def test_motivation_proof_order_assessment_and_scope_are_explicit(self) -> None:
        text = self.required_text(DEPENDENCIES)
        for marker in (
            "方波", "正交投影", "系数计算", "Dirichlet", "Bessel", "Parseval",
            "Fejér", "解析计算", "finite_quadrature_only",
            "finite_truncation_only", "第十三部",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_current_publication_does_not_extend_scope(self) -> None:
        self.assertIn("chapters/chapter-51/", NAVIGATION)
        self.assertNotIn("chapters/chapter-52/", NAVIGATION)
        self.assertFalse((ROOT / "content" / "chapters" / "chapter-55").exists())
        self.assertNotIn("第 55 章", self.required_text(COURSE_MAP))


if __name__ == "__main__":
    unittest.main()
