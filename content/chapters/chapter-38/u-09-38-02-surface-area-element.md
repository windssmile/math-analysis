---
title: 曲面面积元为什么由叉积的模给出？
unit_id: u-09-38-02
hours: {theory: 1.25, applied: 0.25}
difficulty: 4
prerequisites: {book: [u-09-38-01, 局部面积伸缩], higher_algebra: [Gram 行列式], analytic_geometry: [平行四边形面积], python: []}
capabilities: [surface_area_element, local_linearization, area_reparameterization]
learning_goals: [由局部线性化推出面积元, 说明Riemann和的关键估计, 证明重新参数化不变性]
content_standard: 2
---

# 曲面面积元为什么由叉积的模给出？ {#u-09-38-02}

## 先备知识
会用 Fréchet 微分作局部线性化，并会用第 35 章的二维面积伸缩。

## 学习目标
能从参数小矩形的线性像推出面积元，辨明经典 Riemann 证明的假设与误差控制。

## 牵引问题
弯曲曲面没有固定 Jacobian 行列式；为什么两个切向量的叉积恰好承担局部面积倍率？

## 探索与猜想
线性映射 \(L(a,b)=a r_u+b r_v\) 把单位正方形送到由 \(r_u,r_v\) 张成的平行四边形，
其面积是 \(\|r_u\times r_v\|\)。曲面在小尺度上近似这个线性像。

## 概念与理论

### 面积元定理 {#thm-u-09-38-02-area-element}
先设 \(D\) 是闭参数矩形，\(r:D\to\mathbb R^3\) 是一一覆盖其像的 \(C^1\)
正则参数化。取 \(D\) 的**形状正则三角剖分** \(\mathcal T_h\)：最大边长为 \(h\)，
并有与 \(h\) 无关的常数 \(\kappa\)，使每个三角形 \(T\) 的任意两边长之积不超过
\(\kappa\operatorname{area}(T)\)。把 \(T\) 的三个顶点经 \(r\) 映射，再以直线连接，
所得**内接平面三角形**记为 \(P_T\)。定义曲面面积为
\[
\operatorname{Area}(S)
:=\lim_{h\to0}\sum_{T\in\mathcal T_h}\operatorname{area}(P_T),
\]
只要极限存在且与上述剖分族无关。下述证明同时给出存在性、独立性和公式
\[
\operatorname{Area}(S)=\iint_D\|r_u\times r_v\|\,du\,dv,
\qquad dS=\|r_u\times r_v\|\,du\,dv.
\]

### 证明障碍
不能用尚未定义的“曲面小片面积”比较线性像。必须直接比较内接平面三角形面积与
导数线性像面积，并把逐片误差控制成可求和的 \(\operatorname{area}(T)\) 倍数。

### 证明路线
先对每个参数三角形的两条边写 Fréchet 局部线性化；再用叉积的双线性估计比较两个
平面三角形面积。形状正则性把“边长乘积”换成参数三角形面积，求和后误差趋零；
线性像面积和则是连续面积倍率的 Riemann 和。

### 逐步证明
记 \(M=\sup_D\lVert Dr\rVert<\infty\)，并令
\(\omega(h)=\sup_{\lVert x-y\rVert\le h}\lVert Dr(x)-Dr(y)\rVert\to0\)。
对 \(T=[a,a+e_1,a+e_2]\)，沿线段积分或用 Fréchet 微分得两个像边向量
\[
r(a+e_j)-r(a)=Dr(a)e_j+\eta_j,\qquad
\lVert\eta_j\rVert\le\omega(h)\lVert e_j\rVert,\quad j=1,2.
\]
其中 \(\eta_j\) 是线性化余项；这是边向量的关键估计。令 \(A=Dr(a)\)。由叉积的双线性，
\[
\begin{aligned}
&(Ae_1+\eta_1)\times(Ae_2+\eta_2)-Ae_1\times Ae_2\\
&=Ae_1\times\eta_2+\eta_1\times Ae_2+\eta_1\times\eta_2 .
\end{aligned}
\]
再用 \(|\lVert x\rVert-\lVert y\rVert|\le\lVert x-y\rVert\)，单三角形面积差满足
\[
\left|\operatorname{area}(P_T)
-\tfrac12\lVert Ae_1\times Ae_2\rVert\right|
\le \tfrac{\kappa}{2}\bigl(2M+\omega(h)\bigr)\omega(h)
\operatorname{area}(T).
\]
因此常数只依赖形状常数 \(\kappa\)、\(\sup_D\lVert Dr\rVert=M\) 与
\(\omega(h)\)，没有引用待定义的曲面片面积。
也可把右端写成 \(C(\kappa,\sup_D\lVert Dr\rVert,\omega(h))\omega(h)
\operatorname{area}(T)\)。第 35 章的线性面积伸缩给
\[
\tfrac12\lVert Ae_1\times Ae_2\rVert
=\lVert r_u(a)\times r_v(a)\rVert\operatorname{area}(T).
\]
对全部 \(T\) 求和，累计误差至多
\(\frac{\kappa}{2}(2M+\omega(h))\omega(h)\operatorname{area}(D)\to0\)；
右侧线性像面积和是连续函数 \(\lVert r_u\times r_v\rVert\) 的 Riemann 和，故收敛到
所述积分。由于任一形状常数统一有界的剖分族都逼近同一积分，定义的极限与剖分无关。

### 假设位置
\(C^1\) 与紧性给 \(M<\infty\) 和 \(Dr\) 一致连续；形状正则性把
\(\lVert e_1\rVert\lVert e_2\rVert\) 控制为 \(\operatorname{area}(T)\) 的固定倍数；
正则性使面积倍率处处为正；一一覆盖避免同一曲面片被重复计数。

### 边界
有限个参数矩形可逐块三角剖分。一般分片曲面采用有限覆盖：每片内部一一参数化，
不同片只允许在参数边界对应的零面积集合重合，然后逐片相加。若同一开曲面片被有限
多重覆盖，上式按覆盖重数计数而不是几何面积；无限覆盖、退化点、非形状正则剖分或
非 Jordan 可积参数域不在此定理内。

### 迁移
若 \(r\circ\phi\) 是合法参数变换，则链式法则给
\(\|(r\circ\phi)_s\times(r\circ\phi)_t\|=\|r_u\times r_v\|\,|\det D\phi|\)。
参数域换元中的 **Jacobian 的绝对值** 恰好抵消，故面积在重新参数化下不变；
\(\det D\phi\) 的取向符号在取模后消失。

## 例题与迁移

### 例 1：图形曲面 {#ex-u-09-38-02-graph}
\(r(x,y)=(x,y,f(x,y))\)，参数范围 \(D\)。面积元为
\(\sqrt{1+f_x^2+f_y^2}\,dxdy\)，法向可取 \((-f_x,-f_y,1)\)。

### 例 2：球带面积 {#ex-u-09-38-02-sphere}
半径 \(R\) 球面取 \(0\le\theta\le2\pi,\alpha\le\phi\le\beta\)，
\(\|r_\phi\times r_\theta\|=R^2\sin\phi\)，面积为
\(2\pi R^2(\cos\alpha-\cos\beta)\)。

## 即时检验与回望
### 即时检验 1
平面参数化 \(r=(2u,v,0)\) 的面积倍率是多少？
??? note "答案"
    \(\|r_u\times r_v\|=2\)。
### 即时检验 2
反向参数化会改变面积吗？
??? note "答案"
    不会；叉积反向但模不变。

## 常见误区与后续
- 面积元来自局部线性化和 Riemann 极限，不是形式记忆。
- 换元必须带 Jacobian 的绝对值；取向符号不影响无向面积。
- 下一单元以该面积元累积曲面密度。

## 习题与答案
### 习题 1 {#pr-u-09-38-02-01}
求 \(z=0\) 的面积元。
??? note "答案"
    \(dS=dxdy\)。
### 习题 2 {#pr-u-09-38-02-02}
求 \(z=x+y\) 的面积元。
??? note "答案"
    \(dS=\sqrt3\,dxdy\)。
### 习题 3 {#pr-u-09-38-02-03}
求单位圆柱的面积倍率。
??? note "答案"
    为 1。
### 习题 4 {#pr-u-09-38-02-04}
半径 \(R\) 球面的面积元是什么？
??? note "答案"
    \(R^2\sin\phi\,d\phi d\theta\)。
### 习题 5 {#pr-u-09-38-02-05}
为何要限制覆盖次数？
??? note "答案"
    否则参数域积分按覆盖次数重复计面积。
### 习题 6 {#pr-u-09-38-02-06}
正则性在证明中保证什么？
??? note "答案"
    保证局部面积倍率不退化为零。
### 习题 7 {#pr-u-09-38-02-07}
参数交换为何不改面积？
??? note "答案"
    叉积仅反号，其模不变。
### 习题 8 {#pr-u-09-38-02-08}
关键估计中的 \(\omega(h)\) 为何趋零？
??? note "答案"
    因 \(Dr\) 在紧集上一致连续。
### 习题 9 {#pr-u-09-38-02-09}
分片曲面的公共边为何不重复贡献面积？
??? note "答案"
    公共边是二维面积为零的集合。
