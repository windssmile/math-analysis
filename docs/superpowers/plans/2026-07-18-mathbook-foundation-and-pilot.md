# Mathematical Analysis Book Foundation and Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a testable Quarto/GitHub Pages foundation, encode the confirmed 12-part/54-chapter curriculum as machine-checkable data, and publish one representative double-helix learning unit on the intermediate value theorem and bisection method.

**Architecture:** Keep the confirmed design document as the human-readable contract and add TOML registries as the machine-readable source for curriculum structure and unit metadata. Python standard-library validators enforce hours, IDs, dependencies, required learning-unit sections, and generated-site integrity; Quarto renders the static book, while GitHub Actions runs every check before deploying to Pages. This plan deliberately stops after one pilot unit so that unit length, proof density, answer presentation, and site ergonomics can be reviewed before planning all 180 units.

**Tech Stack:** Quarto Book, Markdown/QMD, LaTeX math, Python 3.12 standard library (`unittest`, `tomllib`, `html.parser`), TOML, CSS, GitHub Actions, GitHub Pages.

---

## Scope decomposition

This is the first independently testable implementation slice. Do not create empty files for all 54 chapters and do not bulk-write manuscript prose.

Follow-up plans are intentionally separate:

1. Full 180-unit curriculum map and cross-course prerequisite graph.
2. Multi-unit sample set and exercise/solution baseline.
3. Batch manuscript production by part, with mathematical review gates.

### Specification coverage in this slice

| Confirmed design requirement | Implemented by |
|---|---|
| 12 parts, 54 chapters, 270+90 hours | Tasks 2–3 |
| Three-level navigation and reader-facing course map | Tasks 1 and 3 |
| Explicit book, higher-algebra, analytic-geometry, and Python prerequisites | Task 4 |
| Five-stage learning loop and stable IDs | Tasks 4 and 6 |
| Complete core proof plus problem-driven theory/application convergence | Task 6 |
| Algorithm reasoning before tested Python | Tasks 5–6 |
| Every formal exercise has an answer; representative method has a complete solution | Task 6 |
| Quarto, GitHub Pages, gated build, and site checks | Tasks 1, 7, and 8 |
| CC BY-SA content notice and contribution rules | Task 9 |

The full proof corpus, Fourier/Lebesgue chapters, all remaining units, and the final exercise-solution ratio are not partially scaffolded here; they belong to the named follow-up plans and only begin after the pilot review gate.

## Target file structure

```text
mathbook/
├── .github/workflows/pages.yml
├── .gitignore
├── Makefile
├── README.md
├── CONTRIBUTING.md
├── LICENSE-CONTENT.md
├── _quarto.yml
├── index.qmd
├── styles.css
├── book/
│   ├── preface.qmd
│   ├── curriculum-map.qmd                 # generated, committed
│   ├── bridges/python/functions-loops.qmd
│   └── part-03/chapter-12/
│       └── u-03-12-01-ivt-bisection.qmd
├── curriculum/
│   ├── outline.toml                       # 12 parts, 54 chapters
│   └── units.toml                         # pilot unit registry
├── src/mathbook_examples/
│   ├── __init__.py
│   └── bisection.py
├── scripts/
│   ├── check_outline.py
│   ├── check_units.py
│   ├── render_curriculum_map.py
│   └── check_site.py
├── tests/
│   ├── test_project_structure.py
│   ├── test_outline.py
│   ├── test_units.py
│   ├── test_bisection.py
│   └── test_site.py
└── docs/superpowers/
    ├── specs/2026-07-18-mathematical-analysis-textbook-design.md
    └── plans/2026-07-18-mathbook-foundation-and-pilot.md
```

## Task 1: Establish the Quarto book shell and local commands

**Files:**

- Create: `tests/test_project_structure.py`
- Create: `_quarto.yml`
- Create: `index.qmd`
- Create: `book/preface.qmd`
- Create: `styles.css`
- Create: `Makefile`
- Modify: `.gitignore`

- [ ] **Step 1: Verify the external tool prerequisite**

Run:

```bash
quarto --version
```

Expected before installation: shell reports that `quarto` is not found.

Install the current stable Quarto CLI from the official distribution for the execution environment. On macOS with Homebrew:

```bash
brew install --cask quarto
```

Run `quarto --version` again. Expected: a semantic version is printed and the command exits 0. Do not pin a local machine path in repository files.

- [ ] **Step 2: Write the failing project-structure test**

Create `tests/test_project_structure.py`:

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTest(unittest.TestCase):
    def test_required_book_shell_files_exist(self) -> None:
        required = [
            "_quarto.yml",
            "index.qmd",
            "styles.css",
            "book/preface.qmd",
            "Makefile",
        ]
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the structure test and verify it fails**

Run:

```bash
python3 -m unittest tests.test_project_structure -v
```

Expected: FAIL listing `_quarto.yml`, `index.qmd`, `styles.css`, `book/preface.qmd`, and `Makefile` as missing.

- [ ] **Step 4: Create the minimal Quarto configuration**

Create `_quarto.yml`:

```yaml
project:
  type: book
  output-dir: _site

book:
  title: "数学分析：理论、算法与模型"
  chapters:
    - index.qmd
    - book/preface.qmd
    - book/curriculum-map.qmd
    - part: "第三部：函数极限、连续性与方程"
      chapters:
        - book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd
  appendices:
    - book/bridges/python/functions-loops.qmd

format:
  html:
    theme: cosmo
    css: styles.css
    toc-depth: 3
    number-sections: true
    code-copy: true
    code-overflow: wrap

lang: zh
```

Create `index.qmd`:

```markdown
---
title: "数学分析：理论、算法与模型"
---

这是一部面向普通高校数学类专业本科生、以自主学习为首要场景的数学分析数字教材。

全书以严格理论为依赖骨架，以问题驱动的算法与模型为第二条主线。当前网站处于样章验证阶段，公开内容用于检验学习单元长度、证明密度、答案呈现和数字阅读体验。
```

Create `book/preface.qmd`:

```markdown
# 阅读说明 {#sec-preface}

每个学习单元都会列出建议用时、书内先备内容，以及所需的高等代数、解析几何和 Python 知识。核心定理给出完整证明；算法按“数学转化—算法思想—误差条件—伪代码—Python—结果解释”的顺序展开。

全书规划为约 360 个等效学时，其中理论主线约 270 学时，应用选修线约 90 学时。网页是第一阶段的正式发布版本。
```

Create `styles.css`:

```css
:root {
  --mathbook-reading-width: 48rem;
}

body {
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
}

main.content {
  max-width: var(--mathbook-reading-width);
}

.unit-meta {
  border-left: 0.25rem solid #2f6f8f;
  background: #f3f8fa;
  padding: 0.9rem 1rem;
  margin: 1rem 0 1.5rem;
}

.solution {
  border-left: 0.25rem solid #5c7c3a;
  background: #f6f9f2;
  padding: 0.9rem 1rem;
}

@media (max-width: 700px) {
  main.content {
    max-width: 100%;
  }
}
```

Create `Makefile` with literal tab-indented command lines:

```make
.PHONY: test check generate render verify preview

test:
	python3 -m unittest discover -s tests -v

check:
	python3 scripts/check_outline.py
	python3 scripts/check_units.py

generate:
	python3 scripts/render_curriculum_map.py

render: generate
	quarto render

verify: test check render
	python3 scripts/check_site.py

preview: generate
	quarto preview
```

Append these lines to `.gitignore` if they are not already present:

```gitignore
_site/
*.pyc
```

- [ ] **Step 5: Run the test and verify it passes**

Run:

```bash
python3 -m unittest tests.test_project_structure -v
```

Expected: 1 test passes.

- [ ] **Step 6: Commit the book shell**

```bash
git add .gitignore Makefile _quarto.yml index.qmd styles.css book/preface.qmd tests/test_project_structure.py
git commit -m "build: scaffold Quarto mathbook"
```

## Task 2: Encode and validate the 12-part, 54-chapter outline

**Files:**

- Create: `curriculum/outline.toml`
- Create: `scripts/check_outline.py`
- Create: `tests/test_outline.py`

- [ ] **Step 1: Write failing validator tests**

Create `tests/test_outline.py`:

```python
from copy import deepcopy
from pathlib import Path
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_outline import validate_outline


def load_real_outline() -> dict:
    with (ROOT / "curriculum/outline.toml").open("rb") as handle:
        return tomllib.load(handle)


class OutlineValidationTest(unittest.TestCase):
    def test_confirmed_outline_is_valid(self) -> None:
        self.assertEqual([], validate_outline(load_real_outline()))

    def test_duplicate_chapter_number_is_rejected(self) -> None:
        data = deepcopy(load_real_outline())
        data["parts"][1]["chapters"][0]["number"] = 1
        self.assertIn("chapter numbers must be exactly 1..54", validate_outline(data))

    def test_hour_drift_is_rejected(self) -> None:
        data = deepcopy(load_real_outline())
        data["parts"][0]["theory_hours"] = 21
        self.assertIn("theory hours must total 270, got 271", validate_outline(data))

    def test_part_without_question_is_rejected(self) -> None:
        data = deepcopy(load_real_outline())
        data["parts"][0]["question"] = ""
        self.assertIn("part-01 must have a guiding question", validate_outline(data))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the expected import/file failure**

Run:

```bash
python3 -m unittest tests.test_outline -v
```

Expected: ERROR because `scripts.check_outline` and `curriculum/outline.toml` do not exist.

- [ ] **Step 3: Create the exact curriculum registry**

Create `curriculum/outline.toml`. Use this header and record shape:

```toml
schema_version = 1

[book]
title = "数学分析：理论、算法与模型"
theory_hours = 270
applied_hours = 90
total_hours = 360

[[parts]]
id = "part-01"
number = 1
title = "实数、函数与分析语言"
question = "有限符号怎样描述无限与连续？"
theory_hours = 20
applied_hours = 4

[[parts.chapters]]
id = "chapter-01"
number = 1
title = "函数、集合与数学陈述"
```

Continue with all records below. Each part uses the confirmed hours and question; each chapter is nested under its part.

| Part | Theory + applied | Guiding question | Chapters |
|---|---:|---|---|
| `part-01` 实数、函数与分析语言 | 20+4 | 有限符号怎样描述无限与连续？ | `chapter-01` 函数、集合与数学陈述; `chapter-02` 实数系与完备性公理; `chapter-03` 上界、下界与确界原理; `chapter-04` 递推过程与无限逼近 |
| `part-02` 数列极限与无限过程 | 26+6 | 怎样判断一个无限过程最终稳定？ | `chapter-05` 数列极限与量词结构; `chapter-06` 极限运算与序关系; `chapter-07` 单调性、完备性与收敛准则; `chapter-08` 子列、Cauchy 准则与上/下极限 |
| `part-03` 函数极限、连续性与方程 | 20+6 | 近似值能否保证真实解存在？ | `chapter-09` 函数极限与局部行为; `chapter-10` 连续函数与连续运算; `chapter-11` 闭区间上的整体性质; `chapter-12` 零点、不动点与迭代求解 |
| `part-04` 微分与局部线性化 | 24+10 | 局部变化能告诉我们多少整体信息？ | `chapter-13` 导数、微分与局部线性模型; `chapter-14` 求导法则、反函数与高阶导数; `chapter-15` 微分中值定理; `chapter-16` Taylor 公式与余项; `chapter-17` 优化、函数形态与 Newton 方法 |
| `part-05` 积分、累积与数值求积 | 26+10 | 局部贡献怎样重建整体总量？ | `chapter-18` 原函数与积分方法; `chapter-19` Riemann 积分与可积性; `chapter-20` 微积分基本定理; `chapter-21` 积分的几何与物理模型; `chapter-22` 反常积分与数值求积 |
| `part-06` 无穷级数与函数逼近 | 26+10 | 无限叠加何时仍然可控？ | `chapter-23` 数项级数与基本判别; `chapter-24` 正项、绝对与条件收敛; `chapter-25` 函数列、函数项级数与一致收敛; `chapter-26` 幂级数与解析表示; `chapter-27` 多项式逼近与误差控制 |
| `part-07` Euclid 空间与多元微分 | 26+8 | 多变量系统能否仍用线性对象作局部近似？ | `chapter-28` Euclid 空间的几何与拓扑; `chapter-29` 多元函数的极限与连续; `chapter-30` 全微分、偏导数与导数映射; `chapter-31` 高阶微分与多元 Taylor 公式; `chapter-32` 隐函数、反函数与约束优化 |
| `part-08` 重积分与空间测量 | 24+8 | 怎样计算高维区域上的累积量？ | `chapter-33` 重积分的定义与可积性; `chapter-34` 累次积分与计算; `chapter-35` 重积分的变量代换; `chapter-36` 反常重积分与质量、概率模型 |
| `part-09` 曲线、曲面与向量分析 | 24+8 | 边界上的信息怎样控制区域内部？ | `chapter-37` 参数曲线与曲线积分; `chapter-38` 曲面与曲面积分; `chapter-39` Green 公式与平面场; `chapter-40` Gauss 公式与通量; `chapter-41` Stokes 公式与三大公式的统一 |
| `part-10` 含参变量积分 | 18+6 | 什么时候可以把极限或微分移进积分号？ | `chapter-42` 正常含参变量积分; `chapter-43` 积分号下求导与积分; `chapter-44` 含参反常积分的一致收敛; `chapter-45` Gamma、Beta 函数与参数敏感性 |
| `part-11` 测度与 Lebesgue 积分 | 18+6 | Riemann 积分失效后，“大小”与“总量”应怎样重建？ | `chapter-46` 从长度问题到测度; `chapter-47` σ-代数与测度; `chapter-48` 可测函数与收敛方式; `chapter-49` Lebesgue 积分; `chapter-50` 三大收敛定理与 Riemann 理论比较 |
| `part-12` Fourier 级数初步 | 18+8 | 复杂的周期现象能否分解为简单振动？ | `chapter-51` 正交函数系与最佳逼近; `chapter-52` Fourier 系数与逐点收敛; `chapter-53` Bessel、Parseval 与均方收敛; `chapter-54` 周期模型、逼近误差与 Gibbs 现象 |

- [ ] **Step 4: Implement the outline validator**

Create `scripts/check_outline.py`:

```python
from pathlib import Path
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum/outline.toml"


def validate_outline(data: dict) -> list[str]:
    errors: list[str] = []
    parts = data.get("parts", [])

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if len(parts) != 12:
        errors.append(f"outline must contain 12 parts, got {len(parts)}")

    part_numbers = [part.get("number") for part in parts]
    if part_numbers != list(range(1, 13)):
        errors.append("part numbers must be exactly 1..12")

    theory = sum(part.get("theory_hours", 0) for part in parts)
    applied = sum(part.get("applied_hours", 0) for part in parts)
    if theory != 270:
        errors.append(f"theory hours must total 270, got {theory}")
    if applied != 90:
        errors.append(f"applied hours must total 90, got {applied}")

    chapter_numbers: list[int] = []
    chapter_ids: list[str] = []
    for part in parts:
        part_id = part.get("id", "<missing-part-id>")
        if not str(part.get("question", "")).strip():
            errors.append(f"{part_id} must have a guiding question")
        for chapter in part.get("chapters", []):
            chapter_numbers.append(chapter.get("number"))
            chapter_ids.append(chapter.get("id"))
            if not str(chapter.get("title", "")).strip():
                errors.append(f"{chapter.get('id', '<missing-chapter-id>')} must have a title")

    if chapter_numbers != list(range(1, 55)):
        errors.append("chapter numbers must be exactly 1..54")
    if len(chapter_ids) != len(set(chapter_ids)):
        errors.append("chapter IDs must be unique")

    book = data.get("book", {})
    if book.get("theory_hours") != theory:
        errors.append("book.theory_hours must equal the sum of part theory hours")
    if book.get("applied_hours") != applied:
        errors.append("book.applied_hours must equal the sum of part applied hours")
    if book.get("total_hours") != theory + applied:
        errors.append("book.total_hours must equal theory plus applied hours")
    return errors


def main() -> int:
    with OUTLINE.open("rb") as handle:
        data = tomllib.load(handle)
    errors = validate_outline(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("outline valid: 12 parts, 54 chapters, 270+90=360 hours")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run validator tests and the real-data check**

Run:

```bash
python3 -m unittest tests.test_outline -v
python3 scripts/check_outline.py
```

Expected: 4 tests pass; the script prints `outline valid: 12 parts, 54 chapters, 270+90=360 hours`.

- [ ] **Step 6: Commit the curriculum registry**

```bash
git add curriculum/outline.toml scripts/check_outline.py tests/test_outline.py
git commit -m "feat: encode validated curriculum outline"
```

## Task 3: Generate the reader-facing curriculum map

**Files:**

- Create: `scripts/render_curriculum_map.py`
- Create: `tests/test_curriculum_map.py`
- Generate: `book/curriculum-map.qmd`

- [ ] **Step 1: Write the failing renderer test**

Create `tests/test_curriculum_map.py`:

```python
from pathlib import Path
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.render_curriculum_map import render_map


class CurriculumMapTest(unittest.TestCase):
    def test_map_contains_all_parts_and_chapter_endpoints(self) -> None:
        with (ROOT / "curriculum/outline.toml").open("rb") as handle:
            rendered = render_map(tomllib.load(handle))
        self.assertEqual(12, rendered.count("## 第"))
        self.assertIn("1. 函数、集合与数学陈述", rendered)
        self.assertIn("54. 周期模型、逼近误差与 Gibbs 现象", rendered)
        self.assertIn("**学时：** 理论 270 + 应用 90 = 360", rendered)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
python3 -m unittest tests.test_curriculum_map -v
```

Expected: ERROR because `scripts.render_curriculum_map` does not exist.

- [ ] **Step 3: Implement deterministic curriculum-map rendering**

Create `scripts/render_curriculum_map.py`:

```python
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "curriculum/outline.toml"
TARGET = ROOT / "book/curriculum-map.qmd"
CHINESE_NUMBERS = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]


def render_map(data: dict) -> str:
    book = data["book"]
    lines = [
        "# 全书课程地图 {#sec-curriculum-map}",
        "",
        f"**学时：** 理论 {book['theory_hours']} + 应用 {book['applied_hours']} = {book['total_hours']}",
        "",
        "本页由 `curriculum/outline.toml` 自动生成。请勿直接编辑。",
        "",
    ]
    for index, part in enumerate(data["parts"]):
        lines.extend(
            [
                f"## 第{CHINESE_NUMBERS[index]}部：{part['title']}",
                "",
                f"**问题弧：** {part['question']}",
                "",
                f"**学时：** 理论 {part['theory_hours']} + 应用 {part['applied_hours']}",
                "",
            ]
        )
        lines.extend(f"{chapter['number']}. {chapter['title']}" for chapter in part["chapters"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    with SOURCE.open("rb") as handle:
        rendered = render_map(tomllib.load(handle))
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Generate the map and verify tests**

Run:

```bash
python3 scripts/render_curriculum_map.py
python3 -m unittest tests.test_curriculum_map -v
git add book/curriculum-map.qmd
python3 scripts/render_curriculum_map.py
git diff --exit-code book/curriculum-map.qmd
```

Expected: 1 test passes. The last command produces no diff after regenerating from the staged source, proving deterministic output.

- [ ] **Step 5: Commit the generator and generated map**

```bash
git add scripts/render_curriculum_map.py tests/test_curriculum_map.py book/curriculum-map.qmd
git commit -m "feat: generate curriculum map from outline"
```

## Task 4: Define and enforce learning-unit metadata

**Files:**

- Create: `curriculum/units.toml`
- Create: `scripts/check_units.py`
- Create: `tests/test_units.py`
- Create: `book/bridges/python/functions-loops.qmd`

- [ ] **Step 1: Create the pilot unit registry entry**

Create `curriculum/units.toml`:

```toml
schema_version = 1

[[units]]
id = "u-03-12-01"
chapter_id = "chapter-12"
title = "连续性怎样保证方程有根：介值定理与二分法"
path = "book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd"
theory_hours = 1.25
applied_hours = 0.75
difficulty = 2
book_prerequisites = ["chapter-10", "chapter-11"]
higher_algebra_prerequisites = []
analytic_geometry_prerequisites = []
python_prerequisites = ["函数定义", "while 循环", "异常的基本含义"]
knowledge_bridges = ["book/bridges/python/functions-loops.qmd"]
capabilities = ["concepts", "proof", "numerical_algorithm", "mathematical_expression"]
learning_goals = [
  "准确陈述介值定理并识别连续性假设",
  "使用区间套方法完整证明介值定理",
  "从介值定理推导二分法及其误差上界",
  "解释二分法的停止准则并使用 Python 求近似根",
]
```

- [ ] **Step 2: Write failing unit-validator tests**

Create `tests/test_units.py`:

```python
from copy import deepcopy
from pathlib import Path
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_units import validate_units


def load_toml(path: str) -> dict:
    with (ROOT / path).open("rb") as handle:
        return tomllib.load(handle)


class UnitValidationTest(unittest.TestCase):
    def test_pilot_registry_is_valid_after_content_exists(self) -> None:
        errors = validate_units(load_toml("curriculum/units.toml"), load_toml("curriculum/outline.toml"), ROOT)
        only_missing_content = [error for error in errors if "content file does not exist" in error]
        self.assertEqual(errors, only_missing_content)

    def test_unknown_chapter_is_rejected(self) -> None:
        units = deepcopy(load_toml("curriculum/units.toml"))
        units["units"][0]["chapter_id"] = "chapter-99"
        errors = validate_units(units, load_toml("curriculum/outline.toml"), ROOT)
        self.assertIn("u-03-12-01 references unknown chapter chapter-99", errors)

    def test_missing_prerequisite_categories_are_rejected(self) -> None:
        units = deepcopy(load_toml("curriculum/units.toml"))
        del units["units"][0]["analytic_geometry_prerequisites"]
        errors = validate_units(units, load_toml("curriculum/outline.toml"), ROOT)
        self.assertIn("u-03-12-01 missing analytic_geometry_prerequisites", errors)

    def test_hours_must_be_positive_and_at_most_two(self) -> None:
        units = deepcopy(load_toml("curriculum/units.toml"))
        units["units"][0]["applied_hours"] = 1.0
        errors = validate_units(units, load_toml("curriculum/outline.toml"), ROOT)
        self.assertIn("u-03-12-01 total unit hours must be in (0, 2], got 2.25", errors)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests and verify they fail**

Run:

```bash
python3 -m unittest tests.test_units -v
```

Expected: ERROR because `scripts.check_units` does not exist.

- [ ] **Step 4: Implement the unit validator**

Create `scripts/check_units.py`:

```python
from pathlib import Path
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_LISTS = [
    "book_prerequisites",
    "higher_algebra_prerequisites",
    "analytic_geometry_prerequisites",
    "python_prerequisites",
    "knowledge_bridges",
    "capabilities",
    "learning_goals",
]
ALLOWED_CAPABILITIES = {
    "concepts",
    "proof",
    "analytic_calculation",
    "numerical_algorithm",
    "modeling",
    "mathematical_expression",
}
REQUIRED_SECTIONS = [
    "## 先备知识",
    "## 学习目标",
    "## 牵引问题",
    "## 探索与猜想",
    "## 概念与理论",
    "## 例题与迁移",
    "## 即时检验与回望",
    "## 习题与答案",
]


def validate_units(units_data: dict, outline_data: dict, root: Path) -> list[str]:
    errors: list[str] = []
    units = units_data.get("units", [])
    chapter_ids = {
        chapter["id"]
        for part in outline_data.get("parts", [])
        for chapter in part.get("chapters", [])
    }
    seen_ids: set[str] = set()

    for unit in units:
        unit_id = unit.get("id", "<missing-unit-id>")
        if unit_id in seen_ids:
            errors.append(f"duplicate unit ID {unit_id}")
        seen_ids.add(unit_id)

        chapter_id = unit.get("chapter_id")
        if chapter_id not in chapter_ids:
            errors.append(f"{unit_id} references unknown chapter {chapter_id}")

        for field in REQUIRED_LISTS:
            if field not in unit:
                errors.append(f"{unit_id} missing {field}")
            elif not isinstance(unit[field], list):
                errors.append(f"{unit_id}.{field} must be a list")

        total_hours = unit.get("theory_hours", 0) + unit.get("applied_hours", 0)
        if not 0 < total_hours <= 2:
            errors.append(f"{unit_id} total unit hours must be in (0, 2], got {total_hours}")

        unknown_capabilities = set(unit.get("capabilities", [])) - ALLOWED_CAPABILITIES
        if unknown_capabilities:
            errors.append(f"{unit_id} has unknown capabilities {sorted(unknown_capabilities)}")

        for bridge in unit.get("knowledge_bridges", []):
            if not (root / bridge).is_file():
                errors.append(f"{unit_id} knowledge bridge does not exist: {bridge}")

        relative_path = unit.get("path", "")
        content_path = root / relative_path
        if not content_path.is_file():
            errors.append(f"{unit_id} content file does not exist: {relative_path}")
            continue
        content = content_path.read_text(encoding="utf-8")
        if f"{{#{unit_id}}}" not in content:
            errors.append(f"{unit_id} content is missing its stable anchor")
        for section in REQUIRED_SECTIONS:
            if section not in content:
                errors.append(f"{unit_id} content is missing section {section}")
    return errors


def main() -> int:
    with (ROOT / "curriculum/units.toml").open("rb") as handle:
        units_data = tomllib.load(handle)
    with (ROOT / "curriculum/outline.toml").open("rb") as handle:
        outline_data = tomllib.load(handle)
    errors = validate_units(units_data, outline_data, ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"unit registry valid: {len(units_data['units'])} unit(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Add the exact Python knowledge bridge**

Create `book/bridges/python/functions-loops.qmd`:

```markdown
# Python 知识桥：函数、循环与异常 {#bridge-python-functions-loops}

本知识桥只覆盖二分法单元所需的 Python 语法。

```python
def sign_change(f, left, right):
    return f(left) * f(right) <= 0

count = 0
while count < 3:
    count += 1
```

函数通过参数接收数据并用 `return` 返回结果。`while` 在条件为真时重复执行。若输入不满足算法前提，本书示例会使用 `ValueError` 明确拒绝输入，而不是返回一个看似合理的错误结果。
```

- [ ] **Step 6: Run unit tests at the expected intermediate state**

Run:

```bash
python3 -m unittest tests.test_units -v
```

Expected: all 4 tests pass. The real pilot entry is allowed to report only that its QMD content file is not yet present; the test explicitly verifies there are no other metadata errors.

- [ ] **Step 7: Commit the unit metadata contract**

```bash
git add curriculum/units.toml scripts/check_units.py tests/test_units.py book/bridges/python/functions-loops.qmd
git commit -m "feat: define learning unit metadata contract"
```

## Task 5: Implement the tested bisection example

**Files:**

- Create: `src/mathbook_examples/__init__.py`
- Create: `src/mathbook_examples/bisection.py`
- Create: `tests/test_bisection.py`

- [ ] **Step 1: Write failing algorithm tests**

Create `tests/test_bisection.py`:

```python
from math import sqrt
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.bisection import bisect


class BisectionTest(unittest.TestCase):
    def test_approximates_square_root_two_with_certified_error(self) -> None:
        result = bisect(lambda x: x * x - 2, 1.0, 2.0, tolerance=1e-8)
        self.assertLessEqual(abs(result.root - sqrt(2)), result.error_bound)
        self.assertLessEqual(result.error_bound, 1e-8)
        self.assertGreater(result.iterations, 0)

    def test_returns_an_endpoint_root(self) -> None:
        result = bisect(lambda x: x - 1, 1.0, 3.0, tolerance=1e-6)
        self.assertEqual(1.0, result.root)
        self.assertEqual(0.0, result.error_bound)
        self.assertEqual(0, result.iterations)

    def test_rejects_interval_without_sign_change(self) -> None:
        with self.assertRaisesRegex(ValueError, "opposite signs"):
            bisect(lambda x: x * x + 1, -1.0, 1.0)

    def test_rejects_nonpositive_tolerance(self) -> None:
        with self.assertRaisesRegex(ValueError, "tolerance must be positive"):
            bisect(lambda x: x, -1.0, 1.0, tolerance=0)

    def test_rejects_too_small_iteration_budget(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "maximum iterations"):
            bisect(lambda x: x * x - 2, 1.0, 2.0, tolerance=1e-12, max_iterations=2)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify the import failure**

Run:

```bash
python3 -m unittest tests.test_bisection -v
```

Expected: ERROR because `mathbook_examples.bisection` does not exist.

- [ ] **Step 3: Implement the minimal certified bisection function**

Create an empty `src/mathbook_examples/__init__.py` and create `src/mathbook_examples/bisection.py`:

```python
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class BisectionResult:
    root: float
    error_bound: float
    iterations: int


def bisect(
    function: Callable[[float], float],
    left: float,
    right: float,
    *,
    tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> BisectionResult:
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if left >= right:
        raise ValueError("left endpoint must be smaller than right endpoint")

    f_left = function(left)
    f_right = function(right)
    if f_left == 0:
        return BisectionResult(left, 0.0, 0)
    if f_right == 0:
        return BisectionResult(right, 0.0, 0)
    if f_left * f_right > 0:
        raise ValueError("endpoint values must have opposite signs")

    for iteration in range(1, max_iterations + 1):
        midpoint = (left + right) / 2
        f_midpoint = function(midpoint)
        if f_midpoint == 0:
            return BisectionResult(midpoint, 0.0, iteration)
        if f_left * f_midpoint < 0:
            right = midpoint
        else:
            left = midpoint
            f_left = f_midpoint
        error_bound = (right - left) / 2
        if error_bound <= tolerance:
            return BisectionResult((left + right) / 2, error_bound, iteration)

    raise RuntimeError("maximum iterations reached before tolerance")
```

- [ ] **Step 4: Run algorithm tests and verify they pass**

Run:

```bash
python3 -m unittest tests.test_bisection -v
```

Expected: 5 tests pass.

- [ ] **Step 5: Commit the example**

```bash
git add src/mathbook_examples tests/test_bisection.py
git commit -m "feat: add certified bisection example"
```

## Task 6: Write the representative double-helix learning unit

**Files:**

- Create: `book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd`
- Modify: `tests/test_units.py`

- [ ] **Step 1: Tighten the unit test so the content must be fully valid**

Replace `test_pilot_registry_is_valid_after_content_exists` in `tests/test_units.py` with:

```python
    def test_pilot_registry_and_content_are_valid(self) -> None:
        errors = validate_units(load_toml("curriculum/units.toml"), load_toml("curriculum/outline.toml"), ROOT)
        self.assertEqual([], errors)
```

- [ ] **Step 2: Run the test and verify it fails on the missing QMD file**

Run:

```bash
python3 -m unittest tests.test_units -v
```

Expected: FAIL because `book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd` does not exist.

- [ ] **Step 3: Write the pilot unit to the exact content contract**

Create `book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd` with the following required mathematical content. Use the headings exactly so the metadata validator can check them.

```markdown
# 连续性怎样保证方程有根：介值定理与二分法 {#u-03-12-01}

::: {.unit-meta}
**建议用时：** 2 学时（理论 1.25，应用 0.75）<br>
**书内先备：** 第 10 章连续函数；第 11 章闭区间上的整体性质<br>
**高等代数：** 无新增先备要求<br>
**解析几何：** 无新增先备要求<br>
**Python：** 函数定义、`while` 循环、异常的基本含义（见 @bridge-python-functions-loops）
:::

## 先备知识

准确复述区间上的连续性定义、闭区间套定理，并解释连续性为何是局部条件。给出指向相应书内章节的链接。

## 学习目标

列出 `curriculum/units.toml` 中四项目标，措辞保持一致。

## 牵引问题

从方程 \(x^3+x-1=0\) 出发：只计算 \(f(0)=-1\) 与 \(f(1)=1\)，为什么能够断言两点之间存在根？若要把根计算到误差不超过 \(10^{-6}\)，存在性结论能否同时给出算法？

## 探索与猜想

1. 用连续曲线过零的图像形成猜想，但明确图像不是证明。
2. 给出符号函数在 \([-1,1]\) 上端点异号却没有零点的反例，暴露连续性不可删除。
3. 通过连续二分区间观察：每一步保留端点异号的半区间，区间长度变为原来的一半。

## 概念与理论

正式陈述介值定理及零点定理。使用闭区间套给出完整证明：构造嵌套闭区间；证明长度趋于零；由闭区间套得到唯一公共点；用连续性排除该点函数值非零的两种情况。证明后增加“证明策略复盘”，说明完备性如何从区间序列产生极限点。

随后陈述二分法误差：初始区间长度为 \(b-a\)，完成 \(n\) 次二分后，以当前区间中点为近似根时误差不超过

\[
\frac{b-a}{2^{n+1}}.
\]

从该不等式推导达到容许误差 \(\varepsilon\) 所需的最小迭代次数条件，不跳过取对数时的不等号处理。

## 例题与迁移

完整求解 \(x^3+x-1=0\) 在 \([0,1]\) 上误差不超过 \(10^{-6}\) 的问题：先证明函数连续且端点异号，再推导迭代次数，写出伪代码，最后调用 `src/mathbook_examples/bisection.py` 中经过测试的 `bisect` 函数。解释返回值中的 `error_bound` 是数学保证，不是与未知真根比较得到的经验误差。

给出一个迁移例：讨论二分法为什么收敛稳定但通常比 Newton 方法慢；只比较思想，不提前教授 Newton 方法。

## 即时检验与回望

设置 4 个短任务并紧随折叠答案：识别缺失的连续性条件；补全闭区间套证明的一步；计算指定误差所需次数；判断停止条件应使用区间宽度还是函数值。每题都给出答案，其中证明补全题给出完整解释。

## 习题与答案

至少设置 6 题：2 题概念辨析、2 题证明、1 题算法、1 题反例构造。每题具有稳定 ID `ex-u-03-12-01-01` 至 `ex-u-03-12-01-06`，并全部给出答案。选择“用介值定理证明奇次实系数多项式至少有一个实根”作为代表题，提供完整解答；其余题根据难度给提示、关键步骤或完整结论。
```

Do not leave the instructional sentences above in the final QMD. Expand them into finished textbook prose, a complete proof, executable example invocation, six actual exercises, and their actual answers. The unit is complete only when a self-learner can work through it without consulting an unwritten lecture.

- [ ] **Step 4: Run unit validation and all Python tests**

Run:

```bash
python3 scripts/check_units.py
python3 -m unittest discover -s tests -v
```

Expected: `unit registry valid: 1 unit(s)` and all tests pass.

- [ ] **Step 5: Commit the pilot unit**

```bash
git add book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd tests/test_units.py
git commit -m "docs: add intermediate value and bisection pilot"
```

## Task 7: Render and inspect the static book

**Files:**

- Create: `scripts/check_site.py`
- Create: `tests/test_site.py`

- [ ] **Step 1: Write failing static-site checker tests**

Create `tests/test_site.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_site import validate_site


class SiteValidationTest(unittest.TestCase):
    def test_valid_minimal_site(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text('<a href="unit.html">unit</a>', encoding="utf-8")
            (site / "unit.html").write_text('<div id="u-03-12-01">二分法</div>', encoding="utf-8")
            self.assertEqual([], validate_site(site))

    def test_broken_internal_link_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text('<a href="missing.html">missing</a>', encoding="utf-8")
            errors = validate_site(site)
            self.assertEqual(["index.html links to missing missing.html"], errors)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
python3 -m unittest tests.test_site -v
```

Expected: ERROR because `scripts.check_site` does not exist.

- [ ] **Step 3: Implement the internal-link checker**

Create `scripts/check_site.py`:

```python
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attributes = dict(attrs)
        if attributes.get("href"):
            self.links.append(attributes["href"])


def validate_site(site: Path) -> list[str]:
    errors: list[str] = []
    if not (site / "index.html").is_file():
        return ["site is missing index.html"]

    for html_file in sorted(site.rglob("*.html")):
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith("mailto:") or not parsed.path:
                continue
            relative_target = unquote(parsed.path)
            if relative_target.startswith("/"):
                target = site / relative_target.lstrip("/")
            else:
                target = html_file.parent / relative_target
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{html_file.relative_to(site)} links to missing {relative_target}")
    return errors


def main() -> int:
    errors = validate_site(SITE)
    pilot_pages = list(SITE.rglob("*u-03-12-01-ivt-bisection*.html"))
    if not pilot_pages:
        errors.append("rendered site is missing the pilot unit page")
    else:
        pilot = pilot_pages[0].read_text(encoding="utf-8")
        for required in ["u-03-12-01", "介值定理", "二分法", "习题与答案"]:
            if required not in pilot:
                errors.append(f"pilot unit page is missing {required}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("site valid: internal links and pilot markers present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run checker tests**

Run:

```bash
python3 -m unittest tests.test_site -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Render the complete book and check it**

Run:

```bash
make verify
```

Expected:

- all `unittest` tests pass;
- outline prints `12 parts, 54 chapters, 270+90=360 hours`;
- unit registry prints `1 unit(s)`;
- Quarto render exits 0;
- site checker prints `site valid: internal links and pilot markers present`.

- [ ] **Step 6: Inspect the responsive site manually**

Run:

```bash
quarto preview
```

Inspect desktop and narrow mobile widths. Verify the Chinese font stack is readable, equations do not overflow, the curriculum map is navigable, the stable unit anchor works, code wraps, and answers are visually distinct. Record any real defect as a focused test before fixing it.

- [ ] **Step 7: Commit the site verification**

```bash
git add scripts/check_site.py tests/test_site.py
git commit -m "test: validate rendered mathbook site"
```

## Task 8: Add gated GitHub Pages deployment

**Files:**

- Create: `.github/workflows/pages.yml`

- [ ] **Step 1: Create the build-and-deploy workflow**

Create `.github/workflows/pages.yml`:

```yaml
name: Build and deploy mathbook

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Run manuscript and algorithm tests
        run: python3 -m unittest discover -s tests -v

      - name: Validate curriculum and units
        run: make check

      - name: Render book
        run: make render

      - name: Validate rendered site
        run: python3 scripts/check_site.py

      - name: Configure Pages
        uses: actions/configure-pages@v5

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: _site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Validate the same commands locally**

Run:

```bash
make verify
git diff --check
```

Expected: `make verify` exits 0 and `git diff --check` prints nothing.

- [ ] **Step 3: Commit the deployment workflow**

```bash
git add .github/workflows/pages.yml
git commit -m "ci: deploy validated book to GitHub Pages"
```

- [ ] **Step 4: Enable GitHub Pages after the repository has a remote**

In the GitHub repository, open **Settings → Pages → Build and deployment** and select **GitHub Actions** as the source. Push `main`, then verify the workflow's `build` job succeeds before `deploy`, and open the URL reported by the deployment environment.

Do not add a custom domain in this phase. Use the default project URL reported by the GitHub Pages deployment so publishing failures are not mixed with DNS work.

## Task 9: Document contribution, licensing, and Phase 1 acceptance

**Files:**

- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `LICENSE-CONTENT.md`
- Create after pilot acceptance: `docs/project-status.md`

- [ ] **Step 1: Write the repository README**

Create `README.md` with these exact sections and commands:

````markdown
# 数学分析：理论、算法与模型

面向普通高校数学类专业本科生、以自主学习为首要场景的数学分析数字教材。

## 当前阶段

仓库处于基础工程与代表样章验证阶段。完整规划见 `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md`。

## 本地验证

```bash
make verify
```

该命令检查 12 部 54 章及 270+90 学时基线、学习单元元数据、Python 示例、Quarto 构建和站内链接。

## 本地预览

```bash
make preview
```

## 内容许可

除另有标注外，教材正文与原创图形采用 CC BY-SA 4.0。代码示例在独立代码许可确定前保留全部权利。
````

- [ ] **Step 2: Write stable-ID contribution rules**

Create `CONTRIBUTING.md`:

```markdown
# 贡献约定

## 修改学习单元

1. 先更新 `curriculum/units.toml` 中的元数据，再修改对应 QMD。
2. 单元必须保留八个固定二级标题和稳定单元 ID。
3. 定义、定理、例题和习题一旦公开，不因标题润色改变 ID。
4. 每道正式习题必须提供答案；代表性方法需提供完整解答。
5. Python 代码先写测试，再修改实现；正文必须解释算法思想、误差和适用条件。
6. 提交前运行 `make verify`。

## 修改课程结构

对部、章、学时或问题弧的修改必须同时更新设计文档和 `curriculum/outline.toml`，并解释对 270+90 学时闭合和依赖关系的影响。

## 报告错误

报告数学、文字或代码错误时，请提供稳定单元、定理或习题 ID，以及能够复现问题的最小信息。
```

- [ ] **Step 3: Add the content-license notice**

Create `LICENSE-CONTENT.md`:

```markdown
# 教材内容许可

除文件中另有标注的第三方材料外，本仓库的教材正文与原创图形采用 Creative Commons Attribution-ShareAlike 4.0 International（CC BY-SA 4.0）许可。

许可全文：https://creativecommons.org/licenses/by-sa/4.0/legalcode

使用或改编时必须署名，并以相同许可发布衍生内容。第三方材料继续适用其各自的来源与许可说明。

本声明不授权仓库中的程序代码。代码示例在独立代码许可确定并加入仓库前保留全部权利。
```

- [ ] **Step 4: Run the complete acceptance gate**

Run:

```bash
make verify
git diff --check
git status --short
```

Expected:

- every test and validator exits 0;
- Quarto render and static-site validation exit 0;
- `git diff --check` prints nothing;
- `git status --short` lists only `README.md`, `CONTRIBUTING.md`, and `LICENSE-CONTENT.md` before the final commit.

- [ ] **Step 5: Commit Phase 1 documentation**

```bash
git add README.md CONTRIBUTING.md LICENSE-CONTENT.md
git commit -m "docs: document mathbook contribution and licensing"
```

- [ ] **Step 6: Record the Phase 1 review decision**

Review the published pilot against these explicit gates:

- a self-learner can complete the unit without an unwritten lecture;
- the complete proof exposes every use of continuity and completeness;
- the bisection error bound matches the tested implementation;
- all six formal exercises have answers and the representative proof has a complete solution;
- prerequisite metadata explicitly addresses book content, higher algebra, analytic geometry, and Python;
- desktop and mobile pages render formulas, code, navigation, and answers correctly;
- the curriculum validator still reports 12 parts, 54 chapters, and 270+90 hours.

If any gate fails, add a focused test or content correction and repeat `make verify`. If all gates pass, create `docs/project-status.md` with the exact content below:

```markdown
# Project Status

- Phase: foundation and pilot
- Review state: pilot-baseline-accepted
- Acceptance command: `make verify`
- Next required plan: full learning-unit map and exercise/solution baseline

Do not create the remaining 179 unit files until that next plan is reviewed.
```

Then commit the accepted state:

```bash
git add docs/project-status.md
git commit -m "docs: record accepted pilot baseline"
```
