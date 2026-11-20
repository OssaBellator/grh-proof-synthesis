# Task 03 — reviewed execution record

**Date:** 21 November 2026 (Australia/Brisbane). **CLI:** Codex 0.171.0, `gpt-6.2-sol`, High reasoning effort, user-authorized full-access mode. **No Astra used.** Work was confined to this repository.

## Scope

This pass independently extracted **one existing, source-used elementary lemma** from the Alpöge–Claude Lean submission and proved conditional relationships among its Dirichlet statements. **It did not reproduce the entire submitted proof, establish GRH, or audit the substantive theta-lift estimates.**

- Original pinned mirror: [CocoSgt at commit 0fb9869c6e6d7b54b67de803af0e0be29d37fc22](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/0fb9869c6e6d7b54b67de803af0e0be29d37fc22)
- Source file [`ClaimStrip.lean`](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean#L7-L33), SHA-256 `74498552f19df4bd5b3c296ed247d25d40cabd1057647dd4db1ee7ba1c57ea03`
- Lean 4.33.1; Mathlib [commit `0df444a360eaa60ab8c11dca51a86af692955474`](https://github.com/leanprover-community/mathlib4/tree/0df444a360eaa60ab8c11dca51a86af692955474)
- The exact original theorem statement is compared byte-for-byte (after normalizing line endings) by `tools/check_entrypoint_sources.py`. Its *proof* is independently written in `lean/extraction/Extraction/Factor.lean`, importing only official Mathlib.

## Formal results

The [factor extraction](../lean/extraction/Extraction/Factor.lean) proves

```lean
theorem factor_ne_zero {M : ℕ} (ψ : DirichletCharacter ℂ M) {s : ℂ}
    (hs : 0 < s.re) (p : ℕ) (hp : p.Prime) :
    (1 : ℂ) - ψ p * (p : ℂ) ^ (-s) ≠ 0
```

The [checks](../lean/extraction/Extraction/FactorChecks.lean) include the nonzero factor at modulus 1 / p=2 / s=1, a **counterexample when Re(s)=0**, and the unit factor at modulus 6 / p=2. No project proof archive is imported.

The [semantics proofs](../lean/extraction/Extraction/Semantics.lean) reintroduce the four *exact* local predicates from `Statements.lean` and prove:

- `RiemannZetaZerosOnLine ↔ RiemannHypothesis` (definitional)
- `DirichletLZerosOnLine ↔ DirichletLNonvanishingRightOfHalf`
- `PrimitiveDirichletLZerosOnLine ↔ DirichletLZerosOnLine`
- `DirichletLZerosOnLine → RiemannHypothesis`

The implications **use established Mathlib nonvanishing on Re(s)≥1, primitive functional equations and the factor theorem**. The file does **not** inhabit any of the conjectural GRH predicates; proving equivalent formulations is not proving their truth.

The [analytic interpretation](semantic-audit-dirichlet.md) also identifies zeros created by imprimitive Euler factors on the imaginary axis. These are outside the submitted open-strip predicates; it would be misleading to extend those predicates to all complex zeros without excluding such Euler factors.

## Independently rerun in this conversation

The Codex task first built the pinned standalone project locally using a repository-local Lean 4.33.1 toolchain and Mathlib cache. The assistant then independently executed this command with the same pinned tools, in working directory `lean/extraction`:

```powershell
$repo = (Resolve-Path .).Path  # run from repository root
Push-Location (Join-Path $repo 'lean/extraction')
try {
  & (Join-Path $repo '.lean/task-03/lean-4.33.1-windows/bin/lake.exe') build Extraction
} finally {
  Pop-Location
}
```

In the code block, the binary path is **relative to the repository root**; the actual process working directory was `lean/extraction` and the invoked executable was its absolute path under the repository's ignored `.lean/task-03` directory. For a fresh environment, the reproducible command from `lean/extraction` is `lake exe cache get` then `lake build Extraction`, after installing the toolchain from `lean-toolchain`.

Independent build result: **exit code 0, “Build completed successfully (3578 jobs)”**. Its output contains the following axiom audit results:

```text
Extraction.factor_ne_zero: [propext, Classical.choice, Quot.sound]
Extraction.pole_guard_iff: [propext, Classical.choice, Quot.sound]
Extraction.all_strip_iff_half_plane: [propext, Classical.choice, Quot.sound]
Extraction.primitive_strip_iff_all_strip: [propext, Classical.choice, Quot.sound]
Extraction.zeta_statement_iff: [propext, Classical.choice, Quot.sound]
Extraction.zeta_of_all_strip: [propext, Classical.choice, Quot.sound]
```

The build used incremental artifacts from the initial task run. Neither run checked the *full upstream November proof*. A separate [GitHub Actions workflow](../.github/workflows/lean-extraction.yml) is supplied for a clean Linux environment; its remote status must be checked after publication.

## Related records

- [Exact dependency path and next theorem](next-research-experiments.md)
- [Analysis of principal-character poles, boundary zeros and classical GRH](semantic-audit-dirichlet.md)
- [Source hash and pin verifier](../tools/check_entrypoint_sources.py)
- [Research metadata and extraction tests](../tests/test_extraction_metadata.py)

**Not established:** a new simplification of the hard arithmetic step; a proof of GRH; any GRH result for arbitrary number-field Hecke L-functions; full semantic or kernel audit of the 175,187 upstream modules.
