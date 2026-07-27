---
title: 怎样实现具有保护机制和停止证书的 Newton 算法？
unit_id: u-04-17-04
hours: {theory: 0.25, applied: 1.75}
difficulty: 4
prerequisites:
  book: [u-03-12-02, u-04-17-02, u-04-17-03]
  higher_algebra: [区间不等式, 几何收缩, 对数估算]
  analytic_geometry: [切线交点, 变号区间, 中点]
  python: [函数, 循环, 不可变数据对象, 浮点数]
capabilities: [algorithmic_thinking, invariant_proof, error_analysis, numerical_experiment, interpretation]
learning_goals: [区分停止信号与误差证书, 证明保护算法区间不变量, 实现 Newton 与二分切换, 解读算法结果对象]
content_standard: 2
---

# 怎样实现具有保护机制和停止证书的 Newton 算法？ {#u-04-17-04}

## 先备知识

第 12.2 单元已经实现带区间误差界的二分法；第 17.3 单元说明纯 Newton 在简单根附近
可能二次收敛，也可能遇到零导数、跳出有效区域或进入二周期。本页把两者组合：
Newton 步负责争取速度，变号区间负责保住存在性与误差界。

## 学习目标

完成本单元后，你应当能够：

1. 区分残差、步长、迭代退出与可验证误差证书；
2. 说明哪些条件由调用者证明，哪些条件由程序检查；
3. 用中央半区规则决定接受 Newton 步还是退回二分步；
4. 证明变号区间不变量和最坏 \(3/4\) 收缩率；
5. 解读 `NewtonResult` 中的退出原因、步型和证书字段。

## 牵引问题

纯 Newton 从 \(0\) 求解 \(x^3-2x+2=0\) 时在 \(0,1\) 之间循环；二分法在变号区间
\([-2,-1]\) 上却一定推进。能否让算法在切线可靠时使用 Newton，在切线不可靠时自动
退回二分，并且无论切换多少次都保留一个可核验的误差界？

## 探索与猜想

若当前区间为 \([a,b]\)，仅要求 Newton 候选落在区间内部还不够：候选可以无限靠近
端点，使新区间几乎不缩小。更强的规则是只接受中央半区

```text
[a+w/4,b-w/4]
```

中的候选，其中 \(w=b-a\)。这样无论候选与哪一端同号，更新后的新区间宽度都不超过
\(3w/4\)。若候选不满足条件，就使用中点，宽度直接减半。

## 概念与理论

### 可验证误差证书 {#def-u-04-17-04-verifiable-certificate}

**可验证误差证书**是由已经核验的数学条件推出、对真实误差成立的明确数值上界。

设 \(f\) 在 \([a,b]\) 上连续且 \(f(a)f(b)\le0\)。介值定理保证区间内至少有一个根
\(r\)。若返回中点

\[
m=\frac{a+b}{2},
\]

则

\[
|m-r|\le\frac{b-a}{2}.
\]

右端就是可验证误差证书。这里有一条不能省略的职责边界：

- **连续性由调用者证明**；有限次求值不可能验证整个区间上的连续性；
- **程序能够检查**端点有限、有序、端点函数值有限以及端点变号；
- 程序还能在每一步检查新的端点仍然变号。

相比之下，

\[
|f(x_n)|\le\varepsilon
\quad\text{或}\quad
|x_{n+1}-x_n|\le\varepsilon
\]

通常只是停止信号。没有额外的导数下界时，小残差或小步长不能直接变成自变量误差界。

### 算法思想

算法始终维护一对有限端点及其异号函数值。当前迭代点取残差较小的端点，因为它通常
更适合形成 Newton 候选。每轮依次判断：

1. 导数是否有限且绝对值高于阈值；
2. Newton 候选是否有限；
3. 候选是否位于中央半区；
4. 候选函数值是否有限。

前三项任一失败就直接使用中点；若 Newton 候选求值非有限，再尝试中点。只有有限候选
才能更新区间。

### 保护型 Newton 伪代码 {#alg-u-04-17-04-safeguarded-newton}

```text
验证 a < b、端点有限、f(a) 与 f(b) 有限且异号
若端点是根，返回精确根
若区间宽度已达到容差，返回中点和半宽误差界

x ← 残差较小的端点
重复至多 max_iterations 次：
    midpoint ← 区间中点
    若 f'(x) 有限且不太小：
        candidate ← x - f(x) / f'(x)
    否则：
        candidate ← midpoint

    若 candidate 非有限或不在中央半区：
        candidate ← midpoint

    计算 f(candidate)
    若 Newton 候选值非有限：
        candidate ← midpoint 并重新求值
    若中点值仍非有限：
        退出并标记证书失效

    若 f(candidate) = 0：
        返回精确根
    用 candidate 替换同号端点
    若新区间宽度达到容差：
        返回新区间中点和半宽误差界
    x ← candidate

预算耗尽时返回当前区间中点和当前半宽误差界
```

### 区间不变量与最坏收缩 {#thm-u-04-17-04-bracket-contraction}

**定理。** 假设初始区间满足连续性和端点变号条件。上述算法每完成一个有限候选步后，
新区间仍包含至少一个根。若初始宽度为 \(w_0\)，第 \(n\) 步后的宽度为 \(w_n\)，则

\[
w_n\le\left(\frac34\right)^n w_0.
\]

**证明。** 候选点 \(c\in(a,b)\) 的函数值若与左端点同号，就用 \(c\) 替换左端点；
否则用它替换右端点。新端点仍异号，连续性与介值定理继续保证新区间内有根。

若使用二分点，两段宽度都为 \(w/2\)。若接受 Newton 候选，则

\[
c\in\left[a+\frac w4,b-\frac w4\right].
\]

无论保留 \([a,c]\) 还是 \([c,b]\)，新区间宽度都不超过 \(3w/4\)。所以每一步至少
满足 \(w_{n+1}\le3w_n/4\)。归纳即得结论。证毕。

若目标是让返回中点的误差不超过 \(\varepsilon\)，只需保证 \(w_n\le2\varepsilon\)。
因此一个与函数具体形状无关的最坏步数上界是

\[
n\ge
\left\lceil
\frac{\log(2\varepsilon/w_0)}{\log(3/4)}
\right\rceil.
\]

### 结果对象怎样表达保证

正式实现位于 `src/mathbook_examples/newton.py`，公开函数为 `newton` 和
`safeguarded_newton`。两者统一返回不可变的 `NewtonResult`：

- `value`：实际返回的近似值；
- `converged`：是否达到请求的正常停止条件；
- `certified`：当前 `error_bound` 是否由有效变号区间支持；
- `iterations`：完成的候选步数；
- `reason`：`residual`、`step`、`bracket`、`endpoint`、
  `derivative_too_small`、`nonfinite_value` 或 `max_iterations`；
- `residual`：返回点的 \(|f(x)|\)；
- `last_step`：最后一个已完成步的长度；
- `bracket`：最终变号区间；
- `error_bound`：针对 `value` 的误差上界；
- `step_types`：每个完成步是 `"newton"` 还是 `"bisection"`。

纯 Newton 因残差或步长退出时，可以有 `converged=True`、
`certified=False`。保护算法耗尽预算时，也可以有
`converged=False`、`certified=True`：它没有达到请求的区间宽度，却仍返回一个较宽
但真实的误差上界。

## 例题与迁移

### 例 1：同一失败方程的两种轨迹 {#ex-u-04-17-04-cycle-versus-safeguard}

纯 Newton：

```python
pure = newton(
    lambda x: x**3 - 2*x + 2,
    lambda x: 3*x*x - 2,
    0.0,
    max_iterations=4,
)
```

结果的关键字段为：

```text
value=0.0
converged=False
certified=False
reason='max_iterations'
residual=2.0
step_types=('newton', 'newton', 'newton', 'newton')
```

它正是 \(0\leftrightarrow1\) 二周期。

保护型算法从变号区间启动：

```python
safe = safeguarded_newton(
    lambda x: x**3 - 2*x + 2,
    lambda x: 3*x*x - 2,
    -2.0,
    -1.0,
    interval_tolerance=1e-10,
)
```

真实实现返回约

```text
value=-1.7692923541981085
converged=True
certified=True
reason='bracket'
iterations=35
error_bound=4.052780333552164e-11
```

步型中既有 Newton，也有二分。误差界来自最终括区间，不来自残差
\(2.995\times10^{-10}\)。

### 例 2：预算耗尽不等于证书失效 {#ex-u-04-17-04-budget-certificate}

把同一保护算法限制为两步：

```python
short = safeguarded_newton(
    lambda x: x**3 - 2*x + 2,
    lambda x: 3*x*x - 2,
    -2.0,
    -1.0,
    interval_tolerance=1e-30,
    max_iterations=2,
)
```

得到

```text
value=-1.6710526315789473
converged=False
certified=True
reason='max_iterations'
bracket=(-1.8421052631578947, -1.5)
error_bound=0.17105263157894735
step_types=('bisection', 'newton')
```

算法没有达到极小的目标容差，所以 `converged=False`；但返回值是当前区间中点，半宽
确实覆盖区间内某个根，所以 `certified=True`。

### 方法保证比较 {#tbl-u-04-17-04-certificate-comparison}

| 方法 | 存在 | 唯一 | 迭代收敛 | 可验证误差界 | 速度 |
|---|---|---|---|---|---|
| 介值定理 | 连续且端点变号时保证 | 不保证 | 不提供迭代 | 初始中点只有 \(w_0/2\) 粗界 | 不适用 |
| 二分法 | 继承连续与变号条件 | 不保证 | 保证区间收缩 | 中点误差不超过半宽 | 每步宽度减半 |
| 纯 Newton | 需另证根存在 | 区间单调等条件下可证 | 强区间条件或简单根局部可证 | 一般没有 | 简单根附近局部二次 |
| 保护型 Newton | 继承连续与变号条件 | 不保证 | 宽度保证趋零 | 返回中点时为半宽 | 最坏每步乘 \(3/4\)，安全 Newton 步可加速 |
| 严格凸优化 | 严格凸本身不保证取得 | 极小点若存在则唯一 | 本身不是迭代算法 | 没有通用数值误差界 | 不适用 |

比较时必须带条件阅读。“速度快”不能替代存在性，“存在根”不能替代唯一性，“算法
退出”也不能替代真实误差界。

## 即时检验与回望

### 即时检验 1

对 \(f(x)=x^3-2x+2\)，当前区间是 \([-2,-1]\)，当前点为 \(-2\)。Newton 候选为何
被拒绝？

??? note "答案"
    区间宽度 \(w=1\)，中央半区是

    \[
    [-2+1/4,-1-1/4]=[-1.75,-1.25].
    \]

    在 \(x=-2\) 处，

    \[
    x_N=-2-\frac{-2}{10}=-1.8.
    \]

    它虽在原区间内，却不在中央半区，所以不能保证新区间至少缩短到原来的 \(3/4\)。
    算法改用中点 \(-1.5\)。

### 即时检验 2

初始宽度为 \(1\)。若要求中点误差不超过 \(10^{-6}\)，按最坏 \(3/4\) 收缩估计至少
需要多少步？

??? note "答案"
    需要

    \[
    \left(\frac34\right)^n\le2\times10^{-6}.
    \]

    因此

    \[
    n\ge
    \frac{\log(2\times10^{-6})}{\log(3/4)}
    \approx45.62.
    \]

    取整数上界得 \(n=46\)。实际算法若多次使用二分或有效 Newton 步，可能更早达到
    目标。

回望：保护机制不是在 Newton 之外附加一个经验补丁，而是把“快速候选”和“区间
不变量”分工。前者争取平均速度，后者给出无条件于候选质量的最坏进展。

## 习题与答案

### 习题 1：中央半区判定 {#pr-u-04-17-04-central-region}

当前区间为 \([1,5]\)。判断候选 \(1.8,2.5,4.2\) 是否会被中央半区规则接受。

??? note "答案"
    宽度 \(w=4\)，中央半区为

    \[
    [1+1,5-1]=[2,4].
    \]

    所以只有 \(2.5\) 被接受；\(1.8\) 和 \(4.2\) 都退回二分步。

### 习题 2：最坏步数 {#pr-u-04-17-04-step-budget}

初始宽度为 \(8\)，希望返回中点误差不超过 \(10^{-4}\)。写出保护算法的最坏步数
公式，不要求计算小数。

??? note "答案"
    需要最终宽度不超过 \(2\times10^{-4}\)，所以

    \[
    8\left(\frac34\right)^n\le2\times10^{-4}.
    \]

    因而可取

    \[
    n=
    \left\lceil
    \frac{\log((2\times10^{-4})/8)}{\log(3/4)}
    \right\rceil.
    \]

### 习题 3：诊断错误证书 {#pr-u-04-17-04-false-residual}

有人声称：“因为 \(|f(x)|<10^{-8}\)，所以 \(|x-r|<10^{-8}\)。”指出缺少什么条件。

??? note "答案"
    小残差本身不能控制横向误差。若已知连接 \(x,r\) 的区间上

    \[
    |f'(t)|\ge\mu>0,
    \]

    中值定理才给出

    \[
    |x-r|\le\frac{|f(x)|}{\mu}.
    \]

    没有导数正下界或变号区间半宽，原声称没有误差证书。

### 习题 4：解读预算耗尽结果 {#pr-u-04-17-04-budget-result}

某结果满足 `reason="max_iterations"`、`converged=False`、
`certified=True`、`error_bound=0.02`。怎样准确表述？

??? note "答案"
    算法没有在给定预算内达到请求的区间容差，所以不能说“按目标收敛完成”；但它仍
    维护了有效变号区间，返回中点与区间内某个真实根的距离不超过 \(0.02\)。证书
    有效，只是精度比请求目标粗。

### 习题 5：选择方法 {#pr-u-04-17-04-method-choice}

已知连续函数在 \([a,b]\) 端点变号，但无法证明导数不为零。若必须返回可核验误差界，
应选择纯 Newton 还是保护型 Newton？说明理由。

??? note "答案"
    应选择保护型 Newton。纯 Newton 可能遇到零导数、越界或不收敛，而且一般不返回
    根误差界。保护算法在 Newton 不安全时退回二分，始终维护变号区间，并以中点半宽
    给出可核验误差界。连续性仍需调用者事先证明。

## 常见误区与后续

- **把 `converged` 与 `certified` 当成同一字段：** 它们分别描述目标停止和误差证明。
- **认为程序检查了连续性：** 程序只能检查有限次求值，连续性是数学前提。
- **只要求 Newton 候选在区间内：** 靠近端点的候选不能保证充分收缩。
- **用残差冒充根误差：** 需要导数下界或变号区间才能转换。
- **把保护算法称为处处二次收敛：** 它的统一最坏保证是区间几何收缩，Newton 步只是
  条件性加速。

第四部在此把“定义—证明—算法—证书”闭合。第 18 章将转向原函数与积分方法；本页
不提前使用后续理论。
