---
title: 极限证明怎样从目标误差反推局部范围？
unit_id: u-03-09-05
hours:
  theory: 1.5
  applied: 0.5
difficulty: 3
prerequisites:
  book:
  - chapter-09
  higher_algebra:
  - 因式分解
  - 根式与分式恒等变形
  - 绝对值不等式
  analytic_geometry:
  - 实轴距离
  python: []
capabilities:
- concepts
- proof
- analytic_calculation
- mathematical_expression
learning_goals:
- 从目标误差反推充分的局部条件
- 把反向设计改写为正向证明
- 使用辅助邻域建立局部界
- 完成线性、二次、根式和有理式极限证明
content_standard: 2
---

# 极限证明怎样从目标误差反推局部范围？ {#u-03-09-05}


## 先备知识

本单元默认已经会写

\[
\forall \varepsilon>0\;\exists \delta>0\;\forall x\in D,
\qquad
0<|x-a|<\delta\Longrightarrow |f(x)-L|<\varepsilon,
\]

并能用实轴距离解释 \(|x-a|<\delta\)。证明中会反复使用因式分解、根式与分式恒等变形以及绝对值不等式。所有代入点都必须属于函数的定义域 \(D\)。

## 学习目标

完成本单元后，你应当能够：

1. 从目标误差 \(|f(x)-L|<\varepsilon\) 反推足够的局部条件；
2. 把探索阶段的反向设计整理为量词顺序正确的正向验证；
3. 用 \(|x-a|<1\) 一类辅助邻域控制随 \(x\) 变化的因子或分母；
4. 独立完成线性、二次、根式和有理式的 \(\varepsilon\)-\(\delta\) 证明。

## 牵引问题

要证明 \(\lim_{x\to2}x^2=4\)，仅写

\[
|x^2-4|=|x-2||x+2|
\]

还不够。第一因子可以由 \(\delta\) 控制，第二因子却仍随 \(x\) 变化。怎样先把第二因子固定地界住，再给出只依赖于 \(\varepsilon\) 的 \(\delta\)？

## 探索与猜想

先反向观察目标。若额外要求 \(|x-2|<1\)，则

\[
|x+2|=|(x-2)+4|\le |x-2|+4<5.
\]

因此

\[
|x^2-4|<5|x-2|.
\]

为了让右端小于 \(\varepsilon\)，再要求 \(|x-2|<\varepsilon/5\) 即可。把两个要求合并，得到候选

\[
\delta=\min\left\{1,\frac{\varepsilon}{5}\right\}.
\]

这段推导只是反向设计。正式证明必须重新从“任取 \(\varepsilon>0\)”开始，声明 \(\delta\)，再沿正向不等式链验证结论。

## 概念与理论

### \(\varepsilon\)-\(\delta\) 证明证书 {#def-u-03-09-05-proof-certificate}

对命题 \(\lim_{x\to a}f(x)=L\)，一份可核验的**证明证书**包括：

1. 对任意 \(\varepsilon>0\) 给出的明确正数 \(\delta(\varepsilon)\)；
2. 若有需要，用于控制附加因子或分母的辅助局部条件；
3. 对每个 \(x\in D\) 的正向推导
   \[
   0<|x-a|<\delta(\varepsilon)
   \Longrightarrow
   |f(x)-L|<\varepsilon.
   \]

\(\delta\) 可以依赖 \(\varepsilon\)、固定的讨论点 \(a\) 和函数中已经固定的参数，但不能依赖随后才任取的 \(x\)。

### 反向设计与正向验证 {#prop-u-03-09-05-backward-forward}

构造证明时可以按以下顺序工作。

1. **写出目标：** 从 \(|f(x)-L|<\varepsilon\) 开始。
2. **暴露距离：** 通过因式分解、共轭有理化或通分，使 \(|x-a|\) 出现在估计中。
3. **控制其余量：** 若出现 \(|x+a|\) 或分母，先加上 \(|x-a|<r_0\) 这一辅助条件，推出固定界。
4. **选择局部范围：** 若已经找到常数 \(C>0\)，使得
   \[
   |f(x)-L|\le C|x-a|,
   \]
   就把 \(\varepsilon/C\) 与所有辅助半径一起取最小值。若估计中的 \(C=0\)，则在该
   辅助邻域内误差恒为 \(0\)，保留辅助半径中的任意正数即可。
5. **重写为证明：** 正式论证从给定 \(\varepsilon\) 和所选 \(\delta\) 出发，不把反向箭头当成已经完成的证明。

辅助条件不是额外假设。把它写进 \(\delta=\min\{r_0,\varepsilon/C\}\) 后，\(|x-a|<\delta\) 会自动保证该条件。

## 例题与迁移

### 例题 1：线性函数的精确误差预算 {#ex-u-03-09-05-linear}

证明

\[
\lim_{x\to a}(mx+b)=ma+b.
\]

若 \(m=0\)，误差恒为 \(0\)，任取 \(\delta>0\) 都可以。设 \(m\ne0\)。任给 \(\varepsilon>0\)，取

\[
\delta=\frac{\varepsilon}{|m|}>0.
\]

对任意 \(x\in\mathbb R\)，若 \(0<|x-a|<\delta\)，则

\[
|(mx+b)-(ma+b)|
=|m||x-a|
<|m|\delta
=\varepsilon.
\]

所以结论成立。这里没有随 \(x\) 变化的第二因子，反向设计直接给出精确比例。

### 例题 2：二次函数需要辅助邻域 {#ex-u-03-09-05-quadratic}

证明 \(\lim_{x\to2}x^2=4\)。

任给 \(\varepsilon>0\)，取

\[
\delta=\min\left\{1,\frac{\varepsilon}{5}\right\}>0.
\]

若 \(0<|x-2|<\delta\)，则 \(|x-2|<1\)，从而

\[
|x+2|\le |x-2|+4<5.
\]

于是

\[
|x^2-4|
=|x-2||x+2|
<5|x-2|
<5\delta
\le\varepsilon.
\]

这就是完整的正向验证。常数 \(1\) 只负责建立局部界，\(\varepsilon/5\) 才负责最终误差预算。

### 例题 3：根式用共轭式暴露自变量距离 {#ex-u-03-09-05-radical}

证明

\[
\lim_{x\to4}\sqrt{x}=2,
\qquad D=[0,\infty).
\]

任给 \(\varepsilon>0\)，取 \(\delta=2\varepsilon\)。对任意 \(x\in D\)，若 \(0<|x-4|<\delta\)，则

\[
|\sqrt{x}-2|
=\frac{|x-4|}{\sqrt{x}+2}
\le\frac{|x-4|}{2}
<\frac{\delta}{2}
=\varepsilon.
\]

定义域条件 \(x\ge0\) 保证根式有意义，并给出 \(\sqrt{x}+2\ge2\)。证明没有把定义域外的点纳入量词。

### 例题 4：有理式先让分母远离零 {#ex-u-03-09-05-rational}

证明

\[
\lim_{x\to1}\frac{2x+1}{x+2}=1.
\]

反向通分得到

\[
\left|\frac{2x+1}{x+2}-1\right|
=\frac{|x-1|}{|x+2|}.
\]

任给 \(\varepsilon>0\)，取

\[
\delta=\min\{1,2\varepsilon\}.
\]

若 \(0<|x-1|<\delta\)，则 \(0<x<2\)，因而 \(|x+2|>2\)。所以

\[
\left|\frac{2x+1}{x+2}-1\right|
<\frac{|x-1|}{2}
<\frac{\delta}{2}
\le\varepsilon.
\]

辅助半径 \(1\) 同时保证分母不为零并提供统一下界；这一步不能由“分母在讨论点不为零”一句话代替。

## 即时检验与回望

### 即时检验 1：\(\delta\) 可以依赖 \(x\) 吗？

有人为证明 \(\lim_{x\to2}x^2=4\)，写出
\(\delta=\varepsilon/|x+2|\)。这是否是一份有效证书？

??? note "答案"

    不是。极限定义要求先由给定的 \(\varepsilon\) 选定 \(\delta\)，随后才对所有满足条件的 \(x\) 验证结论；所选 \(\delta\) 不能依赖这个尚未任取的 \(x\)。先用 \(|x-2|<1\) 得到 \(|x+2|<5\)，再取 \(\delta=\min\{1,\varepsilon/5\}\)，才能消除这种循环依赖。

### 即时检验 2：为什么把辅助半径写进最小值？

在二次函数证明中，只取 \(\delta=\varepsilon/5\) 是否总能推出 \(|x+2|<5\)？

??? note "答案"

    不能。当 \(\varepsilon\) 很大时，\(\varepsilon/5\) 也可能很大，条件 \(|x-2|<\varepsilon/5\) 未必把 \(x\) 限制在 \((1,3)\)。把 \(1\) 一并写入最小值，才对所有 \(\varepsilon>0\) 都保证辅助界成立。

## 习题与答案

### 习题 1：线性极限 {#pr-u-03-09-05-01}

用定义证明

\[
\lim_{x\to2}(5x-3)=7.
\]

??? note "答案"

    任给 \(\varepsilon>0\)，取 \(\delta=\varepsilon/5\)。若 \(0<|x-2|<\delta\)，则

    \[
    |(5x-3)-7|=5|x-2|<5\delta=\varepsilon.
    \]

    因此所给极限成立。

### 习题 2：在另一个中心控制二次因子 {#pr-u-03-09-05-02}

用定义证明 \(\lim_{x\to-1}x^2=1\)。

??? note "答案"

    任给 \(\varepsilon>0\)，取

    \[
    \delta=\min\left\{1,\frac{\varepsilon}{3}\right\}.
    \]

    若 \(0<|x+1|<\delta\)，则 \(-2<x<0\)，所以 \(|x-1|<3\)。于是

    \[
    |x^2-1|=|x+1||x-1|<3|x+1|<3\delta\le\varepsilon.
    \]

    故极限为 \(1\)。

### 习题 3：根式极限 {#pr-u-03-09-05-03}

在定义域 \([0,\infty)\) 上证明

\[
\lim_{x\to9}\sqrt{x}=3.
\]

??? note "答案"

    任给 \(\varepsilon>0\)，取 \(\delta=3\varepsilon\)。若 \(x\ge0\) 且 \(0<|x-9|<\delta\)，则

    \[
    |\sqrt{x}-3|
    =\frac{|x-9|}{\sqrt{x}+3}
    \le\frac{|x-9|}{3}
    <\frac{\delta}{3}
    =\varepsilon.
    \]

    因此极限成立。定义域条件保证共轭变形中的根式有意义。

### 习题 4：有理式的分母证书 {#pr-u-03-09-05-04}

用定义证明

\[
\lim_{x\to0}\frac1{1+x}=1.
\]

??? note "答案"

    任给 \(\varepsilon>0\)，取

    \[
    \delta=\min\left\{\frac12,\frac{\varepsilon}{2}\right\}.
    \]

    若 \(0<|x|<\delta\)，则

    \[
    |1+x|\ge1-|x|>\frac12.
    \]

    因此

    \[
    \left|\frac1{1+x}-1\right|
    =\frac{|x|}{|1+x|}
    <2|x|
    <2\delta
    \le\varepsilon.
    \]

    辅助半径 \(1/2\) 保证分母远离零。

### 习题 5：审计一份反向推导 {#pr-u-03-09-05-05}

一份草稿从 \(|x^2-4|<\varepsilon\) 反推到
\(|x-2|<\varepsilon/|x+2|\)，随后直接写“证明完成”。指出缺口，并给出可用的证明证书。

??? note "答案"

    缺口有两个：右端仍依赖 \(x\)，而且从目标反推充分条件并不是正向证明。可先要求 \(|x-2|<1\)，由此得到 \(|x+2|<5\)，再取

    \[
    \delta=\min\left\{1,\frac{\varepsilon}{5}\right\}.
    \]

    正式验证为：若 \(0<|x-2|<\delta\)，则

    \[
    |x^2-4|=|x-2||x+2|<5|x-2|<5\delta\le\varepsilon.
    \]

    这份证书对任意给定的 \(\varepsilon>0\) 都成立。

## 常见误区与后续

- 反向设计用于发现 \(\delta\)，但只有正向验证才是证明。
- \(\delta\) 不必是最大的可用半径；给出一个对所有允许点都有效的正数即可。
- 辅助条件必须通过取最小值纳入同一个 \(\delta\)，不能在证明中临时增加未声明的假设。
- 处理有理式时，必须先给出分母远离零的局部证书。
- 下一单元把双侧去心邻域换成左、右半邻域；本单元的误差设计方法仍可逐侧使用。
