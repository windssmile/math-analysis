---
title: 选读附录：从向量分析到微分形式
---

# 从向量分析到微分形式 {#appendix-part-09-differential-forms}

本附录约需 2–3 学时，只用第九部已经建立的 Euclid 空间、参数曲线、参数曲面和重积分。
它不计入第九部核心单元、核心学时或核心考核，也不是第十部前置。目标只是用一种记号
看见 Green、Gauss、Stokes 背后的共同结构；**不证明一般流形上的广义 Stokes 定理**。

全文默认形式的系数至少属于计算中所用偏导阶数对应的 $C^k$ 类；使用 $d^2=0$ 时
明确要求相关系数为 $C^2$，从而可以使用混合偏导交换。积分对象 $M$ 只取正文允许的
有界分片光滑定向区域或曲面，$\partial M$ 分片光滑且取向相容。

## 在 $\mathbb R^3$ 中先看 0、1、2、3-形式

在坐标 $(x,y,z)$ 中，0-形式就是函数，例如 $f=x^2y+z$。1-形式写成

\[
\alpha=P\,dx+Q\,dy+R\,dz,
\]

它把向量 $v=(v_1,v_2,v_3)$ 送到数 $Pv_1+Qv_2+Rv_3$。因此向量场
$F=(P,Q,R)$ 的功积分正是 1-形式的积分。

2-形式采用固定顺序

\[
\beta=P\,dy\wedge dz+Q\,dz\wedge dx+R\,dx\wedge dy.
\]

我们选定标准体积形式 $\mathrm{vol}=dx\wedge dy\wedge dz$。向量场 $F=(P,Q,R)$
与体积形式的内乘定义为

\[
(\iota_F\mathrm{vol})(u,v)=\mathrm{vol}(F,u,v).
\]

坐标展开给出
$\iota_F\mathrm{vol}=P\,dy\wedge dz+Q\,dz\wedge dx+R\,dx\wedge dy$；它在有向面
$(u,v)$ 上的取值就是 $F\cdot(u\times v)$。这正是通量所需的 2-形式。
3-形式则形如 $g\,dx\wedge dy\wedge dz$，在有向体积区域上积分。

楔积只需两条规则：它对每个因子线性，并且 1-形式反交换，
$dx\wedge dy=-dy\wedge dx$，从而 $dx\wedge dx=0$。这里不建立完整外代数。

## 外微分统一梯度、旋度与散度

外微分把 $k$-形式变成 $(k+1)$-形式，并满足 $d(d\omega)=0$。对函数 $f$，

\[
df=f_x\,dx+f_y\,dy+f_z\,dz,
\]

其系数就是 $\nabla f$。对 $\alpha=P\,dx+Q\,dy+R\,dz$，按上面的 2-形式顺序，

\[
d\alpha=(R_y-Q_z)\,dy\wedge dz+(P_z-R_x)\,dz\wedge dx
 +(Q_x-P_y)\,dx\wedge dy,
\]

系数正是 $\nabla\times F$。对
$\beta=A\,dy\wedge dz+B\,dz\wedge dx+C\,dx\wedge dy$，

\[
d\beta=(A_x+B_y+C_z)\,dx\wedge dy\wedge dz
       =(\nabla\cdot F)\,\mathrm{vol}.
\]

在上述 $C^2$ 条件下，混合偏导交换，因此“梯度的旋度为零”和“旋度的散度为零”
都是 $d^2=0$ 的坐标影子。

## 算例一：1-形式沿参数曲线的拉回

拉回的意思是把空间中的形式改写成参数变量。令
$\alpha=-y\,dx+x\,dy$，圆周参数化 $\gamma(t)=(\cos t,\sin t)$，
$0\le t\le2\pi$。代入 $dx=-\sin t\,dt$、$dy=\cos t\,dt$ 得

\[
\gamma^*\alpha=(-\sin t)(-\sin t\,dt)+(\cos t)(\cos t\,dt)=dt,
\]

所以

\[
\int_\gamma\alpha=\int_0^{2\pi}dt=2\pi.
\]

**方向提醒：** 若用 $\widetilde\gamma(t)=\gamma(2\pi-t)$ 反向走圆周，拉回变为
$-dt$（配合相应参数区间），积分变成 $-2\pi$。

## 算例二：2-形式在参数曲面上的拉回

取 $F=(x,y,z)$，相应通量 2-形式为

\[
\beta=x\,dy\wedge dz+y\,dz\wedge dx+z\,dx\wedge dy.
\]

用 $r(u,v)=(u,v,1)$ 参数化正方形 $0\le u,v\le1$，并取由
$(r_u,r_v)$ 给出的向上法向。因为 $dx=du$、$dy=dv$、$dz=0$，

\[
r^*\beta=1\,du\wedge dv,
\qquad
\int_{r([0,1]^2)}\beta=\int_0^1\int_0^1du\,dv=1.
\]

**方向提醒：** 交换参数次序会把 $du\wedge dv$ 变为 $dv\wedge du=-du\wedge dv$，
也就是反转法向，通量随之变号。

## 边界取向与广义 Stokes 口号

有向曲面诱导边界方向：当头朝所选法向看去时，边界按右手规则前进；对平面向上
法向就是逆时针。三维区域采用外法向。改变整体取向时，边界取向也必须一起改变，
不能只改积分号的一边。

只在上述具体 Euclid 正则对象以及足够光滑的 $\omega$ 语境中，统一口号是

\[
\int_{\partial M}\omega=\int_M d\omega.
\]

这里 $M$ 与 $\partial M$ 必须带相容取向，形式的次数也要匹配；各经典公式的详细条件
回指第 39–41 章。下表只是对照，不替代那些条件检查与证明，也不把口号解释成一般
流形上的定理。

| 经典公式 | $M$ | $\omega$ | $d\omega$ | 边界与取向 |
|---|---|---|---|---|
| Green | 平面有向区域 | $P\,dx+Q\,dy$ | $(Q_x-P_y)\,dx\wedge dy$ | 正向边界（通常逆时针） |
| Gauss | 三维有向区域 | $A\,dy\wedge dz+B\,dz\wedge dx+C\,dx\wedge dy$ | $(\nabla\cdot F)\,\mathrm{vol}$ | 外法向闭曲面 |
| Stokes | 三维有向曲面 | $P\,dx+Q\,dy+R\,dz$ | 与 $\nabla\times F$ 对应的 2-形式 | 法向诱导的右手边界方向 |

## 范围边界与选读回望

本附录排除一般流形、切丛、上同调以及完整外代数；也不讨论链、弱导数或测度论形式。
特别地，本附录不证明一般流形上的广义 Stokes 定理，只解释经典向量分析公式为何能写成
同一个口号。

## 即时检验与选读练习

### 即时检验 1
向量场的功积分对应几形式？
??? note "答案"
    对应 1-形式；沿参数曲线拉回后成为参数变量上的 1-形式再积分。

### 即时检验 2
交换曲面参数 $u,v$ 的次序会怎样改变通量 2-形式的拉回？
??? note "答案"
    楔积反交换使拉回变号；几何上这正对应法向反转，通量随之变号。

### 即时检验 3
$d^2=0$ 的坐标计算为什么需要 $C^2$ 条件？
??? note "答案"
    因为消去二阶项要交换混合偏导；$C^2$ 条件保证所用的混合偏导相等。

### 练习 1：函数的外微分 {#pr-appendix-part-09-01}
写出 $f=xyz$ 的 $df$，再计算 $d(df)$ 并逐项说明抵消来源。
??? note "答案"
    有 $df=yz\,dx+xz\,dy+xy\,dz$。再次外微分后，$xy$、$xz$、$yz$ 的每一对
    混合偏导项分别乘上次序相反的楔积，因 $dx\wedge dy=-dy\wedge dx$ 等关系
    成对抵消，所以 $d(df)=0$。

### 练习 2：1-形式的外微分 {#pr-appendix-part-09-02}
计算 $\alpha=z\,dx+x\,dy+y\,dz$ 的 $d\alpha$，并按固定 2-形式顺序整理。
??? note "答案"
    取 $P=z,Q=x,R=y$，代入坐标公式得到
    $d\alpha=1\,dy\wedge dz+1\,dz\wedge dx+1\,dx\wedge dy$。

回望时始终先问三件事：积分对象是几形式？参数化的拉回是什么？边界取向是否相容？
