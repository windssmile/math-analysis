# 教材侧栏层级与编号修正设计

## 背景与问题

当前工程把每个单元 QMD 文件直接列入 Quarto Book 的 `book.chapters`。Quarto 因而把首页、课程地图以及 48 个单元页面都视为同一级的 chapter，并从全书开头连续编号。第二部第一个单元因此显示为第 17 个 chapter，页内二级标题又显示为 `17.1`、`17.2` 等。

这套编号表达的是“渲染页面序号”，不是教材既有的“部—章—单元”课程结构，也使固定教学环节看起来像知识层级。

## 已确认目标

HTML 站点的左侧目录采用三级结构：

1. 部，例如“第二部：数列极限与无限过程”；
2. 章，例如“第 5 章：数列极限与量词结构”；
3. 单元，例如“5.1 数列怎样记录无限过程？”、“5.2 ‘最终任意接近’怎样写成定义？”。

同时满足以下约束：

- 每个单元继续保持独立页面；
- 单元编号以实际阅读顺序为准，在每章内从 1 重新开始；
- 单元页 H1 保留纯标题，不显示 Quarto 自动生成的 chapter 编号；
- “先备知识”“学习目标”“概念与理论”等页内 H2 不编号；
- 首页、前言和课程地图不参与教材章号；
- 正文、锚点、前后页导航和现有内部链接保持有效。

## 采用方案

将当前仅输出 HTML 的 Quarto Book 壳层改为 Quarto Website，关闭 HTML 自动章节编号，并用 Website 原生递归 sidebar 表达三级导航。

采用 Website 是必要的架构修正：Quarto 1.9 的 Book 转换会清空用户提供的 `book.sidebar.contents`，再从 `book.chapters` 重建侧栏；同时 Book schema 不允许在“部”下面继续嵌套“章”分组。Website sidebar 则原生保留递归 `section`。

`project.render` 显式登记 52 个发布页面，负责：

- 渲染页面集合；
- 避免 worktree、Git ignore 或新增草稿影响发布范围；
- 与 sidebar 页面集合形成可校验的一一对应关系。

`website.sidebar.contents` 负责左侧目录、阅读顺序、面包屑和上一页/下一页导航，结构概念如下：

```yaml
project:
  type: website
  render:
    - index.qmd
    - book/part-01/chapter-01/u-01-01-01-sets.qmd
website:
  page-navigation: true
  sidebar:
    contents:
      - index.qmd
      - book/preface.qmd
      - book/curriculum-map.qmd
      - section: "第一部：实数、函数与分析语言"
        contents:
          - section: "第 1 章：集合、逻辑与函数语言"
            contents:
              - text: "1.1 集合怎样组织数学对象？"
                href: book/part-01/chapter-01/u-01-01-01-sets.qmd
```

HTML 格式关闭 `number-sections`，消除 Quarto 自动产生的 `.chapter-number` 和 `.header-section-number`。侧栏中的 `5.1` 等编号是教材导航标签，不再复用 Quarto 的 chapter 计数器。

## 编号与数据来源

章号和章标题以课程纲要中的 12 章基线为准；单元标题和路径以单元注册表为准；同一章内的显示序号以 `_quarto.yml` 当前 Website sidebar 的阅读顺序为准。

这个规则特意区分“单元 ID”与“阅读序号”。例如 `u-02-05-05` 当前位于第五章第三个阅读位置，因此左栏显示 `5.3`，而不是 `5.5`。

sidebar 和 `project.render` 直接维护在 `_quarto.yml` 中，不增加导航生成步骤。新增校验逐项比对 render 列表、侧栏链接和单元注册表，确保路径、标题、章归属和章内次序一致。

Website 不会像原 Book 壳层那样把正文首个 H1 用作 HTML `<title>`，会退回到文件名。`project.post-render` 因此只做一项兼容处理：从 52 个已登记 QMD 的 YAML `title` 或首个 H1 读取页面标题，并替换对应静态 HTML 的 `<title>`。它不改正文 DOM、锚点、sidebar 或编号，并由整站检查逐页验证。

## 页面与导航行为

- 左侧目录默认展示“部”和“章”的可折叠层级，活动单元所在章保持展开；
- 单元链接文本包含 `章号.章内序号`，例如 `5.3`；
- 活动页面的 H1 只显示单元问题标题；
- 页内右侧目录保留 H2/H3 标题，但不显示数字；
- 面包屑反映部、章、单元三层导航；
- 附录保留独立的“附录”分组，不纳入 1–12 章编号。

## 不采用的方案

### CSS 或 JavaScript 改写现有数字

这种方案只能改变视觉文本，不能修正导航、面包屑、无障碍名称和 HTML 语义，而且依赖 Quarto 当前生成的 DOM 结构，升级后容易失效。

### 每章合并成一个长页面

这种方案可以利用 Quarto 原生章节编号，但会取消独立单元页面，违反已确认约束，也会扩大链接迁移范围。

### 为每个单元维护一套独立自动计数器

Lua 或 JavaScript 过滤器可以重写标题，但会把课程结构藏进渲染逻辑。当前需求只要求导航中的章—单元编号和无编号页内标题，显式 sidebar 更容易检查和维护。

## 验证设计

新增或调整自动测试，至少覆盖：

1. sidebar 恰好包含 12 个章分组和注册表中的全部单元；
2. 每个单元在 sidebar 中只出现一次，路径、标题和章归属正确；
3. 每章内显示编号从 `.1` 开始连续递增，并与 Website sidebar 阅读顺序一致；
4. 首页、前言、课程地图和附录不占用 1–12 的章号；
5. `project.render` 与 sidebar 中的 52 个页面完全一致；
6. 渲染后的单元页面不含自动 `.chapter-number`；
7. 渲染后的 H2/H3 目录项不含 `.header-section-number`；
8. 代表页面的渲染 HTML 含有部、章、单元和 `depth2` 导航标记；
9. 52 个渲染页面的 HTML `<title>` 与各自 QMD 标题一致，不退化为文件名；
10. `make verify` 的纲要、注册表、Quarto 全站渲染、内部链接和必需锚点检查全部通过。

还应进行一次浏览器人工检查，至少抽查第一部第 1 章、第二部第 5 章、第三部第 12 章和附录，确认折叠层级、活动项、长中文标题换行以及窄屏侧栏表现正常。

## 修改范围

修改范围限定为：

- `_quarto.yml` 的 HTML 编号和 sidebar 配置；
- `scripts/check_site.py` 的导航产物校验和小型 HTML 页面标题兼容脚本；
- 对应的自动测试，包括原有章节顺序测试的 Website 路径解析。

不增加导航生成脚本，不修改 `styles.css`、单元正文、课程学时、章节依赖关系、知识锚点或 Python 示例。
