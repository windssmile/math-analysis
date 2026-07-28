---
title: Riemann 和何时拥有与取样无关的极限？
unit_id: u-05-19-02
hours: {theory: 1.50, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-02-05-02, u-02-06-02, u-05-19-01]
  higher_algebra: [有限求和, 三角不等式, 上确界逼近]
  analytic_geometry: [闭区间, 区间长度, 分割]
  python: [有限和, 数值比较]
capabilities: [darboux_integrability, riemann_integrability, epsilon_reasoning, equivalence_proof]
learning_goals: [使用Darboux判据, 正确书写Riemann量词, 控制公共加细误差, 证明两种定义等价]
content_standard: 2
---

# Riemann 和何时拥有与取样无关的极限？ {#u-05-19-02}

## 先备知识

设 \(f:[a,b]\to\mathbb R\) 有界，\(a<b\)。第 19.1 单元已经定义分割 \(P\)、网格
\(\|P\|\)、标记分割 \((P,\xi)\)、Riemann 和 \(S(f;P,\xi)\) 以及 Darboux 上下和，
并证明

\[
L(f,P)\le S(f;P,\xi)\le U(f,P).
\]

本单元使用确界逼近：若 \(M=\sup A\)，则对每个 \(\eta>0\)，存在 \(x\in A\) 使
\(x>M-\eta\)。上确界不必由某个元素取到。

## 学习目标

完成本单元后，你应当能够：

1. 使用上积分、下积分相等定义 Darboux 可积；
2. 证明 \(U-L\) 可任意压小的 Darboux 判据；
3. 正确写出 Riemann 可积定义中的全部量词；
4. 区分“小网格”与“加细固定分割”；
5. 用公共加细误差控制证明 Darboux 可积推出 Riemann 可积；
6. 用逼近上确界和下确界的标记证明反方向。

## 牵引问题

对 \(f(x)=x\) 的等距分割，左端点和、右端点和、中点和都趋近 \(1/2\)。但仅知道这
三条特殊路线还不够：别的非等距分割、别的取样点会不会趋向另一个数？

Riemann 可积要求一个很强的稳定性：

> 只要所有子区间都足够短，无论怎样分割、怎样取样，有限和都必须接近同一个数。

Darboux 上下和怎样把这一无限多选择的要求化成一个可证明的判据？

## 探索与猜想

如果某个分割 \(P\) 满足

\[
U(f,P)-L(f,P)<\varepsilon,
\]

那么这个分割上的所有取样和都落在一个很窄的区间内。但 Riemann 定义还要求控制任意
小网格分割 \(Q\)，而 \(Q\) 不一定加细 \(P\)。

正确桥梁不是假装 \(Q\succeq P\)，而是构造公共加细 \(P\cup Q\)，再估计为了加入
\(P\) 的有限个内部点，需要改动的那些 \(Q\)-子区间总长度。

## 概念与理论

### Darboux 可积 {#def-u-05-19-02-darboux-integrable}

回忆

\[
\underline{\int_a^b}f=\sup_P L(f,P),
\qquad
\overline{\int_a^b}f=\inf_P U(f,P).
\]

若

\[
\underline{\int_a^b}f
=
\overline{\int_a^b}f,
\]

则称 \(f\) 在 \([a,b]\) 上 **Darboux 可积**，公共值记作

\[
\int_a^b f(x)\,dx.
\]

由任意下和不超过任意上和，始终有下积分不超过上积分。可积性就是二者之间没有正间隙。

### Darboux 可积判据 {#thm-u-05-19-02-darboux-criterion}

**定理。** 有界函数 \(f:[a,b]\to\mathbb R\) Darboux 可积，当且仅当对每个
\(\varepsilon>0\)，存在分割 \(P\) 使

\[
U(f,P)-L(f,P)<\varepsilon.
\]

**证明。**

先设上下积分都等于 \(I\)。由下积分是下和集合的上确界，可取分割 \(P_1\) 使

\[
L(f,P_1)>I-\frac{\varepsilon}{2}.
\]

由上积分是上和集合的下确界，可取分割 \(P_2\) 使

\[
U(f,P_2)<I+\frac{\varepsilon}{2}.
\]

令 \(P=P_1\cup P_2\)。由加细单调性，

\[
U(f,P)-L(f,P)
\le U(f,P_2)-L(f,P_1)
<\varepsilon.
\]

反之，设上下和差可任意压小。对给定分割 \(P\)，有

\[
0\le
\overline{\int_a^b}f-\underline{\int_a^b}f
\le U(f,P)-L(f,P).
\]

右端可小于任意正数，故上下积分相等。证毕。

### Riemann 可积 {#def-u-05-19-02-riemann-integrable}

**定义。** 若存在实数 \(I\)，使得对每个 \(\varepsilon>0\)，都存在
\(\delta>0\)，满足：

> 对所有分割 \(Q\) 和所有取样点
> \(\xi_i\in[y_{i-1},y_i]\)，只要 \(\|Q\|<\delta\)，就有
> \[
> |S(f;Q,\xi)-I|<\varepsilon,
> \]

则称 \(f\) 在 \([a,b]\) 上 **Riemann 可积**，积分值为 \(I\)。

量词顺序是

\[
\exists I\ \forall\varepsilon>0\ \exists\delta>0\
\forall Q\ \forall\xi.
\]

“所有分割”和“所有取样点”不能换成某一种等距分割与固定标记。

### 公共加细误差引理 {#lem-u-05-19-02-common-refinement-control}

**引理。** 设 \(|f(x)|\le M\)。固定分割

\[
P=\{x_0,x_1,\ldots,x_n\},
\]

其内部点数为 \(k=n-1\)。对任意标记分割 \((Q,\xi)\)，有

\[
L(f,P)-2Mk\|Q\|
\le S(f;Q,\xi)
\le U(f,P)+2Mk\|Q\|.
\]

当 \(k=0\) 时误差项为零。

**证明。** 把 \(Q\) 的子区间分成两类：

1. 内部不含 \(P\) 的内部点的“良好区间”；
2. 内部至少含一个 \(P\) 的内部点的“跨界区间”。

每个跨界区间至少对应一个 \(P\) 的内部点，因此跨界区间至多 \(k\) 个，总长度不超过

\[
k\|Q\|.
\]

在良好区间上，它完全包含于 \(P\) 的某个子区间，对应标记值被该 \(P\)-子区间的
上、下确界夹住。

在跨界区间上，把它按 \(P\) 的点切开即可得到公共加细 \(P\cup Q\)。原标记贡献与
这些细段的任一上下界贡献，每单位长度最多相差 \(2M\)。所以所有跨界区间引入的总误差
不超过

\[
2M\cdot k\|Q\|.
\]

合并良好区间与跨界区间即得结论。证毕。

这个引理明确说明：\(\|Q\|\) 很小不意味着 \(Q\) 加细 \(P\)；它只保证为了形成公共
加细而受影响的总长度很小。

### Riemann 与 Darboux 等价 {#thm-u-05-19-02-riemann-darboux-equivalence}

**定理。** 有界函数 \(f:[a,b]\to\mathbb R\) Darboux 可积，当且仅当它 Riemann
可积；两种定义给出的积分值相同。

**证明：Darboux 推出 Riemann。**

设 Darboux 积分为 \(I\)，且 \(|f|\le M\)。给定 \(\varepsilon>0\)，由 Darboux
判据选择分割 \(P\)，使

\[
U(f,P)-L(f,P)<\frac{\varepsilon}{2}.
\]

设 \(P\) 有 \(k\) 个内部点。取

\[
M_0=\max\{M,1\},\qquad k_0=\max\{k,1\},
\qquad
\delta=\frac{\varepsilon}{4M_0k_0}.
\]

对任意满足 \(\|Q\|<\delta\) 的标记分割，由公共加细误差引理，

\[
S(f;Q,\xi)
\le U(f,P)+2Mk\|Q\|
<U(f,P)+\frac{\varepsilon}{2}.
\]

又因为 \(L(f,P)\le I\le U(f,P)\)，

\[
U(f,P)-I\le U(f,P)-L(f,P)<\frac{\varepsilon}{2}.
\]

所以 \(S(f;Q,\xi)-I<\varepsilon\)。完全类似地，

\[
I-S(f;Q,\xi)<\varepsilon.
\]

因此对所有分割和所有取样点均有

\[
|S(f;Q,\xi)-I|<\varepsilon.
\]

**证明：Riemann 推出 Darboux。**

设所有足够细的标记和都趋向 \(I\)。给定 \(\varepsilon>0\)，在 Riemann 定义中把
误差取为 \(\varepsilon/4\)，得到相应 \(\delta>0\)。选择一个满足
\(\|P\|<\delta\) 的分割 \(P\)。

令

\[
\eta=\frac{\varepsilon}{8(b-a)}.
\]

在每个子区间上，由上确界定义选择标记 \(\alpha_i\)，使

\[
f(\alpha_i)>M_i-\eta;
\]

由下确界定义选择标记 \(\beta_i\)，使

\[
f(\beta_i)<m_i+\eta.
\]

这就是逼近上确界和逼近下确界，而不假设界一定取到。于是

\[
0\le U(f,P)-S(f;P,\alpha)<\eta(b-a)=\frac{\varepsilon}{8},
\]

\[
0\le S(f;P,\beta)-L(f,P)<\frac{\varepsilon}{8}.
\]

两组标记和都在 \(I\) 的 \(\varepsilon/4\) 邻域内，因此

\[
|S(f;P,\alpha)-S(f;P,\beta)|<\frac{\varepsilon}{2}.
\]

合并三段误差，

\[
U(f,P)-L(f,P)
<\frac{\varepsilon}{8}
+\frac{\varepsilon}{2}
+\frac{\varepsilon}{8}
=\frac{3\varepsilon}{4}
<\varepsilon.
\]

由 Darboux 判据，\(f\) Darboux 可积。夹逼还说明公共值就是 \(I\)。证毕。

## 例题与迁移

### 例 1：Dirichlet 函数暴露取样依赖 {#ex-u-05-19-02-dirichlet-tags}

在 \([0,1]\) 上定义

\[
d(x)=
\begin{cases}
1,&x\in\mathbb Q,\\
0,&x\notin\mathbb Q.
\end{cases}
\]

每个非退化子区间同时含有理数和无理数，所以对任意分割

\[
L(d,P)=0,\qquad U(d,P)=1.
\]

若每段都选有理标记，则 \(S=1\)；若每段都选无理标记，则 \(S=0\)。无论网格多小，
取样点都能制造两个不同结果。

??? note "答案"

    Darboux 判据中的间隙恒为一，Riemann 定义中的“所有取样点”也直接失败。两种
    描述揭示的是同一个振荡障碍。

### 例 2：为什么小网格不是加细 {#ex-u-05-19-02-small-mesh-not-refinement}

固定

\[
P=\{0,1/2,1\}.
\]

对奇数 \(N\) 取等距分割

\[
Q_N=\{0,1/N,\ldots,1\}.
\]

虽然 \(\|Q_N\|=1/N\to0\)，但 \(1/2\notin Q_N\)，所以 \(Q_N\) 不加细 \(P\)。

??? note "答案"

    应加入 \(1/2\) 形成 \(P\cup Q_N\)。只有包含 \(1/2\) 的那个 \(Q_N\)-子区间
    需要被再切开，其长度不超过 \(1/N\)，这正是公共加细误差引理的情形。

### 例 3：单点尖峰满足 Darboux 判据 {#ex-u-05-19-02-spike-criterion}

对第 19.1 单元的单点尖峰 \(h\)，给定 \(\varepsilon>0\)，取

\[
0<\eta<\frac{\varepsilon}{2}
\]

并把 \(c-\eta,c,c+\eta\) 加入分割。于是

\[
U(h,P)-L(h,P)\le2\eta<\varepsilon.
\]

因此 \(h\) Darboux 可积，继而由等价定理 Riemann 可积，积分为零。

??? note "答案"

    取样点若恰好命中 \(c\)，只会影响包含 \(c\) 的短区间；公共加细控制说明任意足够
    细的标记和仍接近零。

## 即时检验与回望

### 即时检验 1

“对每个分割 \(P\)，存在一组选点使取样和接近 \(I\)”是否足以证明 Riemann 可积？

??? note "答案"

    不足。定义要求同一个网格阈值下，所有足够细分割的所有取样点都接近 \(I\)。
    “存在一组好取样”不能排除另一组取样趋向不同数。

### 即时检验 2

为什么反向证明不能直接选择使 \(f(\alpha_i)=M_i\) 的点？

??? note "答案"

    一般有界函数不一定取得上确界。只能对任意 \(\eta>0\) 选择满足
    \(f(\alpha_i)>M_i-\eta\) 的点，并把有限个逼近误差纳入预算。

## 习题与答案

### 练习 1：翻译量词 {#pr-u-05-19-02-01}

用文字解释

\[
\forall\varepsilon>0\ \exists\delta>0\
\forall(Q,\xi),\quad
\|Q\|<\delta\Rightarrow |S(f;Q,\xi)-I|<\varepsilon.
\]

??? note "答案"

    无论要求多小的总误差，都能先选一个统一网格阈值；此后任何分割和任何标记只要网格
    小于阈值，其取样和都必须落在 \(I\) 的指定误差内。

### 练习 2：一条收敛数列为何不够 {#pr-u-05-19-02-02}

说明 Dirichlet 函数在 \([0,1]\) 上的等距左端点和都等于一，却仍不可积。

??? note "答案"

    等距分点 \(i/n\) 都是有理数，左端点取样和确实恒为一；但改用无理标记就恒为零。
    一条特殊序列收敛没有控制所有取样点，因此不能推出 Riemann 可积。

### 练习 3：从判据确定误差 {#pr-u-05-19-02-03}

设 \(U(f,P)-L(f,P)<10^{-4}\)。说明同一分割上的任意两个标记和之差小于多少。

??? note "答案"

    两个标记和都位于 \([L(f,P),U(f,P)]\) 中，所以二者之差的绝对值小于
    \(10^{-4}\)。

### 练习 4：公共加细预算 {#pr-u-05-19-02-04}

设 \(|f|\le3\)，固定分割有四个内部点，且 \(U(f,P)-L(f,P)<\varepsilon/2\)。
给出一个使公共加细误差小于 \(\varepsilon/2\) 的网格条件。

??? note "答案"

    引理误差为
    \[
    2Mk\|Q\|=24\|Q\|.
    \]
    取
    \[
    \|Q\|<\frac{\varepsilon}{48}
    \]
    即可使它小于 \(\varepsilon/2\)。

### 练习 5：逼近确界而非取得确界 {#pr-u-05-19-02-05}

若某子区间长度为 \(\Delta x_i\)，并选到
\(f(\alpha_i)>M_i-\eta\)，估计该段上和贡献与标记贡献之差。

??? note "答案"

    有
    \[
    0\le M_i\Delta x_i-f(\alpha_i)\Delta x_i
    <\eta\Delta x_i.
    \]
    对所有子区间求和后，总误差小于 \(\eta(b-a)\)。

### 练习 6：积分值唯一 {#pr-u-05-19-02-06}

证明 Riemann 定义中的积分值不可能同时为两个不同实数 \(I,J\)。

??? note "答案"

    若 \(I\ne J\)，取 \(\varepsilon=|I-J|/3\)。分别由两个定义得到网格阈值，取更小
    者，并选任一满足它的标记分割。则
    \[
    |I-J|
    \le|I-S|+|S-J|
    <2\varepsilon
    =\frac23|I-J|,
    \]
    矛盾。

## 常见误区与后续

1. **把一条规则分割序列当作完整定义。** 完整定义必须控制所有分割和所有取样点。
2. **把小网格当加细。** 二者之间必须经过公共加细误差引理。
3. **默认一般有界函数取得极值。** 等价性证明只能使用逼近确界的点。
4. **量词顺序倒置。** \(\delta\) 必须先于分割与标记统一选定。
5. **只证明两种积分值相等，不证明可积类相同。** 等价定理必须包含两个方向。

下一单元将使用 Darboux 判据证明连续、单调和有限分段连续函数可积，并分析振荡和
无界性造成的不同障碍。
