# 第一部第一章学习单元 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将第一部第一章“函数、集合与数学陈述”写成四个可发布、可校验的学习单元，为后续实数构造与证明训练建立全书风格基线。

**Architecture:** 继续使用 `curriculum/units.toml` 作为已发布学习单元的唯一机器可读注册表，并让每个 QMD 直接满足既有八段式单元合同。先逐个完成并验证四个页面，最后才将它们加入 Quarto 的书籍导航；这样不会在已发布站点暴露空白或半成品页面。

**Tech Stack:** Quarto Markdown、Python 3.12 标准库 `unittest`、TOML、现有 `scripts/check_units.py` 与 `make verify`。

**Scope decision:** 第一部其余三章（Dedekind 分割、确界原理、递推与无限逼近）依赖本章的符号、证明和习题风格。它们不进入本计划，待本章验收后各自创建计划；14 单元总蓝图见 `docs/superpowers/specs/2026-07-19-part-01-foundation-blueprint-design.md`。

---

## File structure

- Modify: `curriculum/units.toml` — 依次登记四个已完成的第一章单元。
- Modify: `_quarto.yml` — 在全部四页完成后，将它们作为“第一部”导航项加入书籍。
- Create: `book/part-01/chapter-01/u-01-01-01-sets.qmd` — 集合与数学对象。
- Create: `book/part-01/chapter-01/u-01-01-02-quantifiers.qmd` — 命题、量词与否定。
- Create: `book/part-01/chapter-01/u-01-01-03-proofs.qmd` — 证明与反例。
- Create: `book/part-01/chapter-01/u-01-01-04-functions.qmd` — 函数作为映射。
- Create: `tests/test_chapter_01.py` — 锁定第一章稳定 ID、学时和关键正文合同。

## Shared content contract

每个页面必须：

1. 用 `# 标题 {#u-01-01-0x}` 作为首个一级标题，并包含既有的八个精确二级标题。
2. 开头使用 `::: {.unit-meta}` 块，列出总学时、全书先备、高等代数先备、解析几何先备和 Python 先备。
3. 正式习题使用 `ex-u-01-01-0x-yy` 形式的稳定 ID；每题紧随可折叠答案，至少一题提供完整解答。
4. 不使用可执行 Quarto 单元；第一章没有 Python 代码运行时依赖。
5. 每页有 3–6 道正式习题、至少一个概念辨析任务，并在需要处给出证明或反例任务。

### Task 1: 完成集合与数学对象单元

**Files:**

- Create: `book/part-01/chapter-01/u-01-01-01-sets.qmd`
- Modify: `curriculum/units.toml`
- Create: `tests/test_chapter_01.py`

- [ ] **Step 1: 写入失败的第一单元注册测试**

在 `tests/test_chapter_01.py` 创建下列测试。它锁定首个单元的稳定 ID、文件、学时与能力，而不依赖 TOML 条目顺序。

```python
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class ChapterOneRegistryTests(unittest.TestCase):
    def load_units(self) -> dict[str, dict[str, object]]:
        with UNITS.open("rb") as handle:
            data = tomllib.load(handle)
        return {unit["id"]: unit for unit in data["units"]}

    def test_sets_unit_has_published_contract(self) -> None:
        unit = self.load_units()["u-01-01-01"]
        self.assertEqual("chapter-01", unit["chapter_id"])
        self.assertEqual(
            "book/part-01/chapter-01/u-01-01-01-sets.qmd", unit["path"]
        )
        self.assertEqual((1.25, 0.25), (unit["theory_hours"], unit["applied_hours"]))
        self.assertEqual(
            ["concepts", "proof", "mathematical_expression"], unit["capabilities"]
        )
```

- [ ] **Step 2: 运行测试，确认它因缺少注册表条目失败**

Run: `python3.12 -m unittest tests.test_chapter_01 -v`  
Expected: `KeyError: 'u-01-01-01'`.

- [ ] **Step 3: 登记单元并写完整正文**

在 `curriculum/units.toml` 添加如下元数据，位于现有 `[[units]]` 条目之后：

```toml
[[units]]
id = "u-01-01-01"
chapter_id = "chapter-01"
title = "集合怎样组织数学对象？"
path = "book/part-01/chapter-01/u-01-01-01-sets.qmd"
theory_hours = 1.25
applied_hours = 0.25
difficulty = 1
book_prerequisites = []
higher_algebra_prerequisites = []
analytic_geometry_prerequisites = []
python_prerequisites = []
knowledge_bridges = []
capabilities = ["concepts", "proof", "mathematical_expression"]
learning_goals = [
  "用集合、元素关系、子集和集合运算准确表述数学对象",
  "区分属于、包含、相等与空集等常见符号关系",
  "证明集合恒等式并用反例否定错误的集合陈述",
]
```

正文必须以“班级名单、满足条件的实数与平面点集如何用有限符号描述”为牵引问题，依次覆盖集合、元素、子集、并、交、差、补、笛卡尔积和幂集。例题至少完整证明 De Morgan 律之一，并解释逐元素证明策略；即时检验包含量词式集合定义与一个错误等式的反例。习题 3–5 道，包含集合恒等式、笛卡尔积和“何时两个集合相等”，其中至少一题提供完整逐元素证明。

- [ ] **Step 4: 运行单元与章节测试**

Run: `python3.12 -m unittest tests.test_units tests.test_chapter_01 -v`  
Expected: PASS，且 `scripts/check_units.py` 报告 2 个有效单元。

- [ ] **Step 5: 提交首个单元**

```bash
git add curriculum/units.toml tests/test_chapter_01.py \
  book/part-01/chapter-01/u-01-01-01-sets.qmd
git commit -m "docs: add sets learning unit"
```

### Task 2: 完成命题、量词与否定单元

**Files:**

- Create: `book/part-01/chapter-01/u-01-01-02-quantifiers.qmd`
- Modify: `curriculum/units.toml`
- Modify: `tests/test_chapter_01.py`

- [ ] **Step 1: 添加失败的量词单元测试**

向测试类加入：

```python
def test_quantifier_unit_has_published_contract(self) -> None:
    unit = self.load_units()["u-01-01-02"]
    self.assertEqual("chapter-01", unit["chapter_id"])
    self.assertEqual(
        "book/part-01/chapter-01/u-01-01-02-quantifiers.qmd", unit["path"]
    )
    self.assertEqual((1.25, 0.25), (unit["theory_hours"], unit["applied_hours"]))
    self.assertEqual(["concepts", "proof", "mathematical_expression"], unit["capabilities"])
```

- [ ] **Step 2: 运行测试，确认它失败**

Run: `python3.12 -m unittest tests.test_chapter_01.ChapterOneRegistryTests.test_quantifier_unit_has_published_contract -v`  
Expected: `KeyError: 'u-01-01-02'`.

- [ ] **Step 3: 登记并撰写量词单元**

添加 ID `u-01-01-02`、路径 `book/part-01/chapter-01/u-01-01-02-quantifiers.qmd`、理论 1.25、应用 0.25、难度 1、空的三类外部先备和知识桥，能力 `["concepts", "proof", "mathematical_expression"]`。学习目标必须覆盖：识别命题与谓词、正确处理全称和存在量词、否定嵌套量词。

正文从“每个正数是否都有平方根”与“是否存在一个数使所有条件成立”的语序差异出发。概念与理论应定义命题、谓词、量词作用域、蕴含、等价和否定；例题完整推导

```tex
\neg(\forall x\in A,\ \exists y\in B,\ P(x,y))
\quad\Longleftrightarrow\quad
\exists x\in A,\ \forall y\in B,\ \neg P(x,y).
```

即时检验必须包含至少两条量词否定及答案。习题 3–5 道，至少一题要求从自然语言写出量词表达，至少一题要求构造反例说明 `\forall x\exists y` 与 `\exists y\forall x` 不可交换。

- [ ] **Step 4: 验证并提交**

Run: `python3.12 -m unittest tests.test_units tests.test_chapter_01 -v`  
Expected: PASS，`scripts/check_units.py` 报告 3 个有效单元。

```bash
git add curriculum/units.toml tests/test_chapter_01.py \
  book/part-01/chapter-01/u-01-01-02-quantifiers.qmd
git commit -m "docs: add quantifier learning unit"
```

### Task 3: 完成证明与反例单元

**Files:**

- Create: `book/part-01/chapter-01/u-01-01-03-proofs.qmd`
- Modify: `curriculum/units.toml`
- Modify: `tests/test_chapter_01.py`

- [ ] **Step 1: 添加失败的证明单元测试**

向测试类加入：

```python
def test_proof_unit_has_published_contract(self) -> None:
    unit = self.load_units()["u-01-01-03"]
    self.assertEqual(
        "book/part-01/chapter-01/u-01-01-03-proofs.qmd", unit["path"]
    )
    self.assertEqual((1.5, 0.5), (unit["theory_hours"], unit["applied_hours"]))
    self.assertEqual(["proof", "mathematical_expression"], unit["capabilities"])
```

- [ ] **Step 2: 运行测试，确认它失败**

Run: `python3.12 -m unittest tests.test_chapter_01.ChapterOneRegistryTests.test_proof_unit_has_published_contract -v`  
Expected: `KeyError: 'u-01-01-03'`.

- [ ] **Step 3: 登记并撰写证明单元**

添加 ID `u-01-01-03`、路径 `book/part-01/chapter-01/u-01-01-03-proofs.qmd`、理论 1.50、应用 0.50、难度 2、空的三类外部先备与知识桥，能力 `["proof", "mathematical_expression"]`。学习目标必须覆盖：从定义出发组织直接证明、把蕴含改写为逆否命题、用反证法识别矛盾、用单个反例否定全称断言。

正文必须将“所有命题都有同一种证明吗？”作为牵引问题，区分证明与验证有限例子。例题需完整证明“若整数 `n^2` 为偶数，则 `n` 为偶数”的逆否命题，并给出“每个有界数列收敛”这一错误断言的振荡反例。应用活动以“给一段缺少量词或隐含假设的伪证明，标出失效点并修复”为中心。习题 3–6 道，至少一题完整解答采用反证法，至少一题只需给反例。

- [ ] **Step 4: 验证并提交**

Run: `python3.12 -m unittest tests.test_units tests.test_chapter_01 -v`  
Expected: PASS，`scripts/check_units.py` 报告 4 个有效单元。

```bash
git add curriculum/units.toml tests/test_chapter_01.py \
  book/part-01/chapter-01/u-01-01-03-proofs.qmd
git commit -m "docs: add proof learning unit"
```

### Task 4: 完成函数作为映射单元

**Files:**

- Create: `book/part-01/chapter-01/u-01-01-04-functions.qmd`
- Modify: `curriculum/units.toml`
- Modify: `tests/test_chapter_01.py`

- [ ] **Step 1: 添加失败的函数单元测试**

向测试类加入：

```python
def test_function_unit_has_published_contract(self) -> None:
    unit = self.load_units()["u-01-01-04"]
    self.assertEqual(
        "book/part-01/chapter-01/u-01-01-04-functions.qmd", unit["path"]
    )
    self.assertEqual((1.0, 0.0), (unit["theory_hours"], unit["applied_hours"]))
    self.assertEqual(["concepts", "proof", "mathematical_expression"], unit["capabilities"])
```

- [ ] **Step 2: 运行测试，确认它失败**

Run: `python3.12 -m unittest tests.test_chapter_01.ChapterOneRegistryTests.test_function_unit_has_published_contract -v`  
Expected: `KeyError: 'u-01-01-04'`.

- [ ] **Step 3: 登记并撰写函数单元**

添加 ID `u-01-01-04`、路径 `book/part-01/chapter-01/u-01-01-04-functions.qmd`、理论 1.00、应用 0、难度 1；高等代数先备为 `["多项式的基本运算"]`，解析几何先备为 `["平面直角坐标系与图像读取"]`，Python 先备与知识桥为空，能力为 `["concepts", "proof", "mathematical_expression"]`。

正文必须从“同一条公式为什么有时不能定义函数？”切入，明确区分公式、函数、定义域、陪域、值域、图像、复合、单射、满射和可逆。例题完整证明：若 `f:A\to B` 与 `g:B\to C` 都是单射，则 `g\circ f` 是单射；迁移例必须解释 `x\mapsto 1/x` 在不同定义域上的差异。习题 3–5 道，包含定义域辨析、复合、逆函数条件与图像不能代替定义域的反例。

- [ ] **Step 4: 验证并提交**

Run: `python3.12 -m unittest tests.test_units tests.test_chapter_01 -v`  
Expected: PASS，`scripts/check_units.py` 报告 5 个有效单元。

```bash
git add curriculum/units.toml tests/test_chapter_01.py \
  book/part-01/chapter-01/u-01-01-04-functions.qmd
git commit -m "docs: add function learning unit"
```

### Task 5: 将第一章纳入书籍导航并完成章节验收

**Files:**

- Modify: `_quarto.yml`
- Modify: `tests/test_chapter_01.py`

- [ ] **Step 1: 添加失败的章节学时与导航测试**

在 `tests/test_chapter_01.py` 增加：

```python
def test_chapter_one_hours_and_navigation_are_complete(self) -> None:
    units = self.load_units()
    chapter_units = [
        units[f"u-01-01-0{index}"] for index in range(1, 5)
    ]
    self.assertEqual(
        (5.0, 1.0),
        (
            sum(unit["theory_hours"] for unit in chapter_units),
            sum(unit["applied_hours"] for unit in chapter_units),
        ),
    )
    quarto = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
    for unit in chapter_units:
        self.assertIn(unit["path"], quarto)
```

- [ ] **Step 2: 运行测试，确认导航断言失败**

Run: `python3.12 -m unittest tests.test_chapter_01.ChapterOneRegistryTests.test_chapter_one_hours_and_navigation_are_complete -v`  
Expected: FAIL，因为四个路径尚未全部位于 `_quarto.yml`。

- [ ] **Step 3: 加入第一部导航与章节回看**

在 `_quarto.yml` 的 `book.chapters` 中、第三部之前插入：

```yaml
    - part: "第一部：实数、函数与分析语言"
      chapters:
        - book/part-01/chapter-01/u-01-01-01-sets.qmd
        - book/part-01/chapter-01/u-01-01-02-quantifiers.qmd
        - book/part-01/chapter-01/u-01-01-03-proofs.qmd
        - book/part-01/chapter-01/u-01-01-04-functions.qmd
```

检查四页的“即时检验与回望”最后都用一段“第 2 章如何使用本页工具”收束：集合和函数给出对象语言，量词规定定义与命题的精确形式，证明策略处理性质，函数定义域为实数构造中的映射与序比较做准备。

- [ ] **Step 4: 执行完整验证与人工阅读检查**

Run: `make verify`  
Expected: 全部 `unittest`、课程/单元校验、Quarto 渲染与站内链接检查通过。

Run: `quarto render`  
Expected: `_site/book/part-01/chapter-01/` 下生成四个 HTML 页面，页面没有 `mjx-merror`，导航按集合、量词、证明、函数顺序出现。

- [ ] **Step 5: 提交章节集成**

```bash
git add _quarto.yml tests/test_chapter_01.py
git commit -m "docs: publish chapter one learning path"
```

## Final verification

- [ ] Run `git diff --check`; expected: no output.
- [ ] Run `make verify`; expected: all tests and all generated-site checks pass.
- [ ] Open the four rendered pages in order; verify every page has eight section headings, foldable answers, correct previous/next navigation, and no MathJax error.
- [ ] Confirm `curriculum/units.toml` contains exactly five published units at this stage: the existing pilot plus the four Chapter 1 units.

