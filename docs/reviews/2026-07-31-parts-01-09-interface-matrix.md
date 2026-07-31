# 第一至第九部章节接口矩阵

**审查口径：** 本表以 `content/course-map.md`、41 个章节 `index.md`、全部单元 front matter 的
`prerequisites.book`、`docs/curriculum` 的依赖图以及各部设计/一致性审查为证据。每章只有一个
主责；“直接前置”保留可由 front matter 机器复核的关键见证，不等同于穷举所有页内回引。

第一部没有独立的 `docs/curriculum/part-01-dependencies.md`。第 1–4 章据
`docs/superpowers/specs/2026-07-19-part-01-foundation-blueprint-design.md`，并以四章 guide 与 14 个
单元 front matter 交叉核对。第二至第九部优先采用对应 curriculum 依赖图，再以 guide、front
matter、part design/review 校验。附录不作为任何核心章节或单元的前置。

## 权威章级接口

| 章 | 部 | 唯一责任 | 直接前置（规范章 ID） | 背景接口 | 向后输出与主要消费者 | 禁止前借/范围边界 | 关键术语/记号 | 证据 |
|---:|---:|---|---|---|---|---|---|---|
| 1 | I | 建立集合、量词、证明与函数语言 | 无 | `bg-algebra`、`bg-geometry` | 数学陈述与映射语言 → 第 2–41 章 | 不发展公理集合论、模型论或形式逻辑 | $\in,\subseteq,\forall,\exists,f:A\to B$ | `content/chapters/chapter-01/index.md`；`docs/superpowers/specs/2026-07-19-part-01-foundation-blueprint-design.md` |
| 2 | I | 由 Dedekind 分割建立完备实数 | `ch-01` | `bg-algebra` | 实数系与完备性公理 → 第 3、5、7 章 | 不提前讨论 Cauchy 列；不从 Peano 公理构造数系 | $\mathbb Q,\mathbb R$，Dedekind 分割 | `content/chapters/chapter-02/index.md`；`docs/superpowers/specs/2026-07-19-part-01-foundation-blueprint-design.md` |
| 3 | I | 建立界、确界原理及其直接推论 | `ch-02` | `bg-algebra` | 完备性/确界 → 第 5、7、19、25、28 章 | 不系统讲数列极限、连续性或积分 | 上界、下界、$\sup$、$\inf$、Archimedean 性 | `content/chapters/chapter-03/index.md`；`docs/superpowers/specs/2026-07-19-part-01-foundation-blueprint-design.md` |
| 4 | I | 用递推与区间套形成无限逼近和误差预理解 | `ch-03` | `bg-algebra`、`bg-python` | 递推、区间套、二分误差 → 第 5、7、12 章 | 不借介值定理；不系统展开 epsilon-N 理论 | 递推、不变量、区间长度、误差预算 | `content/chapters/chapter-04/index.md`；`docs/superpowers/specs/2026-07-19-part-01-foundation-blueprint-design.md` |
| 5 | II | 定义数列极限并固定 epsilon-N 量词结构 | `ch-03`、`ch-04` | `bg-algebra`、`bg-python` | 数列收敛语言 → 第 6–9、23、25 章 | 不把数值稳定误当数学收敛 | $(a_n)$、$a_n\to L$、$\varepsilon$-$N$ | `content/chapters/chapter-05/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 6 | II | 建立极限代数、序与夹逼法则 | `ch-05` | `bg-algebra`、`bg-python` | 极限运算 → 第 8、9、19、23 章 | 不无条件交换极限与运算 | 和积商极限、保序、夹逼 | `content/chapters/chapter-06/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 7 | II | 从第 3 章完备性推出单调收敛与区间套 | `ch-03`、`ch-05` | `bg-algebra`、`bg-geometry`、`bg-python` | 单调收敛/区间套 → 第 8、11、12 章 | 不用后置紧致性或介值定理倒证 | 单调有界、区间套、完备性 | `content/chapters/chapter-07/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 8 | II | 建立子列、Bolzano–Weierstrass、Cauchy 与上下极限 | `ch-03`、`ch-05`、`ch-06`、`ch-07` | `bg-algebra`、`bg-geometry`、`bg-python` | BW/Cauchy/压缩证书 → 第 11、12、26、28、31 章 | 不借函数连续性；收敛实验不是证书 | 子列、Cauchy、$\limsup$、$\liminf$、压缩 | `content/chapters/chapter-08/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 9 | III | 建立函数极限的局部、单侧、无穷与序列刻画 | `ch-01`、`ch-03`、`ch-05`、`ch-06` | `bg-algebra`、`bg-geometry` | 函数极限 → 第 10、13 章 | 不前借连续性或导数 | 邻域、$\varepsilon$-$\delta$、单侧极限 | `content/chapters/chapter-09/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 10 | III | 建立连续性及其运算、复合与延拓 | `ch-09` | `bg-algebra`、`bg-geometry` | 连续性 → 第 11、12、15、19、25、28 章 | 不前借闭区间整体定理 | 连续、单侧连续、间断、复合 | `content/chapters/chapter-10/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 11 | III | 证明闭区间上紧致、最值与一致连续 | `ch-08`、`ch-10` | `bg-algebra`、`bg-geometry` | 闭区间整体性质 → 第 12、15、19、28 章 | 不把开覆盖紧致性扩成核心；不提前微分 | 序列紧致、EVT、Heine–Cantor | `content/chapters/chapter-11/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 12 | III | 区分存在、区间与压缩三类求根证书 | `ch-07`、`ch-08`、`ch-10` | `bg-algebra`、`bg-geometry`、`bg-python` | IVT、二分、压缩比较 → 第 17、31 章 | 不借导数/Newton；存在不推出迭代收敛 | IVT、不动点、二分、误差证书 | `content/chapters/chapter-12/index.md`；`docs/curriculum/parts-02-03-dependencies.md` |
| 13 | IV | 以极限定义导数并建立局部线性化 | `ch-09`、`ch-10` | `bg-algebra`、`bg-geometry`、`bg-python` | 一元微分 → 第 14–18、29 章 | 不用导数法则反证定义 | 差商、导数、微分、$o(h)$ | `content/chapters/chapter-13/index.md`；`docs/curriculum/part-04-dependencies.md` |
| 14 | IV | 建立代数/链式/反函数求导与高阶导数 | `ch-10`、`ch-13` | `bg-algebra`、`bg-geometry`、`bg-python` | 求导工具 → 第 15–18、29–31 章 | 只处理一元有限阶；不前借隐函数定理 | 链式法则、反函数导数、高阶导数 | `content/chapters/chapter-14/index.md`；`docs/curriculum/part-04-dependencies.md` |
| 15 | IV | 用闭区间整体性质证明微分中值定理链 | `ch-11`、`ch-13`、`ch-14` | `bg-algebra`、`bg-geometry`、`bg-python` | MVT/单调性/L’Hôpital → 第 16–19、30 章 | 不把数值图像当中值定理证明 | Fermat、Rolle、Lagrange、Cauchy MVT | `content/chapters/chapter-15/index.md`；`docs/curriculum/part-04-dependencies.md` |
| 16 | IV | 建立有限阶 Taylor 公式与可计算余项 | `ch-13`、`ch-14`、`ch-15` | `bg-algebra`、`bg-geometry`、`bg-python` | Taylor 与余项 → 第 17、22、26、30 章 | 不引入无穷级数或多元 Taylor | Peano、Lagrange/Cauchy 余项、Horner | `content/chapters/chapter-16/index.md`；`docs/curriculum/part-04-dependencies.md` |
| 17 | IV | 用导数研究形态、凸性、优化与保护 Newton | `ch-12`、`ch-14`、`ch-15`、`ch-16` | `bg-algebra`、`bg-geometry`、`bg-python` | 一元优化/求根诊断 → 第 18、31、32 章 | 不引入积分型余项、级数、多元/KKT | 凸性、极值、Newton、停止状态 | `content/chapters/chapter-17/index.md`；`docs/curriculum/part-04-dependencies.md` |
| 18 | V | 从求导反向建立原函数与积分方法 | `ch-14`、`ch-15`、`ch-17` | `bg-algebra`、`bg-geometry`、`bg-python` | 原函数/换元/分部积分 → 第 20–22 章 | 不使用 Riemann 积分或微积分基本定理 | 原函数、换元、分部积分、部分分式 | `content/chapters/chapter-18/index.md`；`docs/curriculum/part-05-dependencies.md` |
| 19 | V | 以 Darboux/Riemann 体系定义积分与可积性 | `ch-03`、`ch-05`、`ch-06`、`ch-10`、`ch-11` | `bg-algebra`、`bg-geometry`、`bg-python` | 一元 Riemann 积分 → 第 20、22、33、34、37 章 | 不借基本定理定义积分；有限采样不证可积 | 分割、上下和、Riemann 和、可积 | `content/chapters/chapter-19/index.md`；`docs/curriculum/part-05-dependencies.md` |
| 20 | V | 证明微积分基本定理并合法化定积分计算 | `ch-10`、`ch-13`、`ch-18`、`ch-19` | `bg-algebra`、`bg-geometry`、`bg-python` | FTC/Newton–Leibniz → 第 21、22、34、39、40 章 | 不把数值求积当基本定理证明 | 变上限积分、FTC、Newton–Leibniz | `content/chapters/chapter-20/index.md`；`docs/curriculum/part-05-dependencies.md` |
| 21 | V | 用积分建立面积、体积、弧长与物理模型 | `ch-14`、`ch-19`、`ch-20` | `bg-algebra`、`bg-geometry`、`bg-python` | 一元累积建模 → 第 33、36–38 章 | 模型须先说明局部贡献与变量；不扩到重积分 | 面积、截面、弧长、功、质量、平均值 | `content/chapters/chapter-21/index.md`；`docs/curriculum/part-05-dependencies.md` |
| 22 | V | 建立反常积分与带证书的数值求积 | `ch-05`、`ch-06`、`ch-15`、`ch-16`、`ch-19`、`ch-20` | `bg-algebra`、`bg-geometry`、`bg-python` | 尾部界/求积误差 → 第 23、26、36 章 | 网格误差不是统一证书；不提前级数理论 | 反常积分、比较、Simpson、误差预算 | `content/chapters/chapter-22/index.md`；`docs/curriculum/part-05-dependencies.md` |
| 23 | VI | 建立数项级数、Cauchy 尾部与正项判别 | `ch-05`、`ch-06`、`ch-08`、`ch-19` | `bg-algebra`、`bg-geometry`、`bg-python` | 数项级数基础 → 第 24–26 章 | 只处理正项判别及共有语言，不用符号抵消 | 部分和、尾部、比较/比值/根值判别 | `content/chapters/chapter-23/index.md`；`docs/curriculum/part-06-dependencies.md` |
| 24 | VI | 处理一般项级数、绝对/条件收敛、重排与乘积 | `ch-23` | `bg-algebra`、`bg-geometry`、`bg-python` | 一般项级数工具 → 第 25、26 章 | 不把条件收敛当绝对收敛；有限截断不证重排合法 | 绝对/条件收敛、Leibniz、Dirichlet、Cauchy 积 | `content/chapters/chapter-24/index.md`；`docs/curriculum/part-06-dependencies.md` |
| 25 | VI | 定义函数列/函数项级数的一致收敛并给出保性质条件 | `ch-03`、`ch-05`、`ch-10`、`ch-11`、`ch-19`、`ch-20`、`ch-24` | `bg-algebra`、`bg-geometry`、`bg-python` | 一致控制 → 第 26、27 章 | 不反向依赖第 26 或第 27 章；逐点收敛不保连续/积分/微分 | 逐点/一致收敛、统一 Cauchy、M 判别、sup 范数 | `content/chapters/chapter-25/index.md`；`docs/curriculum/part-06-dependencies.md` |
| 26 | VI | 建立幂级数收敛半径与解析表示 | `ch-08`、`ch-16`、`ch-24`、`ch-25` | `bg-algebra`、`bg-geometry`、`bg-python` | 幂级数与解析工具 → 第 27 章及后续函数逼近 | 端点须另判；光滑不等于解析 | 收敛半径、Cauchy–Hadamard、逐项微积分 | `content/chapters/chapter-26/index.md`；`docs/curriculum/part-06-dependencies.md` |
| 27 | VI | 证明多项式逼近并输出显式误差控制 | `ch-10`、`ch-11`、`ch-25` | `bg-algebra`、`bg-geometry`、`bg-python` | Bernstein/多项式逼近 → 后续数值分析 | 网格最大误差不等于一致误差证书；缺正则常数应 uncertified | Bernstein、多项式逼近、模连续性、误差上界 | `content/chapters/chapter-27/index.md`；`docs/curriculum/part-06-dependencies.md` |
| 28 | VII | 建立有限维 Euclid 空间的拓扑、完备、紧致与连续 | `ch-03`、`ch-05`、`ch-08`、`ch-09`、`ch-10`、`ch-11` | `bg-algebra`、`bg-geometry` | 多元空间基础 → 第 29、32–35 章 | 只限有限维；不发展一般拓扑/泛函分析 | 范数、开闭集、完备、Heine–Borel | `content/chapters/chapter-28/index.md`；`docs/curriculum/part-07-dependencies.md` |
| 29 | VII | 以 Fréchet 微分统一偏导、方向导数与 Jacobian | `ch-13`、`ch-14`、`ch-28` | `bg-algebra`、`bg-geometry`、`bg-python` | Fréchet/Jacobian → 第 31、35、38 章 | 偏导存在不推出可微；数值差分不证可微 | $Df(a)$、梯度、Jacobian、条件数 | `content/chapters/chapter-29/index.md`；`docs/curriculum/part-07-dependencies.md` |
| 30 | VII | 建立高阶 Fréchet 微分与多元 Taylor | `ch-14`、`ch-16`、`ch-29` | `bg-algebra`、`bg-geometry` | Hessian/Taylor → 第 31、32 章 | 不把二次模型当全局误差或最优性证书 | $D^2f$、Hessian、多重线性、Taylor | `content/chapters/chapter-30/index.md`；`docs/curriculum/part-07-dependencies.md` |
| 31 | VII | 证明反函数/隐函数定理并建立局部求解 | `ch-08`、`ch-12`、`ch-14`、`ch-17`、`ch-29`、`ch-30` | `bg-algebra`、`bg-geometry`、`bg-python` | 局部可逆/参数化 → 第 32、35、38 章 | 结论局部而非全局；残差小不自动证明存在唯一 | IFT、隐函数、局部参数化、Newton–Kantorovich 边界 | `content/chapters/chapter-31/index.md`；`docs/curriculum/part-07-dependencies.md` |
| 32 | VII | 建立多元极值、Lagrange 乘子与优化核验 | `ch-11`、`ch-15`、`ch-17`、`ch-28`、`ch-29`、`ch-30`、`ch-31` | `bg-algebra`、`bg-geometry`、`bg-python` | 多元优化语言 → 后续应用 | 不发展一般不等式约束或 KKT；收敛状态非最优性证书 | 临界点、Hessian、Lagrange 乘子、约束资格 | `content/chapters/chapter-32/index.md`；`docs/curriculum/part-07-dependencies.md` |
| 33 | VIII | 定义 Riemann 重积分并证明基本可积性 | `ch-03`、`ch-05`、`ch-10`、`ch-11`、`ch-19`、`ch-28` | `bg-geometry` | 重积分 → 第 34–41 章 | 不以 Jordan/Lebesgue 为前置；不借累次积分定义 | 矩形分割、振幅、重积分、零边界 | `content/chapters/chapter-33/index.md`；`docs/curriculum/part-08-dependencies.md` |
| 34 | VIII | 证明累次积分并建立区域描述与换序计算 | `ch-19`、`ch-20`、`ch-33` | `bg-geometry`、`bg-python` | 累次积分/区域分片 → 第 35–41 章 | 换序前先合法化区域与可积性 | Fubini 型经典定理、I/II 型区域、换序 | `content/chapters/chapter-34/index.md`；`docs/curriculum/part-08-dependencies.md` |
| 35 | VIII | 从 Fréchet/Jacobian 建立重积分变量代换 | `ch-29`、`ch-31`、`ch-33`、`ch-34` | `bg-algebra`、`bg-geometry` | Jacobian 面积/体积伸缩 → 第 36–41 章，尤其第 38 章 | 仅处理一一、$C^1$、非退化及有限分片情形 | 绝对 Jacobian 行列式、极/柱/球坐标、变量代换 | `content/chapters/chapter-35/index.md`；`docs/curriculum/part-08-dependencies.md` |
| 36 | VIII | 处理反常重积分及质量/概率模型 | `ch-21`、`ch-22`、`ch-33`、`ch-34`、`ch-35` | `bg-geometry`、`bg-python` | 无界/奇点积分经验 → 第 40 章 | 不把截断数值当收敛证明；不前借向量分析公式 | 截断、奇点、质量、概率密度 | `content/chapters/chapter-36/index.md`；`docs/curriculum/part-08-dependencies.md` |
| 37 | IX | 定义参数曲线、弧长及两类曲线积分 | `ch-19`、`ch-29` | `bg-algebra`、`bg-geometry` | 曲线、功、环流 → 第 39–41 章 | 先定义再应用；重参数化必须检查方向 | 正则曲线、弧长、$ds$、$\int_C F\cdot dr$ | `content/chapters/chapter-37/index.md`；`docs/curriculum/part-09-dependencies.md` |
| 38 | IX | 定义参数曲面、面积元及两类曲面积分 | `ch-29`、`ch-31`、`ch-33`、`ch-34`、`ch-35` | `bg-algebra`、`bg-geometry` | 曲面取向/通量 → 第 39–41 章 | 不引入测度论曲面积分；不可忽略正则性与取向 | $r_u\times r_v$、$dS$、法向、通量 | `content/chapters/chapter-38/index.md`；`docs/curriculum/part-09-dependencies.md` |
| 39 | IX | 从平面场与曲线积分证明 Green 公式 | `ch-20`、`ch-29`、`ch-34`、`ch-37` | `bg-algebra`、`bg-geometry` | Green/平面路径无关 → 第 41 章 | 先简单区域后分片/多连通；内部边界方向须抵消 | 平面散度、标量旋度、Green、正向边界 | `content/chapters/chapter-39/index.md`；`docs/curriculum/part-09-dependencies.md` |
| 40 | IX | 从通量与重积分证明 Gauss 公式 | `ch-20`、`ch-34`、`ch-36`、`ch-38`、`ch-39` | `bg-algebra`、`bg-geometry` | 三维散度/通量 → 第 41 章统一比较 | 不依赖第 41 章；先长方体后有限分片；奇点须挖除 | $\nabla\cdot F$、Gauss、外法向、通量 | `content/chapters/chapter-40/index.md`；`docs/curriculum/part-09-dependencies.md` |
| 41 | IX | 证明 Stokes 并统一 Green/Gauss/Stokes 的选择与核验 | `ch-29`、`ch-37`、`ch-38`、`ch-39`、`ch-40` | `bg-algebra`、`bg-geometry`、`bg-python` | 定向边界与经典三大公式 → 后续物理/几何 | 不发展流形、微分形式、同调；统一不替代三定理各自证明 | $\nabla\times F$、Stokes、右手规则、诱导边界 | `content/chapters/chapter-41/index.md`；`docs/curriculum/part-09-dependencies.md` |

## 锁定的跨部接口

- 第 3 章的完备性/确界输出进入第 5、7 章；第 11 章闭区间整体性质进入第 12、15、19、28 章。
- 第 19 章 Riemann 积分进入第 20、22、33 章；第 25 章一致收敛进入第 26、27 章，且不反向依赖二者。
- 第 29 章 Fréchet/Jacobian 直接进入第 31、35、38 章。第 33–35 章的积分/区域工具向后
  支撑第 38–41 章，但第 37 章只直接取第 19、29 章；其余属于间接输出而非直接前置。
- 第 37 章直接进入第 39、41 章，第 38 章直接进入第 40、41 章；第 39 章不直接依赖
  第 38 章，而取第 20、29、34、37 章；第 39 章进入第 41 章，第 40 章不依赖第 41 章。

## 审查结论与方法

1. 已修复当前出版口径矛盾：逐部合同与物理核心页均为
   **14+21+20+21+25+24+25+18+21=189 个学习单元**，front matter 学时合计 **337**；
   README、课程地图、第九部依赖/审查和当前总量测试现统一为 **189/337**。
   历史累计口径也已纠正：前六部逐部相加为
   **14+21+20+21+25+24=125**，与第六部闭合提交快照 `8b0225f` 一致；再加第七部
   25 个单元得到 **150**，与第七部闭合提交快照 `af50860` 一致。README、课程地图、
   第六/七部依赖、设计回填、审查及测试现统一锁定 **125/150**。
2. 一些 front matter 的 `prerequisites.book` 使用概念名，一些使用 `chapter-*` 或 `u-*`，且少数
   章内单元会把本章概念名写作前置。本矩阵用逐章 witness registry 锁定关键声明，暂不把命名
   风格差异判为依赖错误。
3. 选读附录在第八、九部之后发布，但依赖文档明确它们不进入核心学时、核心考核或后续前置；
   本表据此只记录边界，不将附录提升为章级接口。
4. `content/course-map.md` 已补齐第 24–27 章，并把此前只列章标题的第 1–9 章补到单元级；
   现在 41 个 guide、189 个物理核心页、课程地图与 `mkdocs.yml` 的单元链接逐章同序一致。
5. 直接前置先汇总各章全部 `prerequisites.book`，再与 dependency 文档逐单元依赖交叉；
   `chapter-*` 与 `u-*` 解析为所属章，定理/概念泛称映射到首次主责章（例如“Riemann
   积分”→`ch-19`）。只保留证明或定义实际调用的必要输入；纯阅读顺序、后续消费者及
   高等代数/解析几何/Python 要求分别移到输出或“背景接口”。测试中的
   `DIRECT_PREREQUISITES` 对 41 章规范 ID 做双向相等，`CHAPTER_CONTRACT` 另锁原始
   front matter witness，避免用整段自然语言全等造成脆弱测试。
