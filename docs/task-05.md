# Task 05 — independent audit of the fixed-modulus first-stage exceptional-prime claim

**Date:** 2026-11-21 Brisbane. Continue prior Task 04. Use **gpt-6.2-sol** exclusively for Codex, no Astra. User authorized danger-full-access, but keep all file reads/writes inside this repo except bounded public HTTPS source retrieval. Never access credentials, change global settings, run the giant upstream proof archive, commit, push or create pull requests. Coordinator will review and publish.

## Goal and exact target

At upstream pinned mirror revision `0fb9869c6e6d7b54b67de803af0e0be29d37fc22`, inspect `QH.stage1` in
`src/Development/AutomorphicArithmetic/MeanSquareBounds/Stage1Succ.lean` lines 36–96. Specialize:
`N₀=24`, `ε=1/100`, `τ=1/200`, `K=2`, `η=1/4`.

The source theorem is **stronger** than the specialization: it asserts a single `∃ C>0` *before* arbitrary ε τ K η N₀, followed by `∃ Y₀` and a uniform bad-set bound for all Y≥Y₀ and every subset B of candidate primes. The expected specialization must preserve this scope. Mathematically, for `P_Y = PPset 8 3 (exp(Y^(1/500)))`, assert P_Y nonempty and every B⊆P_Y of primes failing `GoodQ 24 C (1/200) Y (Y²) (Y^(1/500))` has |B|≤|P_Y|/4. **Do not claim an independent proof of the analytic estimate if you only specialize an author's theorem or test finite data.**

Read `AGENTS.md`, `docs/arithmetic-handoff-audit.md`, `docs/next-research-experiments.md`, `lean/extraction/`, and `data/arithmetic-handoff.json` first.

## Work A: source proof obligations, not a wrapper map

1. Trace `QH.stage1` through `QH.stage` in `StagePow.lean` and its *actual theorem* inputs:
`box_of_S`, `meanSqK`, `bad_share`, `count_bad`, `count_a`, `Formalism.ZeroFreeDirichlet.excBound`, `pnt_progressions_relative_weak_holds`; continue one more level into `MeanSq`, exceptional zero-free box, PNT and mean-square statements. Distinguish proved math vs assumptions stored in `Prop` records, and look for any explicit GRH-equivalent input without assuming circularity.
2. Audit quantifier order of `stage1`, `stage`, and `GoodQ`→`BoxAll`→`Box`→`GoodC`, and `PPset` exact definition and whether `q>sqrt(U)`, `q≤U`, `q%8=3`. Explain why small sample failures cannot refute a statement with an existential Y₀.
3. Pin exact original proof source revision, SHA256 raw bytes, lines and signatures of every source selected, with a **bounded** fetch list (10–18 files with total ≤ ~300 KiB) and distinguish direct code vs inferred mathematical narrative.
4. Produce `docs/stage1-exceptional-primes-audit.md` with precise source claims, actual analytic dependencies, quantitative inequalities and logic: e.g. Markov/union estimate, losses by character-count R, PNT in AP lower bound and how log/power thresholds are chosen. Include failure modes (C or Y₀ depending on Y, invalid mean-square-to-uniform step, principal pole mishandling, q sharing conductor factors, nonempty P_Y).
5. Produce `data/stage1-sources.json`, `tools/check_stage1_sources.py`, offline `tests/test_stage1_sources.py` that verify hashes/lengths/known declaration strings, no unbounded recursion, no false promotion of a conditional source fact to independent proof; be economical.

## Work B: genuine independent finite diagnostics (not GRH tests)

1. Add `tools/mod24_prime_diagnostics.py` (stdlib only, exact integer arithmetic where possible) to enumerate 8 Dirichlet characters modulo 24 via group characters of `(ℤ/24ℤ)^× ≅ (ℤ/2ℤ)^3`. Provide 3 explicit quadratic basis characters (mod3, mod4, mod8), enumerate minimal conductors of each over units, expected sorted multiset [1,3,4,8,8,12,24,24]; don't hardcode the output as a check.
2. For q=11,19 (q≡3 mod8; coprime to 24), multiply each ξ by Legendre/Jacobi q and compute minimal inducing conductor by checking invariance on units mod 24q. Expect eight conductors [fq for f in conductor multiset]. Show actual check and precise `Ind` relation only on coprime inputs. Avoid mistaking ξ(n)*Jq(n) as primitive at level 24q when ξ is imprimitive.
3. Use `PPset` definition to independently calculate P when z=3,4 (U=exp(z)), using a mathematically safe integer interval / known inequalities or document floating approximation as illustrative only. In particular z=3 should give P=[11,19] if the pinned definition uses q>sqrt(U), q≤U; demonstrate that |P|=2 and η=1/4 would force an empty bad subset at that scale if the eventual theorem were assumed to hold, but Y=3^500 need not exceed Y₀.
4. Add `tests/test_mod24_prime_diagnostics.py` for all 8 characters and both q, plus negative controls: dropping q-coprimality, wrong modulus, empty candidate set, or wrongly letting the analytic constant depend on the scale Y. These are correctness sanity checks, **not validations of GoodQ, BoxAll, MeanSq, or zero-free boxes**.

## Work C: optional formal extraction

If feasible, independently reproduce the **exact type** of source-used `stage1_prim` from Stage1Succ (or another concrete small original lemma in the chain), with own proof using pinned Lean/Mathlib 4.33.1 under `lean/extraction`, no `sorry` or untrusted axioms. Run build and axiom audit. If infeasible, record partial and do not add an unrelated toy. Do not count theorem `QH.stage1` as independently reproduced by merely applying the upstream term: that would require actual full original formalization or a new proof of difficult analytic inputs.

## Work D: report and validation

- `docs/codex-task-05-result.md` with source hashes, tests actually run, code coverage and precise unresolved analytic obligation.
- Update `docs/next-research-experiments.md`, `README.md`, `data/claims.json` only after evidence is available.
- Run source hash fetch+offline check, test suite, metadata validator, `git diff --check`, and Lean build only if new Lean code. Check no false claims about public acceptance/proof completion.
- Make no commit/push. Keep generated or fetched files in ignored `.source-tmp/`.
