---
title: Newton 法怎样可靠求解非线性方程组？
unit_id: u-07-31-04
hours: {theory: 1.00, applied: 0.75}
difficulty: 5
prerequisites: {book: [反函数定理, Jacobian 核验, 条件数], higher_algebra: [线性方程组求解, 主元消去], analytic_geometry: [], python: [函数, 元组, 异常]}
capabilities: [newton_system_iteration, failure_diagnosis, residual_step_reporting]
learning_goals: [从线性化推导 Newton 步, 说明局部收敛边界, 解释实现的停止与失败状态]
content_standard: 2
---

# Newton 法怎样可靠求解非线性方程组？ {#u-07-31-04}

## 先备知识
掌握 Fréchet 线性化、Jacobian、反函数定理、条件数和线性方程组求解。

## 学习目标
1. 推导方程组 Newton 步；2. 区分局部定理与计算观察；3. 读取全部停止原因和轨迹。

## 牵引问题
把非线性方程反复线性化很自然，但 Jacobian 奇异、初值过远或步长很小而残差仍大时，
程序应怎样诚实地停下？

## 探索与猜想
对 \(F(x)=0\)，在 \(x_k\) 处线性化：
\[
F(x_k+s)\approx F(x_k)+J_F(x_k)s.
\]
令线性模型为零，解
\[
J_F(x_k)s_k=-F(x_k),\qquad x_{k+1}=x_k+s_k.
\]
实现应解线性系统，不显式构造逆矩阵。

## 概念与理论

### 局部收敛边界 {#thm-u-07-31-04-local}
若 \(F\) 在根 \(x^\ast\) 附近充分光滑、\(J_F(x^\ast)\) 可逆、Jacobian 在邻域内满足
适当 Lipschitz 控制，且初值足够接近根，则纯 Newton 迭代局部收敛；在标准条件下可有
二次收敛。该定理不保证任意初值收敛，也不保证迭代始终留在定义域。

### 七步计算单元 {#def-u-07-31-04-workflow}

1. **问题来源：** 明确未知量、方程、定义域、尺度与初值来源。
2. **数学转化：** 写成方阵系统 \(F:\mathbb R^n\to\mathbb R^n\)，推导解析 Jacobian。
3. **算法思想：** 每步求解 \(J_ks_k=-F_k\)，接受有限候选点并记录轨迹。
4. **误差与适用条件：** 检查局部可逆、条件数、残差与步长；局部收敛假设不能省略。
5. **伪代码：**

   ```text
   x = initial
   repeat within budget:
       evaluate F(x), J(x)
       reject singular or ill-conditioned J
       solve J s = -F
       x = x + s
       test residual, then step
   ```

6. **Python：** 复用唯一源码中的 `mathbook_examples.nonlinear.newton_system`。
7. **结果解释：** 报告最终点、残差、步长、条件估计、迭代次数、原因和完整轨迹。

### 停止原因不是证书 {#def-u-07-31-04-status}
实现返回：

- `residual`：残差达到阈值；
- `step`：步长达到阈值；
- `singular_jacobian`：线性系统无可用唯一解；
- `ill_conditioned_jacobian`：条件估计超过限制；
- `nonfinite_value`：函数、Jacobian 或候选点出现非有限数；
- `max_iterations`：预算耗尽。

`residual` 与 `step` 是**停止信号**，不是根误差证书。没有逆函数邻域、误差界或其他
后验定理时，小残差不自动给 \(\|x-x^\ast\|\) 的严格界，小步长也可能只是病态造成。

## 例题与迁移
### 例 1：圆与直线 {#ex-u-07-31-04-circle}
\[
F(x,y)=(x^2+y^2-1,x-y),\quad
J_F(x,y)=\begin{pmatrix}2x&2y\\1&-1\end{pmatrix}.
\]
从 \((0.8,0.6)\) 出发，迭代趋近 \((2^{-1/2},2^{-1/2})\)。

```python
from mathbook_examples.nonlinear import newton_system

F = lambda p: (p[0] ** 2 + p[1] ** 2 - 1.0, p[0] - p[1])
J = lambda p: ((2.0 * p[0], 2.0 * p[1]), (1.0, -1.0))
result = newton_system(F, J, (0.8, 0.6))
print(result.reason, result.point, result.residual_norm)
```

### 例 2：奇异 Jacobian {#ex-u-07-31-04-singular}
若两条方程局部线性相关，消元会遇到零主元。返回 `singular_jacobian` 比产生任意巨大步
更诚实；这也提示模型的方程独立性或变量选择需要检查。

## 即时检验与回望
### 即时检验 1
为什么不直接计算 \(J^{-1}\) 再乘残差？
??? note "答案"
    解线性系统通常更经济、更稳定，也能自然暴露主元与奇异状态。

### 即时检验 2
步长很小但残差很大时能否宣称找到根？
??? note "答案"
    不能；`step` 仅是停止信号，必须同时报告残差并分析病态或尺度。

## 常见误区与后续
- 纯 Newton 法只有局部收敛保证，不含全局化线搜索。
- 条件数描述线性化问题敏感性，不等于实现稳定性。
- 有限次残差下降不是一般收敛证明。
- 轨迹只记录接受的有限点；失败时保留最后有限点。

## 习题与答案
### 习题 1 {#pr-u-07-31-04-01}
从线性化推导 Newton 方程。
??? note "答案"
    令 \(F(x_k)+J_F(x_k)s_k=0\)，得 \(J_F(x_k)s_k=-F(x_k)\)。

### 习题 2 {#pr-u-07-31-04-02}
为什么未知量数应与方程数相同？
??? note "答案"
    本实现求解方阵 Jacobian 系统；欠定或超定问题需要不同理论。

### 习题 3 {#pr-u-07-31-04-03}
初值恰为根时迭代次数应是多少？
??? note "答案"
    零次，直接以 `residual` 停止。

### 习题 4 {#pr-u-07-31-04-04}
`max_iterations` 表示什么？
??? note "答案"
    在给定预算内未触发其他停止条件，不等于数学上发散。

### 习题 5 {#pr-u-07-31-04-05}
`ill_conditioned_jacobian` 与 `singular_jacobian` 有何区别？
??? note "答案"
    前者仍可逆但误差放大超过阈值，后者求解中检测到无可用唯一解。

### 习题 6 {#pr-u-07-31-04-06}
为什么失败时保留最后有限点？
??? note "答案"
    它提供可复查状态，避免用非有限候选覆盖最后可信迭代。

### 习题 7 {#pr-u-07-31-04-07}
小残差何时能转成根误差界？
??? note "答案"
    需另有局部逆的范数界、单调性或后验误差定理等条件。

### 习题 8 {#pr-u-07-31-04-08}
为什么记录完整轨迹？
??? note "答案"
    可诊断振荡、停滞、尺度失衡及进入非定义域前的路径。

### 习题 9 {#pr-u-07-31-04-09}
Newton 法的二次收敛需要哪些典型条件？
??? note "答案"
    根附近充分光滑、根处 Jacobian 可逆、Jacobian 局部 Lipschitz 且初值足够近。

### 习题 10 {#pr-u-07-31-04-10}
条件阈值为什么是策略参数而非数学常数？
??? note "答案"
    可接受放大取决于精度、尺度与应用误差预算。

### 习题 11 {#pr-u-07-31-04-11}
若候选点使函数返回无穷，结果原因是什么？
??? note "答案"
    `nonfinite_value`，并保留更新前的最后有限点。

### 习题 12 {#pr-u-07-31-04-12}
本实现是否包含阻尼或线搜索？
??? note "答案"
    不包含；它是用于展示局部理论和失败状态的纯 Newton 迭代。

### 延伸：停止策略
为什么同时保留残差阈值与步长阈值？
??? note "答案"
    两者诊断不同现象；并列报告可暴露“小步长但大残差”的停滞。

