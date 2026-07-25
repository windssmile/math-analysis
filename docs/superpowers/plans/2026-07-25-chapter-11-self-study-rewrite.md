# 第 11 章自学教材级重写 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 Zensical modern 架构下，把第 11 章重建为 3 个 `content_standard: 2` 核心单元，以实数闭区间的序列紧致性证明最值定理和 Heine–Cantor 定理，并在本章验收后停止。

**Architecture:** `content/chapters/chapter-11/` 保存正文与单元元数据，`mkdocs.yml` 和 `content/course-map.md` 保存阅读入口；`tests/test_chapter_11.py` 固化 `5+1=6` 学时、序列主线和证明边界，`scripts/check_content.py` 检查统一 v2 结构，`scripts/check_site.py` 检查 Zensical 真实锚点。核心正文直接调用第二部 Bolzano–Weierstrass 定理，不重复其证明；开覆盖只允许作为选读前瞻。

**Tech Stack:** Markdown、YAML front matter、Python 3.12 `unittest`、Zensical 0.0.51 modern、MathJax 3、PyMdown details。

---

### Task 1: 写出第 11 章最终合同的失败测试

**Files:**
- Create: `tests/test_chapter_11.py`
- Modify: `tests/test_mkdocs_site.py`
- Modify: `scripts/check_site.py`

- [x] **Step 1: 创建章级合同**

要求以下精确元数据：

```python
EXPECTED_UNITS = [
    ("u-03-11-01", "为什么闭区间中的数列总有收敛子列？", 1.75, 0.25, "compact-intervals"),
    ("u-03-11-02", "连续函数为何一定有界并取得最值？", 1.75, 0.25, "extreme-value-theorem"),
    ("u-03-11-03", "局部连续何时升级为全局一致控制？", 1.50, 0.50, "uniform-continuity"),
]
```

逐页断言 `content_standard == 2`，合计理论 `5.0`、应用 `1.0`，并要求：

```python
REQUIRED_ANCHORS = {
    "u-03-11-01": (
        "def-u-03-11-01-sequential-compactness",
        "thm-u-03-11-01-closed-interval-sequentially-compact",
    ),
    "u-03-11-02": (
        "thm-u-03-11-02-boundedness",
        "thm-u-03-11-02-extreme-value",
    ),
    "u-03-11-03": (
        "def-u-03-11-03-uniform-continuity",
        "thm-u-03-11-03-uniform-continuity",
    ),
}
```

11.1 核心正文必须出现 `Bolzano–Weierstrass` 和闭性保留极限，不得出现旧锚点
`def-u-03-11-01-open-cover`、`def-u-03-11-01-compactness`、
`thm-u-03-11-01-heine-borel`；“开覆盖”只允许出现在
`### 选读前瞻：第七部的开覆盖语言` 之后。

- [x] **Step 2: 先改真实站点锚点合同**

把 `scripts/check_site.py` 的第 11 章代表锚点从旧 Heine–Borel 锚点改成：

```python
[
    "def-u-03-11-01-sequential-compactness",
    "thm-u-03-11-01-closed-interval-sequentially-compact",
]
```

同步更新 `tests/test_mkdocs_site.py` 的静态合同。

- [x] **Step 3: 观察 RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_11 tests.test_mkdocs_site -v
```

Expected: 旧标题、旧学时、v1 页面、开覆盖主线与缺失新锚点造成失败。

### Task 2: 重写 11.1 闭区间的序列紧致性

**Files:**
- Rewrite: `content/chapters/chapter-11/u-03-11-01-compact-intervals.md`

- [x] **Step 1: 建立实数范围内的序列主线**

页面使用 `1.75+0.25`、`content_standard: 2`。正文完成：

1. 定义实数集合的序列紧致性；
2. 证明收敛数列若各项在闭集内，则极限仍在闭集内；
3. 证明 `[a,b]` 中任意数列有界，由第二部 Bolzano–Weierstrass 抽取收敛子列；
4. 用闭性证明子列极限仍在 `[a,b]`；
5. 用 `(0,1)`、`[0,\infty)` 区分闭、有界与序列紧致；
6. 开覆盖只放在 `### 选读前瞻：第七部的开覆盖语言`，不定义、不证明、不参与后续依赖。

加入 2 个完整例题、2 个即时检验、5 道习题和 7 个折叠完整答案。

- [x] **Step 2: 运行内容检查**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_11 -v
```

Expected: 11.1 合同通过，11.2、11.3 仍因 v1 与旧学时保持 RED。

### Task 3: 重写 11.2 最值定理

**Files:**
- Rewrite: `content/chapters/chapter-11/u-03-11-02-extreme-value-theorem.md`

- [x] **Step 1: 分开证明有界与取界**

页面使用 `1.75+0.25`、`content_standard: 2`。先反设无界，选择
\(|f(x_n)|>n\)，抽取 \(x_{n_k}\to c\in[a,b]\)，由连续性推出函数值子列有有限
极限而矛盾。再令 \(M=\sup f([a,b])\)，选择
\(M-1/n<f(x_n)\le M\)，抽取收敛子列并用连续性与夹逼证明 \(f(q)=M\)；
最小值对下确界独立陈述。明确连续性、闭性、有界性各自使用位置。

保留 `thm-u-03-11-02-extreme-value`，新增 `thm-u-03-11-02-boundedness`；
加入开区间、非连续函数和无界区间反例，以及完整 v2 训练结构。

- [x] **Step 2: 运行内容检查**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_11 -v
```

Expected: 11.1、11.2 通过，11.3 保持 RED。

### Task 4: 重写 11.3 一致连续与 Heine–Cantor

**Files:**
- Rewrite: `content/chapters/chapter-11/u-03-11-03-uniform-continuity.md`

- [x] **Step 1: 用成对点列完成反证**

页面使用 `1.50+0.50`、`content_standard: 2`。先对比逐点连续与一致连续的量词
顺序。证明 Heine–Cantor 时反设不一致连续，固定 \(\varepsilon_0>0\)，对每个
\(n\) 选择 \(x_n,y_n\in[a,b]\)，满足
\[
|x_n-y_n|<1/n,\qquad |f(x_n)-f(y_n)|\ge\varepsilon_0.
\]
由 11.1 从 \(x_n\) 抽取 \(x_{n_k}\to c\)，再证明
\(y_{n_k}\to c\)，由 \(f\) 在 \(c\) 连续推出两个函数值子列都趋于 \(f(c)\)，
与固定差距矛盾。

用 \(1/x\) 在 `(0,1)`、\(x^2\) 在实轴上的成对点列反例说明紧致域条件；
加入 2 个例题、2 个即时检验、5 道习题和 7 个折叠答案。

- [x] **Step 2: 使正文合同转 GREEN**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_11 -v
```

Expected: 全部通过。

### Task 5: 闭合导学、导航、课程地图和站点

**Files:**
- Rewrite: `content/chapters/chapter-11/index.md`
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`

- [x] **Step 1: 更新学习入口**

章节导学写明“第二部 Bolzano–Weierstrass → 闭区间序列紧致 → 有界/最值/一致连续”
依赖链以及 `5+1=6` 学时。`mkdocs.yml` 更新 11.1 新标题，保持 11.1–11.3 URL。
课程地图列出 3 个链接和 `本章学时：6 小时（理论 5，应用 1）。`

- [x] **Step 2: 更新章级测试的入口合同**

`tests/test_chapter_11.py` 要求导航与课程地图精确顺序、标题、链接和学时。

- [x] **Step 3: 验证站点**

Run:

```bash
python3.12 -m unittest tests.test_chapter_11 tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: 全部通过，三个页面发布且新序列紧致锚点出现在真实 HTML。

### Task 6: 数学审查和全量验收

**Files:**
- Modify: `docs/superpowers/plans/2026-07-25-chapter-11-self-study-rewrite.md`

- [x] **Step 1: 检查证明边界**

核对：

- 11.1 直接引用而不重证 Bolzano–Weierstrass；
- 闭区间序列极限留在区间内的端点不等式完整；
- 最值定理先证有界，再定义有限上、下确界；
- 逼近上确界的点选择对每个 \(n\) 有效；
- Heine–Cantor 否定量词固定同一个 \(\varepsilon_0\)；
- 成对子列 \(y_{n_k}\to c\) 的三角不等式写全；
- 开覆盖不进入核心证明；
- 不提前使用介值定理、微分或积分理论。

- [x] **Step 2: 最终质量门**

Run:

```bash
rg -n "TBD|TODO|待补|显然|容易看出" content/chapters/chapter-11
git diff --check
make verify
```

Expected: 无占位或证明跳步，全部测试、内容检查、Zensical 严格构建和站点检查通过。

- [x] **Step 3: 记录验收并停止**

标记完成项并记录测试数、页面结构、构建结果与数学审查。本轮不创建、重写或调整第 12 章正文。

## 验收记录

- TDD：章级合同首先按预期暴露旧标题、旧学时、三个 v1 页面、开覆盖主线与旧站点锚点；实现后全部转绿。
- 正文：3 个 `content_standard: 2` 单元，理论 `5` + 应用 `1` = `6` 学时；每页含 2 个稳定例题、2 个即时检验、5 道习题和 7 个折叠完整答案。
- 数学审查：11.1 只引用第二部 Bolzano–Weierstrass，并完整证明闭性保留极限；11.2 分开证明有界与取界；11.3 的否定量词固定同一个 \(\varepsilon_0\)，并完整证明成对子列收敛到公共极限。
- 边界：开覆盖仅留在明确标注的选读前瞻；核心证明未使用第 12 章存在性结论或后续微分、积分理论。
- 全量验收：`make verify` 通过 48 项测试、统一内容检查、Zensical `--strict` 构建和真实站点检查；严格构建报告 `No issues found`。
- 停止边界：未创建、重写或调整第 12 章正文。
