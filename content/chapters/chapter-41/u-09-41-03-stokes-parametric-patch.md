---
title: Stokes 公式怎样在单个参数曲面片上证明？
unit_id: u-09-41-03
hours: {theory: 1.25, applied: 0.25}
difficulty: 5
prerequisites: {book: [u-09-39-02, u-09-41-01, u-09-41-02], higher_algebra: [叉积], analytic_geometry: [正则参数片], python: []}
capabilities: [stokes_patch, pullback_calculation, green_reduction]
learning_goals: [陈述参数片Stokes公式, 展开线积分拉回, 用链式法则和Green公式完成证明]
content_standard: 2
---
# Stokes 公式怎样在单个参数曲面片上证明？ {#u-09-41-03}
## 先备知识
掌握 Green 公式、三维旋度、参数曲面面积向量与诱导边界方向。
## 学习目标
能把曲面边界线积分拉回参数域，逐项识别旋度与叉积，并指出每条假设的位置。
## 牵引问题
为什么空间曲线上的环流，会等于跨越它的曲面上旋度通量？
## 探索与猜想
若把空间线积分写成参数域边界上的二维一形式，Green 公式应把它变成二重积分。
## 概念与理论
### 单参数片上的 Stokes 公式 {#thm-u-09-41-03-stokes-patch}
设 \(D\subset\mathbb R^2\) 是有界简单区域，具有分片光滑边界；\(r\in C^2\) 在
\(D\) 的邻域定义、一一且正则，\(S=r(D)\) 取 \(r_u\times r_v\) 方向，边界取诱导
方向。设 \(F=(P,Q,R)\in C^1(U)\)，其中 \(U\) 是 \(S\) 的邻域。则

\[
\oint_{\partial S}F\cdot dr
=\iint_D\operatorname{curl}F(r(u,v))\cdot(r_u\times r_v)\,du\,dv.
\]

### 证明障碍
左侧沿空间边界积分，Green 公式却只作用于参数域；还必须精确核对链式法则的九项。
### 证明路线
先做拉回计算，把 \(F(r)\cdot dr\) 写成参数域上的 \(A\,du+B\,dv\)，再应用 Green
公式，最后识别叉积。
### 逐步证明
沿参数域曲线有 \(dr=r_u\,du+r_v\,dv\)，因此

\[
F(r)\cdot dr=F(r)\cdot r_u\,du+F(r)\cdot r_v\,dv=A\,du+B\,dv.
\]

诱导边界方向保证 \(\partial D\) 的正向映到 \(\partial S\) 的正向。Green 公式给出

\[
\oint_{\partial S}F\cdot dr=\oint_{\partial D}A\,du+B\,dv
=\iint_D(B_u-A_v)\,du\,dv.
\]

为避免把链式法则藏在记号里，写
\(r=(x,y,z)\)、\(F=(P,Q,R)\)。于是

\[
\begin{aligned}
A&=P(r)x_u+Q(r)y_u+R(r)z_u,\\
B&=P(r)x_v+Q(r)y_v+R(r)z_v.
\end{aligned}
\]

把 \(DF(r)\) 看作 \(F\) 的 Jacobian，乘积法则与链式法则逐项给出

\[
\begin{aligned}
B_u&=r_v\cdot DF(r)r_u+F(r)\cdot r_{vu},\\
A_v&=r_u\cdot DF(r)r_v+F(r)\cdot r_{uv}.
\end{aligned}
\]

因此

\[
B_u-A_v
=r_v\cdot DF(r)r_u-r_u\cdot DF(r)r_v
+F(r)\cdot(r_{vu}-r_{uv}).
\]

因为 \(r\in C^2\)，三个坐标函数的混合偏导都相等，即
\(r_{vu}=r_{uv}\)，所以

\[
F(r)\cdot(r_{vu}-r_{uv})=0.
\]

现在把剩余项完全展开。对角项 \(P_xx_ux_v\)、\(Q_yy_uy_v\)、
\(R_zz_uz_v\) 两两抵消，留下严格的六项排列：

\[
\begin{aligned}
B_u-A_v={}&P_y(y_u x_v-y_v x_u)
+P_z(z_u x_v-z_v x_u)\\
&+Q_x(x_u y_v-x_v y_u)
+Q_z(z_u y_v-z_v y_u)\\
&+R_x(x_u z_v-x_v z_u)
+R_y(y_u z_v-y_v z_u).
\end{aligned}
\]

按偏导差分组，恰为

\[
\begin{aligned}
B_u-A_v={}&(R_y-Q_z)(y_u z_v-z_u y_v)\\
&+(P_z-R_x)(z_u x_v-x_u z_v)\\
&+(Q_x-P_y)(x_u y_v-y_u x_v)\\
=&\operatorname{curl}F(r)\cdot(r_u\times r_v).
\end{aligned}
\]

代回即得结论。
### 假设位置
\(F\in C^1\) 保证 \(DF\) 存在且连续，使上述复合函数链式法则和 Green 公式合法；
\(r\in C^2\) 保证 \(r_u,r_v\) 可再微分并由混合偏导定理得到 \(r_{vu}=r_{uv}\)；
正则性
保证面积向量不退化；一一性避免参数域重复覆盖；分片光滑边界使 Green 与线积分合法。
### 边界
本证明只覆盖上述单个参数片。非一一覆盖、退化点、奇点或多片接缝不能被这一步隐藏。
### 取向检查
若取 \(-(r_u\times r_v)\)，必须同时反转 \(\partial S\)；两侧一起变号，等式保留。
### 迁移
下一页只对有限个满足兼容条件的正则参数片求和。
## 例题与迁移
### 例 1：上向平面圆盘 {#ex-u-09-41-03-disk}
取 \(F=(-y/2,x/2,0)\)，旋度为 \((0,0,1)\)。上向单位圆盘右侧为 \(\pi\)，其边界
从上看逆时针，左侧也为 \(\pi\)。
### 例 2：倾斜图形片 {#ex-u-09-41-03-graph}
\(r(u,v)=(u,v,u+v)\) 有 \(r_u\times r_v=(-1,-1,1)\)。若
\(F=(0,0,u-v)\)（即空间中 \(F=(0,0,x-y)\)），则旋度为 \((-1,-1,0)\)，点乘面积
向量得 \(2\)；单位方形参数域给出通量 \(2\)，边界逐边积分同样为 \(2\)。
## 即时检验与回望
### 即时检验 1
拉回后的 \(A,B\) 分别是什么？
??? note "答案"
    \(A=F(r)\cdot r_u\)，\(B=F(r)\cdot r_v\)。
### 即时检验 2
为什么需要边界诱导方向？
??? note "答案"
    它保证参数域 Green 公式的正边界映到曲面边界的正向。
## 常见误区与后续
- 不能省略复合函数链式法则，也不能把结论当作叉积恒等式直接背诵。
- 单参数片证明没有自动处理接缝和奇点。
## 习题与答案
### 习题 1 {#pr-u-09-41-03-01}
写出 Stokes 公式左侧对象。
??? note "答案"
    诱导方向边界上的第二类曲线积分 \(\oint_{\partial S}F\cdot dr\)。
### 习题 2 {#pr-u-09-41-03-02}
写出右侧面积向量。
??? note "答案"
    \((r_u\times r_v)\,du\,dv\)。
### 习题 3 {#pr-u-09-41-03-03}
Green 公式作用在哪个区域？
??? note "答案"
    参数域 \(D\)。
### 习题 4 {#pr-u-09-41-03-04}
哪个条件使混合偏导相消？
??? note "答案"
    \(r\in C^2\)。
### 习题 5 {#pr-u-09-41-03-05}
哪个条件排除退化面积向量？
??? note "答案"
    参数片正则，即 \(r_u\times r_v\ne0\)。
### 习题 6 {#pr-u-09-41-03-06}
反转曲面取向但不反转边界会怎样？
??? note "答案"
    右侧变号而左侧不变，方向不相容。
### 习题 7 {#pr-u-09-41-03-07}
常向量场的旋度通量是多少？
??? note "答案"
    零。
### 习题 8 {#pr-u-09-41-03-08}
势场能否产生非零闭路环流？
??? note "答案"
    在势函数沿曲线定义的条件下不能，闭路积分为零。
### 习题 9 {#pr-u-09-41-03-09}
参数域有孔时应检查什么？
??? note "答案"
    每个边界分支的正向，尤其内边界应反向。
### 习题 10 {#pr-u-09-41-03-10}
单片证明能否跨过场的奇点？
??? note "答案"
    不能；场必须在曲面邻域中为 \(C^1\)。
