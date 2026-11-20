# Research plan: audit → simplify → compare → bridge

**Priority:** reconstruct and simplify the two proposals *before* exploring alternatives.

## Phase 0 — Define the target (week 0)

Target: for every primitive Dirichlet character `χ` (with appropriate handling of principal factors), every nontrivial zero of `L(s, χ)` has real part `1/2`. Verify equivalent formulations rather than assuming them.

Deliverables:
- One carefully checked English statement and, when feasible, Lean declaration.
- Clear conventions for trivial zeros, completed L-functions, conductors and character parity.
- Frozen primary-source references and artifact checksums.

## Phase 1 — Separate proof graphs

Create one graph per proposal. Each node must list:
- proposition (full quantifiers), hypotheses and definitions;
- upstream results used, including any imported external theorems;
- provenance: source version + page/declaration;
- evidence status: proposed / reproduced / audited / invalid;
- downstream dependents and possible simplifications.

For Alpöge–Claude, prioritize formal statement audit, axioms/dependencies, theta-lift iteration, and the claimed bridge to the needed arithmetic estimates.

For Masullo, prioritize space definitions, completeness/density hypotheses, orbital bases, operator domains, trace-class/nuclearity assertions, limit interchanges, and the claimed implication for zero locations.

## Phase 2 — Isolate minimal lemmas

Pick **one small bottleneck lemma per proposal**. Re-derive it without depending on the claimed GRH conclusion. Record:
1. a conventional proof with all quantifiers and norms;
2. a dependency-minimal formal proof if tractable;
3. a counterexample search against weakened hypotheses.

Deliverable: independently verifiable technical notes, not a compressed informal claim.

## Phase 3 — Simplification before synthesis

For each selected lemma, try:
- eliminate unused hypotheses;
- replace large tools with standard lemmas;
- bound the depth of iterated constructions;
- find a toy case (e.g. quadratic characters or a finite trace model);
- state exactly which uniform constants are required when limits expand.

A simplification is accepted only if it preserves a complete proof under clearly stated assumptions.

## Phase 4 — Explore explicit bridges

Possible interfaces, **not asserted theorems**:
- theta lift/amplification → a bounded prime-sum or von Mangoldt estimate;
- trace localization → a signed Weil quadratic form;
- both → a shared estimate with parameter-uniform error control.

A bridge task is done only when its input and output are both precise theorems, the arrow is proved, and no hidden GRH assumption is present.

## Phase 5 — Alternatives (deferred)

Open only after producing at least one reviewed lemma or a documented obstruction from Phase 2–4. See [alternatives backlog](alternatives-backlog.md).

## Stop conditions

- Primary theorem is not what its surrounding description suggests.
- Proof relies on unlisted axioms, admits, placeholder proofs, unjustified operator manipulations, or circular implications.
- No versioned source can be obtained for a key step.
- A claimed simplification silently strengthens an intermediate hypothesis.

The appropriate output may be a **precise obstruction report**, not a proof.
