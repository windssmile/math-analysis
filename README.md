# 数学分析：理论、算法与模型

面向普通高校数学类专业本科生的自学型数学分析数字教材。网站采用 Zensical modern
的 Material 3 阅读模式；当前发布至第八部第 36 章，共 165 个学习单元、305 学时。
第六部（第 23–27 章）已经完整发布；第七部（第 28–32 章）已经完整发布。第八部已发布
第 33–36 章，包含 18 个核心单元、32 学时。第七部闭合时共 147 个学习单元；
第六部第 27 章，共 122 个学习单元，是第六部闭合时的里程碑。第七部已经完整发布，
共 25 个核心单元、44 学时。第八部另有一篇不计入核心学时的 Jordan 内容选读附录。

## 本地运行

需要 Python 3.12：

```bash
python3.12 -m pip install --requirement requirements.txt
zensical serve
```

浏览器打开终端显示的本地地址即可预览。

## 质量检查与发布

```bash
make verify
zensical build --strict
```

`make verify` 会运行 Python 算法测试、内容结构与稳定锚点检查、Zensical 严格构建和
已生成站点检查。GitHub Pages 工作流使用同一命令并上传 `site/`。

Python 代码只作为可复制的教材示例展示；算法行为由 `src/mathbook_examples/` 与测试验证，不在浏览器中执行。
