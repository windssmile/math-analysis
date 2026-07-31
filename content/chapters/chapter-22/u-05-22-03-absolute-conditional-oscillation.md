---
title: 绝对、条件与振荡收敛怎样区分？
unit_id: u-05-22-03
hours: {theory: 1.5, applied: 0.5}
difficulty: 5
prerequisites:
  book: [u-05-22-01, u-05-22-02, u-05-20-04, u-04-15-01]
  higher_algebra: [绝对值不等式, 分部积分, 三角函数]
  analytic_geometry: [周期区间, 对称截断]
  python: [振荡截断仅作经验观察]
capabilities: [absolute_convergence, conditional_convergence, dirichlet_test, abel_extension, principal_value_boundary]
learning_goals: [证明绝对收敛蕴含收敛, 核对Dirichlet条件, 识别条件收敛, 区分主值与通常积分]
content_standard: 2
---

# 绝对、条件与振荡收敛怎样区分？ {#u-05-22-03}

## 先备知识

正函数可以直接比较大小；换号函数却可能依靠抵消收敛。第 22.1 单元的 Cauchy 尾部
判据适用于两种情形，第 20.4 单元的分部积分则能把振荡部分的有界原函数与逐渐衰减的
振幅分开。

本单元不把“正负面积看起来抵消”当作证明。每个振荡判别都要给出足以控制任意尾段的
不等式。

## 学习目标

完成本单元后，你应能：

1. 区分绝对收敛与条件收敛；
2. 证明绝对收敛推出收敛；
3. 核对并证明本章版 Dirichlet 判别；
4. 用 Abel 判别处理收敛积分乘单调有界因子；
5. 证明 \(\sin x/x\) 条件收敛；
6. 区分 Cauchy 主值与通常反常积分。

## 牵引问题

函数 \(\sin x/x\) 的振幅缓慢衰减，正负波峰不断交替。仅凭图像无法回答：

- 任意远处的尾段是否都很小？
- 取绝对值后是否仍收敛？
- 只看对称截断是否隐藏了一侧发散？

## 探索与猜想

分部积分提示把

\[
\int_A^B f(x)g(x)\,dx
\]

拆成“\(f\) 的原函数”与“\(g\) 的衰减”。若 \(f\) 的累计量始终有界，而 \(g\)
单调递减到零，那么远处的振荡既不会积累成大偏差，剩余振幅又越来越小。

## 概念与理论

### 绝对收敛与条件收敛

设 \(f\) 在每个有限截断区间上可积。

- 若 \(\int_a^\infty |f(x)|\,dx\) 收敛，称 \(\int_a^\infty f(x)\,dx\)
  **绝对收敛**；
- 若 \(\int_a^\infty f\) 收敛而 \(\int_a^\infty|f|\) 发散，称其
  **条件收敛**。

绝对收敛不要求 \(f\) 最终同号；它用非负函数 \(|f|\) 控制所有正负波动的总量。

### 绝对收敛推出收敛 {#thm-u-05-22-03-absolute-implies-convergence}

**定理。** 若 \(\int_a^\infty|f(x)|\,dx\) 收敛，则
\(\int_a^\infty f(x)\,dx\) 收敛。

**证明。** 给定 \(\varepsilon>0\)。由 \(|f|\) 的 Cauchy 尾部判据，存在 \(A\)，
使任意 \(B>C\ge A\) 都有

\[
\int_C^B|f(x)|\,dx<\varepsilon.
\]

正常积分的绝对值估计给出

\[
\left|\int_C^Bf(x)\,dx\right|
\le\int_C^B|f(x)|\,dx<\varepsilon.
\]

所以 \(f\) 也满足 Cauchy 尾部判据，原反常积分收敛。证毕。

反向不成立：抵消可能使 \(\int f\) 收敛，却不能使 \(\int|f|\) 收敛。

### Dirichlet 判别 {#thm-u-05-22-03-dirichlet-test}

**定理。** 设 \(f\) 在 \([a,\infty)\) 上连续，并且其累计函数

\[
F(x)=\int_a^x f(t)\,dt
\]

有界，即存在 \(M>0\) 使 \(|F(x)|\le M\)。又设 \(g\in C^1[a,\infty)\)
非负、单调递减且 \(g(x)\to0\)。则

\[
\int_a^\infty f(x)g(x)\,dx
\]

收敛。

**证明。** 对 \(B>A\ge a\)，令

\[
H_A(x)=\int_A^x f(t)\,dt=F(x)-F(A).
\]

于是 \(|H_A(x)|\le2M\)，且 \(H_A(A)=0\)、\(H_A'=f\)。分部积分得

\[
\int_A^Bfg
=H_A(B)g(B)-\int_A^BH_A(x)g'(x)\,dx.
\]

因为 \(g'\le0\)，

\[
\begin{aligned}
\left|\int_A^Bfg\right|
&\le2Mg(B)+2M\int_A^B[-g'(x)]\,dx\\
&=2Mg(B)+2M[g(A)-g(B)]\\
&=2Mg(A).
\end{aligned}
\]

当 \(A\to\infty\) 时，右侧趋于零，而且这个界对所有 \(B>A\) 同时成立。因此
\(fg\) 满足 Cauchy 尾部判据，积分收敛。证毕。

条件的职责不能互换：

- 有界原函数控制振荡累计量；
- 单调性把 \(-g'\) 变成非负总变化；
- \(g\to0\) 使尾部上界真正趋零。

### Abel 判别 {#cor-u-05-22-03-abel-test}

**推论。** 若 \(\int_a^\infty f(x)\,dx\) 收敛，且 \(g\in C^1[a,\infty)\)
有界并单调，则 \(\int_a^\infty f(x)g(x)\,dx\) 收敛。

**证明。** 单调有界函数 \(g\) 有有限极限 \(\ell\)。若 \(g\) 递减，则
\(g-\ell\ge0\) 且递减到零；若 \(g\) 递增，则 \(\ell-g\ge0\) 且递减到零。

另一方面，\(\int_a^x f\) 因收敛而有界。把

\[
fg=\ell f+f(g-\ell)
\]

或相应的递增版本拆开：第一项是收敛积分的常数倍，第二项满足 Dirichlet 判别。
故 \(\int fg\) 收敛。证毕。

Abel 判别在这里是 Dirichlet 思想的拓展，而不是对任意有界 \(g\) 的结论；单调条件
仍然承担控制总变化的责任。

## 例题与迁移

### 例 1：\(\sin x/x\) 的条件收敛 {#ex-u-05-22-03-conditional-sine-over-x}

考察

\[
\int_1^\infty\frac{\sin x}{x}\,dx.
\]

取 \(f(x)=\sin x\)、\(g(x)=1/x\)。累计函数

\[
F(x)=\int_1^x\sin t\,dt=\cos1-\cos x
\]

有界，而 \(g\) 非负、单调递减到零。Dirichlet 判别说明原积分收敛。

还需证明它不绝对收敛。对每个整数 \(k\ge1\)，在

\[
I_k=\left[k\pi+\frac{\pi}{6},\,k\pi+\frac{5\pi}{6}\right]
\]

上有 \(|\sin x|\ge1/2\)，且 \(x<(k+1)\pi\)。因此

\[
\int_{I_k}\frac{|\sin x|}{x}\,dx
\ge\frac12\cdot\frac{2\pi/3}{(k+1)\pi}
=\frac{1}{3(k+1)}.
\]

累加前 \(N\) 个互不相交区间，并用有限和与对数积分比较：

\[
\sum_{k=1}^{N}\frac1{k+1}
\ge\int_2^{N+2}\frac{dx}{x}
=\log\frac{N+2}{2}\to\infty.
\]

所以 \(\int_1^\infty|\sin x|/x\,dx\) 发散。原积分是条件收敛。

### 例 2：绝对收敛的振荡积分 {#ex-u-05-22-03-absolute-oscillation}

对

\[
\int_1^\infty\frac{\cos x}{x^2}\,dx,
\]

有

\[
\left|\frac{\cos x}{x^2}\right|\le\frac1{x^2}.
\]

右侧可积，所以原积分绝对收敛。这里无需动用 Dirichlet；绝对值比较给出更强结论。

### 例 3：主值不是通常收敛 {#ex-u-05-22-03-principal-value-boundary}

对 \(f(x)=\sin x\)，

\[
\operatorname{PV}\int_{-\infty}^{\infty}\sin x\,dx
:=\lim_{R\to\infty}\int_{-R}^{R}\sin x\,dx=0.
\]

但右侧通常反常积分

\[
\int_0^R\sin x\,dx=1-\cos R
\]

没有极限。故 Cauchy 主值存在并不推出通常反常积分收敛。主值规定了特殊截断路径，
逐端点定义则要求路径不能掩盖任一尾部。

## 即时检验与回望

### 即时检验 1

若 \(\int|f|\) 收敛，证明 \(\left|\int_A^Bf\right|\) 小时需要 \(f\) 最终同号吗？

??? note "答案"

    不需要。正常积分估计

    \[
    \left|\int_A^Bf\right|\le\int_A^B|f|
    \]

    对换号函数同样成立；右侧的 Cauchy 尾部控制已经足够。

### 即时检验 2

在 Dirichlet 判别中，只知道 \(g\) 有界且趋于零，能否删去单调性？

??? note "答案"

    不能直接删去。证明需要

    \[
    \int_A^B|g'|=g(A)-g(B)
    \]

    来控制总变化；没有单调性时，这个等式失效，现有证明不能闭合。

回望：绝对收敛控制总振幅；Dirichlet 控制有界累计量乘衰减振幅；主值只控制一条指定
截断路径。

## 习题与答案

### 练习 1：绝对收敛 {#pr-u-05-22-03-01}

证明 \(\int_2^\infty \sin(x^2)/x^2\,dx\) 绝对收敛。

??? note "答案"

    \[
    \left|\frac{\sin(x^2)}{x^2}\right|\le\frac1{x^2}.
    \]

    上方 \(p\)-积分收敛，故绝对值积分收敛，进而原积分收敛。

### 练习 2：Dirichlet 条件 {#pr-u-05-22-03-02}

用 Dirichlet 判别证明 \(\int_1^\infty \cos x/\sqrt x\,dx\) 收敛。

??? note "答案"

    \(\cos x\) 的累计函数 \(\sin x-\sin1\) 有界；\(x^{-1/2}\) 非负、单调递减且
    趋于零。因此满足 Dirichlet 条件，积分收敛。

### 练习 3：不是绝对收敛的证明 {#pr-u-05-22-03-03}

为什么不等式 \(|\cos x|/\sqrt x\le1/\sqrt x\) 不能证明上一题绝对收敛？

??? note "答案"

    上方函数 \(x^{-1/2}\) 的积分发散。上方函数发散对下方函数没有收敛结论；
    该不等式既不能证明绝对收敛，也不能证明绝对值积分发散。

### 练习 4：Abel 判别 {#pr-u-05-22-03-04}

设 \(\int_1^\infty f\) 收敛。证明
\(\int_1^\infty f(x)(1+x^{-1})\,dx\) 收敛。

??? note "答案"

    \(g(x)=1+x^{-1}\) 有界且单调递减到 \(1\)，满足 Abel 判别。也可拆成

    \[
    \int_1^\infty f+\int_1^\infty\frac{f(x)}x\,dx;
    \]

    第一项按假设收敛，第二项由 Dirichlet 判别收敛。

### 练习 5：缺少趋零条件 {#pr-u-05-22-03-05}

函数 \(f(x)=1\) 的原函数无界；函数 \(g(x)=1\) 不趋于零。解释为什么
\(\int_1^\infty fg\) 发散不与 Dirichlet 判别矛盾。

??? note "答案"

    两个关键条件都不满足：\(F(x)=x-1\) 无界，且 \(g(x)\not\to0\)。定理没有
    对该积分作出收敛承诺。

### 练习 6：尾部定量界 {#pr-u-05-22-03-06}

设 \(|F(x)|\le3\)，\(g\) 满足 Dirichlet 判别条件。证明任意 \(B>A\) 有
\(\left|\int_A^Bfg\right|\le6g(A)\)。

??? note "答案"

    证明中的 \(M=3\)。于是 \(|H_A|\le2M=6\)，分部积分估计直接给出

    \[
    \left|\int_A^Bfg\right|\le2Mg(A)=6g(A).
    \]

### 练习 7：主值诊断 {#pr-u-05-22-03-07}

某解答由 \(\int_{-R}^{R}x\,dx=0\) 宣称
\(\int_{-\infty}^{\infty}x\,dx\) 收敛。指出错误。

??? note "答案"

    对称截断只给出主值候选。通常定义要求
    \(\int_{-\infty}^{0}x\,dx\) 与 \(\int_0^\infty x\,dx\) 分别收敛；
    二者都发散，所以通常积分不存在。

### 练习 8：条件分类 {#pr-u-05-22-03-08}

已知 \(\int_1^\infty f\) 收敛而 \(\int_1^\infty|f|\) 发散。该积分属于哪一类？
它是否可能由正函数直接比较证明收敛？

??? note "答案"

    它是条件收敛。若只把 \(|f|\) 与一个可积正函数作上方比较，就会推出绝对收敛，
    与已知条件矛盾；其收敛必须利用符号抵消或其他振荡结构。

## 常见误区与后续

- 由 \(\int f\) 收敛反推 \(\int|f|\) 收敛；
- 看到振荡就引用 Dirichlet，却没有检查有界原函数；
- 把“\(g\to0\)”误当成足以替代单调总变化控制；
- 用几张数值图像证明条件收敛；
- 把 Cauchy 主值写成通常反常积分。

本单元只使用有限区间分部积分和尾部估计。无穷级数判别、幂级数展开与一致收敛属于
后续部分；下一单元回到有限区间，建立带二阶导数界的中点和梯形求积。
