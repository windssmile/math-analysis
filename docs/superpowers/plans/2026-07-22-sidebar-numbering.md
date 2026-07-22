# Hierarchical Sidebar Numbering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Quarto's continuous page-as-chapter numbering with a semantic part → chapter → independently linked unit sidebar, while leaving unit-page H1/H2 headings unnumbered.

**Architecture:** Use a Quarto Website with an explicit recursive `website.sidebar.contents` tree and an explicit 52-page `project.render` list. Disable HTML section numbering, then enforce source-level consistency against `curriculum/outline.toml` and `curriculum/units.toml` plus rendered-HTML presence of the three-level navigation and absence of Quarto's automatic numbering classes.

**Tech Stack:** Quarto Website 1.9, YAML configuration, Python 3.12 standard library (`unittest`, `tomllib`, `re`, `html.parser`), Playwright CLI for browser QA.

---

## Implementation revision (authoritative)

During full rendered-HTML verification, Quarto 1.9 was shown to discard `book.sidebar.contents` and regenerate Book navigation from `book.chapters`. A minimal isolated project also proved that the Book schema rejects nested parts, so Book cannot natively express part → chapter → independently linked unit.

The user approved conversion to Website. This revision supersedes the Book-specific configuration steps later in this original plan:

1. Set `project.type: website` and add an explicit `project.render` list containing the same 52 QMD paths as the sidebar.
2. Move title, `page-navigation: true`, and the recursive sidebar under `website`.
3. Keep `number-sections: false`; do not modify unit H1/H2 content.
4. Update `tests/test_sidebar.py` to require Website mode, exact render/sidebar parity, 12 chapter sections, 48 unique units, and reading-order-derived labels.
5. Update the Chapter 8 order test to parse Website `href:` entries without weakening its exact-order assertion.
6. Extend `scripts/check_site.py` and `tests/test_site.py` so representative rendered pages must contain part, chapter, unit, and `sidebar-section depth2` markers as well as no automatic numbering classes.
7. Run 169 Python tests, render all 52 pages, validate links and anchors, then inspect representative desktop and narrow-screen pages in a real browser.

The remaining original task text is retained as the execution history that led to this revision; where it mentions `book.chapters` or `book.sidebar`, this revision controls.

## File map

- Modify `_quarto.yml`: disable automatic HTML numbering and declare the three-level sidebar.
- Create `tests/test_sidebar.py`: verify sidebar structure, labels, paths, and reading-order-derived unit numbers without adding PyYAML.
- Modify `scripts/check_site.py`: reject automatic chapter and heading number markup on rendered unit pages.
- Modify `tests/test_site.py`: unit-test the rendered-numbering validation.
- Modify `tests/test_chapter_08.py`: preserve its exact order assertion while reading Website `href:` entries.

No unit QMD file, curriculum hour allocation, chapter dependency, anchor, Python example, or stylesheet changes.

### Task 1: Add the source-level sidebar contract

**Files:**
- Create: `tests/test_sidebar.py`
- Read: `_quarto.yml`
- Read: `curriculum/outline.toml`
- Read: `curriculum/units.toml`

- [ ] **Step 1: Write the failing source-configuration tests**

Create `tests/test_sidebar.py` with this complete content:

```python
from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
QUARTO = ROOT / "_quarto.yml"
OUTLINE = ROOT / "curriculum" / "outline.toml"
UNITS = ROOT / "curriculum" / "units.toml"


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def quarto_sections() -> tuple[str, str]:
    config = QUARTO.read_text(encoding="utf-8")
    chapters, remainder = config.split("  appendices:", 1)
    sidebar = remainder.split("  sidebar:", 1)[1].split("\nformat:", 1)[0]
    return chapters, sidebar


def chapter_unit_paths(chapters: str) -> list[str]:
    return [
        line.strip().removeprefix("- ")
        for line in chapters.splitlines()
        if line.strip().startswith("- book/part-")
        and line.strip().endswith(".qmd")
    ]


def sidebar_unit_items(sidebar: str) -> list[tuple[str, str]]:
    return re.findall(
        r'^\s+- text: "(.+)"\n\s+href: (book/part-.+\.qmd)$',
        sidebar,
        flags=re.MULTILINE,
    )


class SidebarNumberingTests(unittest.TestCase):
    def expected_parts_and_chapters(self) -> tuple[list[str], dict[str, dict]]:
        outline = load_toml(OUTLINE)
        parts = [part for part in outline["parts"] if part.get("show_units")]
        sections: list[str] = []
        chapters: dict[str, dict] = {}
        chinese_part_numbers = {1: "一", 2: "二", 3: "三"}
        for part in parts:
            sections.append(
                f"第{chinese_part_numbers[part['number']]}部：{part['title']}"
            )
            for chapter in part["chapters"]:
                sections.append(f"第 {chapter['number']} 章：{chapter['title']}")
                chapters[chapter["id"]] = chapter
        return sections, chapters

    def expected_unit_items(self, paths: list[str]) -> list[tuple[str, str]]:
        units = load_toml(UNITS)["units"]
        unit_by_path = {unit["path"]: unit for unit in units}
        _, chapter_by_id = self.expected_parts_and_chapters()
        chapter_positions: dict[str, int] = {}
        expected: list[tuple[str, str]] = []
        for path in paths:
            unit = unit_by_path[path]
            chapter_id = unit["chapter_id"]
            chapter_positions[chapter_id] = chapter_positions.get(chapter_id, 0) + 1
            chapter_number = chapter_by_id[chapter_id]["number"]
            label = f"{chapter_number}.{chapter_positions[chapter_id]} {unit['title']}"
            expected.append((label, path))
        return expected

    def test_html_disables_automatic_section_numbering(self) -> None:
        config = QUARTO.read_text(encoding="utf-8")
        self.assertIn("    number-sections: false", config)
        self.assertNotIn("    number-sections: true", config)

    def test_sidebar_has_exact_part_and_chapter_sections(self) -> None:
        _, sidebar = quarto_sections()
        actual = re.findall(r'^\s+- section: "(.+)"$', sidebar, re.MULTILINE)
        expected, _ = self.expected_parts_and_chapters()
        expected.append("附录")
        self.assertEqual(expected, actual)

    def test_sidebar_units_follow_book_reading_order(self) -> None:
        chapters, sidebar = quarto_sections()
        paths = chapter_unit_paths(chapters)
        self.assertEqual(
            self.expected_unit_items(paths),
            sidebar_unit_items(sidebar),
        )

    def test_sidebar_contains_every_registered_unit_once(self) -> None:
        _, sidebar = quarto_sections()
        actual_paths = [path for _, path in sidebar_unit_items(sidebar)]
        registered_paths = [
            unit["path"] for unit in load_toml(UNITS)["units"]
        ]
        self.assertEqual(len(registered_paths), len(actual_paths))
        self.assertEqual(sorted(registered_paths), sorted(actual_paths))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new tests and verify the intended failure**

Run:

```bash
python3.12 -m unittest tests.test_sidebar -v
```

Expected: FAIL because `_quarto.yml` has `number-sections: true` and no `book.sidebar` block. A parsing error at the missing `sidebar` split is acceptable at this RED stage; no `yaml` import may appear.

### Task 2: Configure the semantic sidebar and disable automatic numbering

**Files:**
- Modify: `_quarto.yml`
- Test: `tests/test_sidebar.py`

- [ ] **Step 1: Add the complete nested sidebar configuration**

Under `book`, immediately after the existing `appendices` list, add this exact block:

```yaml
  sidebar:
    collapse-level: 2
    contents:
      - text: "首页"
        href: index.qmd
      - text: "前言"
        href: book/preface.qmd
      - text: "全书课程地图"
        href: book/curriculum-map.qmd
      - section: "第一部：实数、函数与分析语言"
        contents:
          - section: "第 1 章：函数、集合与数学陈述"
            contents:
              - text: "1.1 集合怎样组织数学对象？"
                href: book/part-01/chapter-01/u-01-01-01-sets.qmd
              - text: "1.2 量词怎样改变一句话？"
                href: book/part-01/chapter-01/u-01-01-02-quantifiers.qmd
              - text: "1.3 什么算作一个有效证明？"
                href: book/part-01/chapter-01/u-01-01-03-proofs.qmd
              - text: "1.4 函数为何不只是“公式”？"
                href: book/part-01/chapter-01/u-01-01-04-functions.qmd
          - section: "第 2 章：实数系与完备性公理"
            contents:
              - text: "2.1 有理数为什么仍然不够？"
                href: book/part-01/chapter-02/u-01-02-01-rational-gaps.qmd
              - text: "2.2 怎样用切割构造一个实数？"
                href: book/part-01/chapter-02/u-01-02-02-dedekind-cuts.qmd
              - text: "2.3 构造后怎样计算与比较？"
                href: book/part-01/chapter-02/u-01-02-03-cut-order-operations.qmd
          - section: "第 3 章：上界、下界与确界原理"
            contents:
              - text: "3.1 有上界为什么还不够？"
                href: book/part-01/chapter-03/u-01-03-01-bounds.qmd
              - text: "3.2 最小上界怎样保证存在？"
                href: book/part-01/chapter-03/u-01-03-02-supremum-principle.qmd
              - text: "3.3 确界原理能推出什么？"
                href: book/part-01/chapter-03/u-01-03-03-completeness-consequences.qmd
          - section: "第 4 章：递推过程与无限逼近"
            contents:
              - text: "4.1 递推会不会真的“靠近”目标？"
                href: book/part-01/chapter-04/u-01-04-01-recurrence.qmd
              - text: "4.2 区间怎样把目标逐步夹住？"
                href: book/part-01/chapter-04/u-01-04-02-interval-bisection.qmd
              - text: "4.3 “越来越近”怎样说得严格？"
                href: book/part-01/chapter-04/u-01-04-03-approximation-error.qmd
              - text: "4.4 无限逼近何时会失败？"
                href: book/part-01/chapter-04/u-01-04-04-failure-of-infinite-approximation.qmd
      - section: "第二部：数列极限与无限过程"
        contents:
          - section: "第 5 章：数列极限与量词结构"
            contents:
              - text: "5.1 数列怎样记录无限过程？"
                href: book/part-02/chapter-05/u-02-05-01-sequences.qmd
              - text: "5.2 “最终任意接近”怎样写成定义？"
                href: book/part-02/chapter-05/u-02-05-02-epsilon-n.qmd
              - text: "5.3 极限证明怎样从目标误差反推起点？"
                href: book/part-02/chapter-05/u-02-05-05-limit-consequences.qmd
              - text: "5.4 不收敛与趋于无穷怎样区分？"
                href: book/part-02/chapter-05/u-02-05-03-divergence-infinity.qmd
              - text: "5.5 迭代数据何时值得相信？"
                href: book/part-02/chapter-05/u-02-05-04-iteration-evidence.qmd
          - section: "第 6 章：极限运算与序关系"
            contents:
              - text: "6.1 极限怎样通过代数运算传递？"
                href: book/part-02/chapter-06/u-02-06-01-limit-laws.qmd
              - text: "6.2 倒数与商法则为何必须远离零？"
                href: book/part-02/chapter-06/u-02-06-04-reciprocal-quotient.qmd
              - text: "6.3 序关系怎样给出极限估计？"
                href: book/part-02/chapter-06/u-02-06-02-order-squeeze.qmd
              - text: "6.4 误差如何穿过一次迭代？"
                href: book/part-02/chapter-06/u-02-06-03-error-propagation.qmd
          - section: "第 7 章：单调性、完备性与收敛准则"
            contents:
              - text: "7.1 单调数列为什么会有极限？"
                href: book/part-02/chapter-07/u-02-07-01-monotone-sequences.qmd
              - text: "7.2 递推的界与单调性怎样建立？"
                href: book/part-02/chapter-07/u-02-07-02-recursive-invariants.qmd
              - text: "7.3 区间套怎样保证唯一目标？"
                href: book/part-02/chapter-07/u-02-07-03-nested-intervals.qmd
              - text: "7.4 完备性怎样成为收敛准则？"
                href: book/part-02/chapter-07/u-02-07-04-completeness-criteria.qmd
          - section: "第 8 章：子列、Cauchy 准则与上/下极限"
            contents:
              - text: "8.1 子列揭示了原数列的什么行为？"
                href: book/part-02/chapter-08/u-02-08-01-subsequences.qmd
              - text: "8.2 有界数列为何总能抽出收敛子列？"
                href: book/part-02/chapter-08/u-02-08-02-bolzano-weierstrass.qmd
              - text: "8.3 Cauchy 条件怎样不预知极限而判断收敛？"
                href: book/part-02/chapter-08/u-02-08-03-cauchy-criterion.qmd
              - text: "8.4 严格压缩怎样保证迭代找到唯一根？"
                href: book/part-02/chapter-08/u-02-08-04-contraction-mapping.qmd
              - text: "8.5 不动点计算需要哪些可核验证书？"
                href: book/part-02/chapter-08/u-02-08-06-fixed-point-certificates.qmd
              - text: "8.6 有限迭代轨迹能说明什么、不能说明什么？"
                href: book/part-02/chapter-08/u-02-08-07-iteration-lab.qmd
              - text: "8.7 上/下极限怎样总结所有尾部行为？"
                href: book/part-02/chapter-08/u-02-08-05-limsup-liminf.qmd
              - text: "8.8 上/下极限怎样由子列真正实现？"
                href: book/part-02/chapter-08/u-02-08-08-limsup-subsequences.qmd
      - section: "第三部：函数极限、连续性与方程"
        contents:
          - section: "第 9 章：函数极限与局部行为"
            contents:
              - text: "9.1 函数在一点附近意味着什么？"
                href: book/part-03/chapter-09/u-03-09-01-local-neighborhoods.qmd
              - text: "9.2 “任意接近”怎样定义函数极限？"
                href: book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.qmd
              - text: "9.3 局部估计怎样传递极限？"
                href: book/part-03/chapter-09/u-03-09-03-function-limit-laws.qmd
              - text: "9.4 用点列靠近能否判别函数极限？"
                href: book/part-03/chapter-09/u-03-09-04-sequential-function-limits.qmd
          - section: "第 10 章：连续函数与连续运算"
            contents:
              - text: "10.1 连续性怎样写成局部控制？"
                href: book/part-03/chapter-10/u-03-10-01-epsilon-delta-continuity.qmd
              - text: "10.2 连续性怎样经过运算和复合传递？"
                href: book/part-03/chapter-10/u-03-10-02-continuous-operations.qmd
              - text: "10.3 函数会以哪些方式失去连续性？"
                href: book/part-03/chapter-10/u-03-10-03-discontinuities-elementary-functions.qmd
          - section: "第 11 章：闭区间上的整体性质"
            contents:
              - text: "11.1 为什么闭区间能把无限局部信息压缩为有限控制？"
                href: book/part-03/chapter-11/u-03-11-01-compact-intervals.qmd
              - text: "11.2 连续函数为何一定有界并取得最值？"
                href: book/part-03/chapter-11/u-03-11-02-extreme-value-theorem.qmd
              - text: "11.3 局部连续何时升级为全局一致控制？"
                href: book/part-03/chapter-11/u-03-11-03-uniform-continuity.qmd
          - section: "第 12 章：零点、不动点与迭代求解"
            contents:
              - text: "12.1 连续函数怎样保证取遍中间值？"
                href: book/part-03/chapter-12/u-03-12-01-intermediate-value-theorem.qmd
              - text: "12.2 怎样把有根证明变成误差可证的算法？"
                href: book/part-03/chapter-12/u-03-12-02-certified-bisection.qmd
              - text: "12.3 有固定点是否意味着简单迭代会收敛？"
                href: book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.qmd
      - section: "附录"
        contents:
          - text: "Python 知识桥：函数、循环与异常"
            href: book/bridges/python/functions-loops.qmd
```

- [ ] **Step 2: Disable Quarto's automatic HTML heading numbering**

In `_quarto.yml`, change:

```yaml
    number-sections: true
```

to:

```yaml
    number-sections: false
```

- [ ] **Step 3: Run the focused source tests**

```bash
python3.12 -m unittest tests.test_sidebar -v
```

Expected: 4 tests pass. In particular, Chapter 5 must expose `5.1`, `5.2`, `5.3`, `5.4`, `5.5` in current reading order even though the third file has unit ID `u-02-05-05`.

- [ ] **Step 4: Run the full Python suite**

```bash
python3.12 -m unittest discover -s tests
```

Expected: all existing 159 tests plus the 4 new sidebar tests pass.

- [ ] **Step 5: Commit the configuration change**

```bash
git add _quarto.yml tests/test_sidebar.py
git commit -m "feat: add hierarchical unit sidebar"
```

### Task 3: Enforce rendered HTML numbering semantics

**Files:**
- Modify: `tests/test_site.py`
- Modify: `scripts/check_site.py`

- [ ] **Step 1: Write failing rendered-markup tests**

Add these methods to `SiteValidationTest` in `tests/test_site.py`:

```python
    def test_automatic_chapter_number_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text("book", encoding="utf-8")
            page = site / "unit.html"
            page.write_text(
                '<h1><span class="chapter-number">17</span> Unit</h1>',
                encoding="utf-8",
            )
            self.assertEqual(
                ["rendered unit page unit.html contains automatic chapter numbering"],
                validate_site(site, expected_pages=["unit.html"]),
            )

    def test_automatic_heading_number_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text("book", encoding="utf-8")
            page = site / "unit.html"
            page.write_text(
                '<h2><span class="header-section-number">17.1</span> Goal</h2>',
                encoding="utf-8",
            )
            self.assertEqual(
                ["rendered unit page unit.html contains automatic heading numbering"],
                validate_site(site, expected_pages=["unit.html"]),
            )
```

- [ ] **Step 2: Run the focused tests and verify both fail**

```bash
python3.12 -m unittest \
  tests.test_site.SiteValidationTest.test_automatic_chapter_number_is_reported \
  tests.test_site.SiteValidationTest.test_automatic_heading_number_is_reported -v
```

Expected: both FAIL because `validate_site` currently checks existence and links but not numbering classes.

- [ ] **Step 3: Add the minimal rendered-markup validation**

In `scripts/check_site.py`, replace the current expected-page existence loop:

```python
    for expected_page in expected_pages or []:
        if not (site / expected_page).is_file():
            errors.append(f"rendered site is missing registered unit page: {expected_page}")
```

with:

```python
    for expected_page in expected_pages or []:
        page = site / expected_page
        if not page.is_file():
            errors.append(f"rendered site is missing registered unit page: {expected_page}")
            continue
        rendered = page.read_text(encoding="utf-8")
        if 'class="chapter-number"' in rendered:
            errors.append(
                f"rendered unit page {expected_page} contains automatic chapter numbering"
            )
        if 'class="header-section-number"' in rendered:
            errors.append(
                f"rendered unit page {expected_page} contains automatic heading numbering"
            )
```

- [ ] **Step 4: Run the focused and full site-validator tests**

```bash
python3.12 -m unittest \
  tests.test_site.SiteValidationTest.test_automatic_chapter_number_is_reported \
  tests.test_site.SiteValidationTest.test_automatic_heading_number_is_reported -v
python3.12 -m unittest tests.test_site -v
```

Expected: both focused tests pass, then all `tests.test_site` tests pass.

- [ ] **Step 5: Commit rendered-markup enforcement**

```bash
git add scripts/check_site.py tests/test_site.py
git commit -m "test: reject automatic book numbering markup"
```

### Task 4: Run whole-project verification

**Files:**
- Verify: `_quarto.yml`
- Verify: `scripts/check_site.py`
- Verify: `tests/test_sidebar.py`
- Verify: `tests/test_site.py`

- [ ] **Step 1: Run whitespace and diff checks**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only intentional committed work is present.

- [ ] **Step 2: Run the full verification target**

```bash
DENO_DIR=/private/tmp/mathbook-quarto-sidebar make verify
```

Expected:

- all Python tests pass;
- outline reports `12 parts, 54 chapters, 278+92=370 hours`;
- unit registry reports `48 unit(s)`;
- Quarto renders 52 pages;
- `scripts/check_site.py` reports valid internal links and no automatic numbering markup.

- [ ] **Step 3: Inspect representative rendered HTML directly**

```bash
rg -n 'chapter-number|header-section-number' \
  _site/book/part-01/chapter-01/u-01-01-01-sets.html \
  _site/book/part-02/chapter-05/u-02-05-01-sequences.html \
  _site/book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.html
rg -n '1\.1 集合怎样组织数学对象|5\.1 数列怎样记录无限过程|12\.3 有固定点是否意味着简单迭代会收敛' \
  _site/book/part-02/chapter-05/u-02-05-01-sequences.html
```

Expected: the first command returns no matches; the second finds all three semantic sidebar labels in the rendered page.

### Task 5: Browser QA of the real rendered sidebar

**Files:**
- Inspect: `_site/index.html`
- Inspect: `_site/book/part-01/chapter-01/u-01-01-01-sets.html`
- Inspect: `_site/book/part-02/chapter-05/u-02-05-01-sequences.html`
- Inspect: `_site/book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.html`
- Inspect: `_site/book/bridges/python/functions-loops.html`

- [ ] **Step 1: Confirm Playwright CLI prerequisites**

```bash
command -v npx >/dev/null 2>&1
```

Expected: exit status 0.

- [ ] **Step 2: Serve the rendered site locally**

```bash
python3.12 -m http.server 8765 --directory _site
```

Expected: local server listens on port 8765. Keep it running in its own terminal session for the remaining browser checks.

- [ ] **Step 3: Open and inspect representative desktop pages**

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" open http://127.0.0.1:8765/book/part-02/chapter-05/u-02-05-01-sequences.html --headed
"$PWCLI" snapshot
```

Expected: the sidebar shows Second Part → Chapter 5 → `5.1` through `5.5`; the active item is `5.1`; H1 and right-side H2 entries have no automatic number.

- [ ] **Step 4: Inspect boundary chapters and appendix**

Navigate and snapshot these exact URLs:

```text
http://127.0.0.1:8765/book/part-01/chapter-01/u-01-01-01-sets.html
http://127.0.0.1:8765/book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.html
http://127.0.0.1:8765/book/bridges/python/functions-loops.html
```

Expected: Chapter 1 begins with `1.1`; Chapter 12 ends with `12.3`; the appendix is under “附录” and has no 1–12 chapter number.

- [ ] **Step 5: Inspect narrow-screen behavior**

```bash
"$PWCLI" resize 390 844
"$PWCLI" snapshot
```

Expected: the sidebar toggle remains usable, long Chinese labels wrap without horizontal clipping, and opening the active chapter still exposes the unit links.

- [ ] **Step 6: Close the browser and stop the local server**

```bash
"$PWCLI" close
```

Then send `Ctrl-C` to the terminal session running `python3.12 -m http.server`.

Expected: browser and local HTTP server exit cleanly.

- [ ] **Step 7: Record final repository state**

```bash
git status --short
git log -4 --oneline --decorate
```

Expected: working tree is clean and the two implementation commits are visible after the prior design/plan commits.
