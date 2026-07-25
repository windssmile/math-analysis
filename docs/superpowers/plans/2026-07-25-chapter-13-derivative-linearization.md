# 第 13 章“导数、微分与局部线性模型” Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 发布第 13 章 4 个 `content_standard: 2` 单元，以经典差商为入口，完整建立导数与一阶局部线性化的等价关系。

**Architecture:** Markdown 是教材正文的唯一来源；`tests/test_chapter_13.py` 先冻结单元顺序、学时、核心锚点、前后部边界和导航合同。按 13.1–13.4 逐页完成并验证，最后统一更新 Zensical 导航、课程地图、README 和真实站点锚点；本章不新增 Python 算法模块。

**Tech Stack:** Markdown、Python 3.12 `unittest`、PyYAML、Zensical 0.0.51、MathJax、现有 `make verify` 质量门。

---

## 文件结构

**新增**

- `content/chapters/chapter-13/index.md`：章节问题弧、依赖、7 学时学习路径与章末接口。
- `content/chapters/chapter-13/u-04-13-01-average-instantaneous-rate.md`：平均变化率、差商、导数定义与导数唯一性。
- `content/chapters/chapter-13/u-04-13-02-derivative-existence-failure.md`：单侧导数、双侧判别、从定义求导及不可导类型。
- `content/chapters/chapter-13/u-04-13-03-local-linearization.md`：一阶局部线性化、等价定理与可导蕴含连续。
- `content/chapters/chapter-13/u-04-13-04-sensitivity-linear-model.md`：线性近似、绝对／相对敏感性与条件边界。
- `tests/test_chapter_13.py`：第 13 章结构、内容边界、导航和课程地图合同。

**修改**

- `mkdocs.yml`：增加第四部与第 13 章导航，只发布已经完成的第 13 章。
- `content/course-map.md`：增加第四部问题弧、第 13 章学时和 4 个单元链接。
- `README.md`：把发布范围更新为第一至第四部的已完成部分，并更新单元数为 56。
- `scripts/check_site.py`：增加第 13 章代表性锚点和第四部导航标记。
- `tests/test_mkdocs_site.py`：冻结新增代表性站点合同。

## 固定单元合同

| 顺序 | ID | 文件后缀 | 标题 | 理论+应用 |
|---|---|---|---|---:|
| 13.1 | `u-04-13-01` | `average-instantaneous-rate` | 平均变化率怎样逼近瞬时变化率？ | 1.25+0.50 |
| 13.2 | `u-04-13-02` | `derivative-existence-failure` | 差商极限何时存在，何时失败？ | 1.50+0.25 |
| 13.3 | `u-04-13-03` | `local-linearization` | 可导为什么等价于一阶局部线性化？ | 1.50+0.25 |
| 13.4 | `u-04-13-04` | `sensitivity-linear-model` | 局部线性模型怎样预测增量、误差与敏感性？ | 1.25+0.50 |

本章合计理论 5.5、应用 1.5，共 7 学时。每页必须包含现有 v2 九个固定二级标题、至少 2 个稳定例题、2 个即时检验、5 道分层习题和 7 个折叠完整答案。

### Task 1: 用失败测试冻结第 13 章合同

**Files:**

- Create: `tests/test_chapter_13.py`
- Test: `tests/test_chapter_13.py`

- [ ] **Step 1: 写入单元、学时和锚点失败测试**

创建 `tests/test_chapter_13.py`，使用下列合同：

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-13"

EXPECTED_UNITS = [
    ("u-04-13-01", "平均变化率怎样逼近瞬时变化率？", 1.25, 0.50, "average-instantaneous-rate"),
    ("u-04-13-02", "差商极限何时存在，何时失败？", 1.50, 0.25, "derivative-existence-failure"),
    ("u-04-13-03", "可导为什么等价于一阶局部线性化？", 1.50, 0.25, "local-linearization"),
    ("u-04-13-04", "局部线性模型怎样预测增量、误差与敏感性？", 1.25, 0.50, "sensitivity-linear-model"),
]

REQUIRED_ANCHORS = {
    "u-04-13-01": (
        "def-u-04-13-01-derivative",
        "thm-u-04-13-01-derivative-unique",
    ),
    "u-04-13-02": (
        "thm-u-04-13-02-one-sided-criterion",
        "ex-u-04-13-02-absolute-value",
    ),
    "u-04-13-03": (
        "thm-u-04-13-03-linearization-equivalence",
        "thm-u-04-13-03-differentiable-continuous",
    ),
    "u-04-13-04": (
        "def-u-04-13-04-relative-sensitivity",
        "thm-u-04-13-04-relative-error",
    ),
}
```

实现四项测试：

1. 遍历 `EXPECTED_UNITS`，断言文件、`unit_id`、标题、学时、`content_standard == 2` 和锚点；
2. 累加并断言本章理论 5.5、应用 1.5；
3. 断言 `mkdocs.yml` 与 `content/course-map.md` 按相同顺序各出现一次；
4. 对四页的 `## 常见误区与后续` 之前部分禁止出现 `中值定理`、`L’Hôpital`、`Taylor`、`Newton`、`Riemann 积分`、`无穷级数`。

- [ ] **Step 2: 运行测试并确认按预期失败**

Run:

```bash
python3.12 -m unittest tests.test_chapter_13 -v
```

Expected: FAIL，首先报告第 13 章 Markdown 文件不存在；不能出现测试导入错误。

- [ ] **Step 3: 提交失败测试**

```bash
git add tests/test_chapter_13.py
git commit -m "test: define chapter thirteen derivative contract"
```

### Task 2: 完成章导学与 13.1“从平均变化率到导数”

**Files:**

- Create: `content/chapters/chapter-13/index.md`
- Create: `content/chapters/chapter-13/u-04-13-01-average-instantaneous-rate.md`
- Test: `tests/test_chapter_13.py`

- [ ] **Step 1: 创建章导学页**

章导学页使用标题和锚点：

```markdown
---
title: 第 13 章：导数、微分与局部线性模型
---
# 第 13 章：导数、微分与局部线性模型 {#chapter-13}
```

正文明确：

- 上一章只提供连续性、介值与二分证书，本章不回头重证；
- 本章问题为“局部变化率怎样成为可验证的线性模型”；
- 按 13.1–13.4 列出 4 个相对链接；
- 本章 7 学时，理论 5.5、应用 1.5；
- 中值定理、Taylor 和 Newton 只列为后续去向，不进入本章证明。

- [ ] **Step 2: 写入 13.1 的精确元数据与理论核心**

Front matter：

```yaml
title: 平均变化率怎样逼近瞬时变化率？
unit_id: u-04-13-01
hours: {theory: 1.25, applied: 0.50}
difficulty: 3
prerequisites:
  book: [u-03-09-02, u-03-10-01]
  higher_algebra: [函数运算, 多项式恒等变形]
  analytic_geometry: [割线斜率, 直线方程]
  python: [不要求]
capabilities: [concepts, proof, application, mathematical_expression]
learning_goals: [由平均变化率建立差商, 用极限定义有限导数, 证明导数唯一, 解释切线与瞬时速度]
content_standard: 2
```

理论核心按以下次序书写：

1. 区间平均变化率与点 \(a\) 处差商；
2. 双侧有限导数定义 `{#def-u-04-13-01-derivative}`；
3. 导数唯一性定理及完整证明 `{#thm-u-04-13-01-derivative-unique}`；
4. 切线斜率是差商极限，而不是“把两个点强行重合”；
5. 瞬时速度作为位置函数差商的极限。

两个稳定例题分别从定义证明 \(f(x)=x^2\) 和 \(f(x)=1/x\) 在指定点的导数。即时检验覆盖常函数和线性函数。五道习题覆盖定义辨析、从定义求导、单位解释、割线误读和导数唯一性迁移。

- [ ] **Step 3: 运行内容检查并修复本页合同**

Run:

```bash
python3.12 scripts/check_content.py
```

Expected: 本页不产生元数据、标题、例题、习题、答案或链接错误；第 13 章专项测试仍因其余三页和导航缺失而失败。

- [ ] **Step 4: 提交章导学与 13.1**

```bash
git add content/chapters/chapter-13/index.md content/chapters/chapter-13/u-04-13-01-average-instantaneous-rate.md
git commit -m "feat: introduce derivatives from average rates"
```

### Task 3: 完成 13.2“差商极限的存在与失败”

**Files:**

- Create: `content/chapters/chapter-13/u-04-13-02-derivative-existence-failure.md`
- Test: `tests/test_chapter_13.py`

- [ ] **Step 1: 写入元数据和单侧判别主干**

Front matter：

```yaml
title: 差商极限何时存在，何时失败？
unit_id: u-04-13-02
hours: {theory: 1.50, applied: 0.25}
difficulty: 3
prerequisites:
  book: [u-04-13-01, u-03-09-06]
  higher_algebra: [绝对值, 分段函数]
  analytic_geometry: [左右方向, 尖点与切线]
  python: [不要求]
capabilities: [concepts, proof, counterexample, mathematical_expression]
learning_goals: [定义单侧导数, 判定双侧可导, 从定义计算导数, 区分尖点振荡与无限斜率]
content_standard: 2
```

理论核心必须包含：

- 左、右导数定义；
- 双侧有限导数存在当且仅当两侧有限导数存在且相等，并完整证明 `{#thm-u-04-13-02-one-sided-criterion}`；
- 端点导数必须明确采用相对定义域的单侧语言；
- \(|x|\) 在 0 处的尖点反例 `{#ex-u-04-13-02-absolute-value}`；
- \(x^{1/3}\) 在 0 处差商趋于正无穷，但这不是有限导数；
- \(x\sin(1/x)\) 在 0 处连续但差商振荡，导数不存在；
- 不把“竖直切线”误称为实数值导数。

第二个稳定例题使用分段函数，通过左右差商求参数使函数在连接点可导。五道习题覆盖端点、尖点、跳跃、振荡、无限斜率和分段参数。

- [ ] **Step 2: 运行专项测试并确认只剩预期缺口**

Run:

```bash
python3.12 -m unittest tests.test_chapter_13 -v
```

Expected: 13.1、13.2 的文件、元数据和锚点断言通过；测试仍因 13.3、13.4 与导航缺失失败。

- [ ] **Step 3: 提交 13.2**

```bash
git add content/chapters/chapter-13/u-04-13-02-derivative-existence-failure.md
git commit -m "feat: classify derivative existence and failure"
```

### Task 4: 完成 13.3“可导与局部线性化”

**Files:**

- Create: `content/chapters/chapter-13/u-04-13-03-local-linearization.md`
- Test: `tests/test_chapter_13.py`

- [ ] **Step 1: 写入元数据和等价定理**

Front matter：

```yaml
title: 可导为什么等价于一阶局部线性化？
unit_id: u-04-13-03
hours: {theory: 1.50, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-04-13-01, u-04-13-02, u-03-10-01]
  higher_algebra: [线性函数, 余项分解]
  analytic_geometry: [切线方程]
  python: [不要求]
capabilities: [concepts, proof, proof_strategy, mathematical_expression]
learning_goals: [定义一阶局部线性化, 证明其与差商等价, 证明可导蕴含连续, 识别余项条件]
content_standard: 2
```

定义 \(r(h)=f(a+h)-f(a)-Ah\)。定理
`{#thm-u-04-13-03-linearization-equivalence}` 必须逐向证明：

\[
f'(a)=A
\quad\Longleftrightarrow\quad
f(a+h)=f(a)+Ah+r(h),\qquad \frac{r(h)}{h}\to0.
\]

必须解释 \(r(h)=o(h)\) 是比例条件，不只是 \(r(h)\to0\)。随后由分解

\[
f(a+h)-f(a)=Ah+r(h)\to0
\]

证明可导蕴含连续 `{#thm-u-04-13-03-differentiable-continuous}`，不得使用中值定理。给出连续不蕴含可导的 \(|x|\) 反例。

两个稳定例题分别为 \(x^2\) 的精确主部—余项分解，以及 \(\sqrt{x}\) 在正点的线性化。五道习题覆盖错误余项辨析、系数唯一性、连续性证明、绝对值反例和分段函数线性化。

- [ ] **Step 2: 运行专项测试和内容检查**

Run:

```bash
python3.12 -m unittest tests.test_chapter_13 -v
python3.12 scripts/check_content.py
```

Expected: 13.3 的锚点和 v2 结构通过；不得出现被禁止的后续定理；专项测试只剩 13.4 和发布集成缺口。

- [ ] **Step 3: 提交 13.3**

```bash
git add content/chapters/chapter-13/u-04-13-03-local-linearization.md
git commit -m "feat: establish first order local linearization"
```

### Task 5: 完成 13.4“线性模型、误差与敏感性”

**Files:**

- Create: `content/chapters/chapter-13/u-04-13-04-sensitivity-linear-model.md`
- Test: `tests/test_chapter_13.py`

- [ ] **Step 1: 写入元数据和敏感性合同**

Front matter：

```yaml
title: 局部线性模型怎样预测增量、误差与敏感性？
unit_id: u-04-13-04
hours: {theory: 1.25, applied: 0.50}
difficulty: 4
prerequisites:
  book: [u-04-13-03]
  higher_algebra: [绝对误差, 相对误差, 不等式]
  analytic_geometry: [线性近似]
  python: [不要求]
capabilities: [application, modelling, error_analysis, mathematical_expression]
learning_goals: [建立线性近似, 区分增量与微分, 计算绝对和相对敏感性, 说明一阶误差结论边界]
content_standard: 2
```

理论与应用核心：

- 定义增量 \(\Delta y=f(a+h)-f(a)\) 与线性主部 \(dy=f'(a)h\)，禁止把 \(dy\) 无条件等同于真实增量；
- 从 \(r(h)=o(h)\) 得到局部一阶近似，但不声称二次误差；
- 在 \(a\ne0\)、\(f(a)\ne0\) 时定义相对敏感性
  \[
  \kappa_f(a)=\left|\frac{a f'(a)}{f(a)}\right|
  \]
  `{#def-u-04-13-04-relative-sensitivity}`；
- 证明一阶相对误差关系
  \[
  \frac{\Delta f}{f(a)}
  =
  \frac{a f'(a)}{f(a)}\frac{h}{a}
  +o(h)
  \]
  并明确其定义域条件 `{#thm-u-04-13-04-relative-error}`；
- 说明只有第 16 章的 Taylor 余项才能在额外光滑性下提供可计算高阶误差界。

两个稳定例题采用 \(\sqrt{x}\) 的测量传播和球体体积对半径误差的敏感性。五道习题覆盖线性预测、绝对／相对误差、无量纲条件数、条件失效和模型解释。

- [ ] **Step 2: 运行内容检查**

Run:

```bash
python3.12 scripts/check_content.py
```

Expected: 四个第 13 章学习单元均满足 v2 内容合同。

- [ ] **Step 3: 提交 13.4**

```bash
git add content/chapters/chapter-13/u-04-13-04-sensitivity-linear-model.md
git commit -m "feat: connect linearization to sensitivity"
```

### Task 6: 发布第 13 章并闭合站点合同

**Files:**

- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_mkdocs_site.py`
- Test: `tests/test_chapter_13.py`
- Test: `tests/test_mkdocs_site.py`

- [ ] **Step 1: 更新 Zensical 导航**

在第三部之后、附录之前增加：

```yaml
  - 第四部：微分与局部线性化:
      - 第 13 章：导数、微分与局部线性模型:
          - 本章导学: chapters/chapter-13/index.md
          - 13.1 平均变化率怎样逼近瞬时变化率？: chapters/chapter-13/u-04-13-01-average-instantaneous-rate.md
          - 13.2 差商极限何时存在，何时失败？: chapters/chapter-13/u-04-13-02-derivative-existence-failure.md
          - 13.3 可导为什么等价于一阶局部线性化？: chapters/chapter-13/u-04-13-03-local-linearization.md
          - 13.4 局部线性模型怎样预测增量、误差与敏感性？: chapters/chapter-13/u-04-13-04-sensitivity-linear-model.md
```

- [ ] **Step 2: 更新课程地图和 README**

`content/course-map.md`：

- 把“当前已发布第一至第三部”改为“当前已发布第一至第三部及第四部第 13 章”；
- 增加第四部核心问题；
- 增加第 13 章 7 学时和四个相对路径链接；
- 后续路线改为“第四部第 14 章至第十二部尚未作为发布页面”。

`README.md`：

- 把发布范围改为“当前发布第一至第三部及第四部第 13 章”；
- 把学习单元数从 52 更新为 56；
- 保持 Zensical 运行和验证命令不变。

- [ ] **Step 3: 增加真实站点锚点与导航测试**

向 `REQUIRED_RENDERED_ANCHORS` 增加：

```python
"chapters/chapter-13/u-04-13-03-local-linearization/index.html": [
    "thm-u-04-13-03-linearization-equivalence",
    "thm-u-04-13-03-differentiable-continuous",
],
```

向 `REQUIRED_NAVIGATION_MARKERS` 增加：

```python
"chapters/chapter-13/u-04-13-03-local-linearization/index.html": [
    "md-sidebar",
    "第四部：微分与局部线性化",
    "第 13 章：导数、微分与局部线性模型",
],
```

在 `tests/test_mkdocs_site.py` 中断言这两项精确存在。

- [ ] **Step 4: 运行第 13 章和站点测试**

Run:

```bash
python3.12 -m unittest tests.test_chapter_13 tests.test_mkdocs_site -v
```

Expected: PASS，所有第 13 章文件、学时、锚点、导航和课程地图顺序通过。

- [ ] **Step 5: 运行完整验收**

Run:

```bash
make verify
```

Expected:

- 全量 `unittest` 为 `OK`；
- `scripts/check_content.py` 无输出并返回 0；
- `zensical build --strict` 报告 `No issues found`；
- `scripts/check_site.py` 无输出并返回 0；
- 真实生成第 13 章 5 个页面；
- 工作树中不提交 `site/`。

- [ ] **Step 6: 数学内容复核**

逐页确认：

- 差商中的自变量趋近受定义域限制；
- 导数只定义为有限实数极限；
- 单侧导数相等是双侧导数存在的必要且充分条件；
- \(r(h)=o(h)\) 的比例条件写对；
- 可导蕴含连续的证明没有循环使用中值定理；
- 相对敏感性明确要求 \(a\ne0\)、\(f(a)\ne0\)；
- 一阶近似没有越权声称二次误差；
- 本章核心没有使用第 14 章以后的结果。

- [ ] **Step 7: 提交发布集成**

```bash
git add mkdocs.yml content/course-map.md README.md scripts/check_site.py tests/test_mkdocs_site.py
git commit -m "feat: publish chapter thirteen derivative foundations"
```

## 第 13 章完成检查

- [ ] 4 个单元均为 `content_standard: 2`。
- [ ] 理论 5.5 + 应用 1.5 = 7 学时。
- [ ] 每页至少 2 个稳定例题、2 个即时检验、5 道习题和 7 个折叠完整答案。
- [ ] 差商、单侧导数、局部线性化、连续性和敏感性形成闭环。
- [ ] 未引入中值定理、Taylor、Newton、积分或无穷级数作为核心工具。
- [ ] 导航、课程地图、README、站点锚点和发布页面一致。
- [ ] `make verify` 全量通过。
- [ ] 在此检查点停止；第 14 章另写实施计划后再开始。
