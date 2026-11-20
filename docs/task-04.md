# Task 04 — open the arithmetic core and produce a reproducible source dependency map

Date 2026-11-21 Brisbane. Continue from completed Task 03; use **Codex gpt-6.2-sol only** (no Astra). Run in the user's explicitly authorized full-access CLI mode, but confine file reads/writes to this repository, except HTTPS retrieval of public primary-source text. Do not access secrets/user files, modify global settings, clone/execute the huge upstream submitted proof, download unbounded files, open GH PRs, commit or push.

## Existing proof-evidence boundary
Task 03 extracted and Lean-checked the elementary `Claim.factor_ne_zero` with original type, and checked the three conditional Dirichlet predicate equivalences. No complete GRH proof was reproduced locally; the semantic implications are CONDITIONAL. Our real next question is the giant arithmetic implication to nonvanishing, not an equivalent criterion.

## Source pins
Submission mirror commit `0fb9869c6e6d7b54b67de803af0e0be29d37fc22`:
- root source: https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/
- `Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean`
- `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean`
- `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` may be in a different file; discover its unique declaration path via GitHub repository tree API and exact pinned raw files. Prefer provider GitHub API or bounded requests; do not recursively fetch 175k files.
- `UpperTheory.Top.VWin` and `UpperTheory.One.vwin_of_row` may be vital. Find exact definitions & constructor inputs, and distinguish an abbreviation/record of hypotheses from hard mathematical theorems.

Read `AGENTS.md`, `docs/entrypoint-lean-dependency-map.md`, `docs/next-research-experiments.md`, `docs/semantic-audit-dirichlet.md` and research status.

## Main deliverables

**A. Pin actual source and draw typed handoff graph.**
Find `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` at the exact upstream commit. Extract its complete Lean theorem statement/outer binders, its immediately referenced proof constants, and the exact source segments calling it in `EveryCharacterOfLiteratureOfVWin`. For each provided hypothesis in its type, identify a named producer of that hypothesis and, when feasible, its own mathematical content. Track the conjunction's first & second projection and `UpperTheory.Top.VWin`. Record line ranges, SHA-256 and exact repo links. Avoid guessing that a named theorem is doing deep work: show whether it is a wrapper forwarding a **strong assumed Prop**, or a theorem with real analytic proof.

Deliver `docs/arithmetic-handoff-audit.md` including:
- exact source signature (quoted minimally), normalized English theorem, declared assumptions and their precise role;
- 2–3 levels of graph edges FROM the public `Main.lean` GRH target down to theta integrals and local matching, with `source-backed` vs `inferred` annotations;
- first actual analytic estimate encountered, with all quantifiers and parameter dependencies (`X, m, conductor, rank, level, constants`) if present; if absent say which source file still hides it;
- assessment of whether any nonvanishing is smuggled into a hypothesis or whether this is just a restatement (don't call circularity absent actual proof).
- one ranked bottleneck with a precise proposed next independent lemma, including expected test data and failure modes.

**B. Reproducible receipt and mechanical source audit.**
Add a small script `tools/check_arithmetic_handoff.py` that downloads only a bounded allowlist of pinned Lean source files, checks byte-length+hash and exact declaration/call-site strings (or a robust regex), generates an **offline** `data/arithmetic-handoff.json` data registry with nodes, edges, source IDs and `status` but not an inferred transitive proof graph. Avoid brittle URL crawling and do not execute remote files. Add offline `tests/test_arithmetic_handoff.py` for schema, pins, graph edges resolve, invalid refs and distinction between source-inspected and hypothetical. If source size too big to fetch, mark partial and don't fake checks.

**C. One meaningful targeted mathematical check if possible.**
Find a small genuine sublemma used by the proof, preferably a symbolic estimate, discriminant/trace inequality, scalar bound, or theta-integral estimate. If it can be copied EXACTLY into existing `lean/extraction` without heavy new imports, independently prove it there. Include a known negative control that tests the main hypothesis. Run pinned Lean 4.33.1 `lake build Extraction` and `#print axioms`. If infeasible, make an *explicit conditional lemma skeleton as an exercise only*, not a proof. Do not pad the repo with irrelevant trivialities: source trace alone with sharply stated obstacle is preferable.

**D. Update README and research priority.**
Revise `docs/next-research-experiments.md`, `docs/entrypoint-lean-dependency-map.md`, `README.md` narrowly; preserve statuses. Prepare `docs/codex-task-04-result.md` with specific run commands, hashes, tests, limits and candidate next work. Don't commit/push. Read existing `docs/task-03.md` if needed for evidence conventions.

## Validation and safety
- All Python tests, source checker(s), `git diff --check`, and if new/modified Lean then actual Lean build.
- A coherent audit of source-level *mathematical hypotheses* is the real success criterion, not merely the existence of documentation.
- Bound research to a first source-level pass; if file discovery fails, record what is blocked and continue via independent Mathlib/author notes.
