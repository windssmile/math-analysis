# 数学分析：理论、算法与模型

面向普通高校数学类专业本科生的自学型数学分析数字教材。网站采用 MkDocs Material 的 Material 3 阅读模式；当前发布第一至第三部，共 52 个学习单元。

## 本地运行

需要 Python 3.12：

```bash
python3.12 -m pip install --requirement requirements.txt
mkdocs serve
```

浏览器打开终端显示的本地地址即可预览。

## 质量检查与发布

```bash
make verify
mkdocs build --strict
```

`make verify` 会运行 Python 算法测试、内容结构与稳定锚点检查、MkDocs 严格构建和已生成站点检查。GitHub Pages 工作流使用同一命令并上传 `site/`。

Python 代码只作为可复制的教材示例展示；算法行为由 `src/mathbook_examples/` 与测试验证，不在浏览器中执行。
