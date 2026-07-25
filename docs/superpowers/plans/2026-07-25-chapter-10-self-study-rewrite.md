# 第 10 章自学教材级重写 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 Zensical modern 架构下，把第 10 章重建为 5 个 `content_standard: 2` 核心学习单元，闭合连续性的局部定义、运算、端点与延拓、间断分类和初等函数证明桥，并在本章验收后停止。

**Architecture:** `content/chapters/chapter-10/` 是正文与单元元数据的唯一来源，`mkdocs.yml` 决定阅读顺序，`content/course-map.md` 提供课程地图入口；`tests/test_chapter_10.py` 固化数学边界与章级合同，`scripts/check_content.py` 复用统一 v2 结构检查，`scripts/check_site.py` 检查真实 Zensical 产物。保留现有 10.1–10.3 URL，新增 10.4、10.5，不引入导数、中值定理、积分或一般拓扑。

**Tech Stack:** Markdown、YAML front matter、Python 3.12 `unittest`、Zensical 0.0.51 modern、MathJax 3、PyMdown details。

---

## 文件职责

| 路径 | 责任 |
|---|---|
| `tests/test_chapter_10.py` | 固化 5 单元顺序、标题、学时、v2 标准、锚点和禁用依赖。 |
| `content/chapters/chapter-10/index.md` | 章级问题、依赖、学习路径和 5 单元入口。 |
| `content/chapters/chapter-10/u-03-10-01-epsilon-delta-continuity.md` | 点连续、集合上连续、极限与序列刻画。 |
| `content/chapters/chapter-10/u-03-10-02-continuous-operations.md` | 四则运算与复合连续性。 |
| `content/chapters/chapter-10/u-03-10-04-one-sided-continuity-extension.md` | 单侧连续、端点连续、可去间断与连续延拓。 |
| `content/chapters/chapter-10/u-03-10-03-discontinuities-elementary-functions.md` | 可去、跳跃、无穷、振荡四类间断及序列证伪。 |
| `content/chapters/chapter-10/u-03-10-05-elementary-continuity-bridge.md` | 多项式、有理、绝对值、根式与有限复合的连续性证明桥。 |
| `mkdocs.yml` | 按 10.1、10.2、10.3、10.4、10.5 的教学顺序注册页面。 |
| `content/course-map.md` | 展示第 10 章 5 个可点击核心单元及 `8+2=10` 学时。 |
| `tests/test_parts_02_03_migration.py` | 把新增页面纳入发布页面总表和代表锚点检查。 |
| `scripts/check_site.py` | 在真实 HTML 中检查第 10 章代表锚点。 |

### Task 1: 写出第 10 章最终合同的失败测试

**Files:**
- Create: `tests/test_chapter_10.py`
- Modify: `tests/test_parts_02_03_migration.py`

- [x] **Step 1: 创建章级源文件合同测试**

创建 `tests/test_chapter_10.py`，读取 `content/chapters/chapter-10/` 与 `mkdocs.yml`，要求精确页面顺序：

```python
EXPECTED_UNITS = [
    ("u-03-10-01", "连续性怎样把极限与函数值接起来？", 1.75, 0.25, "epsilon-delta-continuity"),
    ("u-03-10-02", "连续性怎样经过运算和复合传递？", 1.75, 0.25, "continuous-operations"),
    ("u-03-10-04", "端点连续与连续延拓怎样统一处理？", 1.50, 0.50, "one-sided-continuity-extension"),
    ("u-03-10-03", "函数会以哪些方式失去连续性？", 1.50, 0.50, "discontinuities-elementary-functions"),
    ("u-03-10-05", "常见初等函数的连续性从哪里来？", 1.50, 0.50, "elementary-continuity-bridge"),
]
```

测试必须逐页断言 `unit_id`、标题、学时、`content_standard == 2`，总学时为理论 `8.0`、应用 `2.0`，并要求以下代表锚点：

```python
REQUIRED_ANCHORS = {
    "u-03-10-01": ("def-u-03-10-01-continuity", "thm-u-03-10-01-sequential-continuity"),
    "u-03-10-02": ("thm-u-03-10-02-continuous-operations", "thm-u-03-10-02-composition"),
    "u-03-10-04": ("def-u-03-10-04-one-sided-continuity", "thm-u-03-10-04-continuous-extension"),
    "u-03-10-03": ("def-u-03-10-03-discontinuity-types", "ex-u-03-10-03-oscillation"),
    "u-03-10-05": ("thm-u-03-10-05-algebraic-continuity", "thm-u-03-10-05-root-continuity"),
}
```

另设边界测试，在第 10 章正文中禁止把 `导数`、`中值定理`、`Taylor`、`洛必达`、`Newton`、`Riemann 积分` 作为证明依赖；允许仅在“后续”栏目声明这些内容属于后续章节。

- [x] **Step 2: 把新增页面加入迁移合同**

在 `tests/test_parts_02_03_migration.py` 的 `EXPECTED_UNIT_PAGES` 中加入：

```python
"chapter-10/u-03-10-04-one-sided-continuity-extension.md",
"chapter-10/u-03-10-05-elementary-continuity-bridge.md",
```

把数量断言从 `38` 改为 `40`，并在 `REPRESENTATIVE_ANCHORS` 中加入：

```python
"chapter-10/u-03-10-04-one-sided-continuity-extension.md":
    "thm-u-03-10-04-continuous-extension",
"chapter-10/u-03-10-05-elementary-continuity-bridge.md":
    "thm-u-03-10-05-algebraic-continuity",
```

- [x] **Step 3: 观察 RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_10 tests.test_parts_02_03_migration -v
```

Expected: FAIL；失败来自两个新增页面缺失、现有三页标题/学时/v2 合同不符和导航只有三页。

### Task 2: 重写 10.1 点连续与等价刻画

**Files:**
- Rewrite: `content/chapters/chapter-10/u-03-10-01-epsilon-delta-continuity.md`

- [x] **Step 1: 写入最终元数据和完整理论闭环**

把页面元数据改为 `1.75+0.25`、`content_standard: 2`。正文依次完成：

1. \(a\in D\) 时点连续的相对定义；
2. `lim f(x)=f(a)` 与不去心的 \(\varepsilon\)-\(\delta\) 形式等价；
3. 集合 \(E\subset D\) 上连续定义为“在 \(E\) 每一点相对 \(D\) 连续”；
4. 用第 9 章 Heine 判别证明序列刻画的两个方向；
5. 明确孤立点连续是定义的直接结果，不把它误当作邻域图像性质。

保留 `def-u-03-10-01-continuity`，新增 `thm-u-03-10-01-sequential-continuity`。完整例题至少包括 \(x^2\) 在任意点的 \(\delta\) 构造、被改值的分段函数；即时检验至少 2 个；设置 5 个 `pr-u-03-10-01-*` 习题和至少 7 个折叠完整答案。

- [x] **Step 2: 运行单页和章级检查**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_10 -v
```

Expected: 通用内容检查仍因其余第 10 章旧页/缺页失败；章级测试中 10.1 的元数据和锚点通过。

### Task 3: 重写 10.2 连续运算与复合

**Files:**
- Rewrite: `content/chapters/chapter-10/u-03-10-02-continuous-operations.md`

- [x] **Step 1: 完成四则与复合证明**

把元数据改为 `1.75+0.25`、`content_standard: 2`。完整证明：

- 常数倍、和、差、积在 \(a\) 连续；
- 当 \(g(a)\ne0\) 时 \(f/g\) 在 \(a\) 连续，并用连续性先保证分母局部不为零；
- 复合函数连续性，明确 \(g(D)\) 与外层函数定义域的兼容条件；
- 有限次运算闭包，不把无限和或无限复合混入结论。

保留两个定理锚点；例题使用多项式和含分母表达式，另用 \(\sqrt{x^2}\) 强调复合定义域。加入 2 个即时检验、5 个分层习题、7 个折叠完整答案和“条件使用位置”总结。

- [x] **Step 2: 运行单元结构检查**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_10 -v
```

Expected: 10.1、10.2 的 v2 合同通过；其余缺页/旧页仍保持 RED。

### Task 4: 新增 10.3 单侧连续、端点与延拓

**Files:**
- Create: `content/chapters/chapter-10/u-03-10-04-one-sided-continuity-extension.md`

- [x] **Step 1: 写出单侧与延拓定理**

页面使用 `unit_id: u-03-10-04`、`1.50+0.50`、`content_standard: 2`。正文完成：

- 左连续、右连续和区间端点的相对连续定义；
- 区间内部连续当且仅当左右连续；
- 若 \(a\) 是 \(D\) 的聚点且 \(\lim_{x\to a}f(x)=L\in\mathbb R\)，则令 \(\widetilde f(a)=L\) 得到连续延拓；
- 若有限极限不存在，则改一个点值不可能修复；
- 开区间端点延拓需要相应单侧有限极限。

加入 `def-u-03-10-04-one-sided-continuity`、`thm-u-03-10-04-continuous-extension`，两个完整例题、2 个即时检验、5 个习题和 7 个折叠答案。

- [x] **Step 2: 验证新增页面已被测试捕获**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_10 tests.test_parts_02_03_migration -v
```

Expected: 10.4 页面自身合同通过；导航与 10.3/10.5 仍保持 RED。

### Task 5: 重写 10.4 间断分类

**Files:**
- Rewrite: `content/chapters/chapter-10/u-03-10-03-discontinuities-elementary-functions.md`

- [x] **Step 1: 建立不重叠的诊断流程**

把元数据改为 `1.50+0.50`、`content_standard: 2`。以“先检查有限双侧极限，再检查单侧与无界行为”的顺序定义并区分：

- 可去间断；
- 跳跃间断；
- 无穷间断；
- 振荡型间断。

用相对定义域说明“函数未在点上定义”和“在定义域内不连续”的区别；用两条点列证明 \(\sin(1/x)\) 不存在极限；用 \(1/x\)、符号函数、改值函数形成四类对照。加入 `def-u-03-10-03-discontinuity-types`、`ex-u-03-10-03-oscillation`、2 个完整例题、2 个即时检验、5 个习题和 7 个折叠答案。

- [x] **Step 2: 运行内容合同**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_10 -v
```

Expected: 已有四页通过；只剩 10.5 和导航相关失败。

### Task 6: 新增 10.5 初等函数连续性证明桥

**Files:**
- Create: `content/chapters/chapter-10/u-03-10-05-elementary-continuity-bridge.md`

- [x] **Step 1: 写出代数函数证明链**

页面使用 `unit_id: u-03-10-05`、`1.50+0.50`、`content_standard: 2`。证明链固定为：

1. 常数函数、恒等函数连续；
2. 由有限次和、积推出多项式处处连续；
3. 由商法则推出有理函数在分母非零处连续；
4. 由 \(||x|-|a||\le |x-a|\) 证明绝对值连续；
5. 对 \(a>0\) 用有理化证明平方根连续，对 \(a=0\) 单独取 \(\delta=\varepsilon^2\)；
6. 用复合定理得到由这些函数有限组合成的表达式在其自然定义域上连续。

禁止以“初等函数都连续”作为无证明总括；指数、对数只作为明确的先备性质说明，不在本单元重新构造；三角函数证明留给选读桥，不纳入本轮核心页面。加入 `thm-u-03-10-05-algebraic-continuity`、`thm-u-03-10-05-root-continuity`、2 个完整例题、2 个即时检验、5 个习题和 7 个折叠答案。

- [x] **Step 2: 使正文合同转 GREEN**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_10 tests.test_parts_02_03_migration -v
```

Expected: 所有页面内容与迁移页面合同通过；仅导航/课程地图/站点锚点测试尚未完成。

### Task 7: 闭合章节导学、导航、课程地图与真实站点

**Files:**
- Rewrite: `content/chapters/chapter-10/index.md`
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `scripts/check_site.py`

- [x] **Step 1: 重写章节导学**

在 `index.md` 中给出本章问题弧、从第 9 章到第 11 章的依赖边界、5 单元阅读表、理论 `8` + 应用 `2` 学时，以及“点连续不等于一致连续、局部连续不自动推出全局有界”的章末接口。

- [x] **Step 2: 注册精确阅读顺序**

在 `mkdocs.yml` 的第 10 章导航块按下列顺序列出：

```yaml
- 10.1 连续性怎样把极限与函数值接起来？: chapters/chapter-10/u-03-10-01-epsilon-delta-continuity.md
- 10.2 连续性怎样经过运算和复合传递？: chapters/chapter-10/u-03-10-02-continuous-operations.md
- 10.3 端点连续与连续延拓怎样统一处理？: chapters/chapter-10/u-03-10-04-one-sided-continuity-extension.md
- 10.4 函数会以哪些方式失去连续性？: chapters/chapter-10/u-03-10-03-discontinuities-elementary-functions.md
- 10.5 常见初等函数的连续性从哪里来？: chapters/chapter-10/u-03-10-05-elementary-continuity-bridge.md
```

- [x] **Step 3: 更新课程地图**

在 `content/course-map.md` 第 10 章下增加 5 个页面链接，并显示 `8 + 2 = 10` 学时；不修改第 11、12 章内容。

- [x] **Step 4: 增加真实站点代表锚点**

在 `scripts/check_site.py` 的代表锚点映射中加入 10.4 连续延拓定理和 10.5 代数连续性定理，确保 Zensical 产物含对应 HTML `id`。

- [x] **Step 5: 使章级、结构和站点测试转 GREEN**

Run:

```bash
python3.12 -m unittest tests.test_chapter_10 tests.test_parts_02_03_migration tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: 全部通过，Zensical 无严格模式警告，第 10 章 5 页均在 `site/chapters/chapter-10/` 生成。

### Task 8: 数学审查和全量验收

**Files:**
- Modify: `docs/superpowers/plans/2026-07-25-chapter-10-self-study-rewrite.md`

- [x] **Step 1: 执行数学边界检查**

逐页检查并记录：

- 所有连续性定义均带 \(f:D\to\mathbb R\)、\(a\in D\) 或明确的单侧定义域；
- 序列连续性量词覆盖每个 \(x_n\in D\) 且 \(x_n\to a\)；
- 商法则包含 \(g(a)\ne0\) 并解释局部分母非零；
- 复合定理核验内层值落入外层定义域；
- 连续延拓只在有限极限存在时成立；
- 间断分类没有把定义域外的点直接称作“不连续点”；
- 根式在端点 \(0\) 单独证明；
- 无导数、中值定理、Taylor、洛必达、Newton 或积分偷渡。

- [x] **Step 2: 检查源码完整性**

Run:

```bash
rg -n "TBD|TODO|待补|显然|容易看出" content/chapters/chapter-10
git diff --check
```

Expected: 无占位文本、无用“显然/容易看出”跳过关键证明、无空白错误。

- [x] **Step 3: 运行最终质量门**

Run:

```bash
make verify
```

Expected: 全部单元、算法、内容、结构、Zensical 严格构建和真实站点检查通过。

- [x] **Step 4: 记录验收结果**

把本计划已执行项标记为 `[x]`，在末尾记录测试数量、构建结果、第 10 章页面数量和数学边界检查结论。本轮到此停止，不创建或改写第 11 章。

## 验收记录

- TDD：新增章级合同首先按预期失败，明确捕获两个缺页、三个 v1 单元、旧学时和旧导航；正文与注册完成后转绿。
- 正文：第 10 章现有 5 个 `content_standard: 2` 核心单元，理论 `8` + 应用 `2` = `10` 学时；每页含 2 个稳定例题、2 个即时检验、5 道分层习题和 7 个页面内折叠完整答案。
- 数学边界：逐页复核了相对定义域、孤立点、序列量词、商的局部非零、复合定义域、有限连续延拓、间断诊断和根式端点分证；核心证明未使用后续微分、积分或数值求根理论。
- 站点：`mkdocs.yml`、课程地图、迁移页面合同和 `scripts/check_site.py` 已纳入 5 页顺序及新增稳定锚点。
- 全量质量门：`make verify` 通过 44 项测试、统一内容检查、Zensical `--strict` 构建和真实站点检查；严格构建报告 `No issues found`。
- 停止边界：未创建、重写或调整第 11 章正文。
