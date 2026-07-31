---
title: 局部连续何时升级为全局一致控制？
unit_id: u-03-11-03
hours:
  theory: 1.5
  applied: 0.5
difficulty: 4
prerequisites:
  book:
  - u-03-10-01
  - u-03-11-01
  higher_algebra:
  - 绝对值不等式
  analytic_geometry:
  - 闭区间
  python: []
capabilities:
- concepts
- proof
- analytic_calculation
- mathematical_expression
learning_goals:
- 区分逐点连续与一致连续的量词顺序
- 写出一致连续性的否定
- 用成对点列证明 Heine–Cantor 定理
- 构造连续但不一致连续的反例
content_standard: 2
---

# 局部连续何时升级为全局一致控制？ {#u-03-11-03}


## 先备知识

一点连续允许控制半径依赖中心点；11.1 已证明闭区间中的每条数列都有收敛到区间内
一点的子列。你还需要会使用三角不等式证明两条距离趋零的点列拥有同一极限。

## 学习目标

1. 按正确量词顺序定义一致连续；
2. 写出不一致连续的完整否定；
3. 用序列紧致性证明 Heine–Cantor 定理；
4. 用成对点列检验非紧致定义域上的失败。

## 牵引问题

若每个位置都能找到自己的控制半径，是否能为整个区间选一个共同采样间距？普通连续
没有给出这种承诺；一致连续要求半径只依赖目标误差，不依赖正在观察的点。

## 探索与猜想

若不存在统一半径，就会有一个固定输出误差 \(\varepsilon_0\)，无论把输入距离压到
多小，都能找到一对“坏点”。依次把距离压到 \(1/n\)，便得到两列越来越靠近的坏点。
闭区间迫使其中一列出现收敛子列，另一列也会被拖到同一极限，最终与连续性冲突。

## 概念与理论

### 定义：一致连续 {#def-u-03-11-03-uniform-continuity}

函数 \(f:D\to\mathbb R\) 称为在 \(D\) 上一致连续，若

\[
\forall\varepsilon>0\;\exists\delta>0\;\forall x,y\in D,\qquad
|x-y|<\delta\Longrightarrow |f(x)-f(y)|<\varepsilon. \tag{11.3}
\]

这里 \(\delta\) 可以依赖 \(\varepsilon\) 和整个函数，但不能依赖随后选择的
\(x,y\)。与逐点连续比较：

\[
\forall a\in D\;\forall\varepsilon>0\;\exists\delta(a,\varepsilon)>0
\;\forall x\in D.
\]

一致连续把 \(\exists\delta\) 移到所有中心点之前。

一致连续必推出每一点连续：固定 \(a\in D\)，在 (11.3) 中令 \(y=a\) 即可。
反向一般不成立。

### 命题：不一致连续的否定形式 {#prop-u-03-11-03-negation}

\(f\) 在 \(D\) 上不一致连续，当且仅当存在 \(\varepsilon_0>0\)，使对每个
\(\delta>0\)，都存在 \(x,y\in D\) 满足

\[
|x-y|<\delta,\qquad |f(x)-f(y)|\ge\varepsilon_0.
\]

**说明。** 否定“对每个 \(\varepsilon\) 存在一个统一 \(\delta\)”时，必须先固定
一个失败的 \(\varepsilon_0\)；坏点对可以随 \(\delta\) 改变。把
\(\delta=1/n\) 依次代入，可得

\[
|x_n-y_n|<\frac1n,\qquad
|f(x_n)-f(y_n)|\ge\varepsilon_0. \tag{11.4}
\]

### 定理：Heine–Cantor {#thm-u-03-11-03-uniform-continuity}

若 \(f:[a,b]\to\mathbb R\) 连续，则 \(f\) 在 \([a,b]\) 上一致连续。

**证明。** 反设 \(f\) 不一致连续。由否定形式，存在固定
\(\varepsilon_0>0\) 和两列 \(x_n,y_n\in[a,b]\)，满足 (11.4)。

由闭区间序列紧致性，\((x_n)\) 有子列

\[
x_{n_k}\to c\in[a,b].
\]

又因为

\[
|y_{n_k}-c|
\le |y_{n_k}-x_{n_k}|+|x_{n_k}-c|
<\frac1{n_k}+|x_{n_k}-c|\to0,
\]

所以 \(y_{n_k}\to c\)。

函数在 \(c\) 连续，故

\[
f(x_{n_k})\to f(c),\qquad f(y_{n_k})\to f(c).
\]

于是

\[
|f(x_{n_k})-f(y_{n_k})|
\le |f(x_{n_k})-f(c)|+|f(y_{n_k})-f(c)|\to0,
\]

这与它始终不小于 \(\varepsilon_0\) 矛盾。因此 \(f\) 一致连续。\(\square\)

证明只需在抽出的公共极限点 \(c\) 使用一点连续；序列紧致性把假想的全局失败集中到
这个局部点，从而产生矛盾。

### 判据：成对点列证伪 {#prop-u-03-11-03-paired-sequences}

若存在 \(x_n,y_n\in D\)，使

\[
|x_n-y_n|\to0
\]

但 \(|f(x_n)-f(y_n)|\) 不趋于 \(0\)，则 \(f\) 在 \(D\) 上不一致连续。

**证明。** 若 \(f\) 一致连续，给定任意 \(\varepsilon>0\)，统一半径
\(\delta\) 对所有点对有效。充分大的 \(n\) 满足 \(|x_n-y_n|<\delta\)，从而
\(|f(x_n)-f(y_n)|<\varepsilon\)，这会迫使输出差趋于零，矛盾。\(\square\)

## 例题与迁移

### 例题 1：直接给出统一半径 {#ex-u-03-11-03-square-interval}

证明 \(f(x)=x^2\) 在 \([0,2]\) 上一致连续。

**证明。** 对 \(x,y\in[0,2]\)，

\[
|x^2-y^2|=|x-y|\,|x+y|\le4|x-y|.
\]

给定 \(\varepsilon>0\)，取 \(\delta=\varepsilon/4\)。若
\(|x-y|<\delta\)，则输出差小于 \(\varepsilon\)。这个 \(\delta\) 与点的位置
无关。\(\square\)

### 例题 2：开区间上的倒数 {#ex-u-03-11-03-reciprocal}

证明 \(f(x)=1/x\) 在 \((0,1)\) 上不一致连续。

**证明。** 取

\[
x_n=\frac1n,\qquad y_n=\frac1{n+1}.
\]

则

\[
|x_n-y_n|=\frac1{n(n+1)}\to0,
\]

但

\[
|f(x_n)-f(y_n)|=|n-(n+1)|=1.
\]

由成对点列判据，函数不一致连续。坏点向缺失端点 \(0\) 聚集。\(\square\)

## 即时检验与回望

### 即时检验 1：否定中为什么固定同一个 \(\varepsilon_0\)？

??? note "答案"

    若允许输出阈值也随 \(n\) 趋于零，就不能证明存在某种不可消除的统一失败。
    不一致连续的逻辑否定要求先找到一个固定正误差，再说明任何输入半径都挡不住它。

### 即时检验 2：为什么只从 \(x_n\) 抽子列就够？

??? note "答案"

    成对距离满足 \(|x_n-y_n|\to0\)。若 \(x_{n_k}\to c\)，三角不等式给出

    \[
    |y_{n_k}-c|\le|y_{n_k}-x_{n_k}|+|x_{n_k}-c|\to0,
    \]

    所以配对的 \(y_{n_k}\) 自动趋于同一个 \(c\)。

## 习题与答案

### 习题 1：恒等函数 {#pr-u-03-11-03-identity}

证明 \(f(x)=x\) 在 \(\mathbb R\) 上一致连续。

??? note "答案"

    给定 \(\varepsilon>0\)，取 \(\delta=\varepsilon\)。任意
    \(x,y\in\mathbb R\) 满足 \(|x-y|<\delta\) 时，

    \[
    |f(x)-f(y)|=|x-y|<\varepsilon.
    \]

### 习题 2：平方函数在实轴失败 {#pr-u-03-11-03-square-real-line}

证明 \(x^2\) 在 \(\mathbb R\) 上不一致连续。

??? note "答案"

    取 \(x_n=n\)、\(y_n=n+1/n\)。输入差为 \(1/n\to0\)，但

    \[
    y_n^2-x_n^2
    =2+\frac1{n^2}\to2.
    \]

    输出差不趋于零，所以不一致连续。

### 习题 3：一致连续推出连续 {#pr-u-03-11-03-implies-continuity}

直接从定义证明一致连续函数在定义域每一点连续。

??? note "答案"

    固定任意 \(a\in D\)。给定 \(\varepsilon>0\)，取一致连续性提供的统一
    \(\delta\)。若 \(x\in D\) 且 \(|x-a|<\delta\)，在定义中令 \(y=a\)，即得
    \(|f(x)-f(a)|<\varepsilon\)。故 \(f\) 在 \(a\) 连续。

### 习题 4：平方根的统一估计 {#pr-u-03-11-03-square-root}

用

\[
|\sqrt{x}-\sqrt y|\le\sqrt{|x-y|}
\]

证明平方根函数在 \([0,\infty)\) 上一致连续。

??? note "答案"

    给定 \(\varepsilon>0\)，取 \(\delta=\varepsilon^2\)。若
    \(x,y\ge0\) 且 \(|x-y|<\delta\)，则

    \[
    |\sqrt{x}-\sqrt y|
    \le\sqrt{|x-y|}
    <\sqrt{\delta}=\varepsilon.
    \]

    半径与 \(x,y\) 无关。

### 习题 5：有界不等于一致连续 {#pr-u-03-11-03-bounded-not-enough}

函数 \(f(x)=\sin(1/x)\) 在 \((0,1)\) 上有界。说明有界性为什么不能推出一致连续。

??? note "答案"

    取

    \[
    x_n=\frac1{\pi/2+2\pi n},\qquad
    y_n=\frac1{3\pi/2+2\pi n}.
    \]

    两列都趋于 \(0\)，所以 \(|x_n-y_n|\to0\)，但
    \(f(x_n)=1\)、\(f(y_n)=-1\)，输出差恒为 \(2\)。函数虽有界，却不一致连续。

## 常见误区与后续

- 一致连续不是“在每一点都连续”的同义改写，关键是控制半径不依赖点。
- 否定时必须固定一个正的输出差下界。
- 从一列抽子列后，另一列必须保留相同指标才能利用配对距离。
- Heine–Cantor 给出存在性，不一定给出最优或显式的统一半径。

本章已经把闭区间中的无限点列压缩为收敛子列，并由此得到有界、最值与一致连续三个
整体结论。下一章将把连续性用于存在性证明和带误差证书的求解过程。
