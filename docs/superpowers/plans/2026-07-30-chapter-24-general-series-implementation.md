# Chapter 24 General Series, Rearrangements, and Products Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Chapter 24 as five rigorous self-study units that close the number-series stage through absolute/conditional convergence, summation by parts, rearrangements, Cauchy products, and integrated diagnosis.

**Architecture:** Lock exact metadata, theorem conditions, proof anchors, training density, scope, publication, and rendered anchors in failing tests. Write units in dependency order, update the Part VI dependency map from Chapter 23 to Chapter 24 only after all five units pass, then run a chapter audit. Reuse the Chapter 23 certificate implementation; do not add a purported general convergence-deciding algorithm.

**Tech Stack:** Markdown with YAML front matter and MathJax, Python 3.12 `unittest`, PyYAML, Zensical/MkDocs, existing content and site validation scripts.

---

## File map

**Create**

- `content/chapters/chapter-24/index.md`
- `content/chapters/chapter-24/u-06-24-01-absolute-conditional.md`
- `content/chapters/chapter-24/u-06-24-02-leibniz-dirichlet-abel.md`
- `content/chapters/chapter-24/u-06-24-03-rearrangements.md`
- `content/chapters/chapter-24/u-06-24-04-cauchy-products.md`
- `content/chapters/chapter-24/u-06-24-05-series-diagnosis.md`
- `tests/test_chapter_24.py`
- `docs/reviews/2026-07-30-chapter-24-and-number-series-review.md`

**Modify**

- `README.md`
- `content/course-map.md`
- `docs/curriculum/part-06-dependencies.md`
- `mkdocs.yml`
- `scripts/check_site.py`
- current-release assertions in `tests/test_chapter_15.py` through `tests/test_chapter_23.py`
- `tests/test_part_04_consistency.py`
- `tests/test_zensical_structure.py`
- `tests/test_mkdocs_site.py`

## Locked registry

```python
EXPECTED_UNITS = [
    ("u-06-24-01", "绝对收敛为什么能够控制符号变化？", 1.50, 0.25, "absolute-conditional", 8, 10),
    ("u-06-24-02", "交错与振荡级数怎样利用抵消？", 1.50, 0.50, "leibniz-dirichlet-abel", 9, 11),
    ("u-06-24-03", "改变求和次序为什么可能改变结果？", 1.75, 0.25, "rearrangements", 10, 12),
    ("u-06-24-04", "两个无穷和什么时候可以相乘？", 1.75, 0.25, "cauchy-products", 9, 11),
    ("u-06-24-05", "怎样选择判别法并给出收敛证书？", 1.00, 0.75, "series-diagnosis", 12, 15),
]
```

Exact totals: 5 units, 7.5 theory hours, 2 application hours, 9.5 hours, 48 exercises, 59 folded answers.

### Task 1: Lock failing Chapter 24 contracts

- [ ] Create `tests/test_chapter_24.py` using the Chapter 23 parser pattern.
- [ ] Require exact registry, totals, H1 anchors, two anchored examples per page, two immediate checks in Units 24.1–24.4, three in Unit 24.5, and exact exercise/answer counts.
- [ ] Lock proof anchors:

```python
REQUIRED_ANCHORS = {
    "u-06-24-01": (
        "def-u-06-24-01-absolute-conditional",
        "thm-u-06-24-01-absolute-implies-convergence",
        "thm-u-06-24-01-positive-negative-parts",
    ),
    "u-06-24-02": (
        "thm-u-06-24-02-leibniz",
        "cor-u-06-24-02-alternating-remainder",
        "lem-u-06-24-02-summation-by-parts",
        "thm-u-06-24-02-dirichlet",
        "cor-u-06-24-02-abel",
    ),
    "u-06-24-03": (
        "def-u-06-24-03-rearrangement",
        "thm-u-06-24-03-absolute-rearrangement",
        "lem-u-06-24-03-positive-negative-diverge",
        "thm-u-06-24-03-riemann-rearrangement",
    ),
    "u-06-24-04": (
        "def-u-06-24-04-cauchy-product",
        "thm-u-06-24-04-mertens",
        "ex-u-06-24-04-conditional-failure",
    ),
    "u-06-24-05": (
        "alg-u-06-24-05-decision-workflow",
        "tbl-u-06-24-05-test-boundaries",
        "tbl-u-06-24-05-operation-safety",
    ),
}
```

- [ ] Focused tests must require:
  - positive/negative part decomposition and absolute convergence via Cauchy tails;
  - Leibniz monotonicity, zero limit, first-omitted-term bound, finite summation by parts, Dirichlet bounded partial sums, and Abel reduction;
  - absolute rearrangement invariance and the target-overshoot/pullback proof of Riemann rearrangement;
  - distinction between square and triangular finite sums, with Mertens requiring at least one absolute factor;
  - diagnosis that an inconclusive test is not divergence.
- [ ] Forbid function-series, uniform-convergence, power-series, Fourier, Lebesgue, and double-series/Fubini theory before boundary sections.
- [ ] Run `python3.12 -m unittest tests.test_chapter_24 -v`; verify red for missing files.
- [ ] Commit `test: lock chapter 24 general series contracts`.

### Task 2: Write the guide and Units 24.1–24.2

- [ ] Create Chapter 24 guide with exact route:

```text
绝对值控制 → 条件抵消 → 分部求和 → Dirichlet–Abel → 重排 → 乘积 → 综合诊断
```

- [ ] Unit 24.1 must prove absolute convergence through the Cauchy tail criterion, define \(a_n^+=\max(a_n,0)\), \(a_n^-=\max(-a_n,0)\), and prove the positive/negative-part characterization.
- [ ] Unit 24.2 must derive finite summation by parts before Dirichlet and Abel, identify every hypothesis where used, and derive the Leibniz first-omitted-term bound.
- [ ] Run focused tests and `scripts/check_content.py`.
- [ ] Commit each unit separately.

### Task 3: Write Unit 24.3 — rearrangements

- [ ] Define rearrangement using a bijection of \(\mathbb N\).
- [ ] Prove absolute-convergence invariance by capturing a finite head and controlling the absolute tail.
- [ ] Prove that a conditionally convergent real series has divergent positive and negative masses.
- [ ] Construct Riemann rearrangement by adding positive terms until crossing a target, then negative terms until falling below it; prove overshoots tend to zero because terms tend to zero.
- [ ] Cover rearrangements to \(\pm\infty\) and divergence as extensions, not substitutes for the finite-target proof.
- [ ] Run focused tests and commit.

### Task 4: Write Unit 24.4 — Cauchy products

- [ ] Define \(c_n=\sum_{k=0}^{n}a_kb_{n-k}\).
- [ ] Show why \(A_NB_N\) is a square finite sum while \(\sum_{n=0}^{N}c_n\) is triangular.
- [ ] Prove Mertens with one series absolutely convergent and the other convergent; keep the remainder decomposition explicit.
- [ ] Give a conditional-product counterexample whose Cauchy-product terms fail the term test.
- [ ] State that both factors absolutely convergent is a safe corollary.
- [ ] Do not invoke general double-series or Fubini/Tonelli theory.
- [ ] Run focused tests and commit.

### Task 5: Write Unit 24.5 and publish

- [ ] Build a method-selection table covering term test, positive comparison, ratio/root, integral/condensation, absolute convergence, Leibniz, Dirichlet–Abel, rearrangement, and product legality.
- [ ] Require every solution to state object type, hypotheses, conclusion strength, remainder/certificate availability, and failure boundary.
- [ ] Include 12 unlabelled mixed exercises and 15 answers.
- [ ] Update Part VI dependency status to Chapter 24: 10 published units, 18 hours.
- [ ] Update README/course map to Chapter 24 and 108 units.
- [ ] Add only Chapter 24 navigation; do not create Chapter 25 pages.
- [ ] Add representative rendered anchors for Units 24.2–24.4.
- [ ] Run `make verify`, inspect rendered pages, and commit publication.

### Task 6: Audit the complete number-series stage

- [ ] Create `docs/reviews/2026-07-30-chapter-24-and-number-series-review.md`.
- [ ] Audit Chapters 23–24 as one proof chain: definitions, positive tests, cancellation, rearrangement, product legality, certificates, training, and scope.
- [ ] Confirm 10 published Part VI units and 18 hours; confirm no Chapter 25 page exists.
- [ ] Run `make verify`, `python3.12 scripts/check_content.py`, `zensical build --clean --strict`, `python3.12 scripts/check_site.py`, and `git diff --check`.
- [ ] Record exact test/build results and commit the review.

## Plan self-review

- All five approved units, exact 9.5-hour allocation, theorem conditions, training, publication, rendered anchors, and number-series-stage audit are mapped.
- The plan introduces no new algorithm beyond the approved Chapter 23 certificate helpers.
- Chapter 25 and later remain outside this implementation and have no placeholder pages.

