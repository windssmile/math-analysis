# Chapter 25 Function Sequences, Function Series, and Uniform Convergence Implementation Plan

> **Execution:** Follow the existing sequential, test-first chapter workflow.

**Goal:** Publish five rigorous self-study units that distinguish pointwise from uniform convergence,
establish uniform Cauchy and series tests, and prove the exact hypotheses permitting continuity,
integration, and differentiation to pass through limits.

**Architecture:** Lock metadata, proof anchors, quantifier boundaries, counterexamples, training
density, publication scope, and rendered anchors in failing tests. Write units in dependency order.
Do not use power-series theory to prove the general results of this chapter.

## Locked registry

```python
EXPECTED_UNITS = [
    ("u-06-25-01", "逐点收敛为什么不足以控制整体行为？", 1.25, 0.50, "pointwise-uniform", 8, 10),
    ("u-06-25-02", "怎样用统一尾部控制刻画一致收敛？", 1.50, 0.25, "uniform-cauchy", 9, 11),
    ("u-06-25-03", "函数项级数怎样获得一致收敛判别？", 1.50, 0.50, "uniform-series-tests", 10, 12),
    ("u-06-25-04", "极限什么时候可以穿过连续与积分？", 1.50, 0.25, "continuity-integration", 9, 11),
    ("u-06-25-05", "微分为什么需要比积分更强的条件？", 1.25, 0.50, "differentiation", 10, 13),
]
```

Totals: 5 units, 7 theory hours, 2 application hours, 9 hours, 46 exercises, 57 folded answers.

## Required proof chain

1. `25.1`: define pointwise and uniform convergence with explicit quantifier order; use \(x^n\)
   on \([0,1]\) and sup-error calculations to separate them.
2. `25.2`: prove both directions of the uniform Cauchy criterion using real completeness; derive
   the uniform series-tail criterion and state the finite/infinite supremum boundary.
3. `25.3`: prove the Weierstrass M-test, uniform Dirichlet test, and uniform Abel test; distinguish
   uniform absolute convergence, pointwise absolute convergence, and uniform convergence.
4. `25.4`: prove preservation of continuity and the closed-interval Riemann integral interchange;
   derive termwise integration and retain a pointwise counterexample.
5. `25.5`: from \(f_n\in C^1([a,b])\), uniform convergence of \(f_n'\), and convergence at one
   base point, prove uniform convergence to a differentiable limit and derivative interchange.
   Include counterexamples showing uniform convergence alone is insufficient.

## Publication and audit

- Move the release boundary to Chapter 25: 15 Part VI units, 27 hours, 113 total units.
- Add Chapter 25 navigation only; do not create Chapter 26 pages.
- Add rendered checks for quantifiers, uniform Cauchy/M-test, and differentiation interchange.
- Run chapter tests, all unit tests, content validation, strict build, site validation, and
  `make verify`.
- Record a Chapter 25 mathematical/pedagogical/publication audit before proceeding to Chapter 26.

