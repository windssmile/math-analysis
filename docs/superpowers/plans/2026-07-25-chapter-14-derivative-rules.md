# 第 14 章“求导法则、反函数与高阶导数” Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 发布第 14 章 4 个 `content_standard: 2` 单元，从局部线性化严格推出代数法则、链式法则、反函数求导及高阶导数语言。

**Architecture:** Markdown 正文是唯一来源，`tests/test_chapter_14.py` 先冻结单元、学时、证明边界和导航合同。正文按“代数运算 → 复合 → 反函数与初等函数 → 隐式关系与高阶导数”推进；发布前设置独立内容审查门，最后统一更新 Zensical 导航、课程地图、README 和真实站点锚点。

**Tech Stack:** Markdown、Python 3.12 `unittest`、PyYAML、Zensical 0.0.51、MathJax、现有 `make verify` 质量门。

---

## 文件结构

**新增**

- `content/chapters/chapter-14/index.md`：章节问题弧、6 学时路径和依赖边界。
- `content/chapters/chapter-14/u-04-14-01-algebraic-derivative-rules.md`：和、积、倒数与商法则。
- `content/chapters/chapter-14/u-04-14-02-chain-rule.md`：复合的局部线性化与链式法则。
- `content/chapters/chapter-14/u-04-14-03-inverse-elementary-derivatives.md`：反函数定理、有理幂及初等函数导数来源。
- `content/chapters/chapter-14/u-04-14-04-implicit-higher-derivatives.md`：条件式隐式求导和高阶导数。
- `tests/test_chapter_14.py`：结构、学时、证明标记、依赖边界、导航和课程地图合同。

**修改**

- `mkdocs.yml`：在第四部第 13 章之后加入第 14 章。
- `content/course-map.md`：加入第 14 章 6 学时及 4 个单元链接。
- `README.md`：学习单元数从 56 更新为 60，发布范围更新到第四部第 14 章。
- `scripts/check_site.py`：加入链式法则代表页面的锚点和导航标记。
- `tests/test_mkdocs_site.py`：冻结第 14 章真实站点合同。

本章不新增 Python 算法模块。所有例题中的符号运算都必须服务于证明结构与条件辨析。

## 固定单元合同

| 顺序 | ID | 文件后缀 | 标题 | 理论+应用 |
|---|---|---|---|---:|
| 14.1 | `u-04-14-01` | `algebraic-derivative-rules` | 局部线性模型怎样通过和、积、商传递？ | 1.25+0.25 |
| 14.2 | `u-04-14-02` | `chain-rule` | 复合函数的局部误差怎样层层传递？ | 1.25+0.25 |
| 14.3 | `u-04-14-03` | `inverse-elementary-derivatives` | 反函数的变化率为何是原导数的倒数？ | 1.00+0.50 |
| 14.4 | `u-04-14-04` | `implicit-higher-derivatives` | 隐式关系与高阶导数怎样记录复杂变化？ | 1.00+0.50 |

本章合计理论 4.5、应用 1.5，共 6 学时。四页全部执行 v2 合同：2 个稳定例题、2 个即时检验、5 道习题和 7 个折叠完整答案。

## 初等函数依赖合同

第 14.3 单元必须区分“函数构造”和“求导证明”：

- 多项式、有理函数、绝对值和平方根沿用已完成的代数函数体系；
- 有理幂通过反函数求导和整数幂法则推出；
- 三角函数使用弧度制、加法公式和几何基本极限
  \[
  \lim_{h\to0}\frac{\sin h}{h}=1
  \]
  并在页内用单位圆几何不等式证明该基本极限，再给出它到正弦、余弦导数的完整推导；
- 标准实指数函数的构造不是本章任务。本章明确把指数律、连续性和归一化极限
  \[
  \lim_{h\to0}\frac{e^h-1}{h}=1
  \]
  作为“标准实指数函数”先备合同，再完整推出 \(e^x\)、\(\ln x\)、\(a^x\) 的导数；
- 不用尚未建立的积分或无穷级数伪造指数、对数或三角函数的证明来源。

### Task 1: 用失败测试冻结第 14 章合同

**Files:**

- Create: `tests/test_chapter_14.py`
- Test: `tests/test_chapter_14.py`

- [ ] **Step 1: 写入精确单元和锚点合同**

创建测试常量：

```python
EXPECTED_UNITS = [
    ("u-04-14-01", "局部线性模型怎样通过和、积、商传递？", 1.25, 0.25, "algebraic-derivative-rules"),
    ("u-04-14-02", "复合函数的局部误差怎样层层传递？", 1.25, 0.25, "chain-rule"),
    ("u-04-14-03", "反函数的变化率为何是原导数的倒数？", 1.00, 0.50, "inverse-elementary-derivatives"),
    ("u-04-14-04", "隐式关系与高阶导数怎样记录复杂变化？", 1.00, 0.50, "implicit-higher-derivatives"),
]

REQUIRED_ANCHORS = {
    "u-04-14-01": (
        "thm-u-04-14-01-sum-product",
        "thm-u-04-14-01-reciprocal-quotient",
    ),
    "u-04-14-02": (
        "thm-u-04-14-02-chain-rule",
        "ex-u-04-14-02-zero-inner-increment",
    ),
    "u-04-14-03": (
        "thm-u-04-14-03-inverse-derivative",
        "thm-u-04-14-03-elementary-derivatives",
    ),
    "u-04-14-04": (
        "def-u-04-14-04-higher-derivatives",
        "thm-u-04-14-04-implicit-conditional",
    ),
}
```

实现测试：

1. 断言文件、元数据、v2、锚点与理论 4.5 + 应用 1.5；
2. 断言章导学、`mkdocs.yml` 和课程地图顺序一致；
3. 核心正文禁止 `中值定理`、`L’Hôpital`、`Taylor`、`Newton`、`Riemann 积分`、`无穷级数`；
4. 链式法则页必须包含零内层增量处理标记 `即使 \(g(a+h)=g(a)\)`；
5. 反函数定理必须包含 `反函数连续`、`f'(a)\ne0` 和 `y\to b`；
6. 隐式求导页必须包含 `先已知 \(y\) 在该点可导`，并禁止 `隐函数定理保证`。

- [ ] **Step 2: 验证 RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_14 -v
```

Expected: FAIL，原因是第 14 章文件与发布条目不存在；不能出现导入错误。

- [ ] **Step 3: 提交合同测试**

```bash
git add tests/test_chapter_14.py
git commit -m "test: define chapter fourteen derivative rules contract"
```

### Task 2: 完成章导学与 14.1 代数求导法则

**Files:**

- Create: `content/chapters/chapter-14/index.md`
- Create: `content/chapters/chapter-14/u-04-14-01-algebraic-derivative-rules.md`
- Test: `tests/test_chapter_14.py`

- [ ] **Step 1: 创建章导学页**

章标题与锚点：

```markdown
---
title: 第 14 章：求导法则、反函数与高阶导数
---
# 第 14 章：求导法则、反函数与高阶导数 {#chapter-14}
```

正文列出 4 单元、理论 4.5 + 应用 1.5 = 6 学时，并明确本章只负责局部求导结构；区间
整体结论、余项估计和迭代收敛分别留给第 15–17 章。

- [ ] **Step 2: 写入 14.1 元数据**

```yaml
title: 局部线性模型怎样通过和、积、商传递？
unit_id: u-04-14-01
hours: {theory: 1.25, applied: 0.25}
difficulty: 3
prerequisites:
  book: [u-04-13-03]
  higher_algebra: [代数恒等式, 分式运算]
  analytic_geometry: []
  python: [不要求]
capabilities: [proof, analytic_calculation, error_analysis, mathematical_expression]
learning_goals: [证明和与常数倍法则, 证明乘积法则, 推出倒数与商法则, 核验分母条件]
content_standard: 2
```

- [ ] **Step 3: 完成理论核心**

用

\[
f(a+h)=f(a)+f'(a)h+r_f(h),\qquad r_f(h)=o(h)
\]

和 \(g\) 的对应分解证明：

- 常数倍、和、差法则；
- 乘积法则 `{#thm-u-04-14-01-sum-product}`，显式处理
  \(f'(a)g'(a)h^2\) 及余项乘积；
- 倒数法则先证明 \(g(a+h)\) 在小邻域远离零；
- 商法则 `{#thm-u-04-14-01-reciprocal-quotient}`，明确 \(g(a)\ne0\)；
- 由整数幂归纳得到幂法则，不延伸到尚未证明的任意实指数。

稳定例题使用多项式与有理函数；习题覆盖证明补全、分母为零反例、可去间断点的原定义域、
整数负幂和多因子乘积。

- [ ] **Step 4: 运行内容检查并提交**

```bash
python3.12 scripts/check_content.py
git add content/chapters/chapter-14
git commit -m "feat: derive algebraic differentiation rules"
```

### Task 3: 完成 14.2 链式法则

**Files:**

- Create: `content/chapters/chapter-14/u-04-14-02-chain-rule.md`
- Test: `tests/test_chapter_14.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: 复合函数的局部误差怎样层层传递？
unit_id: u-04-14-02
hours: {theory: 1.25, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-04-14-01, u-04-13-03]
  higher_algebra: [函数复合, 线性映射复合]
  analytic_geometry: []
  python: [不要求]
capabilities: [proof, proof_strategy, analytic_calculation, error_analysis]
learning_goals: [证明链式法则, 处理内层增量为零, 追踪复合余项, 解释敏感性相乘]
content_standard: 2
```

- [ ] **Step 2: 完成无除零漏洞的证明**

设 \(g\) 在 \(a\) 可导，\(f\) 在 \(b=g(a)\) 可导。写

\[
g(a+h)=b+g'(a)h+r_g(h),
\]

\[
f(b+k)=f(b)+f'(b)k+r_f(k).
\]

定义

\[
\eta(k)=
\begin{cases}
r_f(k)/k,&k\ne0,\\
0,&k=0,
\end{cases}
\]

则 \(\eta(k)\to0\)。把 \(k=g(a+h)-g(a)\) 代入，不除以可能为零的内层增量。证明中
必须原文说明“即使 \(g(a+h)=g(a)\)，扩展后的 \(\eta\) 仍有定义”。得到

\[
(f\circ g)'(a)=f'(g(a))g'(a)
\]

`{#thm-u-04-14-02-chain-rule}`。

稳定例题一为嵌套多项式。另一例 `{#ex-u-04-14-02-zero-inner-increment}` 取

\[
g(h)=
\begin{cases}
h^2\sin(1/h),&h\ne0,\\
0,&h=0,
\end{cases}
\qquad f(t)=t^2.
\]

先用定义证明 \(g'(0)=0\)，再指出 \(h=1/(n\pi)\) 时
\(g(h)=g(0)\)，说明不能把链式法则证明建立在“内层增量必非零”上。这里仅使用
\(|\sin(1/h)|\le1\)，不预借三角函数求导。习题覆盖多层复合、定义域、错误消去和相对
敏感性乘法。

- [ ] **Step 3: 运行专项测试并提交**

```bash
python3.12 -m unittest tests.test_chapter_14 -v
python3.12 scripts/check_content.py
git add content/chapters/chapter-14/u-04-14-02-chain-rule.md
git commit -m "feat: prove the chain rule through linearization"
```

Expected: 14.1、14.2 内容合同通过；测试只因 14.3、14.4 和发布集成缺失而失败。

### Task 4: 完成 14.3 反函数与初等函数导数

**Files:**

- Create: `content/chapters/chapter-14/u-04-14-03-inverse-elementary-derivatives.md`
- Test: `tests/test_chapter_14.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: 反函数的变化率为何是原导数的倒数？
unit_id: u-04-14-03
hours: {theory: 1.00, applied: 0.50}
difficulty: 4
prerequisites:
  book: [u-04-14-02, u-03-10-05]
  higher_algebra: [反函数, 有理指数, 实指数函数及指数律, 弧度制与三角恒等式]
  analytic_geometry: [反函数图像关于直线对称]
  python: [不要求]
capabilities: [proof, analytic_calculation, dependency_awareness, mathematical_expression]
learning_goals: [证明反函数求导定理, 推出有理幂导数, 追溯三角导数基本极限, 说明指数函数归一化合同]
content_standard: 2
```

- [ ] **Step 2: 完成反函数求导定理**

定理 `{#thm-u-04-14-03-inverse-derivative}` 的假设必须逐项出现：

- \(f\) 在区间上连续且严格单调；
- \(a\) 是区间内点，\(b=f(a)\)；
- 反函数 \(g=f^{-1}\) 在 \(b\) 连续；
- \(f\) 在 \(a\) 可导且 \(f'(a)\ne0\)。

令 \(x=g(y)\)，由 \(y\to b\) 和反函数连续得到 \(x\to a\)，再证明

\[
\frac{g(y)-g(b)}{y-b}
=
\frac{x-a}{f(x)-f(a)}
\longrightarrow\frac1{f'(a)}.
\]

必须解释 \(f'(a)=0\) 时为何不能取倒数，并用立方根在零点作边界例。

- [ ] **Step 3: 建立初等函数导数来源**

定理 `{#thm-u-04-14-03-elementary-derivatives}` 分四组：

1. 整数幂与反函数定理推出正定义域上的有理幂；
2. 在弧度制下由单位圆面积比较得到
   \(\cos h\le \sin h/h\le1\)（\(0<h<\pi/2\)），结合奇偶性证明双侧基本极限，
   再用加法公式推出 \(\sin x\)、\(\cos x\)；
3. 明确声明标准实指数函数的归一化极限是本页先备合同，由它推出
   \((e^x)'=e^x\)；
4. 由反函数定理推出 \((\ln x)'=1/x\)，再由链式法则推出
   \((a^x)'=a^x\ln a\)。

正文不得声称使用积分或无穷级数构造了这些函数。稳定例题覆盖根式与指数—对数复合；
习题覆盖条件、弧度制、反函数导数、定义域和错误公式诊断。

- [ ] **Step 4: 运行内容检查并提交**

```bash
python3.12 scripts/check_content.py
git add content/chapters/chapter-14/u-04-14-03-inverse-elementary-derivatives.md
git commit -m "feat: derive inverse and elementary derivatives"
```

### Task 5: 完成 14.4 隐式关系与高阶导数

**Files:**

- Create: `content/chapters/chapter-14/u-04-14-04-implicit-higher-derivatives.md`
- Test: `tests/test_chapter_14.py`

- [ ] **Step 1: 写入元数据**

```yaml
title: 隐式关系与高阶导数怎样记录复杂变化？
unit_id: u-04-14-04
hours: {theory: 1.00, applied: 0.50}
difficulty: 4
prerequisites:
  book: [u-04-14-01, u-04-14-02, u-04-14-03]
  higher_algebra: [隐式方程, 递推记号]
  analytic_geometry: [圆与参数曲线]
  python: [不要求]
capabilities: [analytic_calculation, dependency_awareness, modelling, mathematical_expression]
learning_goals: [定义高阶导数, 条件式执行隐式求导, 计算二阶导数, 识别存在性边界]
content_standard: 2
```

- [ ] **Step 2: 建立高阶导数语言**

定义 `{#def-u-04-14-04-higher-derivatives}`：

\[
f''=(f')',\qquad f^{(n)}=(f^{(n-1)})'.
\]

明确“\(f\) 可导”不自动推出 \(f''\) 存在，高阶可导性必须逐阶声明。例题计算多项式、
指数和三角函数的高阶导数，并识别周期模式。

- [ ] **Step 3: 建立条件式隐式求导**

定理 `{#thm-u-04-14-04-implicit-conditional}` 只声称：

> 先已知 \(y\) 在该点可导，并且恒等式在邻域成立，才能对恒等式两边应用链式法则。

用

\[
x^2+y(x)^2=1
\]

推出 \(2x+2yy'=0\)，并明确只有在 \(y\ne0\) 时才能解出 \(y'=-x/y\)。再通过一次
求导计算 \(y''\)，每次除法都核验分母。

不得写“隐函数定理保证”或从一条方程无条件推出局部可微函数存在。第二个稳定例题使用
已知可微参数关系。习题覆盖分母为零、不同分支、高阶记号和存在性辨错。

- [ ] **Step 4: 运行内容检查并提交**

```bash
python3.12 -m unittest tests.test_chapter_14 -v
python3.12 scripts/check_content.py
git add content/chapters/chapter-14/u-04-14-04-implicit-higher-derivatives.md
git commit -m "feat: add conditional implicit and higher derivatives"
```

Expected: 四页内容、学时、锚点和边界测试通过；只剩导航和课程地图缺口。

### Task 6: 发布前内容审查与修复

**Files:**

- Review: `content/chapters/chapter-14/index.md`
- Review: `content/chapters/chapter-14/u-04-14-01-algebraic-derivative-rules.md`
- Review: `content/chapters/chapter-14/u-04-14-02-chain-rule.md`
- Review: `content/chapters/chapter-14/u-04-14-03-inverse-elementary-derivatives.md`
- Review: `content/chapters/chapter-14/u-04-14-04-implicit-higher-derivatives.md`
- Test: `tests/test_chapter_14.py`

- [ ] **Step 1: 数学正确性审查**

逐页核对：

- 乘积余项是否真的为 \(o(h)\)；
- 倒数和商法则是否先建立分母远离零；
- 链式法则是否处理内层增量等于零；
- 反函数证明是否使用反函数连续性并保持趋近方向合法；
- 初等函数的“构造先备”与“本页推导”是否明确分开；
- 弧度制和指数归一化条件是否明确；
- 隐式求导是否先假定局部可微函数存在；
- 高阶导数存在性是否逐阶声明；
- 例题、检验、习题和答案是否遵守相同定义域。

- [ ] **Step 2: 自学可用性审查**

核对每页牵引问题是否闭合、证明障碍与路线是否显式、公式是否说明条件和来源、错误方法
是否配有反例、答案是否解释关键转折、下一页接口是否准确。

- [ ] **Step 3: 先补失败测试再修复可固化缺陷**

运行：

```bash
python3.12 -m unittest tests.test_chapter_14 -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: 内容、构建、现有站点和格式检查通过；专项测试只允许因尚未发布导航而失败。

- [ ] **Step 4: 提交审查修复**

```bash
git add tests/test_chapter_14.py content/chapters/chapter-14
git commit -m "fix: strengthen chapter fourteen content"
```

若没有文件变化，不创建空提交，但最终报告必须列出审查项目。

### Task 7: 发布第 14 章并闭合站点合同

**Files:**

- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_mkdocs_site.py`
- Test: `tests/test_chapter_14.py`
- Test: `tests/test_mkdocs_site.py`

- [ ] **Step 1: 先写站点失败测试**

在 `tests/test_mkdocs_site.py` 中要求页面

```text
chapters/chapter-14/u-04-14-02-chain-rule/index.html
```

具有锚点：

```python
[
    "thm-u-04-14-02-chain-rule",
    "ex-u-04-14-02-zero-inner-increment",
]
```

和导航标记：

```python
[
    "md-sidebar",
    "第四部：微分与局部线性化",
    "第 14 章：求导法则、反函数与高阶导数",
]
```

运行目标测试，确认因字典尚无该页面而 FAIL。

- [ ] **Step 2: 更新导航、课程地图和 README**

`mkdocs.yml` 在第 13 章后加入第 14 章及四个单元。

`content/course-map.md` 加入：

- 第 14 章链接与锚点 `{#chapter-14}`；
- 本章 6 学时（理论 4.5，应用 1.5）；
- 四个单元的精确路径与顺序；
- 后续路线从第 15 章开始。

`README.md` 把发布范围更新到第四部第 14 章，单元数从 56 改为 60。

- [ ] **Step 3: 更新真实站点检查**

向 `scripts/check_site.py` 的两个字典加入 Task 7 Step 1 的锚点和导航标记，使站点测试转绿。

- [ ] **Step 4: 运行专项和完整验收**

```bash
python3.12 -m unittest tests.test_chapter_14 tests.test_mkdocs_site -v
make verify
```

Expected:

- 全量 `unittest` 为 `OK`；
- 内容检查无错误；
- `zensical build --strict` 报告 `No issues found`；
- 站点检查无错误；
- 第 14 章 5 个页面真实生成；
- `site/` 不进入提交。

- [ ] **Step 5: 提交发布集成**

```bash
git add mkdocs.yml content/course-map.md README.md scripts/check_site.py tests/test_mkdocs_site.py
git commit -m "feat: publish chapter fourteen derivative rules"
```

## 第 14 章完成检查

- [ ] 4 个核心单元全部达到 v2。
- [ ] 理论 4.5 + 应用 1.5 = 6 学时。
- [ ] 代数、链式、反函数与高阶导数依赖闭合。
- [ ] 链式法则证明没有内层增量除零漏洞。
- [ ] 初等函数构造边界诚实、明确，无积分或级数循环依赖。
- [ ] 隐式求导不冒充隐函数存在定理。
- [ ] 发布前内容审查发现均已修复或明确记录。
- [ ] 导航、课程地图、README 和真实站点一致。
- [ ] `make verify` 全量通过。
- [ ] 在此停止；第 15 章另写实施计划。
