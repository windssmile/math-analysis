# 第一至第九部跨章一致性审查汇总

日期：2026-07-31

汇总基线：`19fd49e`（`codex/part-09-vector-analysis`）

机器基线：`make verify` 通过，**456 tests** 全部通过；`check_content.py`、
`zensical build --strict`（`No issues found`）和 `check_site.py` 均通过；
`git diff --check` 通过。

## 汇总结论

本汇总读取并逐项对照：

- `docs/reviews/2026-07-31-parts-01-09-interface-matrix.md`；
- `docs/reviews/2026-07-31-parts-01-03-cross-chapter-review.md`；
- `docs/reviews/2026-07-31-parts-04-06-cross-chapter-review.md`；
- `docs/reviews/2026-07-31-parts-07-09-cross-chapter-review.md`。

四份材料均已通过独立规格复核与质量复核；复核结论未另立文件，证据保留在原报告及
`a424bdf..19fd49e` 的澄清提交链。本汇总不把复核结论当作新的数学证据，接受项仍须满足
原审查合同中的双侧文本证据。

去重后结论为：**Blocking 0，待修 Important 3，待修 Minor 4，矩阵阶段已解决 4，
拒绝 0**。三份跨章报告的全部 finding 均已处置：第一至三部 I1、M1、M2、M3；第四至
六部 I1、M1（第 20–22 章）；第七至九部 I1。没有只凭关键词缺失、单侧表述或推测接受
新 finding。

修复必须按 `早期定义/接口 → 中期 guide/依赖 → 第八部证明引理 → 出版残留` 的顺序进行。
其中前置缺口先于消费者措辞修复；第 33.4 的核心引理先于第 35.2 的回引。

## 已在接口矩阵阶段解决

以下项目不进入 remediation；相应当前态已经由矩阵、内容与测试双向锁定：

1. **总量口径：** 41 章共 **189 个核心单元、337 学时**，README、课程地图、第九部
   dependency/review 与总量测试一致。
2. **历史里程碑：** 前六部 **125** 个单元、前七部 **150** 个单元，已与闭合提交
   `8b0225f`、`af50860` 及相关设计、依赖、审查和测试统一。
3. **课程地图：** `content/course-map.md` 已补齐第 24–27 章，并把第 1–9 章补到单元级；
   41 个 guide、189 个物理核心页、课程地图和 `mkdocs.yml` 同序。
4. **guide 路由与接口表述：** 已纠正历史 guide 路由/发布表述，并把矩阵的 direct
   prerequisites 与 background interfaces 分栏；41 章规范 direct prerequisite 集合已由
   witness registry 双向锁定。这里的“已解决”不包含下文第 20–22 章仍残留的逐章验收话术，
   也不包含第 26/27 章局部措辞漂移。

## 待修 Important

### P0103-I1（顺序 1）：第 11 章核心证明前借一般开集/闭集理论

- **级别/类型：** Important；forward dependency / 课程接口缺口。不是数学循环，闭区间
  主链可用保序性完整替代。
- **双侧证据：** `content/chapters/chapter-11/u-03-11-01-compact-intervals.md:71-80`
  用“闭集的补集是开集”证明一般闭集保极限，`:102-119` 又证明一般序列紧致集闭且有界；
  但 `content/chapters/chapter-11/index.md:17-24` 声明本章只以 BW 和闭区间为主线、开覆盖
  仅为第七部前瞻，接口矩阵第 11 章也只输出闭区间整体性质。一般开/闭集的正式定义首次
  位于 `content/chapters/chapter-28/`。
- **根因：** 在闭区间定理页顺手加入了一般拓扑推广，却没有同步提升第 9–11 章课程合同和
  front matter。
- **影响：** 自学读者无法从已学材料解释证明中的“开集”“闭集”和补集刻画；前置声明
  不诚实，但闭区间序列紧致、EVT、Heine–Cantor 的结论本身不受影响。
- **精确修复文件：** 修改
  `content/chapters/chapter-11/u-03-11-01-compact-intervals.md`，只保留闭区间序关系证明；
  核验 `content/chapters/chapter-28/u-07-28-02-open-closed-sets.md` 保留一般化责任。
- **TDD 回归：** 先在 `tests/test_chapter_11.py` 增加失败测试：第 11 章核心页不得以未经定义的
  一般闭集/补集开承担证明，同时必须保留 `a <= x_n <= b` 传极限及闭区间序列紧致链；
  在 `tests/test_chapter_28.py` 锁定一般开闭集定义仍存在。
- **验收：** 测试先红后绿；人工重读第 11.1 两处删改与第 28 章首次定义；运行两个聚焦测试、
  `make verify` 和 `git diff --check`。

### P0406-I1（顺序 5）：第 26 章可选背景被写成第 27 章直接输入

- **级别/类型：** Important；direct/background interface drift。
- **双侧证据：** `content/chapters/chapter-27/index.md:27-28` 写“输入是第 26 章与更早章节”，
  `content/chapters/chapter-27/u-06-27-01-approximation-error.md:14-16` 又写“上一章的一致误差
  记号”；但 `docs/curriculum/part-06-dependencies.md:41-44` 与接口矩阵第 27 章把直接输入
  锁为第 10、11、25 章。矩阵第 26 章的输出箭头又容易把出版顺序误读成强依赖。实际
  Bernstein 证明 `u-06-27-02:36-82` 和定量界 `u-06-27-03:36-79` 只用闭区间一致连续、
  二项式有限矩和一致误差，不用收敛半径、逐项运算或解析表示。
- **根因：** guide 用“上一章/输入”描述相邻出版关系，混淆可选解析对照和必要先备。
- **影响：** 读者会误以为必须先学幂级数才能学 Weierstrass–Bernstein；数学证明没有缺口。
- **精确修复文件：** 修改 `content/chapters/chapter-27/index.md`、
  `content/chapters/chapter-27/u-06-27-01-approximation-error.md` 和
  `docs/reviews/2026-07-31-parts-01-09-interface-matrix.md`；必要时同步
  `docs/curriculum/part-06-dependencies.md` 的解释文字，但不得改变已正确的 direct 集合。
- **TDD 回归：** 先在 `tests/test_chapter_27.py` 锁定 guide 不含“输入是第 26 章”及首单元
  不含“上一章的一致误差”，并锁定 front matter 不含幂级数/解析表示；在
  `tests/test_parts_01_09_cross_consistency.py` 锁定 `ch-27` direct 不含 `ch-26`，且 `ch-26`
  只标“可选背景（解析对照）”。
- **验收：** 聚焦测试先红后绿；人工重读 guide、27.1、Bernstein 主证明及矩阵两栏；运行
  两个聚焦模块、`make verify` 和 `git diff --check`。

### P0709-I1（顺序 6）：核心区域积分与换元暗用未证明的边界薄盒覆盖引理

- **级别/类型：** Important；theorem-hypothesis/proof dependency gap。
- **双侧证据：** `content/chapters/chapter-33/u-08-33-04-bounded-regions.md:45-46` 断言有限
  分片光滑边界附近小格贡献可压小，却不证明覆盖估计；
  `content/chapters/chapter-35/u-08-35-02-change-of-variables.md:32-42` 再次依赖边界格总面积
  可压小。全书唯一陈述 Jordan 边界覆盖判据的是
  `content/appendices/part-08-jordan-content.md:41-43`，该附录同样没有证明“有限分片 `C^1`
  边界满足判据”，且 `:8` 与第八部 dependency 明确它不是核心前置。接口矩阵又要求第 33 章
  不以 Jordan/Lebesgue 为前置。
- **根因：** 把几何直观“光滑边界体积为零”当作可直接调用的常识，同时把唯一相关陈述放在
  非前置选读附录。
- **影响：** 自学读者无法沿核心路线证明常用 I/II 型区域的零延拓可积性和经典换元；矩形
  Riemann 积分、连续矩形 Fubini 型定理及可直接分片例题不受影响。
- **精确修复文件：** 在
  `content/chapters/chapter-33/u-08-33-04-bounded-regions.md` 增加完整 `C^1`–Lipschitz
  薄盒覆盖引理和证明；在
  `content/chapters/chapter-35/u-08-35-02-change-of-variables.md` 精确回引；同步核验
  `content/appendices/part-08-jordan-content.md` 仍只是非前置概念重述。
- **TDD 回归：** 先在 `tests/test_chapter_33.py` 锁定稳定定理锚点、紧参数域上导数有界推出
  Lipschitz、曲线片 `O(delta^-1)`/曲面片 `O(delta^-2)` 个直径 `O(delta)` 盒、总面积/体积
  `O(delta)`、有限片求并和共同细分后的振幅控制；在 `tests/test_chapter_35.py` 锁定回引；
  在 `tests/test_part_08_consistency.py` 锁定 Jordan 附录仍非核心、非前置。
- **验收：** 聚焦测试先红后绿；逐行复核维数计数、有限片常数和 Riemann 上下和估计；运行
  `make verify`、`python3.12 scripts/check_content.py`、`zensical build --strict`、
  `python3.12 scripts/check_site.py` 和 `git diff --check`。

## 待修 Minor

### P0103-M1（顺序 3）：压缩映射标题把不动点称为根

- **双侧证据/根因：** `content/chapters/chapter-08/u-02-08-04-contraction-mapping.md:2,34`
  标题写“唯一根”，同页定理 `:101-105` 的对象却是 `g(p)=p` 的唯一不动点；
  `content/chapters/chapter-12/u-03-12-03-fixed-points-and-iteration.md:43-56` 刻意区分不动点
  存在、唯一、迭代收敛与证书。根因是把可经 `f(x)=g(x)-x` 转换的两个对象简称为同一词。
- **影响：** 不改定理正确性，但削弱第 12 章的证书分类。
- **精确修复/TDD：** 修改该第 8.4 页 front matter 标题和 H1；若 guide、课程地图或导航含
  同标题则同步。先在 `tests/test_parts_02_03_migration.py` 锁定所有显示表面使用“唯一不动点”，
  并在 `tests/test_parts_01_09_cross_consistency.py` 锁定课程地图/导航一致。
- **验收：** 测试先红后绿；浏览器核验页面标题和导航；运行聚焦测试、`make verify`、
  `git diff --check`。

### P0103-M2（顺序 2）：开区间反例首项不在声明集合中

- **双侧证据/根因：** `content/chapters/chapter-11/u-03-11-01-compact-intervals.md:123-129`
  写 `x_n=1/n in (0,1)`，又补“从 `n>=2` 开始”；而同页 `:57-67` 的序列紧致定义及
  `content/chapters/chapter-05/u-02-05-01-sequences.md:34-40` 固定本书
  `N={1,2,...}`，故原式 `x_1=1` 不在集合中。根因是尾指标说明没有同步重编号。
- **影响：** 反例思想正确，但原样不是定义要求的 `K` 内数列。
- **精确修复/TDD：** 修改第 11.1 页两处相关公式为 `x_n=1/(n+1)`（含后续回指）；先在
  `tests/test_chapter_11.py` 增加公式与“所有 `n in N` 均落在 `(0,1)`”断言。
- **验收：** 与 P0103-I1 同组重读第 11.1；聚焦测试先红后绿，再跑 `make verify` 和
  `git diff --check`。

### P0103-M3（顺序 4）：第 12 章阅读次序与稳定 unit ID 交叉

- **双侧证据/根因：** `content/chapters/chapter-12/index.md:12-15` 的阅读次序是
  `12-01 -> 12-03 -> 12-02 -> 12-04`；`u-03-12-01:94-96` 因此把不动点称为下一单元，
  `u-03-12-03:88-90` 又把二分称为下一单元。接口矩阵以“IVT、二分、压缩比较”概述责任，
  稳定文件/锚点 ID 则自然诱发 `01 -> 02 -> 03 -> 04` 的节次预期。根因是内容重排后保留
  稳定 ID，却未在 guide 解释 ID 与显示阅读次序的差别。
- **影响：** 当前导航和数学依赖正确；外部引用“12.2/12.3”时可能混淆物理 ID 和显示节次。
- **精确修复/TDD：** 不做高风险物理重命名；修改 `content/chapters/chapter-12/index.md`
  明示稳定 unit ID 不等于显示节次，修改两个“下一单元”回引为标题/稳定锚点；先在
  `tests/test_chapter_12.py` 锁定说明、实际导航顺序及无歧义回引。
- **验收：** 聚焦测试先红后绿；浏览器按 guide 顺序逐页点击并核对 URL/上下页；运行
  `make verify` 和 `git diff --check`。

### P0406-M1（顺序 7）：第 20–22 章 guide 残留开发期发布流程

- **双侧证据/根因：** `content/chapters/chapter-20/index.md:67-69` 和
  `chapter-21/index.md:68-70` 写“验收后停在本章、不创建下一章空白页面”，
  `chapter-22/index.md:99-100` 写“不创建第六部空白页面”；但第 21、22 章和完整第六部
  已发布，第五/六部 dependency 也已声明闭合。根因是逐章开发检查点被保留在正式 guide。
- **影响：** 不影响数学逻辑，但正式出版表面与当前范围矛盾。
- **精确修复/TDD：** 修改上述三个 guide，只保留后续数学职责和范围边界；先在 guide 内容
  测试中截取相应边界段，使用 `re.sub(r"\s+", " ", section)` 规范空白后拒绝“验收后停在”
  及“（暂）不创建……空白页面”等模式，避免跨行漏检。
- **验收：** 测试须先对三处同时变红、修复后变绿；人工核验后续数学边界未被误删；运行
  聚焦测试、`make verify` 和 `git diff --check`。

## Minor 去重与拒绝说明

- **合并：** 第 20、21、22 章三处发布话术共享同一根因、影响、修复形态和空白规范化回归，
  因而合并为一个稳定 finding `P0406-M1`，但验收必须逐处覆盖，不能只修一章。
- **不合并：** `P0103-M1` 是术语对象漂移，`P0103-M2` 是反例索引错误，`P0103-M3` 是
  稳定 ID 与显示顺序的引用歧义；三者的根因、修复文件和回归均不同。
- **拒绝：** 无。四个 Minor 均有双侧证据且经独立复核确认。M3 虽不破坏当前导航，仍有
  可定位的外部引用歧义，因此降为 Minor 而不是拒绝；本轮没有额外接受任何单侧候选。

## 可执行 remediation checklist

### Commit group 1：早期定义与闭区间接口

- [ ] 为 P0103-I1、P0103-M2 先添加失败回归。
- [ ] 用保序性重写第 11.1 的闭区间封闭证明，移除一般开闭集对核心证明的承担。
- [ ] 把 `(0,1)` 反例统一重编号为 `1/(n+1)`。
- [ ] 重读第 11.1 与第 28 章一般化两侧；运行 chapter 11/28 测试、`make verify`、
      `git diff --check`。
- [ ] 建议提交：`docs: close chapter 11 prerequisite interface`。

### Commit group 2：中期 guide、术语与依赖路由

- [ ] 为 P0103-M1、P0103-M3、P0406-I1 先添加失败回归。
- [ ] 统一第 8.4 的“不动点”标题；保留并说明第 12 章稳定 ID，改为无歧义锚点回引。
- [ ] 把第 26 章降为第 27 章可选解析对照，统一 guide、27.1、矩阵两栏和 dependency 解释。
- [ ] 浏览器核验第 8、12、27 章 guide/导航；运行 chapter 8/12/27 与 cross-consistency 测试、
      `make verify`、`git diff --check`。
- [ ] 建议提交：`docs: align fixed-point and approximation interfaces`。

### Commit group 3：第八部核心证明引理

- [ ] 为 P0709-I1 先添加覆盖估计、回引和非前置附录的失败回归。
- [ ] 在 33.4 完整证明 `C^1` 参数片的 Lipschitz 薄盒覆盖与边界格振幅控制。
- [ ] 在 35.2 回引稳定锚点；保持 Jordan 附录为选读且非前置。
- [ ] 逐行数学复核后运行 chapter 33/35 与 part 08 测试、全套四门发布 gate、
      `git diff --check`。
- [ ] 建议提交：`docs: prove the boundary thin-box lemma`。

### Commit group 4：出版残留

- [ ] 为 P0406-M1 先添加 normalize-whitespace 后覆盖三章的失败回归。
- [ ] 删除第 20–22 章 guide 的开发流程话术，保留数学后续边界。
- [ ] 运行聚焦测试、`make verify` 和 `git diff --check`。
- [ ] 建议提交：`docs: remove stale guide publication workflow`。

## 已核验无问题链

- **完备性主链：** Dedekind/确界 → 单调有界 → 区间套 → BW → Cauchy，未见循环；
  P0103-I1 只涉及一般拓扑的放置。
- **极限与求根证书：** 数列/函数极限量词、IVT、二分、连续自映射与压缩证书边界一致；
  算法停止、残差和有限样本均未冒充存在唯一性或误差证明。
- **一元微积分链：** 导数定义 → 法则 → 中值定理 → 有限 Taylor → 原函数 → 独立的
  Riemann 定义 → FTC → 反常积分/求积，未发现反向定义或后置前借。
- **级数与逼近链：** 数项级数 → 一致收敛 → 幂级数单向闭合；Bernstein 从第 10、11、25 章
  分叉。P0406-I1 是接口措辞，不是证明缺口。
- **多元分析链：** Euclid 拓扑 → Frechet/Jacobian → 高阶/Taylor → IFT/隐函数 →
  Lagrange/优化，有限维、局部/全局、必要/充分及数值非证书边界均明确。
- **重积分与向量分析链：** 矩形 Riemann、经典累次积分、曲线/曲面、Green、盒复形 Gauss、
  单片/有限兼容片 Stokes 的陈述范围、正则性、取向、奇点挖除和数值非证书语义一致；唯一
  待闭合的核心证明输入是 P0709-I1。
- **附录边界：** Jordan 与微分形式附录均未进入核心学时、考核或 front matter 前置；微分
  形式附录没有反向承担三大公式证明。

完成四组修复后，须由独立 reviewer 逐项核销 7 个稳定 ID，并在最终全书审查中记录每项的
失败测试、修复提交、双侧重读与全 gate 结果；不得仅以“456 tests 通过”替代数学验收。
