# Chapter 26 Power Series and Analytic Representation Implementation Plan

**Goal:** Publish five self-study units that derive convergence radius, compact-subinterval
uniformity, termwise operations, analytic representation, and reliable standard expansions.

## Locked registry

```python
EXPECTED_UNITS = [
    ("u-06-26-01", "系数怎样决定收敛半径？", 1.25, 0.25, "radius", 8, 10),
    ("u-06-26-02", "幂级数为什么在收敛区间内部表现稳定？", 1.25, 0.25, "interior-uniformity", 8, 10),
    ("u-06-26-03", "为什么幂级数可以逐项积分与微分？", 1.25, 0.25, "termwise-operations", 9, 11),
    ("u-06-26-04", "Taylor 级数什么时候真的等于原函数？", 1.25, 0.50, "taylor-analytic", 9, 11),
    ("u-06-26-05", "常用展开怎样形成可靠计算工具？", 1.00, 0.75, "standard-expansions", 12, 15),
]
```

Totals: 5 units, 6 theory hours, 2 application hours, 8 hours, 46 exercises, 57 answers.

## Proof and scope contracts

1. Derive Cauchy–Hadamard from root-test control; prove inside absolute convergence and outside
   divergence; test endpoints separately.
2. Prove uniform absolute convergence on every \(|x-x_0|\le r<R\) by the M-test. Never replace
   “every compact subinterval” with uniformity on the full open interval.
3. Prove derivative series has the same radius, then invoke Chapter 25 legitimately for termwise
   integration and differentiation; prove coefficient uniqueness.
4. Separate finite Taylor polynomial, Taylor series, and equality with the function. Give a
   remainder criterion and prove the smooth non-analytic \(e^{-1/x^2}\) example.
5. Derive geometric, exponential, sine, cosine, logarithmic, and binomial expansions with domains,
   endpoints, and explicit error sources. Include the course-level real Abel endpoint theorem.

## Publication

- Move release boundary to Chapter 26: 20 Part VI units, 35 hours, 118 total units.
- Add Chapter 26 navigation only and no Chapter 27 placeholder.
- Add representative rendered anchors for radius, termwise operations, and analytic boundary.
- Run all gates and record a Chapter 26 audit before Chapter 27.

