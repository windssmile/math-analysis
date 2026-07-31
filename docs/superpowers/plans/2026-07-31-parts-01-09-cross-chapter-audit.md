# Parts I–IX Cross-Chapter Consistency Audit Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to execute this plan sequentially. Audit agents are read-only; remediation agents use TDD and commit fixes. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-read Parts I–IX from the beginning, find and repair cross-chapter logical contradictions, prerequisite inversions, terminology drift, duplicated or misplaced responsibilities, and publication-order problems.

**Architecture:** Build one authoritative chapter-interface matrix, then audit the book in reading order in three bounded passes. Consolidate only evidence-backed findings, remediate them by dependency order, and finish with an independent whole-book review plus all existing and new quality gates.

**Tech Stack:** Markdown/Zensical content, Python 3.12 `unittest`, existing dependency maps and chapter tests, `scripts/check_content.py`, post-build `scripts/check_site.py`, browser checks at 390×844, and Git.

---

## Audit evidence contract

Every reported issue must include:

- source chapter/unit and exact statement;
- conflicting chapter/unit or missing prerequisite;
- issue class: contradiction, forward dependency, terminology drift, responsibility duplication, theorem-hypothesis mismatch, notation/normalization drift, or sequencing problem;
- mathematical impact and reader impact;
- proposed correction and why it preserves already approved scope;
- a regression check capable of detecting recurrence.

Absence of a keyword is not evidence of consistency. Auditors must read theorem statements, proof inputs, examples, exercises, chapter guides, course map, dependency maps, and prior consistency reviews.

## Task 1: Build the authoritative Parts I–IX interface matrix

**Files:**
- Create: `docs/reviews/2026-07-31-parts-01-09-interface-matrix.md`
- Create: `tests/test_parts_01_09_cross_consistency.py`

- [ ] Inventory all 41 chapter guides and 186 core unit front matters in reading order.
- [ ] Record for each chapter: unique responsibility, direct prerequisites, exported results, forbidden forward dependencies, notation introduced, and later consumers.
- [ ] Add tests that compare matrix chapter/unit inventory with actual content, navigation, course map, and declared prerequisites.
- [ ] Run the new test and the existing full gate, then commit the matrix.

## Task 2: Audit Parts I–III and their outgoing interfaces

**Scope:** Chapters 1–12, including foundations, real-number completeness, limits, continuity, compactness on intervals, existence theorems, and iterative solving.

- [ ] Read every guide and core unit in order; compare definitions and theorem hypotheses with later uses in Parts IV–IX.
- [ ] Check especially: completeness/compactness dependencies, sequence versus function limit language, continuity/existence assumptions, contraction and bisection certificates, and terminology reused in multivariable chapters.
- [ ] Record evidence-backed findings in `docs/reviews/2026-07-31-parts-01-03-cross-chapter-review.md` without editing content.

## Task 3: Audit Parts IV–VI and their incoming/outgoing interfaces

**Scope:** Chapters 13–27, differentiation, Taylor theory, one-variable integration, numerical certificates, series, uniform convergence, power series, and approximation.

- [ ] Check every proof uses only prior results or explicitly restated inputs.
- [ ] Compare derivative/Taylor hypotheses, Riemann integrability language, improper-limit conventions, numerical certificate semantics, and uniform-convergence interchange rules with Parts VII–IX.
- [ ] Record findings in `docs/reviews/2026-07-31-parts-04-06-cross-chapter-review.md` without editing content.

## Task 4: Audit Parts VII–IX and the complete multivariable chain

**Scope:** Chapters 28–41 plus the Jordan and differential-forms appendices.

- [ ] Verify the chain Euclid topology → Fréchet derivative → inverse/implicit functions → multiple integration → parameterized curves/surfaces → Green/Gauss/Stokes.
- [ ] Check Jacobian, regularity, orientation, boundary, singularity, and numerical non-certificate conventions across every transition.
- [ ] Check the optional appendices never become core prerequisites or retroactive proofs.
- [ ] Record findings in `docs/reviews/2026-07-31-parts-07-09-cross-chapter-review.md` without editing content.

## Task 5: Consolidate and prioritize the whole-book findings

**Files:**
- Create: `docs/reviews/2026-07-31-parts-01-09-cross-chapter-audit.md`

- [ ] Deduplicate findings and reject any claim lacking two-sided textual evidence.
- [ ] Order accepted findings by prerequisite direction, with earlier definitions fixed before later consumers.
- [ ] Classify each as blocking logic, important pedagogy, or minor consistency.
- [ ] Produce a remediation checklist mapping every accepted issue to files, tests, and verification evidence.

## Task 6: Remediate accepted findings in dependency order

- [ ] For each finding, first add or strengthen a regression test that fails for the documented contradiction.
- [ ] Make the smallest mathematically complete correction; update all affected later consumers, guides, maps, and reviews.
- [ ] Run focused tests and commit each dependency-closed remediation group separately.
- [ ] Re-read both sides of every repaired interface; a green keyword test alone is insufficient.

## Task 7: Close the Parts I–IX audit

**Files:**
- Create: `docs/reviews/2026-07-31-parts-01-09-final-consistency-review.md`
- Strengthen: `tests/test_parts_01_09_cross_consistency.py`

- [ ] Dispatch an independent final reviewer over the complete branch diff and all four audit reports.
- [ ] Run `make verify`, `python3.12 scripts/check_content.py`, `zensical build --strict`, `python3.12 scripts/check_site.py`, and `git diff --check` from a clean generated-site state.
- [ ] Browser-check representative dependency transitions and every page changed by remediation at 390×844.
- [ ] Record resolved findings, accepted scope boundaries, exact command results, and any non-blocking future work.
- [ ] Confirm Part IX remains closed, Chapter 42 is absent, and no optional appendix has entered core prerequisites.
