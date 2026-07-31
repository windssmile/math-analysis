---
title: 怎样选择并核验 Green、Gauss 与 Stokes 公式？
unit_id: u-09-41-05
hours: {theory: 1.00, applied: 1.00}
difficulty: 5
prerequisites: {book: [u-09-39-04, u-09-40-04, u-09-41-04], higher_algebra: [内积与叉积], analytic_geometry: [定向边界], python: [函数与元组]}
capabilities: [vector_theorem_selection, line_integral_check, flux_integral_check]
learning_goals: [按对象选择三大公式, 核验方向正则性与奇点, 用非证书算法复核解析值]
content_standard: 2
---
# 怎样选择并核验 Green、Gauss 与 Stokes 公式？ {#u-09-41-05}
## 先备知识
掌握 Green、Gauss、Stokes 三条公式的经典证明、积分对象与方向约定。
## 学习目标
能从内部微分算子、定向对象、诱导边界、正则性与奇点五项选择公式并核验结果。
## 牵引问题
三个“内部积分等于边界积分”的公式相似，怎样避免凭关键词误套？
## 探索与猜想
先辨认待转换的是闭曲线、闭曲面还是曲面边界，再检查算子、方向与合法性。
## 概念与理论
### 三大公式对照

| 公式 | 内部微分算子 | 定向对象 | 诱导边界 | 典型等式 |
|---|---|---|---|---|
| Green | \(Q_x-P_y\) 或 \(P_x+Q_y\) | 有向平面区域 | 分支正向边界 | 面积分与闭曲线积分 |
| Gauss | \(\operatorname{div}F\) | 有向三维区域 | 正外法向闭曲面 | 体积分与通量 |
| Stokes | \(\operatorname{curl}F\) | 有向曲面 | 右手规则诱导曲线 | 旋度通量与环流 |

三者都需要相应的正则性、分片结构与方向。奇点若落在所需邻域内，先挖孔并增加边界，
不能把不合法的积分用形式相似遮住。

### 公式选择流程 {#workflow-u-09-41-05-selection}
1. 写出已知与目标积分的维数和类型。
2. 匹配内部微分算子：平面标量旋度或散度、三维散度、三维旋度。
3. 标定向对象，并从它推出诱导边界；Green 逐分支、Gauss 用外法向、Stokes 用右手规则。
4. 检查区域或曲面的有限分片、参数正则性、场的连续偏导和奇点。
5. 先解析变换，再用独立直接积分或数值采样核验符号与算术。

### 取向检查
任何数值比较前先写方向。若反转曲线或法向，相关有向积分应变号；不变往往暴露方向
漏乘，而不是“更稳定”。

### 数值核验：教材唯一调用点
下面从 `src.mathbook_examples.vector_analysis` 导入两个固定复合中点接口，并各调用一次：

```python
import math
from src.mathbook_examples.vector_analysis import composite_midpoint_line_integral, composite_midpoint_flux_integral

line_check = composite_midpoint_line_integral(
    lambda p: (-p[1] / 2, p[0] / 2, 0),
    curve=lambda t: (math.cos(t), math.sin(t), 0),
    curve_derivative=lambda t: (-math.sin(t), math.cos(t), 0),
    bounds=(0, 2 * math.pi), n=64,
)
flux_check = composite_midpoint_flux_integral(
    lambda p: (0, 0, 1),
    surface=lambda u, v: (u, v, 0),
    surface_u=lambda u, v: (1, 0, 0),
    surface_v=lambda u, v: (0, 1, 0),
    u_bounds=(0, 1), v_bounds=(0, 1), nu=16, nv=16,
)
```

第一次是线积分核验，解析值为 \(\pi\)；第二次是通量核验，解析值为 \(1\)。固定采样
只能检查方向、法向量、Jacobian 因子与算术。数值结果不能证明 Green 公式；数值结果
不能证明 Gauss 公式；数值结果不能证明 Stokes 公式。采样也不能证明正则性、参数化无关
或给出误差证书；接口返回值不是经过认证的上下界。
## 例题与迁移
### 例 1：闭曲面通量 {#ex-u-09-41-05-gauss}
求 \(F=(x,y,z)\) 穿出单位球的通量。对象是闭曲面通量，其边界为三维区域，故选 Gauss：
\(\operatorname{div}F=3\)，通量为 \(3\cdot4\pi/3=4\pi\)。球含原点但场在原点正则。
### 例 2：同边界跨曲面 {#ex-u-09-41-05-stokes}
求 \(F=(-y/2,x/2,0)\) 沿上向单位圆盘诱导边界的环流。选 Stokes，旋度为
\((0,0,1)\)，上向通量为 \(\pi\)。若改下向曲面，边界也须反向，答案为 \(-\pi\)。
## 即时检验与回望
### 即时检验 1
闭曲面通量优先匹配哪条公式？
??? note "答案"
    Gauss 公式，并检查正外法向与场在区域邻域的正则性。
### 即时检验 2
曲面边界环流优先匹配哪条公式？
??? note "答案"
    Stokes 公式，并检查曲面法向诱导的边界方向。
### 即时检验 3
数值值与解析值接近能证明参数化无关吗？
??? note "答案"
    不能；有限采样不是参数化无关的证明，也没有自动误差证书。
## 常见误区与后续
- Green 是平面公式；Gauss 的边界对象是闭曲面；Stokes 的边界对象是曲线。
- 三大公式的统一是选择与核验框架，不替代前三章各自的经典证明。
## 习题与答案
### 习题 1 {#pr-u-09-41-05-01}
平面闭路环流可直接选哪条公式？
??? note "答案"
    Green 的切向形式；也可视为平面片上的 Stokes，但仍须检查方向。
### 习题 2 {#pr-u-09-41-05-02}
三维闭曲面通量对应哪个内部算子？
??? note "答案"
    散度 \(\operatorname{div}F\)。
### 习题 3 {#pr-u-09-41-05-03}
曲面边界环流对应哪个内部算子？
??? note "答案"
    旋度 \(\operatorname{curl}F\)。
### 习题 4 {#pr-u-09-41-05-04}
Gauss 的方向合同是什么？
??? note "答案"
    闭曲面取区域的正外法向。
### 习题 5 {#pr-u-09-41-05-05}
Stokes 的方向合同是什么？
??? note "答案"
    边界方向由曲面法向按右手规则诱导。
### 习题 6 {#pr-u-09-41-05-06}
Green 的多连通边界怎样定向？
??? note "答案"
    外边界逆时针、内边界顺时针，使区域在左侧。
### 习题 7 {#pr-u-09-41-05-07}
场在区域内有奇点时怎么办？
??? note "答案"
    先挖去奇点邻域，计入新增边界，再单独分析极限。
### 习题 8 {#pr-u-09-41-05-08}
算法会检查曲面处处正则吗？
??? note "答案"
    不会；它只拒绝采样点上检测到的退化法向。
### 习题 9 {#pr-u-09-41-05-09}
固定网格值能否给误差上界？
??? note "答案"
    不能，接口没有误差证书。
### 习题 10 {#pr-u-09-41-05-10}
为什么解析结果与数值结果应独立获得？
??? note "答案"
    独立路径才能有效暴露方向与算术错误。
### 习题 11 {#pr-u-09-41-05-11}
闭曲面可否直接作为 Stokes 曲面的边界？
??? note "答案"
    闭曲面自身没有曲线边界，Stokes 左侧为零。
### 习题 12 {#pr-u-09-41-05-12}
统一表能否替代定理证明？
??? note "答案"
    不能；它只组织对象、方向、条件和选择流程。
