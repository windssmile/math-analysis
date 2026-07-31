# Chapter 27 Polynomial Approximation and Error Control Implementation Plan

**Goal:** Publish four self-study units that formulate uniform approximation, prove the constructive
Bernstein–Weierstrass theorem, derive quantitative error bounds, and provide one tested reliable
Bernstein implementation.

## Locked registry

```python
EXPECTED_UNITS = [
    ("u-06-27-01", "函数逼近问题应怎样衡量误差？", 0.75, 0.75, "approximation-error", 8, 10),
    ("u-06-27-02", "Bernstein 多项式怎样逼近连续函数？", 1.50, 0.25, "bernstein-weierstrass", 9, 11),
    ("u-06-27-03", "连续性模怎样给出显式误差界？", 1.00, 0.75, "modulus-error", 9, 11),
    ("u-06-27-04", "怎样可靠构造并评价逼近多项式？", 0.25, 1.75, "reliable-bernstein", 12, 15),
]
```

Totals: 4 units, 3.5 theory hours, 3.5 application hours, 7 hours, 38 exercises, 47 answers.

## Proof contracts

1. Define uniform error and best-error infimum without asserting attainment. Separate interpolation,
   least squares, pointwise approximation, and uniform approximation; include Runge-type failure and
   affine normalization.
2. Define Bernstein weights, prove positivity, partition of unity, preservation of constants and
   linear functions, and the exact second central moment. Prove uniform convergence by splitting
   near and far indices using uniform continuity, without probability theory.
3. Define the modulus of continuity and derive a visible uniform Bernstein bound. Give Lipschitz
   degree budgets and a second-derivative estimate; keep theoretical bounds separate from grid
   observations and unknown true sup errors.
4. Implement the required sequence
   `问题来源 → 数学转化 → 算法思想 → 误差与适用条件 → 伪代码 → Python → 结果解释`.
   Reuse one tested source module, evaluate Bernstein weights stably, validate all inputs, and never
   label grid error as a certificate.

## Engineering and publication

- Add `src/mathbook_examples/approximation.py` and `tests/test_approximation.py`.
- Move release boundary to all of Part VI: 24 units, 42 hours, 125 total units.
- Add Chapter 27 navigation and representative rendered checks.
- Run all gates, audit Chapter 27, then perform a separate full Part VI dependency, proof,
  pedagogy, publication, and rendered-site audit.
