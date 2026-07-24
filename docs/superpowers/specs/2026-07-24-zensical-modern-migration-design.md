# Zensical Modern 数学教材站迁移设计

**状态：** 已确认，2026-07-24

## 目标

将数学分析教材的静态站构建驱动从 MkDocs Material 更换为 Zensical，并升级为 Zensical `modern` 原生主题。迁移保留现有 Markdown 正文、稳定锚点、章节 URL、导航语义、MathJax 公式、Python 源码和自动化质量门；不重新编写教材内容，也不保留双构建驱动。

## 已确认的决策

1. 生产构建与预览命令改为 `zensical build --strict` 和 `zensical serve`；`mkdocs` 与 `mkdocs-material` 不再是运行依赖。
2. 继续保留 `mkdocs.yml` 作为 Zensical 兼容配置，不在本次迁移中转换为 `zensical.toml`。
3. 主题使用 `theme.variant: modern`。学习单元元数据卡片继续通过最小 `main.html` block override 呈现；它只使用 Zensical 已声明的 `content` block、`page.meta` 和 MiniJinja 的内置能力，不调用 Python 函数或依赖旧 Material 专有 partial。
4. `content/` 仍是全部可发布教材的唯一来源；`docs/` 只存设计和计划；`src/mathbook_examples/` 与 `tests/` 仍是可执行算法的唯一来源。
5. GitHub Pages 继续在 `main` 推送时执行 `make verify` 并上传 `site/`；不引入 Flutter SDK、Dart、Node.js 或浏览器内 Python。

## 目标架构

```text
content/                   # 发布内容、MathJax 与小范围现代主题 CSS
  chapters/                # 52 个现有学习单元及章节导学
  stylesheets/extra.css    # 仅保留主题无关的阅读增强
mkdocs.yml                 # Zensical 兼容配置、modern 主题和导航
requirements.txt           # 固定 Zensical 运行依赖
Makefile                   # zensical build/serve 与已有检查的统一入口
scripts/check_content.py   # 单元元数据、栏目、锚点和链接检查
scripts/check_site.py      # 构建结果的 URL、锚点、标题和 MathJax 检查
tests/                     # 算法、内容、构建和站点回归检查
```

每页 front matter 保留 `unit_id`、学时、先备、能力和学习目标。`overrides/main.html` 与 `overrides/partials/unit-meta.html` 保持为仅呈现该元数据的最小扩展点；迁移时按 Zensical 的 `main.html`/`content` block 契约验证其 MiniJinja 兼容性。`extra.css` 只处理行长、中文排版、数学/代码溢出和移动端留白，不覆盖主题结构或颜色系统。

## 兼容性与风险控制

Zensical 能读取当前 `mkdocs.yml`、Markdown 前置元数据、导航、Python-Markdown/PyMdown 扩展、额外 CSS/JavaScript 和目录式 URL。构建试验需特别验证：

- `pymdownx.arithmatex` 与现有 MathJax 3 配置能渲染公式；
- `pymdownx.snippets` 继续从 `src/mathbook_examples/` 嵌入已测试的 Python 源码；
- admonition、折叠答案、tabbed 内容和代码高亮在 modern 主题下正常工作；
- `site/` 中的稳定 `u-`、`def-`、`thm-`、`alg-` 锚点、相对链接和目录式 URL 不变；
- 单元信息模板在 MiniJinja 下能渲染，不调用 Python 函数，且 modern 主题中不会出现空白或错位结构。

若某项原 MkDocs 设置不能被 Zensical 接受，只允许用等价的 Zensical 语法替换；不为维持一个非必要视觉效果恢复 MkDocs 双驱动。

## 验收边界

完成后应满足以下条件：

1. `requirements.txt` 不再列出 MkDocs 或 Material，`make build` / `make preview` 不再调用 `mkdocs`。
2. `zensical build --strict` 成功，输出仍在 `site/`，所有 52 个单元、章节导学、首页、前言、课程地图和 Python 知识桥都可发布。
3. 全部算法测试、内容检查、站点链接/锚点检查和更新后的 Zensical 构建测试通过。
4. GitHub Pages 工作流只安装 Zensical 依赖并从 `site/` 上传产物。
5. 站点采用 Zensical modern 原生阅读界面，在桌面和窄屏下保留可读的中文正文、公式、长代码与折叠答案。

本次不承诺更改课程内容、不添加客户端交互应用、不重定向旧 Quarto URL，也不发布 PDF/ePub。
