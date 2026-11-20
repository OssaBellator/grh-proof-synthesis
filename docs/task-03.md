# Task 03 — Extract a source-used Euler factor theorem and check Dirichlet GRH semantics

Date: 2026-11-21 Brisbane. Use **gpt-6.2-sol only** for Codex; never Astra. This is a focused continuation of the public research repository. The user's prior full-access authorization applies but restrict **actual filesystem operations to this repo**. Do not access unrelated user files, change global configurations, execute untrusted proof archives or push commits.

Read AGENTS.md, docs/entrypoint-lean-dependency-map.md and docs/next-research-experiments.md, then docs/dependency-map-alpoge.md and data/claims.json.

## Key source pins, no invented mathematical statements

Lean proof mirror at commit `0fb9869c6e6d7b54b67de803af0e0be29d37fc22`:
- https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean
- https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Statements.lean
- https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Main.lean
- Official Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`, Lean 4.33.1. Relevant Dirichlet continuation, complex powers and character norm facts.

## Objective A: independently reproduce a **source-used** small lemma

1. Inspect the **exact** type and proof of `Claim.factor_ne_zero` in pinned ClaimStrip and the call site inside `Claim.prim_zero`. Determine all explicit/implicit assumptions.
2. Establish a clean Lean 4.33.1 / Mathlib v4.33.1 standalone project in e.g. `lean/extraction/` with pinned toolchain and mathlib revision. Prefer minimal Mathlib import or `import Mathlib` as reliable fallback. You MAY download official Mathlib sources/cache as trusted dependencies, but **do not download Alpöge's massive source archive**. Keep generated .lake/caches excluded from Git. Do not modify user's global Lean config; local build only. If package downloads too large or impossible, record exact error and use an honest uncompiled code sketch rather than claim success.
3. Copy exact original theorem statement to the independent project (new theorem namespace), then write your OWN proof using standard Mathlib lemmas and no author proof imports. Avoid `sorry`, `admit`, and new axioms. Check `#print axioms` for your declaration.
4. Test expected cases: χ=1 mod 1 at p=2, s=1 (nonzero); s=0 SHOULD fail if strict Re(s)>0 is dropped; for χ=1 mod 6 and p=2 dividing modulus factor equals 1; at s=i t edge cases cannot be covered by lemma. Prefer Lean checks if feasible or separate mathematical verification with explicit status.
5. Write `docs/claim-factor-extraction.md` explaining theorem, exact source URL/lines, independent proof, analytic reasoning, results, exclusions and all commands & status.
6. A small `tests/test_extraction_metadata.py` can check source digest/pins and no `sorry`/admit statements if useful, but never equate grep with formal proof verification.

## Objective B: semantic audit of the actual five headline GRH predicates

1. Inspect pinned Statements/Mathlib from `docs/entrypoint-lean-dependency-map.md`; map the exact quantifiers and target proposition to classical Dirichlet GRH, including imprimitive Euler factors, principal character at s=1, modulus 1, zero/pole handling, open strip boundaries and s with Re(s)>1.
2. Write `docs/semantic-audit-dirichlet.md` with a **truthful** case matrix and precise mathematical implications. Show which implications can be deduced by elementary classical analytic continuation and functional equation, and identify lemmas requiring external mathematics. Do not conflate “the statements look equivalent” with a completed Lean theorem. Explicitly distinguish RiemannHypothesis from custom Dirichlet predicates. If a rigorous counterexample to equivalence exists, state it with full proof; if not, report open obligations.
3. If feasible write a smaller Lean semantics test with only Mathlib to confirm source definitions and a case-based proposition (e.g. principal pole guard) and run it; make success claims only for actual run.

## Objective C: next priorities

Update `docs/next-research-experiments.md` and `README.md` with concrete results. Record the **next nontrivial node** past `Claim.factor_ne_zero` to explore (avoid presenting Euler-factor lemma as the main novelty). Keep a task run report `docs/codex-task-03-result.md`, including commands, source/pin hashes, tests, unresolved questions. Do not change established source classifications without new evidence.

## Checks

Run relevant Lean checks and Python tests if possible. Record actual results separately. Keep all files in repository. Stage/commit/push NOTHING; coordinator will review and publish. Do not run a giant formal proof archive. Accuracy > output quantity.
