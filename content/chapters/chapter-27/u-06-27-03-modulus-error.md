---
title: 连续性模怎样给出显式误差界？
unit_id: u-06-27-03
hours: {theory: 1.00, applied: 0.75}
difficulty: 4
prerequisites: {book: [Bernstein 二阶矩, 一致连续, 一致误差], higher_algebra: [Cauchy–Schwarz 不等式], analytic_geometry: ["区间 [0,1]"], python: [误差预算]}
capabilities: [modulus_of_continuity, quantitative_bernstein_bound, degree_budget]
learning_goals: [定义连续性模, 推导 Bernstein 显式界, 计算 Lipschitz 次数预算, 区分证书与观测]
content_standard: 2
---

# 连续性模怎样给出显式误差界？ {#u-06-27-03}

## 先备知识

需要 Bernstein 权重、一阶与二阶中心矩，以及闭区间连续函数的一致连续性。

## 学习目标

1. 定义连续性模并证明基本性质；
2. 从二阶矩推出显式一致误差界；
3. 为 Lipschitz 函数反解次数预算；
4. 在有二阶导数界时获得更强估计；
5. 区分理论上界、网格最大误差和未知真实上确界。

## 牵引问题

定性证明只说“充分大”。若希望误差不超过 \(\varepsilon\)，怎样把函数的连续性强弱
转化成可计算次数？

## 探索与猜想

连续性模把“距离不超过 \(\delta\)”时的最坏函数变化压缩成一个数。Bernstein 二阶矩
则量化权重偏离 \(x\) 的尺度，两者结合便给出统一误差。

## 概念与理论

### 连续性模 {#def-u-06-27-03-modulus}

对 \(f\in C([0,1])\)，定义

\[
\omega_f(\delta)=
\sup_{\substack{x,y\in[0,1]\\|x-y|\le\delta}}|f(x)-f(y)|.
\]

它非负、关于 \(\delta\) 单调不减，且由一致连续性
\(\omega_f(\delta)\to0\)（\(\delta\downarrow0\)）。分段连接两点可得

\[
|f(u)-f(x)|\le\left(1+\frac{|u-x|}{\delta}\right)\omega_f(\delta).
\]

### 定量 Bernstein 界 {#thm-u-06-27-03-quantitative-bound}

把上式乘权重求和，并用 Cauchy–Schwarz 与二阶中心矩：

\[
\begin{aligned}
|B_n(f;x)-f(x)|
&\le\omega_f(\delta)\left(
1+\frac1\delta\sum_k|k/n-x|p_{n,k}(x)\right)\\
&\le\omega_f(\delta)\left(1+\frac1{2\delta\sqrt n}\right).
\end{aligned}
\]

取 \(\delta=n^{-1/2}\)，得到显式一致界

\[
\|B_n(f)-f\|_\infty\le\frac32\,\omega_f(n^{-1/2}).
\]

### Lipschitz 次数预算 {#cor-u-06-27-03-lipschitz-budget}

若 \(|f(u)-f(x)|\le L|u-x|\)，则直接由一阶绝对中心矩得

\[
\|B_n(f)-f\|_\infty\le\frac{L}{2\sqrt n}.
\]

要使误差不超过 \(\varepsilon\)，足够取

\[
n\ge\left(\frac{L}{2\varepsilon}\right)^2.
\]

若 \(f\in C^2([0,1])\) 且 \(\|f''\|_\infty\le M\)，对每个样本点作一阶 Taylor
展开；常数与线性项由矩恒等式精确保持，余项给出

\[
\|B_n(f)-f\|_\infty\le\frac{M}{8n}.
\]

一般区间 \([a,b]\) 上两界分别乘 \(b-a\) 与 \((b-a)^2\)。

## 例题与迁移

### 例 1：绝对值函数 {#ex-u-06-27-03-absolute}

\(f(x)=|x-1/2|\) 的 Lipschitz 常数为 \(1\)，故次数 \(n\) 的理论上界为
\(1/(2\sqrt n)\)。

### 例 2：二次函数 {#ex-u-06-27-03-quadratic}

\(f(x)=x^2\) 有 \(M=2\)，二阶导数界给 \(1/(4n)\)，并且这正是精确最大误差。

## 即时检验与回望

### 即时检验 1
连续性模为何趋于零？
??? note "答案"

    因为闭区间连续函数一致连续。

### 即时检验 2
网格最大误差为何不是理论上界？
??? note "答案"

    网格没有检查点与点之间，可能漏掉更大的真实误差。

## 习题与答案

### 习题 1 {#pr-u-06-27-03-01}
证明 \(\omega_f\) 单调不减。
??? note "答案"

    增大 \(\delta\) 只会扩大取上确界的点对集合。

### 习题 2 {#pr-u-06-27-03-02}
若 \(f\) 为常数，连续性模是多少？
??? note "答案"

    对所有 \(\delta\) 都为零。

### 习题 3 {#pr-u-06-27-03-03}
Lipschitz 常数为 \(2\)，\(n=100\) 时理论界是多少？
??? note "答案"

    \(2/(2\sqrt{100})=0.1\)。

### 习题 4 {#pr-u-06-27-03-04}
要使该 Lipschitz 界不超过 \(0.01\)，需怎样的 \(n\)？
??? note "答案"

    \(n\ge(2/(2\cdot0.01))^2=10000\)。

### 习题 5 {#pr-u-06-27-03-05}
二阶导数界为何比一般 Lipschitz 界快？
??? note "答案"

    线性项被构造精确保持，只剩二阶余项，量级为 \(1/n\)。

### 习题 6 {#pr-u-06-27-03-06}
区间长度翻倍时 Lipschitz 界怎样？
??? note "答案"

    放大两倍；二阶导数界则放大四倍。

### 习题 7 {#pr-u-06-27-03-07}
理论界大于观测误差是否矛盾？
??? note "答案"

    不矛盾；理论界是保守的全域保证。

### 习题 8 {#pr-u-06-27-03-08}
观测误差大于正确理论界可能说明什么？
??? note "答案"

    实现、输入的正则性常数或理论公式至少有一处错误。

### 习题 9 {#pr-u-06-27-03-09}
未知真实上确界误差能否由有限网格精确确定？
??? note "答案"

    一般不能，除非有额外结构证明网格间控制。

## 常见误区与后续

- 理论上界无需等于真实误差。
- 调用者提供的正则性常数必须先有数学依据。
- 下一单元实现时把证书字段和网格观测字段永久分开。

