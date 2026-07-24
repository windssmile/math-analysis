# MkDocs Material 迁移设计

**状态：** 已确认，2026-07-24

## 目标

将数学分析教材从 Quarto 网站迁移为 MkDocs Material 网站，降低日常维护的重复登记成本，同时保留自学教材的内容标准、稳定锚点、Python 源码与自动化测试。站点采用 Material 3（Flutter 风格）阅读模式：它借用 Flutter Material 的 surface、圆角、状态色和触摸反馈，但不打包 Flutter SDK，也不把教材做成一套 App。

## 已确认的决策

1. 发布形态是 Web-first 静态站；本次不提供 PDF、Word、ePub 或浏览器内 Python 运行时。
2. Python 代码继续放在 `src/mathbook_examples/`，继续由 `tests/test_bisection.py` 和 `tests/test_fixed_point.py` 执行；教材只嵌入同一份源代码。
3. 每个学习单元的学时、先备、能力与目标进入该页 YAML front matter。它既是唯一元数据来源，也由主题 partial 呈现为“单元信息”卡片。
4. 章节 `index.md` 是该章的导学与单元目录；顶层 `course-map.md` 只维护部/章级路线，不再逐单元复制导航。
5. 页面继续保留现有稳定的 `u-`、`def-`、`thm-`、`ex-`、`pr-`、`alg-` 锚点。旧页面 URL 不承诺永久兼容，因为当前是试点发布；站内链接必须全部迁移为新路径。
6. 第 1 部是迁移试点。只有在内容检查、算法测试、严格构建、链接检查和人工移动端阅读验收均通过后，才开始第 2、3 部。

## 目标结构

```text
content/
  index.md
  preface.md
  course-map.md
  bridges/python-functions-loops.md
  chapters/
    01-analysis-language/
      index.md
      01-01-sets.md
      ...
      01-04-failure-of-infinite-approximation.md
    02-real-numbers/
    ...
    12-equations-iteration/
  javascripts/mathjax.js
  stylesheets/extra.css
overrides/
  main.html
  partials/unit-meta.html
scripts/
  check_content.py
  check_site.py
  migrate_quarto_to_mkdocs.py
src/mathbook_examples/
tests/
mkdocs.yml
requirements.txt
Makefile
```

`content/` 是全部可发布教材的单一来源；`docs/` 只保存课程设计与计划；`src/` 与 `tests/` 是可执行算法的单一来源。`curriculum/*.toml`、`_quarto.yml` 和 Quarto 专用脚本不进入新结构。

## 内容与渲染契约

每个学习单元包含 YAML front matter，至少有 `title`、`unit_id`、`hours`、`difficulty`、`prerequisites`、`capabilities`、`learning_goals` 与 `content_standard`。页面正文继续使用当前八个核心栏目和 `content_standard = 2` 的补充栏目。`check_content.py` 从单元自身验证：

- `unit_id` 与一级标题稳定锚点一致；
- 理论与应用学时非负、各不超过 2、总和不超过 2.25；
- 所有先备类别、能力与目标非空；
- 八个核心栏目完整；自学标准页还有“常见误区与后续”、至少 2 个例题、5 个习题和 7 个折叠答案；
- 站内 Markdown 链接指向已发布的 Markdown 页面。

Material 主题使用 `pymdownx.arithmatex` 加 MathJax、`pymdownx.highlight`、`pymdownx.superfences`、`pymdownx.snippets`、`pymdownx.details` 和 `pymdownx.tabbed`。代码可以从 `src/` 嵌入、带行号和复制按钮；它不在构建页面时执行。

## Material 3 阅读模式

视觉采用浅暖中性色阅读底、深墨正文、靛蓝主色与低饱和语义色；导航使用 Material 的 tab/section 层级，正文保持约 48rem 的最优行长。单元信息、定义、例题、即时检验和答案使用统一的 surface 与圆角，不用营销式渐变或大面积卡片。桌面端保留侧栏与页内目录；窄屏端收起导航，确保公式、长代码和折叠答案可横向处理或自然换行。

## 验收边界

迁移完成时，现有 48 个已注册单元、前言、课程地图与 Python 知识桥均可访问；两项算法测试保持不变；全站 `mkdocs build --strict` 成功；`check_content.py` 和 `check_site.py` 成功；GitHub Actions 不再安装 Quarto 或使用 Deno。第 4 部及之后尚未编写的课程只在课程地图保留章级路线，不创建空的发布页面。
