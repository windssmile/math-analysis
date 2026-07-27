# 第 16 章“Taylor 公式与余项” Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 发布第 16 章 4 个 `content_standard: 2` 单元，严格建立 Peano、Lagrange、Cauchy 三种有限阶余项，并提供经过测试的 Horner 求值、前向差分和中心差分算法。

**Architecture:** Markdown 正文是唯一教学内容来源，`tests/test_chapter_16.py` 先冻结单元、学时、证明条件、公式阶数和发布合同。正文按“局部渐近 → 可计算误差界 → 中值结构 → 可信近似”推进。独立的 `src/mathbook_examples/differentiation.py` 只负责有限多项式求值和无证书的数值差分；理论误差界留在调用者和正文中。正文、算法完成后先经过独立内容审查，再统一发布到 Zensical 导航和真实站点检查。

**Tech Stack:** Markdown、Python 3.12 标准库、`unittest`、PyYAML、Zensical 0.0.51、MathJax、现有 `make verify` 质量门。

---

## 文件结构

**新增**

- `content/chapters/chapter-16/index.md`：章节问题弧、7 学时路径、余项阶梯和范围边界。
- `content/chapters/chapter-16/u-04-16-01-peano-expansion.md`：Taylor 多项式、Peano 余项和系数唯一性。
- `content/chapters/chapter-16/u-04-16-02-lagrange-remainder.md`：Lagrange 余项、反复 Rolle 和误差预算。
- `content/chapters/chapter-16/u-04-16-03-cauchy-remainder.md`：Cauchy 余项及三种余项比较。
- `content/chapters/chapter-16/u-04-16-04-trusted-approximation.md`：阶数选择、Horner 与数值微分实验。
- `src/mathbook_examples/differentiation.py`：正式 Taylor 求值和差分实现。
- `tests/test_chapter_16.py`：结构、学时、条件、公式、证明边界和发布合同。
- `tests/test_differentiation.py`：算法行为、经验步长、数值稳定性和错误输入合同。

**修改**

- `mkdocs.yml`：在第 15 章之后加入第 16 章。
- `content/course-map.md`：加入第 16 章 7 学时及 4 个单元链接。
- `README.md`：学习单元数从 64 更新为 68，发布范围更新到第四部第 16 章。
- `tests/test_zensical_structure.py`：同步冻结 README 的 68 单元发布范围。
- `scripts/check_site.py`：加入 16.4 的 Horner 与中心差分稳定锚点。
- `tests/test_mkdocs_site.py`：冻结第 16 章真实站点合同。

第四部总量保持理论 25、应用 10.5、合计 35.5，不修改
`docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md` 的总学时。

## 固定单元合同

| 顺序 | ID | 文件后缀 | 标题 | 理论+应用 |
|---|---|---|---|---:|
| 16.1 | `u-04-16-01` | `peano-expansion` | 高阶局部信息怎样形成 Peano 展开？ | 1.25+0.50 |
| 16.2 | `u-04-16-02` | `lagrange-remainder` | Lagrange 余项怎样给出可计算误差界？ | 1.50+0.25 |
| 16.3 | `u-04-16-03` | `cauchy-remainder` | Cauchy 余项揭示了怎样的证明结构？ | 1.50+0.25 |
| 16.4 | `u-04-16-04` | `trusted-approximation` | 怎样把 Taylor 多项式变成可信的近似工具？ | 0.25+1.50 |

本章合计理论 4.5、应用 2.5，共 7 学时。四页全部执行 v2 合同：至少 2 个稳定例题、
2 个即时检验、5 道习题和 7 个折叠完整答案。

## 数学与算法合同

- 所有定理从任意中心 \(a\) 陈述，例题先从 Maclaurin 情形进入。
- Peano 使用展开点逐阶可导条件，不误加 \(f^{(n)}\) 连续或在整个去心邻域存在。
- Lagrange 与 Cauchy 使用连接 \(a,x\) 的开区间上直到 \(n+1\) 阶导数存在。
- 三种公式统一使用 \(P_n\) 和 \(R_n=f-P_n\)；Lagrange 分母为
  \((n+1)!\)，Cauchy 分母为 \(n!\)。
- `evaluate_taylor` 接受已除以阶乘的升幂系数，使用逆序 Horner，不返回误差证书。
- 差分函数默认使用
  \(\sqrt{\varepsilon}\max(1,|x|)\) 和
  \(\varepsilon^{1/3}\max(1,|x|)\)，返回实际步长，但不宣称最优或认证。
- 凸性、Newton 方法、无穷 Taylor 级数、解析函数和符号求导均不进入本章核心。

### Task 1: 用失败测试冻结第 16 章内容合同

**Files:**

- Create: `tests/test_chapter_16.py`
- Test: `tests/test_chapter_16.py`

- [ ] **Step 1: 写入单元、学时、路径和锚点常量**

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-16"

EXPECTED_UNITS = [
    (
        "u-04-16-01",
        "高阶局部信息怎样形成 Peano 展开？",
        1.25,
        0.50,
        "peano-expansion",
    ),
    (
        "u-04-16-02",
        "Lagrange 余项怎样给出可计算误差界？",
        1.50,
        0.25,
        "lagrange-remainder",
    ),
    (
        "u-04-16-03",
        "Cauchy 余项揭示了怎样的证明结构？",
        1.50,
        0.25,
        "cauchy-remainder",
    ),
    (
        "u-04-16-04",
        "怎样把 Taylor 多项式变成可信的近似工具？",
        0.25,
        1.50,
        "trusted-approximation",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-16-01": (
        "def-u-04-16-01-taylor-polynomial",
        "thm-u-04-16-01-peano",
        "thm-u-04-16-01-uniqueness",
    ),
    "u-04-16-02": (
        "thm-u-04-16-02-lagrange-remainder",
        "cor-u-04-16-02-error-bound",
        "ex-u-04-16-02-order-budget",
    ),
    "u-04-16-03": (
        "thm-u-04-16-03-cauchy-remainder",
        "tbl-u-04-16-03-remainder-comparison",
    ),
    "u-04-16-04": (
        "alg-u-04-16-04-horner",
        "alg-u-04-16-04-centered-difference",
        "ex-u-04-16-04-step-study",
    ),
}

FORBIDDEN_CORE_TERMS = ("凸函数", "Newton 方法", "无穷 Taylor 级数", "解析函数")


def unit_path(unit: tuple[str, str, float, float, str]) -> Path:
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text
```

- [ ] **Step 2: 写入结构、顺序和发布范围测试**

`ChapterSixteenTests` 至少实现：

```python
class ChapterSixteenTests(unittest.TestCase):
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
        self.assertEqual(4.5, theory)
        self.assertEqual(2.5, applied)

    def test_chapter_guide_lists_units_hours_and_boundaries(self) -> None:
        guide_path = CHAPTER / "index.md"
        self.assertTrue(guide_path.is_file(), "missing chapter guide")
        guide = guide_path.read_text(encoding="utf-8")
        self.assertIn("本章共4个核心单元，7学时（理论4.5，应用2.5）。", guide)
        self.assertIn("第 17 章", guide)
        self.assertIn("有限阶 Taylor 公式不等于无穷 Taylor 级数", guide)
        for unit in EXPECTED_UNITS:
            unit_id, title, _theory, _applied, suffix = unit
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_navigation_course_map_and_readme_use_final_order(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("本章学时：7 小时（理论 4.5，应用 2.5）。", course_map)
        self.assertIn("第四部第 16 章，共 68 个学习单元", readme)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-16/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)

    def test_core_does_not_use_later_topics(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)
```

- [ ] **Step 3: 写入条件和公式防回归测试**

```python
    def test_peano_uses_pointwise_recursive_differentiability(self) -> None:
        text = unit_path(EXPECTED_UNITS[0]).read_text(encoding="utf-8")
        for marker in (
            "不要求最高阶导函数在展开点连续",
            r"G'(t)=o\!\left((t-a)^{n-1}\right)",
            r"|\xi-a|\le |x-a|",
            r"c_k=\frac{f^{(k)}(a)}{k!}",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("假设最高阶导函数连续", text)

    def test_lagrange_remainder_has_correct_order_and_interval_bound(self) -> None:
        text = unit_path(EXPECTED_UNITS[1]).read_text(encoding="utf-8")
        for marker in (
            r"R_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}",
            r"|R_n(x)|\le\frac{M}{(n+1)!}|x-a|^{n+1}",
            "包含连接 \(a\) 与 \(x\) 的闭线段",
            "不要求最高阶导函数连续",
            "最低阶数",
        ):
            self.assertIn(marker, text)

    def test_cauchy_remainder_has_correct_cancellation_and_factorial(self) -> None:
        text = unit_path(EXPECTED_UNITS[2]).read_text(encoding="utf-8")
        for marker in (
            r"\Phi'(t)=-\frac{f^{(n+1)}(t)}{n!}(x-t)^n",
            r"R_n(x)=\frac{f^{(n+1)}(\xi)}{n!}(x-\xi)^n(x-a)",
            "分母函数的导数恒为 \(-1\)",
            "中间点一般不同",
            "不能无条件互换",
        ):
            self.assertIn(marker, text)

    def test_numerical_error_orders_keep_their_smoothness_conditions(self) -> None:
        text = unit_path(EXPECTED_UNITS[3]).read_text(encoding="utf-8")
        for marker in (
            "二阶导数存在并有界",
            r"f'(x)+O(h)",
            "三阶导数存在并有界",
            r"f'(x)+O(h^2)",
            "经验步长不提供误差证书",
            "不能倒过来证明函数可导",
        ):
            self.assertIn(marker, text)
```

- [ ] **Step 4: 验证 RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_16 -v
```

Expected: FAIL，原因是第 16 章正文和发布条目尚不存在；不能出现测试文件自身的语法或
导入错误。

- [ ] **Step 5: 提交内容合同测试**

```bash
git add tests/test_chapter_16.py
git commit -m "test: define chapter sixteen Taylor contract"
```

### Task 2: 用 TDD 实现 Taylor 多项式求值

**Files:**

- Create: `tests/test_differentiation.py`
- Create: `src/mathbook_examples/differentiation.py`
- Test: `tests/test_differentiation.py`

- [ ] **Step 1: 写入 Horner 正常行为测试**

```python
from math import e, inf, isclose, nan
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.differentiation import evaluate_taylor


class TaylorEvaluationTest(unittest.TestCase):
    def test_evaluates_constant_and_ascending_power_coefficients(self) -> None:
        self.assertEqual(3.5, evaluate_taylor([3.5], 2.0, -7.0))
        self.assertEqual(17.0, evaluate_taylor([1.0, 2.0, 3.0], 0.0, 2.0))

    def test_evaluates_about_a_nonzero_center(self) -> None:
        self.assertEqual(3.0, evaluate_taylor([1.0, -2.0, 4.0], 2.0, 3.0))

    def test_uses_coefficients_that_already_include_factorials(self) -> None:
        approximation = evaluate_taylor([1.0, 1.0, 0.5, 1 / 6], 0.0, 1.0)
        self.assertTrue(isclose(approximation, 8 / 3, rel_tol=0.0, abs_tol=1e-15))
        self.assertLess(abs(approximation - e), 0.052)
```

- [ ] **Step 2: 写入输入和溢出测试**

```python
    def test_rejects_empty_or_nonfinite_coefficients(self) -> None:
        with self.assertRaisesRegex(ValueError, "^coefficients must not be empty$"):
            evaluate_taylor([], 0.0, 1.0)
        for coefficient in (nan, inf, -inf):
            with self.subTest(coefficient=coefficient):
                with self.assertRaisesRegex(ValueError, "^coefficient 1 must be finite$"):
                    evaluate_taylor([1.0, coefficient], 0.0, 1.0)

    def test_rejects_nonfinite_center_and_point(self) -> None:
        for center in (nan, inf, -inf):
            with self.subTest(center=center):
                with self.assertRaisesRegex(ValueError, "^center must be finite$"):
                    evaluate_taylor([1.0], center, 0.0)
        for point in (nan, inf, -inf):
            with self.subTest(point=point):
                with self.assertRaisesRegex(ValueError, "^point must be finite$"):
                    evaluate_taylor([1.0], 0.0, point)

    def test_rejects_nonfinite_horner_intermediate(self) -> None:
        with self.assertRaisesRegex(ValueError, "^Taylor evaluation must remain finite$"):
            evaluate_taylor([1e308, 1e308], 0.0, 2.0)
```

- [ ] **Step 3: 验证 RED**

Run:

```bash
python3.12 -m unittest tests.test_differentiation.TaylorEvaluationTest -v
```

Expected: ERROR，明确为 `mathbook_examples.differentiation` 尚不存在。

- [ ] **Step 4: 写出最小 Horner 实现**

```python
"""Finite Taylor evaluation and uncertified numerical differentiation."""

from collections.abc import Sequence
from math import isfinite


def _require_finite(value: float, label: str) -> float:
    converted = float(value)
    if not isfinite(converted):
        raise ValueError(f"{label} must be finite")
    return converted


def evaluate_taylor(
    coefficients: Sequence[float], center: float, point: float
) -> float:
    """Evaluate ascending-power Taylor coefficients by reverse Horner steps.

    ``coefficients[k]`` is the coefficient of ``(point - center) ** k`` and
    therefore already includes any factorial denominator.  This function does
    not certify the Taylor remainder.
    """
    if not coefficients:
        raise ValueError("coefficients must not be empty")
    center_value = _require_finite(center, "center")
    point_value = _require_finite(point, "point")
    finite_coefficients = []
    for index, coefficient in enumerate(coefficients):
        finite_coefficients.append(_require_finite(coefficient, f"coefficient {index}"))

    offset = point_value - center_value
    if not isfinite(offset):
        raise ValueError("Taylor evaluation must remain finite")
    value = finite_coefficients[-1]
    for coefficient in reversed(finite_coefficients[:-1]):
        value = value * offset + coefficient
        if not isfinite(value):
            raise ValueError("Taylor evaluation must remain finite")
    return value
```

- [ ] **Step 5: 验证 GREEN 并提交**

```bash
python3.12 -m unittest tests.test_differentiation.TaylorEvaluationTest -v
git add tests/test_differentiation.py src/mathbook_examples/differentiation.py
git commit -m "feat: evaluate finite Taylor polynomials"
```

### Task 3: 用 TDD 实现前向和中心差分

**Files:**

- Modify: `tests/test_differentiation.py`
- Modify: `src/mathbook_examples/differentiation.py`
- Test: `tests/test_differentiation.py`

- [ ] **Step 1: 写入结果对象、显式步长和精度测试**

先把测试文件的 `math` 导入扩展为：

```python
from dataclasses import FrozenInstanceError
from math import e, exp, inf, isclose, nan, sqrt
```

并把正式模块导入扩展为：

```python
from mathbook_examples.differentiation import (
    DifferenceEstimate,
    centered_difference,
    evaluate_taylor,
    forward_difference,
)
```

然后加入：

```python
class DifferenceTest(unittest.TestCase):
    def test_returns_frozen_result_with_method_and_explicit_step(self) -> None:
        result = forward_difference(lambda x: x * x, 2.0, step=1e-5)
        self.assertIsInstance(result, DifferenceEstimate)
        self.assertEqual("forward", result.method)
        self.assertEqual(1e-5, result.step)
        self.assertLess(abs(result.value - 4.0), 2e-5)
        with self.assertRaisesRegex(FrozenInstanceError, "cannot assign to field"):
            result.value = 0.0  # type: ignore[misc]

    def test_centered_difference_is_accurate_for_a_smooth_function(self) -> None:
        result = centered_difference(exp, 0.0, step=1e-4)
        self.assertEqual("centered", result.method)
        self.assertLess(abs(result.value - 1.0), 2e-9)

    def test_result_has_no_certificate_fields(self) -> None:
        result = centered_difference(exp, 0.0)
        self.assertFalse(hasattr(result, "error_bound"))
        self.assertFalse(hasattr(result, "certified"))
```

- [ ] **Step 2: 写入默认经验步长的精确规则测试**

```python
    def test_automatic_steps_follow_the_documented_rules(self) -> None:
        scale = 3.0
        forward = forward_difference(lambda x: x * x, -scale)
        centered = centered_difference(lambda x: x * x, -scale)
        self.assertEqual(sqrt(sys.float_info.epsilon) * scale, forward.step)
        self.assertEqual(sys.float_info.epsilon ** (1 / 3) * scale, centered.step)
        self.assertEqual(sqrt(sys.float_info.epsilon), forward_difference(exp, 0.25).step)

    def test_documentation_calls_defaults_uncertified_heuristics(self) -> None:
        module_doc = sys.modules[forward_difference.__module__].__doc__ or ""
        for text in (
            module_doc,
            forward_difference.__doc__ or "",
            centered_difference.__doc__ or "",
        ):
            self.assertIn("heuristic", text)
            self.assertIn("not an error certificate", text)
```

- [ ] **Step 3: 写入边界输入和异常传播测试**

```python
    def test_rejects_nonfinite_point_and_invalid_explicit_step(self) -> None:
        for point in (nan, inf, -inf):
            with self.subTest(point=point):
                with self.assertRaisesRegex(ValueError, "^point must be finite$"):
                    forward_difference(exp, point)
        for step in (0.0, -1.0, nan, inf, -inf):
            with self.subTest(step=step):
                with self.assertRaisesRegex(
                    ValueError, "^step must be positive and finite$"
                ):
                    centered_difference(exp, 0.0, step=step)

    def test_rejects_nonfinite_sample_points_and_function_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "^sample point must be finite$"):
            forward_difference(lambda x: x, 1e308, step=1e308)
        for output in (nan, inf, -inf):
            with self.subTest(output=output):
                with self.assertRaisesRegex(ValueError, "^function value must be finite$"):
                    centered_difference(lambda _x, value=output: value, 0.0)

    def test_preserves_function_domain_exceptions(self) -> None:
        def unavailable(_x: float) -> float:
            raise RuntimeError("domain unavailable")

        with self.assertRaisesRegex(RuntimeError, "^domain unavailable$"):
            forward_difference(unavailable, 0.0)
```

- [ ] **Step 4: 验证 RED**

Run:

```bash
python3.12 -m unittest tests.test_differentiation.DifferenceTest -v
```

Expected: FAIL/ERROR，原因是差分对象和函数尚未实现。

- [ ] **Step 5: 写出最小差分实现**

先把模块导入扩展为：

```python
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from math import isfinite
import sys
```

再加入：

```python
@dataclass(frozen=True)
class DifferenceEstimate:
    """An uncertified finite-difference estimate."""

    value: float
    step: float
    method: str


def _difference_step(point: float, step: float | None, power: float) -> float:
    if step is not None:
        step_value = float(step)
        if not isfinite(step_value) or step_value <= 0:
            raise ValueError("step must be positive and finite")
        return step_value
    return sys.float_info.epsilon**power * max(1.0, abs(point))


def _sample(function: Callable[[float], float], point: float) -> float:
    if not isfinite(point):
        raise ValueError("sample point must be finite")
    value = float(function(point))
    if not isfinite(value):
        raise ValueError("function value must be finite")
    return value


def forward_difference(
    function: Callable[[float], float], point: float, *, step: float | None = None
) -> DifferenceEstimate:
    """Use a heuristic step for an estimate, not an error certificate."""
    point_value = _require_finite(point, "point")
    step_value = _difference_step(point_value, step, 0.5)
    right = point_value + step_value
    value = (_sample(function, right) - _sample(function, point_value)) / step_value
    if not isfinite(value):
        raise ValueError("difference estimate must be finite")
    return DifferenceEstimate(value, step_value, "forward")


def centered_difference(
    function: Callable[[float], float], point: float, *, step: float | None = None
) -> DifferenceEstimate:
    """Use a heuristic step for an estimate, not an error certificate."""
    point_value = _require_finite(point, "point")
    step_value = _difference_step(point_value, step, 1 / 3)
    right = point_value + step_value
    left = point_value - step_value
    value = (_sample(function, right) - _sample(function, left)) / (2 * step_value)
    if not isfinite(value):
        raise ValueError("difference estimate must be finite")
    return DifferenceEstimate(value, step_value, "centered")
```

同时把模块文档改为包含原文：

```python
"""Finite Taylor tools with heuristic differences, not an error certificate."""
```

- [ ] **Step 6: 运行算法全测并提交**

```bash
python3.12 -m unittest tests.test_differentiation -v
git diff --check
git add tests/test_differentiation.py src/mathbook_examples/differentiation.py
git commit -m "feat: add heuristic finite differences"
```

### Task 4: 完成章导学与 16.1 Peano 展开

**Files:**

- Create: `content/chapters/chapter-16/index.md`
- Create: `content/chapters/chapter-16/u-04-16-01-peano-expansion.md`
- Test: `tests/test_chapter_16.py`

- [ ] **Step 1: 创建章导学页**

```markdown
---
title: 第 16 章：Taylor 公式与余项
---

# 第 16 章：Taylor 公式与余项 {#chapter-16}
```

章导学逐项列出 4 个单元与 4.5 + 2.5 = 7 学时，呈现
Peano → Lagrange → Cauchy → 可信数值近似的问题阶梯。边界段原文写明
“有限阶 Taylor 公式不等于无穷 Taylor 级数”，并把凸性和 Newton 方法留到第 17 章。

- [ ] **Step 2: 写入 16.1 元数据**

```yaml
title: 高阶局部信息怎样形成 Peano 展开？
unit_id: u-04-16-01
hours: {theory: 1.25, applied: 0.50}
difficulty: 4
prerequisites:
  book: [u-04-13-03, u-04-14-03, u-04-15-01]
  higher_algebra: [多项式, 阶乘, 最低次项比较]
  analytic_geometry: [局部多项式近似]
  python: [不要求]
capabilities: [proof, asymptotic_reasoning, analytic_calculation, condition_checking]
learning_goals: [构造任意中心 Taylor 多项式, 证明 Peano 余项, 证明系数唯一性, 判断逐阶可导条件]
content_standard: 2
```

- [ ] **Step 3: 写出递归条件和 Peano 归纳证明**

定义 `{#def-u-04-16-01-taylor-polynomial}` 后，把“直到 \(n\) 阶可导结构”递归展开：

- \(n=1\) 时在 \(a\) 可导；
- \(n\ge2\) 时，\(f'\) 在 \(a\) 的某个邻域存在，并在 \(a\) 具有直到
  \(n-1\) 阶可导结构；
- 明确“不要求最高阶导函数在展开点连续”。

定理 `{#thm-u-04-16-01-peano}` 使用归纳。令 \(G=f-P_n\)，先从归纳假设得到

\[
G'(t)=o\!\left((t-a)^{n-1}\right),
\]

再对 \(a,x\) 之间使用 Lagrange：

\[
G(x)=G'(\xi)(x-a).
\]

用 \(|\xi-a|\le |x-a|\) 同时覆盖 \(x>a\) 与 \(x<a\)，得
\(G(x)=o((x-a)^n)\)。逐项指出递归条件如何保证中值定理合法。

- [ ] **Step 4: 证明系数唯一性并完成 v2 结构**

定理 `{#thm-u-04-16-01-uniqueness}` 先调用标准 Peano 展开，再比较两个展开；若最低
次非零差系数为第 \(j\) 项，除以 \(h^j\) 后左侧趋于非零常数、右侧趋于零，矛盾。
写出

\[
c_k=\frac{f^{(k)}(a)}{k!}.
\]

稳定例题至少包含 \(e^x,\sin x\) 的 Maclaurin 展开和一个局部极限；边界例说明高阶
导数不存在时不能继续。2 个检验与 5 道习题覆盖非零中心、阶数判断、系数唯一性、
Peano 求极限和“不能给定点误差证书”，提供 7 个折叠完整答案。

- [ ] **Step 5: 验证并提交 16.1**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest \
  tests.test_chapter_16.ChapterSixteenTests.test_peano_uses_pointwise_recursive_differentiability \
  tests.test_chapter_16.ChapterSixteenTests.test_core_does_not_use_later_topics -v
git add content/chapters/chapter-16
git commit -m "feat: establish Peano Taylor expansion"
```

### Task 5: 完成 16.2 Lagrange 余项与误差预算

**Files:**

- Create: `content/chapters/chapter-16/u-04-16-02-lagrange-remainder.md`
- Test: `tests/test_chapter_16.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: Lagrange 余项怎样给出可计算误差界？
unit_id: u-04-16-02
hours: {theory: 1.50, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-04-16-01, u-04-15-01, u-04-14-03]
  higher_algebra: [多项式求导, 阶乘, 不等式]
  analytic_geometry: [局部近似]
  python: [不要求]
capabilities: [proof, proof_strategy, error_analysis, analytic_calculation]
learning_goals: [证明 Lagrange 余项, 追踪反复 Rolle 的条件, 建立高阶导数误差界, 由误差预算选择最低阶数]
content_standard: 2
```

- [ ] **Step 2: 用反复 Rolle 完整证明余项**

定理 `{#thm-u-04-16-02-lagrange-remainder}` 对固定 \(x\ne a\)，要求 \(f\) 在
“包含连接 \(a\) 与 \(x\) 的闭线段”的开区间内具有直到 \(n+1\) 阶导数，并明确
“不要求最高阶导函数连续”。令

\[
R=f(x)-P_n(x),\qquad
F(t)=f(t)-P_n(t)-R\left(\frac{t-a}{x-a}\right)^{n+1}.
\]

逐项核验 \(F(a)=F(x)=0\) 及 \(F^{(k)}(a)=0\ (1\le k\le n)\)。逐轮列出 Rolle
产生的零点和下一阶导函数的两个零点，最后得到严格位于两端之间的 \(\xi\) 和

\[
R_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}.
\]

- [ ] **Step 3: 建立误差界并完成最低阶数例题**

推论 `{#cor-u-04-16-02-error-bound}` 写出

\[
|R_n(x)|\le\frac{M}{(n+1)!}|x-a|^{n+1}.
\]

每次写清 \(M\) 控制的具体闭线段。稳定例 `{#ex-u-04-16-02-order-budget}` 对
\(e^x\) 或 \(\sin x\) 从 \(n=0\) 开始逐阶验证不等式，停止在第一个满足目标误差的
阶数，并检查前一阶确实不满足，从而证明“最低阶数”。第二个稳定例从已知阶数算上界。

- [ ] **Step 4: 完成 v2 结构并验证提交**

2 个即时检验和 5 道习题覆盖辅助函数零点、反复 Rolle、区间导数界、阶数选择和
“未知 \(\xi\) 不能直接计算”，提供 7 个折叠完整答案。

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest \
  tests.test_chapter_16.ChapterSixteenTests.test_lagrange_remainder_has_correct_order_and_interval_bound \
  tests.test_chapter_16.ChapterSixteenTests.test_core_does_not_use_later_topics -v
git add content/chapters/chapter-16/u-04-16-02-lagrange-remainder.md
git commit -m "feat: prove Lagrange remainder and error bounds"
```

### Task 6: 完成 16.3 Cauchy 余项与比较

**Files:**

- Create: `content/chapters/chapter-16/u-04-16-03-cauchy-remainder.md`
- Test: `tests/test_chapter_16.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: Cauchy 余项揭示了怎样的证明结构？
unit_id: u-04-16-03
hours: {theory: 1.50, applied: 0.25}
difficulty: 5
prerequisites:
  book: [u-04-16-02, u-04-15-03, u-04-14-03]
  higher_algebra: [求和记号, 乘积求导, 逐项抵消]
  analytic_geometry: []
  python: [不要求]
capabilities: [proof, proof_strategy, formula_comparison, condition_checking]
learning_goals: [构造 Cauchy 余项辅助函数, 验证逐项抵消, 证明 Cauchy 余项, 比较三种余项的条件与用途]
content_standard: 2
```

- [ ] **Step 2: 展开抵消并证明 Cauchy 余项**

定理 `{#thm-u-04-16-03-cauchy-remainder}` 使用与 16.2 相同的区间条件。固定 \(x\)，
构造

\[
\Phi(t)=f(x)-\sum_{k=0}^{n}\frac{f^{(k)}(t)}{k!}(x-t)^k.
\]

先把 \(k=0,1,2\) 项的导数相邻写出，让
\(f'(t), f''(t)(x-t),\ldots\) 的正负项可见，再归纳到

\[
\Phi'(t)=-\frac{f^{(n+1)}(t)}{n!}(x-t)^n.
\]

核验 \(\Phi(a)=R_n(x),\Phi(x)=0\)。对 \(\Phi(t)\) 与 \(x-t\) 使用 Cauchy
中值定理，原文说明“分母函数的导数恒为 \(-1\)”，得到

\[
R_n(x)=\frac{f^{(n+1)}(\xi)}{n!}(x-\xi)^n(x-a).
\]

- [ ] **Step 3: 建立正式比较表与边界**

比较表锚点 `{#tbl-u-04-16-03-remainder-comparison}` 必须逐行包含：

- Peano：展开点逐阶可导；\(o((x-a)^n)\)；局部渐近；
- Lagrange：连接区间 \(n+1\) 阶可导；\((n+1)!\) 形式；直接误差界；
- Cauchy：同样的区间条件；\(n!\) 与 \((x-\xi)^n(x-a)\)；中值结构。

正文原文包含“三种余项不能无条件互换”“中间点一般不同”，并说明 Cauchy 公式不是
Lagrange 公式的简单代数变形。

- [ ] **Step 4: 完成 v2 结构并验证提交**

稳定例一用一个低阶多项式逐项核对抵消；稳定例二在同一函数上并列三种结论，指出各自
能回答和不能回答的问题。2 个检验与 5 道习题覆盖符号、阶乘、\(\xi\) 位置、条件比较
和错误互换，提供 7 个折叠完整答案。

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest \
  tests.test_chapter_16.ChapterSixteenTests.test_cauchy_remainder_has_correct_cancellation_and_factorial \
  tests.test_chapter_16.ChapterSixteenTests.test_core_does_not_use_later_topics -v
git add content/chapters/chapter-16/u-04-16-03-cauchy-remainder.md
git commit -m "feat: prove and compare Cauchy remainder"
```

### Task 7: 完成 16.4 可信近似与算法实验

**Files:**

- Create: `content/chapters/chapter-16/u-04-16-04-trusted-approximation.md`
- Modify: `tests/test_chapter_16.py`
- Test: `tests/test_chapter_16.py`
- Test: `tests/test_differentiation.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: 怎样把 Taylor 多项式变成可信的近似工具？
unit_id: u-04-16-04
hours: {theory: 0.25, applied: 1.50}
difficulty: 3
prerequisites:
  book: [u-04-16-02, u-04-16-03]
  higher_algebra: [多项式嵌套, 误差不等式]
  analytic_geometry: [割线斜率与切线斜率]
  python: [函数, 列表, 循环, 浮点数]
capabilities: [algorithmic_thinking, numerical_experiment, error_analysis, interpretation]
learning_goals: [按误差预算选择阶数, 用 Horner 计算 Taylor 多项式, 比较前向和中心差分, 解释截断误差与舍入误差]
content_standard: 2
```

- [ ] **Step 2: 按统一故事写误差预算与 Horner**

正文顺序固定为：

```text
问题来源 → 数学转化 → 算法思想 → 误差与适用条件
→ 伪代码 → Python → 结果解释
```

先复用 16.2 的误差预算选择最低阶数，再把
`coefficients[k] = f^(k)(a) / k!` 的升幂合同写清。算法锚点
`{#alg-u-04-16-04-horner}` 只展示逆序 Horner 伪代码，并引用
`src/mathbook_examples/differentiation.py` 的 `evaluate_taylor`；不得复制第二份 Python
实现。比较理论上界与真实误差，明确上界通常不等于实际误差。

- [ ] **Step 3: 推出差分误差阶并运行步长实验**

在“二阶导数存在并有界”条件下推出前向差分
\(f'(x)+O(h)\)；在“三阶导数存在并有界”条件下，对两侧 Taylor 式相减推出中心差分
\(f'(x)+O(h^2)\)。锚点 `{#alg-u-04-16-04-centered-difference}` 对应中心差分伪代码
和正式接口引用。

实验 `{#ex-u-04-16-04-step-study}` 对 `exp` 或 `sin` 使用一列递减步长，并调用正式
`forward_difference`、`centered_difference` 生成结果表。比较自动经验步长和至少两个
显式步长，指出误差通常先下降后因相消、舍入上升。原文写明“经验步长不提供误差证书”
和“不能倒过来证明函数可导”，不得称经验规则为最优。

- [ ] **Step 4: 完成 v2 结构**

两个稳定例分别为完整误差预算—Horner 流程和步长实验。2 个即时检验与 5 道习题覆盖
系数顺序、Horner 手算、误差界解释、差分阶数条件、自动步长边界，提供 7 个折叠完整
答案。页面说明结果对象只有 `value`、`step`、`method`，没有证书字段。

- [ ] **Step 5: 增加正文与正式实现不漂移的断言**

在 `test_numerical_error_orders_keep_their_smoothness_conditions` 中再加入：

```python
        for marker in (
            "evaluate_taylor",
            "forward_difference",
            "centered_difference",
            "DifferenceEstimate",
            "src/mathbook_examples/differentiation.py",
        ):
            self.assertIn(marker, text)
```

- [ ] **Step 6: 验证并提交 16.4**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_differentiation -v
python3.12 -m unittest \
  tests.test_chapter_16.ChapterSixteenTests.test_numerical_error_orders_keep_their_smoothness_conditions -v
git add tests/test_chapter_16.py content/chapters/chapter-16/u-04-16-04-trusted-approximation.md
git commit -m "feat: connect Taylor bounds to numerical differentiation"
```

### Task 8: 发布前内容、数学与算法审查

**Files:**

- Review: `content/chapters/chapter-16/index.md`
- Review: `content/chapters/chapter-16/u-04-16-01-peano-expansion.md`
- Review: `content/chapters/chapter-16/u-04-16-02-lagrange-remainder.md`
- Review: `content/chapters/chapter-16/u-04-16-03-cauchy-remainder.md`
- Review: `content/chapters/chapter-16/u-04-16-04-trusted-approximation.md`
- Review: `src/mathbook_examples/differentiation.py`
- Test: `tests/test_chapter_16.py`
- Test: `tests/test_differentiation.py`

- [ ] **Step 1: 数学正确性审查**

逐项核对并记录结果：

1. \(P_n,R_n\) 的阶数约定在四页一致；
2. Peano 递归条件足够支持归纳，且没有误加最高阶导函数连续；
3. Peano 的 \(|\xi-a|\le|x-a|\) 同时覆盖左右趋近；
4. 系数唯一性确实使用 \(o(h^n)\) 和逐阶可导条件；
5. Lagrange 辅助函数在 \(a,x\) 的零点及 \(a\) 处前 \(n\) 阶零点正确；
6. 每次 Rolle 前都有连续、可导和两个零点；
7. Lagrange 公式使用 \(f^{(n+1)}\)、\((n+1)!\) 和 \((x-a)^{n+1}\)；
8. Cauchy 逐项抵消的符号、\(n!\) 和 \((x-\xi)^n(x-a)\) 正确；
9. Cauchy 中值定理的分母导数为 \(-1\)，不存在除零；
10. 每个导数界 \(M\) 都绑定具体区间，最低阶例检查前一阶；
11. 前向 \(O(h)\) 与中心 \(O(h^2)\) 都附带相应光滑条件；
12. 有限阶公式没有被偷换为无穷 Taylor 级数。

- [ ] **Step 2: 算法合同与数值边界审查**

核对：

- 系数为升幂且已含阶乘，Horner 从最高次向下；
- 空序列、非有限输入、非有限中间值均拒绝；
- 默认步长公式和 `max(1, abs(point))` 完全一致；
- 显式正有限步长覆盖默认值；
- 非有限采样点和函数值被拒绝，函数自身其他异常原样传播；
- 结果对象不可变且仅有 `value`、`step`、`method`；
- 文档和正文都不把经验步长称为最优或误差证书；
- 稳定精度测试使用误差容限，不冻结无意义的浮点尾数。

- [ ] **Step 3: 自学与渲染预审**

逐页核对牵引问题在回望中闭合，证明障碍、路线、条件使用位置和迁移边界明确；所有例题、
检验、习题和折叠答案的定义域、展开中心、阶数和数值一致。运行：

```bash
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: 内容、构建和已有站点合同通过；此时第 16 章尚未进入导航是预期状态。

- [ ] **Step 4: 对发现的可固化缺陷先 RED 后 GREEN**

对每个可由稳定文本、元数据、API 或锚点冻结的问题：

1. 先在 `tests/test_chapter_16.py` 或 `tests/test_differentiation.py` 增加精确断言；
2. 运行对应单测并看到目标失败；
3. 修复正文或算法；
4. 重跑专项测试和 `git diff --check`。

- [ ] **Step 5: 提交审查修复**

```bash
python3.12 -m unittest tests.test_chapter_16 tests.test_differentiation -v
python3.12 scripts/check_content.py
git diff --check
git add tests/test_chapter_16.py tests/test_differentiation.py \
  content/chapters/chapter-16 src/mathbook_examples/differentiation.py
git commit -m "fix: strengthen chapter sixteen content and algorithms"
```

若没有文件变化，不创建空提交；但最终报告必须逐项给出审查结论。

### Task 9: 发布第 16 章并闭合真实站点合同

**Files:**

- Modify: `tests/test_mkdocs_site.py`
- Modify: `tests/test_zensical_structure.py`
- Modify: `scripts/check_site.py`
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Test: `tests/test_chapter_16.py`
- Test: `tests/test_mkdocs_site.py`
- Test: `tests/test_zensical_structure.py`

- [ ] **Step 1: 先写站点和 README 失败测试**

在 `tests/test_mkdocs_site.py` 加入：

```python
    def test_checks_chapter_sixteen_trusted_approximation_page(self) -> None:
        page = "chapters/chapter-16/u-04-16-04-trusted-approximation/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "alg-u-04-16-04-horner",
                "alg-u-04-16-04-centered-difference",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 16 章：Taylor 公式与余项",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )
```

把 `tests/test_zensical_structure.py` 的 README 断言改为：

```python
self.assertIn("第四部第 16 章，共 68 个学习单元", readme)
```

Run:

```bash
python3.12 -m unittest \
  tests.test_mkdocs_site.ZensicalSiteValidationTests.test_checks_chapter_sixteen_trusted_approximation_page \
  tests.test_zensical_structure.ZensicalStructureTests.test_readme_uses_zensical_commands_and_current_release_scope -v
```

Expected: FAIL，分别因为 `scripts/check_site.py` 尚无第 16 章合同、README 仍为 64 单元。

- [ ] **Step 2: 更新站点检查器**

在 `scripts/check_site.py` 中加入：

```python
"chapters/chapter-16/u-04-16-04-trusted-approximation/index.html": [
    "alg-u-04-16-04-horner",
    "alg-u-04-16-04-centered-difference",
],
```

以及导航标记：

```python
"chapters/chapter-16/u-04-16-04-trusted-approximation/index.html": [
    "md-sidebar",
    "第四部：微分与局部线性化",
    "第 16 章：Taylor 公式与余项",
],
```

- [ ] **Step 3: 更新导航、课程地图和 README**

- `mkdocs.yml` 在第 15 章四页之后加入第 16 章导学与四页，顺序与
  `EXPECTED_UNITS` 完全一致；
- `content/course-map.md` 增加章标题、原文
  “本章学时：7 小时（理论 4.5，应用 2.5）。”和四个单元链接；
- `README.md` 把发布范围改为“第四部第 16 章，共 68 个学习单元”；
- 第四部总学时仍是 35.5，不修改总量。

- [ ] **Step 4: 运行专项集成测试**

```bash
python3.12 -m unittest \
  tests.test_chapter_16 \
  tests.test_differentiation \
  tests.test_mkdocs_site \
  tests.test_zensical_structure -v
python3.12 scripts/check_content.py
git diff --check
```

Expected: 全部通过。

- [ ] **Step 5: 构建真实站点并检查代表锚点**

```bash
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: Zensical 输出 `No issues found`，站点检查退出码为 0；渲染后的 16.4 页面同时
包含 Horner、中心差分锚点和第 16 章侧栏标记。

- [ ] **Step 6: 提交发布集成**

```bash
git add tests/test_mkdocs_site.py tests/test_zensical_structure.py \
  scripts/check_site.py mkdocs.yml content/course-map.md README.md
git commit -m "feat: publish chapter sixteen Taylor formulas"
```

### Task 10: 最终全量验证并在第 16 章停止

**Files:**

- Verify: all changed files
- Do not create: any Chapter 17 content

- [ ] **Step 1: 检查提交范围和未跟踪文件**

```bash
git status --short
git diff --check
git diff main...HEAD --stat
git log --oneline main..HEAD
```

确认仅包含第 16 章正文、算法、测试、导航、课程地图、README 和本计划；`site/`、
缓存、临时实验输出均未进入提交。

- [ ] **Step 2: 运行完整质量门**

```bash
make verify
```

Expected:

- 全部 `unittest` 通过；
- `scripts/check_content.py` 通过；
- `zensical build --strict` 输出 `No issues found`；
- `scripts/check_site.py` 退出码为 0。

- [ ] **Step 3: 核验关键公式与接口的最终搜索**

```bash
rg -n "R_n\\(x\\).*\\(n\\+1\\)!|R_n\\(x\\).*n!|经验步长不提供误差证书|alg-u-04-16-04-(horner|centered-difference)" \
  content/chapters/chapter-16
rg -n "class DifferenceEstimate|def evaluate_taylor|def forward_difference|def centered_difference" \
  src/mathbook_examples/differentiation.py
```

Expected: 三种余项、非证书声明、两个发布锚点和四个公开接口均出现。

- [ ] **Step 4: 最终报告**

报告：

- 4 个单元和 7 学时闭合；
- 三种余项的证明与条件差异；
- Horner 和两种差分接口及其非证书边界；
- 发布前 12 项数学审查和 8 项算法审查结果；
- `make verify` 的实际测试数和构建结果；
- 分支提交列表。

在此停止。不要自动设计或撰写第 17 章。
