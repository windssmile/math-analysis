# 第一部第二章学习单元 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完成“实数系与完备性公理”的三个学习单元，使读者从有理数缺口进入 Dedekind 分割构造，并能使用分割的序、运算和完备性。

**Architecture:** 三页依次发布、依次加入第一部 Quarto 导航和 `curriculum/units.toml`。不在第 2 章调用 Cauchy 列或连续性；Cauchy 列的比较留给第 4 章，确界原理的系统应用留给第 3 章。

**Tech Stack:** Quarto Markdown、Python 3.12 `unittest`、TOML、既有单元/站点验证器。

---

## Shared chapter contract

- 单元：`u-01-02-01`、`u-01-02-02`、`u-01-02-03`；总学时为理论 5、应用 0.5。
- 每页有稳定 H1、八个既定 H2、完整元数据、3–6 道稳定 ID 习题与折叠答案；长证明至少一题给出完整解答。
- 第 2 章仅假设已知 `\mathbb N,\mathbb Z,\mathbb Q` 的基本运算及第 1 章的集合/量词/证明语言；不从 Peano 公理构造数系。
- 每增加一个注册单元，立刻加入 `_quarto.yml` 第一部导航并通过 `scripts/check_site.py` 的已登记页面检查。

### Task 1: 有理数为什么仍然不够？

**Files:** Create `book/part-01/chapter-02/u-01-02-01-rational-gaps.qmd`; modify `curriculum/units.toml`, `tests/test_chapter_02.py`, `_quarto.yml`.

- [ ] **Step 1: 写失败的注册测试**

新增 `tests/test_chapter_02.py`，断言 `u-01-02-01` 的路径、理论/应用学时为 `(1.5, 0.0)`、能力为 `["concepts", "proof", "mathematical_expression"]`；先运行并确认 `KeyError`。

- [ ] **Step 2: 登记与撰写**

登记标题“有理数为什么仍然不够？”，难度 2；高等代数先备为 `["整数与有理数的四则运算", "平方与因式分解"]`，其余外部先备为空。正文以“是否存在有理数平方等于 2？”为牵引：完整证明 `\sqrt2\notin\mathbb Q`；用 `\{q\in\mathbb Q:q^2<2\text{ 或 }q<0\}` 展示缺口；区分“有理数中无解”和“还需扩张数系”。不得把十进制展开或计算器近似当作无理性的证明。给出 3–5 道带折叠答案习题，其中一题完整解答为互素分数的奇偶矛盾。

- [ ] **Step 3: 发布、验证、提交**

将页面加入第一部导航末尾，运行 `python3.12 -m unittest tests.test_chapter_02 tests.test_units -v`、`python3.12 scripts/check_units.py`、受控单进程 Quarto 渲染和 `scripts/check_site.py`；确认 HTML 与无 `mjx-merror`。提交 `docs: add rational gaps learning unit`。

### Task 2: 怎样用切割构造一个实数？

**Files:** Create `book/part-01/chapter-02/u-01-02-02-dedekind-cuts.qmd`; modify registry/tests/navigation.

- [ ] **Step 1: 写失败测试**

增加 `u-01-02-02` 的路径断言、学时 `(2.0, 0.25)` 和能力 `["concepts", "proof", "mathematical_expression"]`；运行并确认失败。

- [ ] **Step 2: 登记与撰写**

标题“怎样用切割构造一个实数？”，难度 3；高等代数先备为 `["有理数的序与稠密性"]`。精确定义 Dedekind 分割为有理数真子集 `A`，满足非空、非全体、向下封闭、无最大元四条件；解释有理数 `r` 的嵌入 `A_r=\{q:q<r\}`；构造 `\sqrt2` 对应分割。至少完整证明该 `\sqrt2` 集合满足四条件，特别处理“无最大元”而不循环引用实数。例题/即时检验要辨别错误切割；习题 3–6 道、折叠答案，代表题完整解答。

- [ ] **Step 3: 发布、验证、提交**

导航紧随 02-01；同样执行测试、注册校验、受控渲染、站点检查和差异检查；提交 `docs: add Dedekind cuts learning unit`。

### Task 3: 构造后怎样计算与比较？

**Files:** Create `book/part-01/chapter-02/u-01-02-03-cut-order-operations.qmd`; modify registry/tests/navigation.

- [ ] **Step 1: 写失败测试**

增加 `u-01-02-03` 的路径、学时 `(1.5, 0.25)`、能力 `["concepts", "proof", "mathematical_expression"]` 的断言并确认失败。

- [ ] **Step 2: 登记与撰写**

标题“构造后怎样计算与比较？”，难度 3；高等代数先备 `["有理数的序与四则运算"]`。定义切割比较为包含关系，给出加法与相反数的可读定义（必要时用下确界式描述并说明边界），证明有理数嵌入保持序；用“所有低于一族切割的有理数的并集”给出完备性的构造性理由。避免逐项证明完整有序域公理，只证明至少一个代表性性质并清晰说明哪些代数细节作为练习/附录。不得引入 Cauchy 列。习题包含比较切割、嵌入保持序、并集构成上确界的关键条件，3–6 道全有折叠答案。

- [ ] **Step 3: 发布与章节验收**

导航紧随 02-02；在 `tests/test_chapter_02.py` 断言三个单元合计理论 5、应用 .5 并检查三页都在 QML。运行 `make verify`（使用可写的 Quarto 用户缓存/单进程），确认 8 个已登记单元均生成 HTML，站点检查通过；提交 `docs: publish real-number construction chapter`。

