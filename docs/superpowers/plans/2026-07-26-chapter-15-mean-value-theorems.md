# 第 15 章“微分中值定理” Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 发布第 15 章 4 个 `content_standard: 2` 单元，严格建立 Fermat、Rolle、Lagrange、Darboux、Cauchy 与 L’Hôpital 的证明链，并完整处理五类非基本未定式。

**Architecture:** Markdown 正文是唯一内容来源，`tests/test_chapter_15.py` 先冻结单元、学时、证明条件、依赖边界和发布合同。正文按“单函数中值定理 → 区间整体性质 → 双函数中值定理 → 未定式极限”推进；每页独立通过内容检查，正文完成后先做发布前内容审查，最后统一更新 Zensical 导航、课程地图、README、第四部设计和真实站点检查。

**Tech Stack:** Markdown、Python 3.12 `unittest`、PyYAML、Zensical 0.0.51、MathJax、现有 `make verify` 质量门。

---

## 文件结构

**新增**

- `content/chapters/chapter-15/index.md`：章节问题弧、8.5 学时路径、证明阶梯和依赖边界。
- `content/chapters/chapter-15/u-04-15-01-fermat-rolle-lagrange.md`：Fermat、Rolle 与 Lagrange 中值定理。
- `content/chapters/chapter-15/u-04-15-02-monotonicity-darboux.md`：单调性、常值判别、增量控制与 Darboux 定理。
- `content/chapters/chapter-15/u-04-15-03-cauchy-mean-value.md`：Cauchy 中值定理的交叉乘积形式与有条件比值形式。
- `content/chapters/chapter-15/u-04-15-04-lhopital-rule.md`：完整约定范围内的 L’Hôpital 法则、五类转化和失败边界。
- `tests/test_chapter_15.py`：结构、学时、证明标记、条件边界、导航和课程地图合同。

**修改**

- `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md`：把第 15 章改为 8.5 学时，并把第四部总量改为理论 25、应用 10.5、合计 35.5。
- `mkdocs.yml`：在第四部第 14 章之后加入第 15 章。
- `content/course-map.md`：加入第 15 章 8.5 学时及 4 个单元链接。
- `README.md`：学习单元数从 60 更新为 64，发布范围更新到第四部第 15 章。
- `scripts/check_site.py`：加入 Cauchy 中值定理代表页面的锚点和导航标记。
- `tests/test_mkdocs_site.py`：冻结第 15 章真实站点合同。

本章不新增 Python 算法模块。L’Hôpital 的“算法性”体现在固定的条件核验流程，不把符号
求导器或自动极限求解器纳入本章。

## 固定单元合同

| 顺序 | ID | 文件后缀 | 标题 | 理论+应用 |
|---|---|---|---|---:|
| 15.1 | `u-04-15-01` | `fermat-rolle-lagrange` | 两个端点的信息怎样迫使中间出现特殊切线？ | 1.75+0.25 |
| 15.2 | `u-04-15-02` | `monotonicity-darboux` | 导数符号能推出哪些整体性质？ | 1.75+0.50 |
| 15.3 | `u-04-15-03` | `cauchy-mean-value` | 两个函数的变化率怎样进行严格比较？ | 1.50+0.50 |
| 15.4 | `u-04-15-04` | `lhopital-rule` | L’Hôpital 法则何时能判定未定式极限？ | 1.50+0.75 |

本章合计理论 6.5、应用 2.0，共 8.5 学时。四页全部执行 v2 合同：至少 2 个稳定例题、
2 个即时检验、5 道习题和 7 个折叠完整答案。

## 证明与条件合同

- 定理依赖顺序固定为 Fermat → Rolle → Lagrange → Darboux → Cauchy →
  L’Hôpital，不用 Taylor 公式、积分或无穷级数证明任何核心结论。
- Cauchy 定理先给无除法的交叉乘积形式；只有在 \(g'\) 于整个开区间不为零并推出端点
  增量非零后，才能写比值形式。
- L’Hôpital 的 \(0/0\) 与 \(\infty/\infty\) 分开陈述和证明；有限点、单侧、无穷远、
  有限导数比极限及正负无穷分别说明量词和趋近方向。
- 幂型未定式必须先核验底数在去心邻域内为正，再取对数；重复使用 L’Hôpital 时每轮
  重新核验形式和条件。
- 凸性、Taylor 公式、Newton 方法、Riemann 积分与无穷级数留给后续章节。

### Task 1: 用失败测试冻结第 15 章合同

**Files:**

- Create: `tests/test_chapter_15.py`
- Test: `tests/test_chapter_15.py`

- [ ] **Step 1: 写入精确单元、学时和锚点合同**

创建以下常量和辅助函数：

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-15"

EXPECTED_UNITS = [
    (
        "u-04-15-01",
        "两个端点的信息怎样迫使中间出现特殊切线？",
        1.75,
        0.25,
        "fermat-rolle-lagrange",
    ),
    (
        "u-04-15-02",
        "导数符号能推出哪些整体性质？",
        1.75,
        0.50,
        "monotonicity-darboux",
    ),
    (
        "u-04-15-03",
        "两个函数的变化率怎样进行严格比较？",
        1.50,
        0.50,
        "cauchy-mean-value",
    ),
    (
        "u-04-15-04",
        "L’Hôpital 法则何时能判定未定式极限？",
        1.50,
        0.75,
        "lhopital-rule",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-15-01": (
        "thm-u-04-15-01-fermat",
        "thm-u-04-15-01-rolle",
        "thm-u-04-15-01-lagrange",
    ),
    "u-04-15-02": (
        "thm-u-04-15-02-monotonicity",
        "thm-u-04-15-02-darboux",
        "ex-u-04-15-02-discontinuous-derivative",
    ),
    "u-04-15-03": (
        "thm-u-04-15-03-cauchy-cross",
        "cor-u-04-15-03-cauchy-ratio",
    ),
    "u-04-15-04": (
        "thm-u-04-15-04-lhopital-zero-zero",
        "thm-u-04-15-04-lhopital-infinity-infinity",
        "ex-u-04-15-04-power-forms",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "Taylor",
    "Newton",
    "Riemann 积分",
    "无穷级数",
    "凸函数",
)


def unit_path(unit: tuple[str, str, float, float, str]) -> Path:
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text
```

- [ ] **Step 2: 写入结构、顺序和边界测试**

`ChapterFifteenTests` 至少实现：

```python
class ChapterFifteenTests(unittest.TestCase):
    def test_units_have_final_metadata_hours_and_anchors(self) -> None:
        theory = 0.0
        applied = 0.0
        for unit in EXPECTED_UNITS:
            unit_id, title, theory_hours, applied_hours, _suffix = unit
            path = unit_path(unit)
            with self.subTest(unit=unit_id):
                self.assertTrue(path.is_file(), f"missing {path.name}")
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
        self.assertEqual(6.5, theory)
        self.assertEqual(2.0, applied)

    def test_chapter_guide_lists_units_hours_and_boundaries(self) -> None:
        guide_path = CHAPTER / "index.md"
        self.assertTrue(guide_path.is_file(), "missing chapter guide")
        guide = guide_path.read_text(encoding="utf-8")
        self.assertIn("本章共4个核心单元，8.5学时（理论6.5，应用2.0）。", guide)
        self.assertIn("第 16–17 章", guide)
        for unit in EXPECTED_UNITS:
            unit_id, title, _theory, _applied, suffix = unit
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_navigation_course_map_and_part_design_use_final_order(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        part_design = (
            ROOT / "docs" / "superpowers" / "specs"
            / "2026-07-25-part-04-differentiation-design.md"
        ).read_text(encoding="utf-8")
        self.assertIn("本章学时：8.5 小时（理论 6.5，应用 2.0）。", course_map)
        self.assertIn("第四部第 15 章，共 64 个学习单元", readme)
        self.assertIn("| 第 15 章 | 6.5 | 2.0 | 8.5 |", part_design)
        self.assertIn("| **第四部** | **25** | **10.5** | **35.5** |", part_design)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-15/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)

    def test_core_proofs_do_not_use_later_calculus(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)
```

- [ ] **Step 3: 写入数学条件防回归测试**

加入以下测试；标记文本必须在正文中原样出现：

```python
    def test_darboux_does_not_assume_derivative_continuity(self) -> None:
        text = unit_path(EXPECTED_UNITS[1]).read_text(encoding="utf-8")
        self.assertIn(r"\(a,b\) 都是导数定义区间的内部点", text)
        self.assertIn(r"证明没有假设 \(f'\) 连续", text)
        self.assertNotIn("因为导函数连续", text)

    def test_cauchy_cross_product_precedes_ratio_form(self) -> None:
        text = unit_path(EXPECTED_UNITS[2]).read_text(encoding="utf-8")
        cross = text.index("{#thm-u-04-15-03-cauchy-cross}")
        ratio = text.index("{#cor-u-04-15-03-cauchy-ratio}")
        self.assertLess(cross, ratio)
        self.assertIn(r"g'(x)\ne0\qquad(x\in(a,b))", text)
        self.assertIn("不能对定理给出的未知点追加条件", text)

    def test_lhopital_separates_forms_and_rechecks_conditions(self) -> None:
        text = unit_path(EXPECTED_UNITS[3]).read_text(encoding="utf-8")
        self.assertLess(
            text.index("{#thm-u-04-15-04-lhopital-zero-zero}"),
            text.index("{#thm-u-04-15-04-lhopital-infinity-infinity}"),
        )
        for marker in (
            r"0\cdot\infty",
            r"\infty-\infty",
            r"1^\infty",
            r"0^0",
            r"\infty^0",
            "每一轮都重新核验",
            "去心邻域内为正",
        ):
            self.assertIn(marker, text)

    def test_lhopital_includes_one_sided_infinite_and_failure_cases(self) -> None:
        text = unit_path(EXPECTED_UNITS[3]).read_text(encoding="utf-8")
        for marker in (
            r"x\to a^+",
            r"x\to a^-",
            r"x\to+\infty",
            r"x\to-\infty",
            "导数之比没有极限",
            "非未定式",
        ):
            self.assertIn(marker, text)
```

- [ ] **Step 4: 验证 RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_15 -v
```

Expected: FAIL，原因是第 15 章文件与发布条目不存在；不能出现导入错误。

- [ ] **Step 5: 提交合同测试**

```bash
git add tests/test_chapter_15.py
git commit -m "test: define chapter fifteen mean value contract"
```

### Task 2: 完成章导学与 15.1 Fermat、Rolle、Lagrange

**Files:**

- Create: `content/chapters/chapter-15/index.md`
- Create: `content/chapters/chapter-15/u-04-15-01-fermat-rolle-lagrange.md`
- Test: `tests/test_chapter_15.py`

- [ ] **Step 1: 创建章导学页**

使用精确标题与锚点：

```markdown
---
title: 第 15 章：微分中值定理
---

# 第 15 章：微分中值定理 {#chapter-15}
```

章导学列出 4 个单元及理论 6.5 + 应用 2.0 = 8.5 学时，写明证明阶梯
Fermat → Rolle → Lagrange → Darboux → Cauchy → L’Hôpital。边界段明确凸性、
Taylor 公式和 Newton 方法留给第 16–17 章。

- [ ] **Step 2: 写入 15.1 元数据**

```yaml
title: 两个端点的信息怎样迫使中间出现特殊切线？
unit_id: u-04-15-01
hours: {theory: 1.75, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-03-11-02, u-04-13-01, u-04-13-02]
  higher_algebra: [直线斜率, 辅助函数构造]
  analytic_geometry: [割线与切线]
  python: [不要求]
capabilities: [proof, proof_strategy, counterexample, mathematical_expression]
learning_goals: [证明 Fermat 必要条件, 证明 Rolle 定理, 证明 Lagrange 中值定理, 核验中值定理条件]
content_standard: 2
```

- [ ] **Step 3: 完成三层证明**

按以下固定路线写出完整证明：

1. Fermat `{#thm-u-04-15-01-fermat}`：局部极大点处，分别令 \(h>0\) 与 \(h<0\)，
   比较差商符号；双侧导数存在迫使导数同时不大于零且不小于零。
2. Rolle `{#thm-u-04-15-01-rolle}`：闭区间最值定理给出最大值和最小值；恒定情形任取
   内点，非恒定情形由端点等值证明至少一个非端点极值存在，再用 Fermat。
3. Lagrange `{#thm-u-04-15-01-lagrange}`：构造

   \[
   F(x)=f(x)-\frac{f(b)-f(a)}{b-a}(x-a),
   \]

   核验 \(F(a)=F(b)\)，用 Rolle 得到
   \[
   f(b)-f(a)=f'(c)(b-a).
   \]

每个条件至少配一个边界例；明确反例用于说明条件不可随意删去，不宣称列出的条件都是
逻辑上独立的最弱条件。

- [ ] **Step 4: 补齐 v2 自学结构并验证**

两个稳定例题分别使用“端点等值找水平切线”和“割线斜率找瞬时速度”。即时检验要求
学生先核验条件再找 \(c\)；5 道习题覆盖证明补全、绝对值尖点、开区间连续性漏洞、
端点不等值和辅助函数构造，并为 2 个检验与 5 道习题提供 7 个折叠完整答案。

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_15.ChapterFifteenTests.test_core_proofs_do_not_use_later_calculus -v
```

Expected: 内容检查和依赖边界测试通过。

- [ ] **Step 5: 提交 15.1**

```bash
git add content/chapters/chapter-15
git commit -m "feat: prove the classical mean value ladder"
```

### Task 3: 完成 15.2 单调性、增量控制与 Darboux

**Files:**

- Create: `content/chapters/chapter-15/u-04-15-02-monotonicity-darboux.md`
- Test: `tests/test_chapter_15.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: 导数符号能推出哪些整体性质？
unit_id: u-04-15-02
hours: {theory: 1.75, applied: 0.50}
difficulty: 4
prerequisites:
  book: [u-04-15-01, u-03-11-02]
  higher_algebra: [不等式, 分段函数]
  analytic_geometry: [函数图像的增减]
  python: [不要求]
capabilities: [proof, proof_strategy, counterexample, error_analysis]
learning_goals: [由导数符号判断单调性, 证明常值与增量估计, 区分充分条件与必要条件, 证明导数的 Darboux 性质]
content_standard: 2
```

- [ ] **Step 2: 从 Lagrange 推出整体性质**

定理 `{#thm-u-04-15-02-monotonicity}` 对任意 \(x_1<x_2\) 使用 Lagrange：

- \(f'\ge0\) 推出单调不减，\(f'>0\) 推出严格递增；
- \(f'\le0\) 与 \(f'<0\) 给出对应结论；
- 单调函数在可导点的差商符号给出必要方向；
- \(f'\equiv0\) 推出区间常值；
- \(|f'|\le M\) 推出
  \[
  |f(x)-f(y)|\le M|x-y|.
  \]

用 \(f(x)=x^3\) 说明严格递增不要求导数处处严格为正，明确区分“充分”“必要”与
“等价”。

- [ ] **Step 3: 完整证明 Darboux 定理**

定理 `{#thm-u-04-15-02-darboux}` 明确写出
“\(a,b\) 都是导数定义区间的内部点”。在
\[
f'(a)<\lambda<f'(b)
\]
时构造
\[
F(x)=f(x)-\lambda x.
\]

由 \(F'(a)<0\) 的右侧差商排除 \(a\) 取得最小值；由 \(F'(b)>0\) 的左侧差商排除
\(b\) 取得最小值。闭区间最值定理于是给出内部最小点 \(c\)，Fermat 条件给出
\(F'(c)=0\)，即 \(f'(c)=\lambda\)。反向次序用 \(-f\) 或最大值论证。

正文原文声明“证明没有假设 \(f'\) 连续”，并解释 Darboux 性质不等于导函数连续。

- [ ] **Step 4: 完成反直觉例和 v2 结构**

稳定例 `{#ex-u-04-15-02-discontinuous-derivative}` 使用

\[
f(x)=
\begin{cases}
x^2\sin(1/x),&x\ne0,\\
0,&x=0,
\end{cases}
\]

先由定义求 \(f'(0)=0\)，再给出 \(x\ne0\) 时
\[
f'(x)=2x\sin(1/x)-\cos(1/x),
\]
说明导数在零点不连续且剧烈振荡，但不能发生跳跃。

另一个稳定例使用导数界估计函数增量。即时检验与 5 道习题覆盖严格单调反例、常值判别、
Lipschitz 型估计、Darboux 证明端点排除和“导数有介值性不等于连续”，提供 7 个完整
折叠答案。

- [ ] **Step 5: 验证并提交 15.2**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest \
  tests.test_chapter_15.ChapterFifteenTests.test_darboux_does_not_assume_derivative_continuity \
  tests.test_chapter_15.ChapterFifteenTests.test_core_proofs_do_not_use_later_calculus -v
git add content/chapters/chapter-15/u-04-15-02-monotonicity-darboux.md
git commit -m "feat: derive monotonicity and Darboux properties"
```

### Task 4: 完成 15.3 Cauchy 中值定理

**Files:**

- Create: `content/chapters/chapter-15/u-04-15-03-cauchy-mean-value.md`
- Test: `tests/test_chapter_15.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: 两个函数的变化率怎样进行严格比较？
unit_id: u-04-15-03
hours: {theory: 1.50, applied: 0.50}
difficulty: 4
prerequisites:
  book: [u-04-15-01, u-04-15-02]
  higher_algebra: [交叉乘积, 比值与非零条件]
  analytic_geometry: [参数曲线的变化率]
  python: [不要求]
capabilities: [proof, proof_strategy, condition_checking, mathematical_expression]
learning_goals: [构造双函数辅助函数, 证明 Cauchy 中值定理, 从交叉乘积合法推出比值形式, 比较总变化率与局部变化率]
content_standard: 2
```

- [ ] **Step 2: 先证明无除法形式**

对在 \([a,b]\) 连续、在 \((a,b)\) 可导的 \(f,g\)，构造

\[
H(x)=[g(b)-g(a)][f(x)-f(a)]
-[f(b)-f(a)][g(x)-g(a)].
\]

核验 \(H(a)=H(b)=0\)，由 Rolle 得到 \(H'(c)=0\)，推出

\[
[f(b)-f(a)]g'(c)
=[g(b)-g(a)]f'(c)
\]

并以 `{#thm-u-04-15-03-cauchy-cross}` 标记。证明过程不得出现任何除以
\(g(b)-g(a)\) 或 \(g'(c)\) 的步骤。

- [ ] **Step 3: 有条件地推出比值形式**

推论 `{#cor-u-04-15-03-cauchy-ratio}` 额外假设

\[
g'(x)\ne0\qquad(x\in(a,b)).
\]

由 Darboux 得到 \(g'\) 在开区间同号，由 Lagrange 得到
\(g(b)-g(a)\ne0\)。因此交叉乘积定理给出的 \(c\) 也满足 \(g'(c)\ne0\)，才能写

\[
\frac{f(b)-f(a)}{g(b)-g(a)}
=\frac{f'(c)}{g'(c)}.
\]

正文明确写出“不能对定理给出的未知点追加条件”；条件必须在应用定理前成立或由已知
条件推出。

- [ ] **Step 4: 完成例题、边界和 v2 结构**

稳定例一以 \(g(x)=x\) 还原 Lagrange，说明 Cauchy 是真正的推广；稳定例二比较参数
曲线两个坐标的总变化率与局部变化率。反例用 \(g\) 的端点增量为零或 \(g'\) 在区间
内取零说明比值形式可能无定义，但交叉乘积形式仍合法。

即时检验与 5 道习题覆盖辅助函数构造、退化为 Lagrange、分母条件、未知 \(c\) 的量词
和为 L’Hôpital 准备的区间应用，提供 7 个折叠完整答案。

- [ ] **Step 5: 验证并提交 15.3**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest \
  tests.test_chapter_15.ChapterFifteenTests.test_cauchy_cross_product_precedes_ratio_form \
  tests.test_chapter_15.ChapterFifteenTests.test_core_proofs_do_not_use_later_calculus -v
git add content/chapters/chapter-15/u-04-15-03-cauchy-mean-value.md
git commit -m "feat: prove Cauchy mean value theorem"
```

### Task 5: 完成 15.4 L’Hôpital 法则与五类转化

**Files:**

- Create: `content/chapters/chapter-15/u-04-15-04-lhopital-rule.md`
- Test: `tests/test_chapter_15.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: L’Hôpital 法则何时能判定未定式极限？
unit_id: u-04-15-04
hours: {theory: 1.50, applied: 0.75}
difficulty: 5
prerequisites:
  book: [u-04-15-03, u-04-14-03]
  higher_algebra: [分式变形, 有理化, 对数恒等式]
  analytic_geometry: []
  python: [不要求]
capabilities: [proof, analytic_calculation, condition_checking, error_analysis]
learning_goals: [证明零比零型法则, 证明无穷比无穷型法则, 处理单侧与无穷远情形, 合法转化五类非基本未定式, 诊断机械套用错误]
content_standard: 2
```

- [ ] **Step 2: 分层证明 \(0/0\) 型**

定理 `{#thm-u-04-15-04-lhopital-zero-zero}` 先写右侧有限端点版本。若
\(f(x),g(x)\to0\)，在端点补定义 \(f(a)=g(a)=0\)，由极限得到单侧连续；对
\([a,x]\) 使用 Cauchy 比值形式。对任意足够靠近端点的 \(x\)，存在
\(c_x\in(a,x)\)，使

\[
\frac{f(x)}{g(x)}
=\frac{f'(c_x)}{g'(c_x)}.
\]

由 \(x\to a^+\) 推出 \(c_x\to a^+\)，完成有限值极限证明。\(x\to a^-\) 改变区间
方向；\(x\to+\infty\) 与 \(x\to-\infty\) 用 \(t=1/x\) 化为单侧有限端点，明确两个
导数中的 \(-1/t^2\) 因子抵消。正负无穷导数比用任意阈值 \(M\) 的不等式版本单独
证明，不把扩展实数当作普通实数代数运算。

所有版本写明相应去心邻域内 \(f,g\) 可导、\(g(x)\ne0\)，使用比值形式时
\(g'(x)\ne0\)。

- [ ] **Step 3: 单独证明 \(\infty/\infty\) 型**

定理 `{#thm-u-04-15-04-lhopital-infinity-infinity}` 不复用“端点补零”证明。右侧
有限端点情形先选固定 \(x_0\)；对 \(x\) 与 \(x_0\) 之间区间使用 Cauchy，控制

\[
\frac{f(x)-f(x_0)}{g(x)-g(x_0)}.
\]

再使用恒等式
\[
\frac{f(x)}{g(x)}
=
\frac{f(x)-f(x_0)}{g(x)-g(x_0)}
\cdot
\frac{g(x)-g(x_0)}{g(x)}
+\frac{f(x_0)}{g(x)}.
\]
分别证明第二个因子趋于 \(1\)、最后一项趋于 \(0\)。这样不在误差项中重新引入尚待
证明极限的 \(f(x)/g(x)\)。单侧和无穷远版本分别说明 \(x_0\) 的选择方向；有限极限
与正负无穷极限分别用 \(\varepsilon\) 或阈值不等式完成。

- [ ] **Step 4: 完整展开五类非基本未定式**

每个主线例固定写出“识别形式 → 合法转化 → 核验条件 → 应用法则 → 还原结论”：

1. \(0\cdot\infty\)：
   \[
   x\ln x=\frac{\ln x}{1/x}\longrightarrow0\qquad(x\to0^+).
   \]
2. \(\infty-\infty\)：
   \[
   \frac1{e^x-1}-\frac1x
   =\frac{x-(e^x-1)}{x(e^x-1)}
   \longrightarrow-\frac12\qquad(x\to0).
   \]
   每次使用 L’Hôpital 前重新验证仍为 \(0/0\)。
3. \(1^\infty\)：
   \[
   \left(1+\frac1x\right)^x\longrightarrow e\qquad(x\to+\infty).
   \]
4. \(0^0\)：
   \[
   x^x\longrightarrow1\qquad(x\to0^+).
   \]
5. \(\infty^0\)：
   \[
   x^{1/x}\longrightarrow1\qquad(x\to+\infty).
   \]

后三类合并在稳定例 `{#ex-u-04-15-04-power-forms}`，统一令
\(y=u(x)^{v(x)}\)，在底数“去心邻域内为正”后研究
\(\ln y=v(x)\ln u(x)\)，最后用指数函数连续性还原。

- [ ] **Step 5: 写清失败边界和 v2 结构**

至少包含：

- \(f(x)=x+\sin x,\ g(x)=x\) 在 \(x\to+\infty\) 时原商趋于 1，但导数之比
  \(1+\cos x\) 没有极限；
- 一个“非未定式”机械求导得到错误结论的例子；
- 一个代数化简明显优于 L’Hôpital 的例子；
- 连续使用法则时“每一轮都重新核验”形式和条件。

本页例题数可以超过 2，但仍保留 2 个即时检验、5 道分层习题和 7 个页内折叠完整答案。

- [ ] **Step 6: 验证并提交 15.4**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest \
  tests.test_chapter_15.ChapterFifteenTests.test_lhopital_separates_forms_and_rechecks_conditions \
  tests.test_chapter_15.ChapterFifteenTests.test_lhopital_includes_one_sided_infinite_and_failure_cases \
  tests.test_chapter_15.ChapterFifteenTests.test_core_proofs_do_not_use_later_calculus -v
git add content/chapters/chapter-15/u-04-15-04-lhopital-rule.md
git commit -m "feat: establish L'Hopital rule and transformations"
```

### Task 6: 发布前内容审查与修复

**Files:**

- Review: `content/chapters/chapter-15/index.md`
- Review: `content/chapters/chapter-15/u-04-15-01-fermat-rolle-lagrange.md`
- Review: `content/chapters/chapter-15/u-04-15-02-monotonicity-darboux.md`
- Review: `content/chapters/chapter-15/u-04-15-03-cauchy-mean-value.md`
- Review: `content/chapters/chapter-15/u-04-15-04-lhopital-rule.md`
- Test: `tests/test_chapter_15.py`

- [ ] **Step 1: 数学正确性审查**

逐页核对：

- Fermat 是否正确处理左右差商符号；
- Rolle 非恒定情形是否真的得到内部极值；
- Lagrange 辅助函数的端点值与斜率计算是否一致；
- 单调性的充分条件、必要方向和严格性是否分开；
- Darboux 是否只用最值定理与 Fermat，没有假设导函数连续；
- Cauchy 交叉乘积是否先于除法，比值形式的两个分母是否已证明非零；
- \(0/0\) 与 \(\infty/\infty\) 是否使用各自合法的证明；
- 单侧、无穷远、有限极限与正负无穷的量词是否一致；
- 幂型未定式取对数前底数是否为正；
- 重复 L’Hôpital 是否逐轮核验；
- 例题、检验、习题和答案的定义域与趋近方向是否一致；
- 是否循环使用 Taylor、积分或级数。

- [ ] **Step 2: 自学可用性审查**

核对每页牵引问题是否在回望中闭合，证明障碍、路线、条件使用位置和反例是否明确，答案
是否解释关键转折，四页接口是否形成连续的证明阶梯。重点检查第 15.4 页是否因例题较多
而挤压两类 L’Hôpital 证明。

- [ ] **Step 3: 先补失败测试再修复可固化缺陷**

凡是可通过稳定文本、元数据或锚点冻结的问题，先在 `tests/test_chapter_15.py` 加入会失败
的具体断言，运行看到目标失败，再修改正文。运行：

```bash
python3.12 -m unittest tests.test_chapter_15 -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: 内容、构建、现有站点和格式检查通过；专项测试只允许因尚未发布导航、课程地图
和第四部总设计而失败。

- [ ] **Step 4: 提交审查修复**

```bash
git add tests/test_chapter_15.py content/chapters/chapter-15
git commit -m "fix: strengthen chapter fifteen content"
```

若没有文件变化，不创建空提交，但最终报告必须逐项列出审查结果。

### Task 7: 发布第 15 章并闭合站点合同

**Files:**

- Modify: `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md`
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_mkdocs_site.py`
- Test: `tests/test_chapter_15.py`
- Test: `tests/test_mkdocs_site.py`

- [ ] **Step 1: 先写站点失败测试**

在 `tests/test_mkdocs_site.py` 新增：

```python
    def test_checks_chapter_fifteen_cauchy_page(self) -> None:
        page = "chapters/chapter-15/u-04-15-03-cauchy-mean-value/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "thm-u-04-15-03-cauchy-cross",
                "cor-u-04-15-03-cauchy-ratio",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 15 章：微分中值定理",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )
```

Run:

```bash
python3.12 -m unittest \
  tests.test_mkdocs_site.ZensicalSiteValidationTests.test_checks_chapter_fifteen_cauchy_page -v
```

Expected: FAIL，原因是两个站点合同字典还没有第 15.3 页。

- [ ] **Step 2: 更新导航、课程地图和 README**

`mkdocs.yml` 在第 14 章后加入：

```yaml
      - 第 15 章：微分中值定理:
          - 本章导学: chapters/chapter-15/index.md
          - 15.1 两个端点的信息怎样迫使中间出现特殊切线？: chapters/chapter-15/u-04-15-01-fermat-rolle-lagrange.md
          - 15.2 导数符号能推出哪些整体性质？: chapters/chapter-15/u-04-15-02-monotonicity-darboux.md
          - 15.3 两个函数的变化率怎样进行严格比较？: chapters/chapter-15/u-04-15-03-cauchy-mean-value.md
          - 15.4 L’Hôpital 法则何时能判定未定式极限？: chapters/chapter-15/u-04-15-04-lhopital-rule.md
```

`content/course-map.md` 加入第 15 章锚点 `{#chapter-15}`、8.5 学时及四个精确链接，把
“后续路线”改为从第 16 章开始。`README.md` 把发布范围更新到第四部第 15 章，单元数
从 60 改为 64。

- [ ] **Step 3: 更新第四部正式设计**

在 `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md` 同步：

- 第 15 章导语改为理论 6.5、应用 2.0、合计 8.5；
- 四单元学时依次改为 `1.75+0.25`、`1.75+0.50`、`1.50+0.50`、
  `1.50+0.75`；
- 非基本未定式列表补齐 \(0^0\) 与 \(\infty^0\)；
- 学时闭合表改为第 15 章 `6.5 | 2.0 | 8.5`，第四部
  `25 | 10.5 | 35.5`。

- [ ] **Step 4: 更新真实站点检查**

向 `scripts/check_site.py` 加入：

```python
REQUIRED_RENDERED_ANCHORS[
    "chapters/chapter-15/u-04-15-03-cauchy-mean-value/index.html"
] = [
    "thm-u-04-15-03-cauchy-cross",
    "cor-u-04-15-03-cauchy-ratio",
]

REQUIRED_NAVIGATION_MARKERS[
    "chapters/chapter-15/u-04-15-03-cauchy-mean-value/index.html"
] = [
    "md-sidebar",
    "第四部：微分与局部线性化",
    "第 15 章：微分中值定理",
]
```

实际编辑时把键值直接写入现有两个字典，不在模块加载后做赋值。

- [ ] **Step 5: 运行专项和完整验收**

```bash
python3.12 -m unittest tests.test_chapter_15 tests.test_mkdocs_site -v
make verify
git diff --check
git status --short
```

Expected:

- 全量 `unittest` 至少为 74 个既有测试加第 15 章新增测试，最终为 `OK`；
- 内容检查无错误；
- `zensical build --strict` 报告 `No issues found`；
- 站点检查无错误；
- 第 15 章 5 个页面真实生成；
- README 报告 64 个学习单元；
- `site/` 不进入提交，状态中只出现计划内文件。

- [ ] **Step 6: 提交发布集成**

```bash
git add \
  docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md \
  mkdocs.yml content/course-map.md README.md \
  scripts/check_site.py tests/test_mkdocs_site.py
git commit -m "feat: publish chapter fifteen mean value theorems"
```

## 第 15 章完成检查

- [ ] 4 个核心单元全部达到 v2。
- [ ] 理论 6.5 + 应用 2.0 = 8.5 学时。
- [ ] Fermat、Rolle、Lagrange、Darboux 与 Cauchy 均有完整证明。
- [ ] Cauchy 交叉乘积先于有条件比值形式。
- [ ] L’Hôpital 的 \(0/0\) 与 \(\infty/\infty\) 分开证明。
- [ ] 单侧、无穷远、有限值和正负无穷情形均有明确条件。
- [ ] 五类非基本未定式全部进入主线并合法转化。
- [ ] 核心证明没有使用 Taylor、积分、级数或后续凸性工具。
- [ ] 发布前内容审查发现均已修复或明确记录。
- [ ] 导航、课程地图、README、第四部设计和真实站点一致。
- [ ] `make verify` 全量通过。
- [ ] 在此停止；第 16 章另写设计和实施计划。
