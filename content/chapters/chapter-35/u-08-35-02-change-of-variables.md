---
title: 重积分换元公式需要哪些条件？
unit_id: u-08-35-02
hours: {theory: 1.5, applied: 0.25}
difficulty: 4
prerequisites: {book: [Jacobian 局部伸缩, 反函数定理, Riemann 重积分, 区域零延拓], higher_algebra: [行列式], analytic_geometry: [区域映射], python: []}
capabilities: [change_of_variables_theorem, hypothesis_audit, transformed_region]
learning_goals: [陈述换元定理, 解释每项假设, 证明一致小盒像体积估计, 按 Riemann 和证明公式]
content_standard: 2
---

# 重积分换元公式需要哪些条件？ {#u-08-35-02}

## 先备知识
掌握局部线性化、Jacobian 伸缩、反函数定理和区域积分。

## 学习目标
在使用换元公式前核验区域、映射、Jacobian 和坐标覆盖。

## 牵引问题
只算出 Jacobian 不为零，为什么仍可能把同一区域重复计算？

## 探索与猜想
非零 Jacobian 只控制局部；还需映射在目标参数域上**一一对应**，并控制边界和
导数变化，才能把所有小块可靠拼回。

## 概念与理论

### 经典重积分换元定理 {#thm-u-08-35-02-change-of-variables}
令 \(d=2\) 或 \(3\)。设 \(G\subset\mathbb R^d\) 是有限矩形并的内部或常用 Jordan 型
开参数域：它有界，边界由有限个分片 \(C^1\) 参数片组成。设 \(T\) 在 \(\overline G\)
的一个开邻域内为 \(C^1\)，在 \(G\) 内部一一对应，并且 \(\det DT\ne0\)；允许在边界上出现后续
坐标公式所需的有限退化片。令 \(D=T(G)\)，并设 \(f\) 在 \(\overline D\) 上连续。则
\[
\int_D f(x)\,dx
=\int_G f(T(u))\,|\det DT(u)|\,du.
\]
这里的积分是第 33 章定义的经典 Riemann 区域积分；二维写作二重积分，三维写作三重
积分。

| 假设 | 在证明中的用途 |
|---|---|
| 有限矩形并或常用 Jordan 型参数域 | 第 33.4 的薄盒引理可压小参数域边界层 |
| \(T\) 在邻域内 \(C^1\) | 紧内部上导数一致连续，余项控制对所有小盒统一 |
| 内部 \(\det DT\ne0\) | 紧内部上逆矩阵范数一致有界，局部像有内包而不被压扁 |
| \(T\) 在内部一一 | 不同参数小盒的像内部不重叠，不会重复累计 |
| \(f\) 在 \(\overline D\) 连续 | 被积函数有界且一致连续，Riemann 和振幅可统一压小 |
| 有限边界片 | \(\partial G\) 及其 Lipschitz 像可由任意小总体积的有限薄盒覆盖 |

### 引理：小盒像体积的一致估计 {#lem-u-08-35-02-uniform-box-volume}

设 \(K\Subset G\) 为紧集。对中心 \(a\in K\)、边长 \(h\) 的闭立方体
\(Q=a+[-h/2,h/2]^d\subset K\)，当 \(h\to0\) 时一致地有
\[
\operatorname{vol}(T(Q))
=|\det DT(a)|\operatorname{vol}(Q)+o(\operatorname{vol}(Q)).
\]

**证明：紧内部的一致线性化。** 记 \(A=DT(a)\)、
\(R_a(z)=T(z)-T(a)-A(z-a)\)。因 \(DT\) 在 \(K\) 的一个紧邻域上一致连续，存在
\(\omega(t)\downarrow0\) 使同一邻域内
\[
\|R_a(z)-R_a(w)\|\le\omega(Ch)\|z-w\|\qquad(z,w\in Q).
\]
又因 \(|\det DT|\) 在 \(K\) 上有正下界，\(\|A\|\) 与 \(\|A^{-1}\|\) 分别有统一
上界 \(L\) 与 \(M\)。这些常数都不依赖 \(a\) 或小盒。

**线性像的体积。** 线性代数中的平行多面体公式给出
\[
\operatorname{vol}(A(Q-a))=|\det A|h^d.
\]
这一步只处理线性主部，尚不能直接替代 \(T(Q)\)。

**余项的外包与内包。** 令 \(\rho_h=C\omega(Ch)h\)。由余项估计，
\[
T(Q)\subset T(a)+A(Q-a)+B(0,\rho_h).
\]
反向内包也必须证明。若 \(y\in A(Q-a)\) 且 \(A^{-1}y\) 到立方体边界的距离大于
\(2M\rho_h\)，考虑
\[
\Phi_y(z)=a+A^{-1}\bigl(y-R_a(z)\bigr).
\]
充分小的 \(h\) 使 \(M\omega(Ch)<1/2\)；中心点 \(a+A^{-1}y\) 的边界余量保证
\(\Phi_y\) 把 \(Q\) 送入自身且为压缩映射。第 8 章压缩定理给出唯一不动点 \(z\in Q\)，即
\(T(z)=T(a)+y\)。故线性平行多面体去掉厚度 \(O(\rho_h)\) 的边界层后包含于
\(T(Q)-T(a)\)，而 \(T(Q)-T(a)\) 又包含在线性像的 \(O(\rho_h)\) 外层中。

\(\|A\|,\|A^{-1}\|\) 一致有界，所以这两个平行多面体边界层的体积均不超过
\(C\rho_h h^{d-1}=C\omega(Ch)h^d\)。因此
\[
\left|\operatorname{vol}(T(Q))-|\det DT(a)|h^d\right|
\le C\omega(Ch)h^d=o(h^d),
\]
且估计对 \(a\in K\) 一致。\(\square\)

### 换元定理的 Riemann 和证明

**目标边界确实来自参数边界。** 先补上后面零延拓所需的逻辑。若 \(u\in G\)，则
\(\det DT(u)\ne0\)，反函数定理给出 \(u\) 的邻域，其像是 \(T(u)\) 的一个开邻域；
这个像包含于 \(D=T(G)\)，故 \(T(u)\in\operatorname{int}D\)。另一方面，若
\(y\in\partial D\)，取 \(y_n=T(u_n)\to y\)。由 \(\overline G\) 紧致，可取子列
\(u_{n_k}\to\bar u\in\overline G\)，连续性给出 \(y=T(\bar u)\)。若
\(\bar u\in G\)，上一段会使 \(y\) 成为 \(D\) 的内点，矛盾；所以
\(\bar u\in\partial G\)，从而
\[
\partial D\subset T(\partial G).
\]
把 \(T\) 与 \(\partial G\) 的有限个分片 \(C^1\) 参数化复合，仍得到有限个分片
\(C^1\) 参数片。第 33.4 的薄盒论证因而适用于 \(T(\partial G)\)，也控制
**目标边界的零延拓**；边界上的 Jacobian 退化不影响这个结论。

**规则立方网格选出固定内核。** 给定 \(\eta>0\)，先像第 33.4 那样取覆盖
\(\partial G\) 的有限开盒并 \(U\)，使 \(\operatorname{vol}(U)<\eta\)，且边界到
\(\mathbb R^d\setminus U\) 有正距离。取充分细的边长 \(s\) 的**规则立方网格**。
网格还可细到使每个与边界相交的格都落在 \(T\) 的定义邻域中。凡粗网格闭立方体
\(Q_0\) 满足 \(Q_0\cap\partial G\ne\varnothing\)，它都整体包含于 \(U\)。记这些边界
立方体之并为 \(W\)；其内部不交，故
\(\operatorname{vol}(W)<\eta\)。保留其余完全落在 \(G\) 内的粗立方体，记其有限族为
\(\mathcal K_0\)，并定义闭内域
\[
K=\bigcup_{Q_0\in\mathcal K_0}Q_0\Subset G.
\]
任意 \(G\) 中点所在的粗格若未保留，该格必与 \(\partial G\) 相交。因此**所有未保留格**
对 \(G\) 的遗漏都包含在 \(W\) 中，特别地
\[
G\setminus K\subset W,
\qquad \operatorname{vol}(G\setminus K)<C\eta
\]
（这里实际可取 \(C=1\)）。这一步没有把覆盖盒端点插入网格，保留下来的几何对象始终
是边长 \(s\) 的立方体。

**固定内核上的像块。** 固定这个 \(K\)，把每个 \(Q_0\in\mathcal K_0\) 等分成边长
\(h=s/n\) 的闭立方体，所得有限族记为 \(\mathcal K_h\)。于是对每个 \(n\) 都有精确穷尽
\[
K=\bigcup_{Q\in\mathcal K_h}Q.
\]
不同 \(Q\) 的内部不交；由 \(T\) 在 \(G\) 内一一且局部为微分同胚，不同
\(T(Q)\) 的内部也不交。每个 \(T(Q)\) 的边界是有限个 \(C^1\) 参数片的像，故可积；
有限块可由区域可加性求和。

**被积函数与 Jacobian 的振幅控制。** 写 \(J=|\det DT|\)。对每个细立方体明确取
\[
a_Q=\operatorname{center}(Q).
\]
于是 \(Q=a_Q+[-h/2,h/2]^d\)，与上一引理的立方体完全相同，且一致地
\[
\operatorname{vol}(T(Q))=J(a_Q)\operatorname{vol}(Q)
+o_h(\operatorname{vol}(Q)).
\]
由 \(DT\) 有界，\(\operatorname{diam}T(Q)\le Ch\)。上一引理与连续性进一步给出
\[
\begin{aligned}
\int_{T(Q)}f
&=f(T(a_Q))\operatorname{vol}(T(Q))
  +O\!\left(\omega_f(Ch)\operatorname{vol}(T(Q))\right),\\
\int_Q(f\circ T)J
&=f(T(a_Q))J(a_Q)\operatorname{vol}(Q)\\
&\quad+O\!\left(
 [\omega_f(Ch)+\|f\|_\infty\omega_J(h)]\operatorname{vol}(Q)
 \right).
\end{aligned}
\]
再用一致小盒体积误差，逐块之差除以 \(\operatorname{vol}(Q)\) 后由一个与 \(Q\)
无关且趋于零的量控制。细立方体精确穷尽固定 \(K\)，其总体积就是
\(\operatorname{vol}(K)\)，所以求和并令 \(h\to0\) 得到
\[
\int_{T(K)}f=\int_K(f\circ T)J.
\]

**从固定内核回到全域。** \(T\) 在 \(\overline G\) 的紧邻域上有某个 Lipschitz 常数
\(L\)。每个边界粗立方体 \(Q_0\) 的像都装在边长 \(L\sqrt d\,s\) 的轴对齐盒中；把
这些盒合并，便得到 \(T(W)\) 的有限覆盖，其总体积不超过
\(C\operatorname{vol}(W)<C\eta\)。由于
\[
D\setminus T(K)=T(G)\setminus T(K)\subset T(G\setminus K)\subset T(W),
\]
且 \(f\) 与 \((f\circ T)J\) 都有界，遗漏的目标积分和参数积分的绝对值都小于
\(C\eta\)。注意这里粗网格中所有未保留格都已通过 \(W\) 计入误差，没有残余格。

因此顺序是：对每个固定 \(\eta\)，先固定上述 \(K\)，令 \(h\to0\) 得到 \(K\) 上的
等式；再令 \(\eta\to0\)，两侧边界薄层同时消失。结合已经证明的
\(\partial D\subset T(\partial G)\) 及目标边界薄盒控制，区域零延拓均可积，最终得到
全域换元公式。\(\square\)

以上证明没有借用 Jordan 测度或 Lebesgue 理论；第 33.4 的核心薄盒引理承担全部边界
控制。边界上的有限退化片只在最后的薄层中处理，不能当作普通内部点。

## 例题与迁移

### 例 1：线性换元 {#ex-u-08-35-02-linear}
\(T(u,v)=(2u+v,u+2v)\) 的行列式为 \(3\)。若 \(G\) 选得使 \(T\) 一一对应，
则 \(D=T(G)\) 上积分需乘 \(3\)。

### 例 2：重复覆盖 {#ex-u-08-35-02-cover}
\((r,\theta)\mapsto(r\cos\theta,r\sin\theta)\) 若取
\(0\le\theta\le4\pi\)，除边界外几乎每点覆盖两次；即使局部 Jacobian 非零，
直接套公式也会重复计数。

## 即时检验与回望

### 即时检验 1
一点 Jacobian 非零能保证全局一一对应吗？
??? note "答案"
    不能，只能由反函数定理得到该点附近的局部可逆。

### 即时检验 2
为何积分乘绝对值？
??? note "答案"
    换元传递的是非负面积或体积，不让取向反转改变累积量符号。

## 常见误区与后续
- 同时写清参数域 \(G\) 与像域 \(D\)。
- 检查坐标范围是否重复覆盖或遗漏。
- 极坐标原点 Jacobian 为零，需要作为边界退化点单独理解。

## 习题与答案

### 习题 1 {#pr-u-08-35-02-01}
换元前必须列出的四项检查是什么？
??? note "答案"
    一一对应、连续可微、内部 Jacobian 不退化、边界有限分片。

### 习题 2 {#pr-u-08-35-02-02}
若变换二对一，公式会发生什么风险？
??? note "答案"
    像域的大部分点被重复累计。

### 习题 3 {#pr-u-08-35-02-03}
恒等变换给出什么公式？
??? note "答案"
    参数域与像域相同，Jacobian 为 \(1\)，积分不变。

### 习题 4 {#pr-u-08-35-02-04}
反射换元的因子是多少？
??? note "答案"
    行列式绝对值为 \(1\)。

### 习题 5 {#pr-u-08-35-02-05}
为何连续可微强于只处处可微？
??? note "答案"
    它给导数的统一变化控制，使有限分割上的线性化误差同时变小。

### 习题 6 {#pr-u-08-35-02-06}
Jacobian 为零的曲线能否直接当普通内部点？
??? note "答案"
    不能；定理要求相关内部不退化，退化边界需单独处理。

### 习题 7 {#pr-u-08-35-02-07}
被积函数为什么要复合 \(T\)？
??? note "答案"
    参数点 \((u,v)\) 对应原区域点 \(T(u,v)\)，函数应在该像点取值。

### 习题 8 {#pr-u-08-35-02-08}
边界分片在证明中做什么？
??? note "答案"
    把边界附近无法整齐映射的小格总贡献控制到任意小。

### 习题 9 {#pr-u-08-35-02-09}
线性变换为什么是定理的局部模型？
??? note "答案"
    可微定义说明增量主部正是导数线性映射。

### 习题 10 {#pr-u-08-35-02-10}
换元完成后怎样核验？
??? note "答案"
    检查像域、覆盖次数、Jacobian、单位，并用简单函数或面积作独立回验。
