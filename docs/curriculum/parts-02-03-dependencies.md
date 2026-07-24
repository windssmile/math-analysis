# 第二、三部依赖与内容归属

本文规定第二部“数列极限与无限过程”和第三部“函数极限、连续性与方程”的自学改写边界。它是正文改写、单元注册和课程地图更新的共同依据；既有注册表中的 URL 必须保持可用。

## 第三部的学时与核心范围

第三部的正式课程合同为 **理论 32 小时 + 应用 8 小时 = 40 小时**，其中有 **20 个核心单元**。20 个核心单元是权威目标；迁移期间，生成视图可以暂时只显示已注册单元，完成条件仍是注册齐全的 20 个核心单元。

- 第 9 章完整覆盖函数极限的类型：双侧极限、单侧极限、无穷极限及其局部判别语言。
- 第 10 章覆盖一点连续、单侧连续、集合上的连续，以及初等函数与代数运算下的连续性。
- 第 11 章以第二部的 Bolzano–Weierstrass 定理为基础建立序列紧致性；闭区间的紧致性首先按这个序列路径组织。
- 第 12 章明确区分三类证书：存在性证书、区间证书和压缩证书。介值与零点论证提供存在性，二分法提供区间误差证书，压缩映射提供迭代收敛与误差证书。

开覆盖紧致性只作为可选预览，不能挤占第三部核心学时。可选三角函数页面也在注册表和核心学时之外。

## 定理依赖

第二部的完备性证明链为：确界原理 → 单调有界收敛定理 → 区间套定理 → Bolzano–Weierstrass 定理 → Cauchy 收敛准则。第三部使用这条链，但不重复其中的数列论证明。

- 函数极限是连续性理论的直接前提。
- 第二部的 Bolzano–Weierstrass 定理与闭区间的封闭性给出闭区间的序列紧致性：区间内任意序列先由有界性取得收敛子列，再由封闭性保证极限仍在区间内。
- 连续性与序列紧致性给出闭区间上连续函数的有界性、最值存在性和一致连续性。
- 介值定理（包括零点定理）由连续性与第二部的区间套定理推出；它不依赖最值定理或一致连续性。
- 若连续函数 \(g:[a,b]\to[a,b]\)，令 \(h(x)=g(x)-x\)，则对 \(h\) 应用介值定理（零点定理）得到 \(g\) 的不动点；这一存在性结论不保证不动点唯一，也不保证简单迭代收敛。
- 二分法中，介值定理与符号不变量保留含根区间，区间长度公式给出误差证书。
- 压缩映射的唯一性、迭代收敛性和误差界属于第二部；第三部只比较其压缩证书与存在性、区间证书，且需明确回引第二部。

## 与第四部的边界

第四部独立负责导数、微分中值定理、Taylor 公式、Newton 方法和收敛阶。第三部不得把这些微分工具提前计入其核心单元或核心学时。

## 机器校验标记

以下字符串仅用于结构测试；语义以上述中文约定为准。

```text
supremum -> monotone
monotone -> nested intervals
nested intervals -> Bolzano-Weierstrass
Bolzano-Weierstrass -> Cauchy
Part II owns contraction convergence
Part III owns continuous existence
finite function limits -> continuity
Bolzano-Weierstrass + closed interval -> sequential compactness
continuity + sequential compactness -> boundedness/extreme value/uniform continuity
continuity + nested intervals -> IVT
IVT -> continuous self-map fixed point existence
IVT/sign invariant + interval length -> bisection certificates
IVT independent of extreme value and uniform continuity
bisection error independent of compactness
```
