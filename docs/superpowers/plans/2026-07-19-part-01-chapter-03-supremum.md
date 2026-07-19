# 第一部第三章学习单元 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 以“有上界为什么还不够？”为问题弧完成上界、下界、确界原理及其基本推论，使读者能够完成基于确界的存在性证明。

**Architecture:** 三个单元按概念失败案例、最小上界原理、推论迁移顺序发布；只使用第 1–2 章已建立的实数与切割完备性，不引入连续性或数列收敛作为前置。

**Tech Stack:** Quarto Markdown、Python 3.12 `unittest`、TOML、既有 unit/site validators。

---

## Shared contract

- `u-01-03-01`、`u-01-03-02`、`u-01-03-03`，合计理论 5、应用 0。
- 每页：稳定单元 H1、八个固定 H2、所有先备类别、稳定定义/定理/例题/习题 ID、3–6 道折叠答案习题。
- 逐页登记并加入第一部导航；每次用 `DENO_DIR=/private/tmp/mathbook-quarto-deno make verify` 取得渲染证据，不改变 HOME。

### Task 1: 有上界为什么还不够？

**Files:** create `book/part-01/chapter-03/u-01-03-01-bounds.qmd`; modify registry, `tests/test_chapter_03.py`, QML.

- [ ] TDD 注册 `u-01-03-01`，学时 1.5+0，能力 `["concepts","proof","mathematical_expression"]`，先确认 KeyError。
- [ ] 登记标题“有上界为什么还不够？”，高等代数先备 `["不等式的基本性质"]`，难度 2。正文区分上界、下界、最大/最小元、上确界/下确界；以 `\{q\in\mathbb Q:q^2<2\text{ 或 }q<0\}` 说明有理数中可有上界却没有最小上界。定义与例题均给稳定锚点；习题必须包含识别界/最大值/确界和一个反例。
- [ ] 发布、渲染、确认 HTML/锚点/no-mjx-error，提交 `docs: add bounds learning unit`。

### Task 2: 最小上界怎样保证存在？

**Files:** create `book/part-01/chapter-03/u-01-03-02-supremum-principle.qmd`; modify registry/tests/QML.

- [ ] TDD 注册 `u-01-03-02`，学时 2+0，能力 `["concepts","proof","mathematical_expression"]`。
- [ ] 登记标题“最小上界怎样保证存在？”，难度 3。精确陈述实数最小上界原理及下确界对偶形式，并明确它来自上一章的切割并集构造。核心例题完整证明：若 `a>0`，集合 `\{x\ge0:x^2<a\}` 有上确界 `s` 且 `s^2=a`；证明必须避免用连续性或预先存在的平方根。用适当的有理扰动/不等式完成 `s^2<a` 与 `s^2>a` 两种矛盾。稳定定理/例题 ID、折叠答案和完整证明均必需。
- [ ] 发布、全量验证、提交 `docs: add supremum principle learning unit`。

### Task 3: 确界原理能推出什么？

**Files:** create `book/part-01/chapter-03/u-01-03-03-completeness-consequences.qmd`; modify registry/tests/QML.

- [ ] TDD 注册 `u-01-03-03`，学时 1.5+0，能力 `["concepts","proof","mathematical_expression"]`。
- [ ] 登记标题“确界原理能推出什么？”，难度 3。给出 Archimedean 性质、\(\mathbb Q\) 在 \(\mathbb R\) 中稠密、平方根存在三项推论；至少完整证明 Archimedean 性质与一个稠密性或平方根推论。明确在本单元后第 1 章的量词练习可以使用这些结论。不得引入数列极限作为证明工具。提供稳定锚点、3–6 道带折叠答案习题。
- [ ] 章节测试锁定三页理论总计 5、应用 0 与导航；全量受控渲染/站点/MathJax 检查，提交 `docs: publish supremum chapter`。
