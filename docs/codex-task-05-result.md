# Task 05 — exceptional-prime audit and independently checked conductor reduction

**Date:** 21 November 2026, Brisbane. **Execution:** Codex CLI 0.171.0 with `gpt-6.2-sol` at High reasoning effort (no Astra). Full-access mode was authorized by the user; repository-local work was required. An initial attempt through an Elan shim began automatic toolchain installation and was interrupted; the successful Lean check instead used the already installed **repository-local** Lean 4.33.1 executable. No upstream proof archive was downloaded, built, or executed.

## Result and precise evidence level

The [source audit](stage1-exceptional-primes-audit.md) inspects `QH.stage1` at [pinned Stage1Succ.lean, lines 36–96](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/Stage1Succ.lean#L36-L96). The source theorem selects one positive `C` **before** all other parameters. Specializing to `N₀=24, ε=1/100, τ=1/200, K=2, η=1/4`, it claims a nonempty candidate prime set and an exceptional subset of at most one quarter of that set eventually in `Y`. **We have not independently proved the eventual analytic statement.** The public mirror's proof derives the claim from deeper mean-square, zero-density, and prime-counting theorems that require additional mathematics.

The audit makes the numerical bound explicit. Writing `U=exp(Y^(1/500))`, the source uses `F≤sqrt(U)`, a zero-density count bounded by `C_b(FU)^(1/4)`, and a candidate-prime lower bound `|P|≥U^(9/10)`. Consequently this source branch contributes at most `C_b U^(-21/40)` of candidates. The mean-square branch uses a separate bad-set budget `η/[2(R+1)]`, giving `1/72` for the eight characters and `η=1/4`. Its `bad_share` step uses derivative/integral estimates and dyadic blocks to handle a **different real witness `y_q` for each prime**; merely applying a pointwise mean-square estimate would be invalid.

## Reproducible sources

The [machine-readable source registry](../data/stage1-sources.json) pins **18 Lean files, totalling 134,978 bytes**, to mirror commit `0fb9869c6e6d7b54b67de803af0e0be29d37fc22`. It stores raw SHA-256 hashes and the exact lines and types for the selected declarations. The [allowlisted checker](../tools/check_stage1_sources.py) rejects unexpected files/paths and checks downloaded/cached file lengths, digests, anchors and the extraction's source signature.

**Independently rerun by the coordinating assistant:** `python tools/check_stage1_sources.py` returned exit code 0, matched **18/18** HTTPS raw source files and their anchors, and printed the 134,978-byte total. The offline variant was separately exercised during the Codex pass.

## Finite calculations and negative controls

The [standard-library diagnostic](../tools/mod24_prime_diagnostics.py) evaluates all eight group characters of `(ℤ/24ℤ)^×` using mod-3, mod-4, and mod-8 sign characters, then determines each least inducing conductor by enumerating fibres of the unit-reduction map. The base multiset is `[1,3,4,8,8,12,24,24]`. At `q=11` and `q=19` (coprime to 24), twisted conductors are respectively `[11,33,44,88,88,132,264,264]` and `[19,57,76,152,152,228,456,456]`.

The prime-window calculation encloses `exp(3)` and `exp(4)` with rational Taylor bounds. For `P=PPset 8 3 (exp z)`, it gets `P(3)={11,19}` and `P(4)={11,19,43}`. The integer cap `floor(|P|/4)=0` is only a **conditional consequence** if an eventual bound applied there. It does not: the source's sufficient large-scale conditions include `Y^(1/500)≥48` for `N₀=24`. Its logarithmic threshold also fails at the two illustrative values.

The [finite diagnostics tests](../tests/test_mod24_prime_diagnostics.py) cover the eight distinct characters, multiplicativity, primitive induction under the coprime twist, wrong modulus and nonunit counterexamples, finite prime windows and empty sets. **No numerical experiment computes `GoodQ`, proves a zero-free box, or establishes the asymptotic prime density.**

## Independently reproduced source-used Lean lemma

[`Extraction/Stage1Primitive.lean`](../lean/extraction/Extraction/Stage1Primitive.lean) proves the exact type of the source's `stage1_prim`: every Dirichlet character at a positive modulus has a primitive inducing character of conductor at most that modulus and agreeing on integers coprime to it. The proof is newly written using official pinned Mathlib, and **does not import** the November formal proof archive.

The coordinating assistant independently ran `lake build Extraction` with the repository-local Lean **4.33.1** binary and pinned Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. The command exited **0** with `Build completed successfully (3580 jobs)`; `#print axioms` for `Extraction.stage1_prim` listed only `propext`, `Classical.choice`, and `Quot.sound`. That verifies the small conductor-reduction lemma, **not** `QH.stage1`.

## Validation commands and results

From repository root:

```sh
python tools/check_stage1_sources.py
python tools/check_stage1_sources.py --offline
python tools/mod24_prime_diagnostics.py
python -m unittest discover -s tests -v
python tools/validate_claims.py
git diff --check
```

The independently rerun Python suite passed **25 tests**, including **8 new tests** for source pins and finite diagnostics. The pin checker passed online. The ledger now has **14 source-classified claims**, with the eventual exceptional-prime theorem categorized as **source-inspected**, not independently reproduced. The staged and final Git checks will be recorded by the coordinator before publication.

To rebuild Lean with the existing repository-local Windows toolchain:

```powershell
$repo = (Resolve-Path .).Path
Push-Location (Join-Path $repo 'lean/extraction')
try {
  & (Join-Path $repo '.lean/task-03/lean-4.33.1-windows/bin/lake.exe') build Extraction
} finally {
  Pop-Location
}
```

For a fresh environment, first install `lean/extraction/lean-toolchain` and retrieve the Mathlib cache for the pinned manifest.

## What remains to prove or audit

For `U=exp(Y^(1/500))` and `Z=Y^800`, the main unresolved independent proof target is the uniform mean-square estimate

$
\sum_{q\in P_Y}|S(Z,y,q,\kappa)|^2
\le C_m y\log y\,|P_Y|
$

simultaneously for all sufficiently large `Y`, all real `y∈[Y,Y²]`, and every coefficient sequence with `|κ(n)|≤1`. The source uses `twistK` with `A=1600, B=3` and then `meanSq_abs`, including treatment of **one possible exceptional index** in the quadratic character correlation bound. The selected source files identify, but do not independently validate, the required PNT in AP, exceptional-zero bound, logarithmic derivative/tail estimates and the mean-square proof.

These are the next high-information verification steps. **No new proof or disproof of GRH was obtained.**
