from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-35"
EXPECTED = [
    ("u-08-35-01", "Jacobian 行列式为什么描述局部面积与体积伸缩？", 1.50, 0.25, "jacobian-scaling", 9, 11),
    ("u-08-35-02", "重积分换元公式需要哪些条件？", 1.50, 0.25, "change-of-variables", 10, 12),
    ("u-08-35-03", "极坐标怎样处理圆形与径向对称区域？", 1.50, 0.25, "polar-coordinates", 10, 12),
    ("u-08-35-04", "柱面、球面坐标怎样处理三维区域？", 1.50, 0.25, "cylindrical-spherical", 11, 13),
]
MARKERS = {
    "u-08-35-01": ("线性变换", "行列式绝对值", "局部伸缩", "取向"),
    "u-08-35-02": ("一一对应", "连续可微", "Jacobian 不退化", "边界分片", "thm-u-08-35-02-change-of-variables"),
    "u-08-35-03": ("极坐标", "Jacobian", "det", "r"),
    "u-08-35-04": ("柱面坐标", "球面坐标", "rho^2", "sin", "det"),
}

def path(unit):
    return CHAPTER / f"{unit[0]}-{unit[4]}.md"

class ChapterThirtyFiveTests(unittest.TestCase):
    def text(self, file):
        self.assertTrue(file.is_file(), f"missing {file}")
        return file.read_text(encoding="utf-8") if file.is_file() else ""

    def test_contract(self):
        totals = [0.0, 0.0, 0, 0]
        for row in EXPECTED:
            uid, title, theory, applied, _suffix, exercises, answers = row
            text = self.text(path(row))
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            with self.subTest(uid=uid):
                self.assertEqual((uid, title), (meta["unit_id"], meta["title"]))
                self.assertEqual((theory, applied), (meta["hours"]["theory"], meta["hours"]["applied"]))
                self.assertEqual(exercises, text.count(f"{{#pr-{uid}-"))
                self.assertEqual(answers, text.count('??? note "答案"'))
                self.assertGreaterEqual(text.count("{#ex-"), 2)
                for marker in MARKERS[uid]:
                    self.assertIn(marker, text)
                self.assertNotIn("由公式可得面积元", text)
            totals = [totals[0]+theory, totals[1]+applied, totals[2]+exercises, totals[3]+answers]
        self.assertEqual([6.0, 1.0, 40, 48], totals)

    def test_guide_and_release(self):
        guide = self.text(CHAPTER / "index.md")
        for row in EXPECTED:
            self.assertEqual(1, guide.count(f"[{row[1]}]({row[0]}-{row[4]}.md)"))
        nav = self.text(ROOT / "mkdocs.yml")
        self.assertIn("chapters/chapter-35/", nav)

    def test_change_of_variables_proof_has_all_classical_riemann_steps(self):
        text = self.text(path(EXPECTED[1]))
        ordered_structure = (
            "有限矩形并的内部或常用 Jordan 型",
            "假设 | 在证明中的用途",
            "{#lem-u-08-35-02-uniform-box-volume}",
            "紧内部的一致线性化",
            "线性像的体积",
            "余项的外包与内包",
            "规则立方网格选出固定内核",
            "被积函数与 Jacobian 的振幅控制",
            "从固定内核回到全域",
        )
        positions = []
        for marker in ordered_structure:
            self.assertIn(marker, text)
            positions.append(text.index(marker))
        self.assertEqual(sorted(positions), positions)
        for formula in (
            r"\operatorname{vol}(T(Q))",
            r"|\det DT(a)|\operatorname{vol}(Q)",
            r"o(\operatorname{vol}(Q))",
            r"\omega_f(Ch)+\|f\|_\infty\omega_J(h)",
        ):
            self.assertIn(formula, text)

    def test_change_of_variables_uses_only_regular_cubes_and_charges_omissions(self):
        text = self.text(path(EXPECTED[1])).split("### 换元定理的 Riemann 和证明", 1)[1]
        self.assertNotIn("覆盖盒坐标端点与边长", text)
        ordered = (
            "规则立方网格",
            r"Q_0\cap\partial G\ne\varnothing",
            "所有未保留格",
            r"\operatorname{vol}(G\setminus K)<C\eta",
        )
        positions = []
        for marker in ordered:
            self.assertIn(marker, text)
            positions.append(text.index(marker))
        self.assertEqual(sorted(positions), positions)

    def test_change_of_variables_first_exhausts_a_fixed_inner_core(self):
        text = self.text(path(EXPECTED[1])).split("### 换元定理的 Riemann 和证明", 1)[1]
        ordered = (
            r"K=\bigcup_{Q_0\in\mathcal K_0}Q_0\Subset G",
            r"固定这个 \(K\)",
            r"K=\bigcup_{Q\in\mathcal K_h}Q",
            r"h\to0",
            r"\int_{T(K)}f=\int_K(f\circ T)J",
            r"\eta\to0",
        )
        positions = []
        for marker in ordered:
            self.assertIn(marker, text)
            positions.append(text.index(marker))
        self.assertEqual(sorted(positions), positions)

    def test_change_of_variables_samples_each_cube_at_its_center(self):
        text = self.text(path(EXPECTED[1])).split("### 换元定理的 Riemann 和证明", 1)[1]
        center = r"a_Q=\operatorname{center}(Q)"
        local_volume = r"J(a_Q)\operatorname{vol}(Q)"
        uniform_error = r"o_h(\operatorname{vol}(Q))"
        self.assertIn(center, text)
        self.assertIn(local_volume, text)
        self.assertIn(uniform_error, text)
        self.assertLess(text.index(center), text.index(local_volume))
        self.assertLess(text.index(local_volume), text.index(uniform_error))

    def test_target_boundary_is_derived_from_ift_and_compactness(self):
        text = self.text(path(EXPECTED[1])).split("### 换元定理的 Riemann 和证明", 1)[1]
        ordered = (
            r"u\in G",
            "反函数定理",
            r"T(u)\in\operatorname{int}D",
            r"y_n=T(u_n)\to y",
            r"u_{n_k}\to\bar u\in\overline G",
            r"y=T(\bar u)",
            r"\bar u\in\partial G",
            r"\partial D\subset T(\partial G)",
            "目标边界的零延拓",
        )
        positions = []
        for marker in ordered:
            self.assertIn(marker, text)
            positions.append(text.index(marker))
        self.assertEqual(sorted(positions), positions)

if __name__ == "__main__":
    unittest.main()
