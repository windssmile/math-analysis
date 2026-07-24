# MkDocs Material 数学教材迁移 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 Quarto 数学分析网站迁移为采用 Material 3 阅读模式的 MkDocs Material 网站，并保留已发布的教材内容、稳定锚点、Python 源码与质量门。

**Architecture:** `content/` 成为网站内容唯一来源；每个单元在自己的 YAML front matter 保存教学元数据，主题 partial 负责呈现，内容检查器负责验证。MkDocs Material 负责静态构建、导航、搜索、MathJax 和代码展示；算法代码仍由 Python 单元测试验证，不在网页构建时执行。

**Tech Stack:** Python 3.12、MkDocs 1.6.1、Material for MkDocs 9.7.7、Python-Markdown/PyMdown Extensions、MathJax 3、GitHub Actions、GitHub Pages。

---

## 已锁定的范围与停止点

- 不引入 Flutter SDK、Dart、Node.js 或浏览器内 Python 运行时；“Flutter 样式”只指 Material 3 视觉语言。
- 不迁移第 4 部及之后的空章节为发布页面。
- 第 1–5 个任务只完成基础设施和第 1 部试点。完成任务 5 后停止，等待用户确认阅读体验，再执行任务 6–8。
- 不保留 `units.toml`、`outline.toml` 或自动生成的逐单元课程地图；每页 front matter 是教学元数据唯一来源，章节页和课程地图只保留导航性摘要。

## 目标文件职责

| 路径 | 责任 |
|---|---|
| `requirements.txt` | 固定 MkDocs 与 Material 版本。 |
| `mkdocs.yml` | 站点导航、Material 功能、Markdown 扩展、JavaScript、CSS 与输出目录的唯一配置。 |
| `content/` | 所有将发布的教材 Markdown、MathJax 配置与主题 CSS。 |
| `overrides/main.html` | 在文章正文之前有条件地呈现单元信息 partial。 |
| `overrides/partials/unit-meta.html` | 从 `page.meta` 输出单元学时、难度、先备、能力与目标。 |
| `scripts/migrate_quarto_to_mkdocs.py` | 可重复地把 Quarto 常用语法转换到 Material Markdown，输出转换清单。 |
| `scripts/check_content.py` | 从 `content/` 自身验证单元 front matter、栏目、锚点、答案数和 Markdown 链接。 |
| `scripts/check_site.py` | 检查 `site/` 的内部链接、代表页、稳定锚点、页面标题和 Material 导航标志。 |
| `src/mathbook_examples/` | 唯一可执行的 Python 算法实现。 |
| `tests/test_bisection.py`、`tests/test_fixed_point.py` | 算法行为与误差证书测试，保持原有断言。 |
| `.github/workflows/pages.yml` | 安装 Python/MkDocs，运行检查，构建并部署 Pages。 |

### Task 1: 建立 MkDocs 依赖、构建外壳与失败测试

**Files:**
- Create: `requirements.txt`
- Create: `mkdocs.yml`
- Create: `content/index.md`
- Create: `content/javascripts/mathjax.js`
- Create: `tests/test_mkdocs_structure.py`
- Modify: `Makefile`
- Modify: `.gitignore`

- [ ] **Step 1: 写出 MkDocs 结构的失败测试**

在 `tests/test_mkdocs_structure.py` 中要求配置、首页、MathJax 文件、依赖文件存在，并要求 `mkdocs.yml` 包含 `docs_dir: content`、`site_dir: site`、`strict: true` 与 `content.code.copy`。测试的核心断言为：

```python
required = ("requirements.txt", "mkdocs.yml", "content/index.md", "content/javascripts/mathjax.js")
missing = [path for path in required if not (ROOT / path).is_file()]
self.assertEqual(missing, [])
config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
for marker in ("docs_dir: content", "site_dir: site", "strict: true", "content.code.copy"):
    self.assertIn(marker, config)
```

- [ ] **Step 2: 运行失败测试确认基线**

Run: `python3.12 -m unittest tests.test_mkdocs_structure -v`  
Expected: FAIL，报告缺少 `requirements.txt`、`mkdocs.yml` 与 `content/index.md`。

- [ ] **Step 3: 写入最小站点外壳**

创建以下固定依赖：

```text
mkdocs==1.6.1
mkdocs-material==9.7.7
```

在 `mkdocs.yml` 配置 `theme.name: material`、中文界面、`navigation.tabs`、`navigation.sections`、`navigation.top`、`search.suggest`、`search.highlight`、`content.code.copy` 与 `toc.follow`。配置 `pymdownx.arithmatex`、`pymdownx.highlight`、`pymdownx.inlinehilite`、`pymdownx.superfences`、`pymdownx.snippets`（`base_path: ['.']`）、`pymdownx.details` 和 `pymdownx.tabbed`，并加载 `javascripts/mathjax.js` 与 MathJax 3 CDN。首页只描述教材定位和第 1–3 部已发布状态。

将 `site/` 加入 `.gitignore`，将 Makefile 的临时目标改为：

```make
PYTHON ?= python3.12

test:
	$(PYTHON) -m unittest discover -s tests -v

check:
	$(PYTHON) scripts/check_content.py

build: check
	mkdocs build --strict

verify: test build
```

- [ ] **Step 4: 运行结构测试和最小构建**

Run: `python3.12 -m unittest tests.test_mkdocs_structure -v && python3.12 -m pip install --requirement requirements.txt && mkdocs build --strict`  
Expected: 结构测试 PASS；MkDocs 在 `site/` 生成首页，无 warning。

- [ ] **Step 5: 提交独立的站点外壳**

```bash
git add requirements.txt mkdocs.yml content/index.md content/javascripts/mathjax.js tests/test_mkdocs_structure.py Makefile .gitignore
git commit -m "build: add MkDocs Material site shell"
```

### Task 2: 定义页面元数据、Material 3 阅读主题与其测试

**Files:**
- Create: `content/stylesheets/extra.css`
- Create: `overrides/main.html`
- Create: `overrides/partials/unit-meta.html`
- Create: `tests/test_theme_contract.py`
- Modify: `mkdocs.yml`

- [ ] **Step 1: 写出主题契约的失败测试**

在 `tests/test_theme_contract.py` 中断言 `mkdocs.yml` 启用了 `custom_dir: overrides` 和 `extra_css`；断言 CSS 含 `--md-primary-fg-color`、`.unit-meta`、`@media`；断言 partial 读取 `page.meta.unit_id`、`page.meta.hours` 和 `page.meta.learning_goals`。

- [ ] **Step 2: 运行主题契约测试确认失败**

Run: `python3.12 -m unittest tests.test_theme_contract -v`  
Expected: FAIL，因为主题覆盖和 CSS 尚不存在。

- [ ] **Step 3: 实现 Material 3 阅读模式**

在 `extra.css` 以 CSS variables 定义靛蓝主色、低饱和辅助色、暖白 surface 与深墨文字；将 `.md-content__inner` 设为 48rem 左右的正文宽度；为 `.unit-meta`、Material admonition、代码块和详情块定义一致的圆角、细边框与低阴影；在 768px 以下取消固定宽度，并保证长公式与代码可滚动。

在 `main.html` 中继承 Material 的 `main.html`，仅当 `page.meta.unit_id` 存在时、在 `tabs` block 后插入 partial。partial 不写死课程内容，而是循环渲染 `hours`、`prerequisites`、`capabilities` 与 `learning_goals`，使每个单元只维护自己的 YAML 数据。

- [ ] **Step 4: 运行主题契约测试**

Run: `python3.12 -m unittest tests.test_theme_contract -v`  
Expected: PASS。

- [ ] **Step 5: 提交主题层**

```bash
git add content/stylesheets/extra.css overrides/main.html overrides/partials/unit-meta.html tests/test_theme_contract.py mkdocs.yml
git commit -m "feat: add Material 3 reading theme"
```

### Task 3: 先实现内容检查器，再实现可重复转换器

**Files:**
- Create: `scripts/check_content.py`
- Create: `scripts/migrate_quarto_to_mkdocs.py`
- Create: `tests/test_check_content.py`
- Create: `tests/test_migrate_quarto_to_mkdocs.py`

- [ ] **Step 1: 写入内容检查的失败测试**

在 `tests/test_check_content.py` 用临时 `content/chapters/01-analysis-language/01-01-sets.md` 覆盖以下情形：有效 v2 单元、缺失 `unit_id`、标题缺失 `{#u-...}`、总学时 2.26、缺失“概念与理论”、仅 1 个例题、仅 4 个习题、仅 6 个 `??? note "答案"`，以及指向不存在页面的相对链接。每个异常应返回一条包含页面相对路径和字段名的错误。

- [ ] **Step 2: 运行检查器测试确认失败**

Run: `python3.12 -m unittest tests.test_check_content -v`  
Expected: FAIL，原因是 `scripts.check_content` 不存在。

- [ ] **Step 3: 实现最小内容检查器**

实现 `validate_content(content_root: Path) -> list[str]`。它解析 YAML front matter，验证 `unit_id`、`hours.theory`、`hours.applied`、`difficulty`、四类 `prerequisites`、`capabilities`、`learning_goals` 与 `content_standard`。它跳过代码围栏后检查一级标题锚点、八个核心二级标题、v2 数量约束和相对 Markdown 链接。`main()` 打印每条错误并返回 1；无错误时返回 0。

- [ ] **Step 4: 写入 Quarto 转换器的失败测试**

在 `tests/test_migrate_quarto_to_mkdocs.py` 传入一个代表性 QMD 字符串，要求转换结果满足：`.qmd` 链接变为 `.md`；`::: {.callout-note collapse="true"}` 变为 `??? note "答案"`；非折叠 `.callout-note` 变为 `!!! note`；`{.unnumbered}` 被移除；原有 `{#u-01-...}` 和 `### ... {#def-...}` 保持不变。

- [ ] **Step 5: 运行转换器测试确认失败**

Run: `python3.12 -m unittest tests.test_migrate_quarto_to_mkdocs -v`  
Expected: FAIL，原因是 `scripts.migrate_quarto_to_mkdocs` 不存在。

- [ ] **Step 6: 实现确定性转换器**

实现纯函数 `convert_markdown(source: str) -> str` 与 CLI：

```text
python3.12 scripts/migrate_quarto_to_mkdocs.py --source book --destination content --report /private/tmp/mathbook-migration-report.json
```

CLI 按明确映射复制 QMD 为 Markdown；不覆盖已有目标，发现不支持的 fenced div、未关闭块或无法映射的链接时非零退出并报告源路径。单元 YAML front matter 从当前 `.unit-meta` 列表和 `curriculum/units.toml` 的同一单元记录组合生成；标题、正文、公式、stable IDs、例题与习题原文不改写。

- [ ] **Step 7: 运行全部新增检查**

Run: `python3.12 -m unittest tests.test_check_content tests.test_migrate_quarto_to_mkdocs -v`  
Expected: PASS。

- [ ] **Step 8: 提交转换与检查基础设施**

```bash
git add scripts/check_content.py scripts/migrate_quarto_to_mkdocs.py tests/test_check_content.py tests/test_migrate_quarto_to_mkdocs.py
git commit -m "feat: add MkDocs content migration checks"
```

### Task 4: 迁移第 1 部并验证教材、公式与源码嵌入

**Files:**
- Create: `content/preface.md`
- Create: `content/course-map.md`
- Create: `content/bridges/python-functions-loops.md`
- Create: `content/chapters/01-analysis-language/index.md`
- Create: `content/chapters/01-analysis-language/01-01-sets.md`
- Create: `content/chapters/01-analysis-language/01-02-quantifiers.md`
- Create: `content/chapters/01-analysis-language/01-03-proofs.md`
- Create: `content/chapters/01-analysis-language/01-04-functions.md`
- Create: `content/chapters/02-real-numbers/index.md`
- Create: `content/chapters/02-real-numbers/02-01-rational-gaps.md`
- Create: `content/chapters/02-real-numbers/02-02-dedekind-cuts.md`
- Create: `content/chapters/02-real-numbers/02-03-cut-order-operations.md`
- Create: `content/chapters/03-supremum/index.md`
- Create: `content/chapters/03-supremum/03-01-bounds.md`
- Create: `content/chapters/03-supremum/03-02-supremum-principle.md`
- Create: `content/chapters/03-supremum/03-03-completeness-consequences.md`
- Create: `content/chapters/04-approximation/index.md`
- Create: `content/chapters/04-approximation/04-01-recurrence.md`
- Create: `content/chapters/04-approximation/04-02-interval-bisection.md`
- Create: `content/chapters/04-approximation/04-03-approximation-error.md`
- Create: `content/chapters/04-approximation/04-04-failure-of-infinite-approximation.md`
- Modify: `mkdocs.yml`
- Create: `tests/test_part_01_migration.py`

- [ ] **Step 1: 写出第 1 部迁移完成的失败测试**

在 `tests/test_part_01_migration.py` 断言 14 个目标单元页面均存在，每页的 front matter `unit_id` 与原 ID 相同，`01-04-interval-bisection.md` 通过 snippets 嵌入 `src/mathbook_examples/bisection.py`，以及 `mkdocs.yml` 的导航顺序为前言、课程地图、第 1–4 章和 Python 知识桥。

- [ ] **Step 2: 运行第 1 部迁移测试确认失败**

Run: `python3.12 -m unittest tests.test_part_01_migration -v`  
Expected: FAIL，报告缺少目标单元页面。

- [ ] **Step 3: 执行转换器并人工修订第 1 部**

运行转换器，只写入第 1 部、前言、课程地图与知识桥。将原 `book/part-01/chapter-XX/` 文件映射到目标列表的章节目录。逐页检查：YAML 元数据、公式、所有稳定锚点、折叠答案、例题/习题 ID 与相对链接；将原课程地图缩减为部/章路线，并在每个章节 `index.md` 保留本章问题、先备、成果、单元目录与边界。把二分法源代码改为 snippets 嵌入，不复制代码文本。

- [ ] **Step 4: 完成第 1 部导航**

在 `mkdocs.yml` 只登记发布页，使用如下层级：

```yaml
nav:
  - 首页: index.md
  - 阅读说明: preface.md
  - 全书课程地图: course-map.md
  - 第一部：实数、函数与分析语言:
      - 第 1 章：函数、集合与数学陈述:
          - 本章导学: chapters/01-analysis-language/index.md
          - 1.1 集合怎样组织数学对象？: chapters/01-analysis-language/01-01-sets.md
```

按此模式列出第 1–4 章的所有 14 个单元和附录知识桥。

- [ ] **Step 5: 运行第 1 部迁移、算法与内容检查**

Run: `python3.12 -m unittest tests.test_part_01_migration tests.test_bisection -v && python3.12 scripts/check_content.py && mkdocs build --strict`  
Expected: 全部 PASS，`site/` 出现第 1 部的 14 个单元和 Python 知识桥。

- [ ] **Step 6: 提交第 1 部迁移**

```bash
git add content/chapters content/preface.md content/course-map.md content/bridges mkdocs.yml tests/test_part_01_migration.py
git commit -m "feat: migrate part one to MkDocs"
```

### Task 5: 对第 1 部执行渲染与人工阅读验收，然后停止

**Files:**
- Create: `tests/test_mkdocs_site.py`
- Modify: `scripts/check_site.py`
- Modify: `Makefile`
- Delete: `tests/test_site.py`（旧 Quarto `_site` 输出契约测试，由新的 MkDocs 站点测试取代）

- [ ] **Step 1: 写出渲染站点检查的失败测试**

在 `tests/test_mkdocs_site.py` 创建最小 `site/` fixture，验证断链、缺失代表锚点、错误页面标题和代表页缺少 `md-sidebar` 时都会返回错误。代表锚点包含 `u-01-02-02`、`def-u-01-02-02-dedekind-cut`、`alg-u-01-04-02-bisection` 与 `thm-u-01-04-03-bisection-step-count`。

- [ ] **Step 2: 运行站点检查测试确认失败**

Run: `python3.12 -m unittest tests.test_mkdocs_site -v`  
Expected: FAIL，因为旧的 `check_site.py` 仍读取 `_site` 和 TOML registry。

- [ ] **Step 3: 改写站点检查器与 Makefile**

令 `check_site.py` 默认读取 `site/`，从 `content/` 枚举单元页面而不是 TOML。它检查内部链接、代表 HTML 页、稳定锚点、中文 title、MathJax 脚本和 Material 侧栏标记。Makefile 使用：

```make
site-check: build
	$(PYTHON) scripts/check_site.py

verify: test check build site-check
```

- [ ] **Step 4: 替换旧站点输出契约并运行完整第 1 部验证**

删除仅依赖 Quarto `_site` 路径、自动章节编号和 TOML registry 的 `tests/test_site.py`；这些行为不属于 MkDocs 的发布契约，断链、锚点、标题和导航检查改由 `tests/test_mkdocs_site.py` 覆盖。

Run: `python3.12 -m unittest discover -s tests -v && python3.12 scripts/check_content.py && mkdocs build --strict && python3.12 scripts/check_site.py`  
Expected: PASS；无 Quarto、Deno、TOML registry 或 `_site` 依赖。

- [ ] **Step 5: 执行人工视觉验收**

Run: `mkdocs serve`  
Expected: 在桌面和约 390px 宽的移动端检查首页、`01-04-interval-bisection.md`、`02-02-dedekind-cuts.md`：正文约 48rem、侧栏层次清楚、公式完整、代码可复制、折叠答案可操作、浅深色均可读、Material 3 surface 不遮盖教材层级。

- [ ] **Step 6: 提交试点质量门并停止**

```bash
git add scripts/check_site.py tests/test_mkdocs_site.py Makefile docs/superpowers/plans/2026-07-24-mkdocs-material-migration.md
git add -u -- tests/test_site.py
git commit -m "test: validate MkDocs part one site"
```

停止条件：向用户展示第 1 部试点，获得明确的阅读体验确认后才进入任务 6。

### Task 6: 迁移第 2、3 部、课程路线与 Python 知识桥链接

**Files:**
- Create: `content/chapters/05-sequences/` 到 `content/chapters/12-equations-iteration/` 下的 34 个单元页和 8 个章节导学页
- Modify: `content/course-map.md`
- Modify: `content/bridges/python-functions-loops.md`
- Modify: `mkdocs.yml`
- Create: `tests/test_parts_02_03_migration.py`

- [ ] **Step 1: 写出第 2、3 部迁移的失败测试**

`tests/test_parts_02_03_migration.py` 应列出全部 34 个目标 Markdown 页面，断言每个旧 `u-02-*`、`u-03-*` ID 仍为新页 H1 ID；断言压缩映射、Cauchy、limsup/liminf、函数极限、紧致、介值定理和二分法的代表定义/定理锚点仍存在；断言 Python 链接仍指向知识桥。

- [ ] **Step 2: 运行迁移测试确认失败**

Run: `python3.12 -m unittest tests.test_parts_02_03_migration -v`  
Expected: FAIL，报告缺少第 2、3 部目标页面。

- [ ] **Step 3: 执行转换并逐章复核**

将第 2 部映射为 `05-sequences`、`06-limit-laws`、`07-completeness`、`08-subsequences`；将第 3 部映射为 `09-function-limits`、`10-continuity`、`11-compact-intervals`、`12-equations-iteration`。每章先生成 `index.md`，再转换单元；人工检查原先备关系、Part II/III 边界、稳定锚点、折叠答案和所有跨章链接。将算法代码展示改为 snippets；不改变 `fixed_point.py` 与 `bisection.py` 的算法行为。

- [ ] **Step 4: 完成新导航与课程路线**

在 `mkdocs.yml` 登记第 5–12 章；`course-map.md` 只列出第 1–12 章的部级问题弧、章标题、总学时与章节入口，不再次罗列单元。知识桥页使用新相对 Markdown 链接回到第 2、3 部使用它的单元。

- [ ] **Step 5: 运行迁移、算法和站点全量验证**

Run: `python3.12 -m unittest discover -s tests -v && python3.12 scripts/check_content.py && mkdocs build --strict && python3.12 scripts/check_site.py`  
Expected: PASS；内容检查发现 48 个单元页，站点有 52 个左右的可发布页面，算法测试保持 PASS。

- [ ] **Step 6: 提交第 2、3 部内容迁移**

```bash
git add content/chapters content/course-map.md content/bridges mkdocs.yml tests/test_parts_02_03_migration.py
git commit -m "feat: migrate parts two and three to MkDocs"
```

### Task 7: 切换 GitHub Pages 工作流并删除 Quarto 运行时

**Files:**
- Modify: `.github/workflows/pages.yml`
- Modify: `.gitignore`
- Delete: `_quarto.yml`
- Delete: `styles.css`
- Delete: `index.qmd`
- Delete: `book/`
- Delete: `curriculum/outline.toml`
- Delete: `curriculum/units.toml`
- Delete: `scripts/check_outline.py`
- Delete: `scripts/check_units.py`
- Delete: `scripts/fix_page_titles.py`
- Delete: Quarto 专用测试 `tests/test_outline.py`、`tests/test_units.py`、`tests/test_curriculum_map.py`、`tests/test_page_titles.py`、`tests/test_sidebar.py`
- Modify: `tests/test_project_structure.py`

- [ ] **Step 1: 写出部署工作流的失败测试**

在 `tests/test_project_structure.py` 断言 Pages workflow 包含 `pip install --requirement requirements.txt`、`make verify` 和 `path: site`；断言 workflow 不含 `quarto-dev/quarto-actions`、`make render`、`_site` 或 Deno。

- [ ] **Step 2: 运行结构测试确认失败**

Run: `python3.12 -m unittest tests.test_project_structure -v`  
Expected: FAIL，当前 workflow 仍安装 Quarto 并上传 `_site`。

- [ ] **Step 3: 替换 CI 并移除已废弃运行时**

把 workflow build job 改为 Python 3.12、安装 `requirements.txt`、运行 `make verify`、配置 Pages、上传 `site`。先运行任务 6 的完整命令并确认 Git 跟踪的新 `content/` 完整，再删除 Quarto 源、TOML registry、生成器和只测试其行为的测试文件。保留 `curriculum/parts-02-03-dependencies.md`，移动到 `docs/curriculum/`，并更新结构测试读取的新路径。

- [ ] **Step 4: 运行最终本地验收**

Run: `python3.12 -m unittest discover -s tests -v && python3.12 scripts/check_content.py && mkdocs build --strict && python3.12 scripts/check_site.py && git status --short`  
Expected: 所有测试 PASS；`site/` 未被 Git 跟踪；仅计划中的迁移文件发生变更。

- [ ] **Step 5: 提交运行时切换**

```bash
git add .github/workflows/pages.yml .gitignore Makefile content docs/curriculum scripts tests
git add -u -- _quarto.yml styles.css index.qmd book curriculum
git commit -m "build: switch textbook site from Quarto to MkDocs"
```

### Task 8: 发布后验收与回滚边界

**Files:**
- Create: `README.md`
- Modify: `.github/workflows/pages.yml`

- [ ] **Step 1: 更新运行和发布说明**

README 明确写出 Python 3.12、`python3.12 -m pip install --requirement requirements.txt`、`mkdocs serve`、`make verify`，并说明网站为 Material 3 阅读模式、Python 代码只展示和测试、不在浏览器执行。

- [ ] **Step 2: 提交发布文档**

```bash
git add README.md .github/workflows/pages.yml
git commit -m "docs: document MkDocs textbook workflow"
```

- [ ] **Step 3: 在分支上运行 Pages 工作流**

Run: `git push origin HEAD`  
Expected: GitHub Actions 的 build 和 deploy 任务成功，Pages artifact 来源为 `site`。

- [ ] **Step 4: 检查已部署站点**

检查首页、一个第 1 部页面、一个第 2 部页面、一个第 3 部算法页面与 Python 知识桥：页面标题、导航、锚点、MathJax、代码复制、折叠答案、桌面/移动端 Material 3 阅读体验全部正确。

## 计划自检

- 设计中的 Web-first、Python 保留、稳定锚点、Material 3 阅读模式、轻量元数据和第 1 部停止门均有对应任务。
- 所有转换、检查、构建、部署与删除动作都有明确文件、命令和预期结果。
- 文档未要求任何未确认的 Flutter runtime、浏览器执行 Python 或第 4 部以上的空内容页。
