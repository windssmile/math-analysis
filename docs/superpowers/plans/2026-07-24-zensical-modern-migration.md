# Zensical Modern 数学教材站迁移 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 将数学教材站从 MkDocs Material 构建迁移到 Zensical `modern`，且保持内容、URL、锚点、MathJax、Python 示例与 Pages 产物不变。

**Architecture:** 保留 `mkdocs.yml`、`content/` 和 `site/`，由固定版本 Zensical 读取兼容配置。最小 MiniJinja `content` block override 继续用页面 front matter 输出学习单元信息；额外 CSS 只保证中文正文、公式和代码的阅读体验。

**Tech Stack:** Python 3.12、Zensical 0.0.51、Python-Markdown/PyMdown Extensions、MathJax 3、MiniJinja、GitHub Pages。

---

## 文件职责

| 路径 | 责任 |
|---|---|
| `requirements.txt` | 只固定 `zensical==0.0.51`。 |
| `mkdocs.yml` | Zensical 兼容配置、modern 主题、导航和扩展。 |
| `Makefile` | 严格构建、预览和既有检查入口。 |
| `overrides/` | 使用 `page.meta` 呈现学习单元信息的最小 MiniJinja 覆写。 |
| `content/stylesheets/extra.css` | 中文、元数据、公式和代码的响应式阅读增强。 |
| `tests/test_zensical_*.py` | 新驱动的配置和真实严格构建回归。 |

### Task 1: 写出 Zensical 失败用例

**Files:**
- Create: `tests/test_zensical_structure.py`
- Create: `tests/test_zensical_build.py`
- Modify: `tests/test_project_structure.py`
- Modify: `tests/test_theme_contract.py`
- Delete: `tests/test_mkdocs_build.py`
- Delete: `tests/test_mkdocs_structure.py`

- [x] **Step 1: 创建配置契约测试**

在 `tests/test_zensical_structure.py` 创建 `ZensicalStructureTests.test_zensical_shell_declares_the_content_site_contract`。它读取 `requirements.txt`、`mkdocs.yml` 和 `Makefile`，并执行：

```python
self.assertEqual(requirements.strip(), "zensical==0.0.51")
for marker in ("docs_dir: content", "site_dir: site", "strict: true", "variant: modern"):
    self.assertIn(marker, config)
self.assertIn("zensical build --strict", makefile)
self.assertIn("zensical serve", makefile)
self.assertNotIn("mkdocs build", makefile)
self.assertNotIn("mkdocs serve", makefile)
```

- [x] **Step 2: 创建真实构建测试**

在 `tests/test_zensical_build.py` 创建 `ZensicalBuildTests.test_modern_theme_builds_in_strict_mode`，以 `subprocess.run(["zensical", "build", "--strict"], cwd=ROOT, capture_output=True, text=True, check=False)` 运行构建，并断言 `returncode == 0`。

- [x] **Step 3: 观察 RED**

Run: `python3.12 -m unittest tests.test_zensical_structure -v`
Expected: FAIL，依赖不是 `zensical==0.0.51`，Makefile 尚未包含 Zensical 命令。

- [x] **Step 4: 迁移现有测试术语**

在 `tests/test_project_structure.py` 的工作流断言中要求 `Install Zensical dependencies`、`make verify` 和 `path: site`，并禁止 `mkdocs-material`、`mkdocs build` 和 `mkdocs serve`。在 `tests/test_theme_contract.py` 将方法更名为 `test_modern_reading_theme_has_its_required_contract`，要求配置包含 `variant: modern`、`custom_dir: overrides` 和 `extra_css:`，同时保留 `.unit-meta`、`@media`、`page.meta.unit_id`、`page.meta.hours` 与 `page.meta.learning_goals`。删除旧 `test_mkdocs_build.py` 与 `test_mkdocs_structure.py`。

- [x] **Step 5: 观察完整 RED 并提交**

Run: `python3.12 -m unittest tests.test_zensical_structure tests.test_project_structure tests.test_theme_contract -v`
Expected: FAIL，失败仅来自依赖、主题变体、Makefile 和 workflow 尚未替换。
Commit: `git add tests && git commit -m "test: define Zensical migration contract"`。

### Task 2: 用最小配置切换到 Zensical modern

**Files:**
- Modify: `requirements.txt`
- Modify: `mkdocs.yml`
- Modify: `Makefile`
- Modify: `overrides/main.html`
- Modify: `overrides/partials/unit-meta.html`
- Modify: `content/stylesheets/extra.css`

- [x] **Step 1: 确认构建用例为 RED**

Run: `python3.12 -m unittest tests.test_zensical_build -v`
Expected: FAIL，`zensical` 不存在，证明测试没有继续调用 MkDocs。

- [x] **Step 2: 写入最小生产配置**

将 `requirements.txt` 完全替换为 `zensical==0.0.51`，运行 `python3.12 -m pip install --requirement requirements.txt`。将 `mkdocs.yml` 的主题段替换为：

```yaml
theme:
  variant: modern
  custom_dir: overrides
  language: zh
```

保留 `docs_dir`、`site_dir`、`use_directory_urls`、`nav`、Markdown 扩展、MathJax、额外 CSS 与 `strict: true`；删除 `name: material` 和 `features:`。将 Makefile 的两个命令改成 `zensical build --strict` 与 `zensical serve`。

- [x] **Step 3: 保留兼容的单元信息模板与通用 CSS**

把 `overrides/main.html` 限定为：

```html
{% extends "base.html" %}
{% block content %}
  {% if page and page.meta and page.meta.unit_id %}{% include "partials/unit-meta.html" %}{% endif %}
  {{ super() }}
{% endblock %}
```

`unit-meta.html` 只能使用属性读取、`if`、`for` 与 `join("、")`。实际构建证明 Zensical modern 保留了兼容的 `.md-*` DOM 与现有响应式 CSS 变量，因此保留 `.unit-meta`、中文字体和 `@media` 布局，不为主题升级重写已验证的阅读样式；仅将不兼容的 `page.meta.prerequisites.items()` 改为 MiniJinja 的 `page.meta.prerequisites | items`。

- [x] **Step 4: 观察 GREEN 并提交**

Run: `python3.12 -m unittest tests.test_zensical_structure tests.test_theme_contract tests.test_zensical_build -v`
Expected: PASS；Zensical 严格构建退出码为 0。
Commit: `git add requirements.txt mkdocs.yml Makefile overrides content/stylesheets/extra.css && git commit -m "build: migrate textbook site to Zensical modern"`。

### Task 3: 迁移站点检查与 Pages 工作流

**Files:**
- Modify: `scripts/check_site.py`
- Modify: `tests/test_mkdocs_site.py`
- Modify: `.github/workflows/pages.yml`
- Modify: `tests/test_project_structure.py`

- [x] **Step 1: 为站点检查增加命令回归**

将 `tests/test_mkdocs_site.py` 中的类改为 `ZensicalSiteValidationTests`，将验证 Makefile 的测试改名为 `test_verify_target_runs_the_zensical_site_checker`，并增加：

```python
self.assertIn("zensical build --strict", makefile)
self.assertNotIn("mkdocs build", makefile)
```

Run: `python3.12 -m unittest tests.test_mkdocs_site -v`
Expected: Task 2 前 FAIL，Task 2 后 PASS。

- [x] **Step 2: 校准 Zensical modern 的导航产物断言**

运行 `zensical build --strict`，查看 `site/index.html` 与二分法单元 HTML。若 `scripts/check_site.py` 的 Material 专有导航标志不在真实输出内，则换为同一页面实际含有的 Zensical modern 原生导航属性或 class；不得移除导航检查。保留内部链接、代表锚点、中文 title 和 MathJax 检查。

- [x] **Step 3: 更新 Pages 安装步骤并观察 GREEN**

将 `.github/workflows/pages.yml` 中步骤名改为 `Install Zensical dependencies`，但保持命令 `python3.12 -m pip install --requirement requirements.txt`、`make verify` 与 `path: site` 不变。
Run: `python3.12 -m unittest tests.test_project_structure tests.test_mkdocs_site -v`
Expected: PASS。
Commit: `git add scripts/check_site.py tests/test_mkdocs_site.py tests/test_project_structure.py .github/workflows/pages.yml && git commit -m "ci: build Pages with Zensical"`。

### Task 4: 进行全量验收并记录结果

**Files:**
- Modify: `docs/superpowers/plans/2026-07-24-zensical-modern-migration.md`

- [x] **Step 1: 清除旧驱动引用**

Run: `rg -n "mkdocs build|mkdocs serve|mkdocs-material==|mkdocs==" Makefile requirements.txt mkdocs.yml .github scripts`
Expected: 无匹配；测试中的负向断言允许保留这些字符串，`mkdocs.yml` 文件名本身也保留，因为它是 Zensical 的兼容配置格式。

- [x] **Step 2: 运行全量质量门**

Run: `make verify`
Expected: 全部算法、内容、迁移、结构、主题和站点测试通过，`zensical build --strict` 和站点检查成功。

- [x] **Step 3: 检查真实输出和阅读体验**

Run: `rg -n "u-01-04-02|def-u-02-08-04-contraction|thm-u-03-12-01-intermediate-value|unit-meta|mathjax" site/index.html site/chapters/chapter-04/u-01-04-02-interval-bisection/index.html site/chapters/chapter-08/u-02-08-04-contraction-mapping/index.html site/chapters/chapter-12/u-03-12-01-intermediate-value-theorem/index.html`
Expected: 每个稳定锚点、单元卡片和 MathJax 标志均出现在对应 HTML。
Run: `zensical serve`；在桌面与约 390px 宽视口检查首页、二分法、压缩映射和介值定理，确认 modern 导航、中文段落、长公式、代码、折叠答案和单元信息可读。

- [x] **Step 4: 写入验收记录并提交**

将本计划所有完成项改为 `[x]`，末尾追加 `make verify`、严格构建、核心锚点/MathJax/单元信息和桌面/窄屏阅读检查的实际结果。
Commit: `git add docs/superpowers/plans/2026-07-24-zensical-modern-migration.md && git commit -m "docs: record Zensical migration verification"`。

## 验收记录

- `make verify`：通过，40 项测试、内容检查、`zensical build --strict` 与站点检查均成功。
- 严格构建：Zensical 0.0.51 输出至 `site/`，没有警告或错误。
- 核心单元：二分法、压缩映射和介值定理的稳定锚点、MathJax 与 `unit-meta` 均已在真实 HTML 中核对。
- 浏览器阅读检查：Zensical modern 在桌面端保留三级阅读布局；390px 窄屏下单元信息卡变为单列，文本与公式未出现横向溢出。
