# 第 41 章一致性审查

## 范围

审查第 41 章五个单元的元数据、证明、取向、练习答案、出版表面和数值证书边界。

## 内容结论

- 元数据：5 个单元均为 `content_standard: 2`，合计理论 6、应用 2 学时。
- Stokes 主线：小矩形旋度推导含余项；单参数片证明显式完成拉回、链式法则与 Green 归约。
- 规格复审：41.1 的 display math 已禁止嵌套行内定界符；41.3 已逐项展开
  `B_u-A_v`，显式核对混合偏导抵消、六个交叉项及旋度与叉积的对应。
- 取向：参数域正边界、右手规则和“曲面在左侧”严格对照，多边界分支逐支说明。
- 有限分片：只覆盖有限兼容正则参数片，内部接缝相反方向抵消，奇点需挖孔。
- 算法唯一调用点：41.5 对线积分与通量接口各调用一次，并明确数值结果不是证明或误差证书。

## 出版与可见性

- README、课程地图、依赖图谱和导航统一到第 41 章；第 42 章无正文。
- 严格构建后的 41.1 代表 HTML 含 43 个 arithmatex 节点且无 MathJax 错误或嵌套
  display 定界，41.3 含 59 个、41.5 含 15 个；应用内 Chromium 以 390 × 844
  移动视口实测三页均为 `scrollWidth = clientWidth = 390`，
  无页面级横向溢出。Playwright CLI 因本机 root-owned npm 缓存报 `EPERM`，故依照
  安全边界改用浏览器连接器，没有修改用户缓存权限。

## 绿门证据

- `python3.12 -m unittest tests.test_chapter_41`：通过。
- `make verify`：通过。
- `python3.12 scripts/check_content.py`：通过。
- `zensical build --strict`：通过。
- `python3.12 scripts/check_site.py`：通过。
- `git diff --check`：通过。
