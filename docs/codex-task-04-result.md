# Task 04 — verified arithmetic handoff research pass

**Run date:** 21 November 2026 (Brisbane); **Codex:** CLI 0.171.0, `gpt-6.2-sol` with High reasoning effort and the user's authorized full-access setting. **No Astra used.** Work and generated artifacts remained inside the repository; upstream mathematical files were fetched only as bounded source text.

## What was actually accomplished

The [arithmetic handoff audit](arithmetic-handoff-audit.md) locates `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` at [pinned `SiegelEisensteinSecondTermHypotheses.lean`, lines 69–73](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean#L69-L73). It traces the seven inputs (`P,F,hA,hM,hX,hL,hV`) through their source-visible producers, both projections of the theta-local matching bundle, the covolume estimate and the `VWin` number-field window property.

The theorem is a **conditional reduction** to `UpperTheory.EveryCharacter`: its body invokes `UpperTheory.Top.every_character_of_green_v_win`, passes `hV` unchanged, and constructs a third hypothesis from the remaining inputs. Source statements for `ThetaIntegralsAgree`, `LocalMatching` and `VWin` contain substantial quantified analytical and arithmetic conditions. Finding the wrapper does **not** prove the hypotheses or establish GRH.

The next high-information target is a fixed-parameter version of the **first-stage exceptional-prime count** used in constructing `PairEx`: modulus 24 and exceptional fraction at most one quarter, with explicit quantifier order and negative controls. See [the proposed experiment](arithmetic-handoff-audit.md#highest-priority-independent-check). Other branches to examine include `kDecay`, theta comparison scalar existence/nonvanishing, and uniform covolume/lift losses.

## Source identity and mechanical checks

The [pinned source registry](../data/arithmetic-handoff.json) contains **60 source files**, **92 nodes**, **110 edges**, and exactly **one explicitly inferred research connection**. The pins total 366,578 source bytes; receipt SHA-256:

`7a14cbc79244eb4f33df8022862986f88f8135388f4c806d424da85b9d4f060e`

The [source checker](../tools/check_arithmetic_handoff.py) has a static allowlist at upstream mirror commit `0fb9869c6e6d7b54b67de803af0e0be29d37fc22`, bounds individual responses to 128 KiB and the allowlist to 512 KiB, disallows redirects, and checks sizes, SHA-256 values, line-local declaration/call-site anchors, and source-vs-extraction signatures.

**Independently rerun by the assistant after the Codex task:**

```sh
python tools/check_arithmetic_handoff.py
python tools/check_arithmetic_handoff.py --offline
python -m unittest discover -s tests -v
```

All passed: **60/60 source files matched** and **17/17 offline Python tests passed**. The original entrypoint checker, claim-ledger validator and `git diff --check` also passed. These checks verify provenance and metadata, not a 60-file Lean theorem elaboration. Downloaded source text lives under ignored `.source-tmp/` and is **not committed**.

## Independent Lean extraction and controls

The active source path uses `UpperTheory.Top.log_sq_le_rpow` in `DivinNOfHypV.lean`. [`Extraction/LogSquare.lean`](../lean/extraction/Extraction/LogSquare.lean) has the same theorem type, proved independently with Mathlib's little-o bound:

```lean
theorem log_sq_le_rpow {eps : ℝ} (h : 0 < eps) :
    ∃ x0 : ℝ, ∀ x ≥ x0, Real.log x ^ 2 ≤ x ^ eps
```

Its negative control, `log_sq_not_eventually_le_one`, refutes the same eventual bound for exponent zero. No original November proof modules were imported; Mathlib remained pinned to `0df444a360eaa60ab8c11dca51a86af692955474`, Lean to 4.33.1.

I independently reran the pinned project using repository-local Lean 4.33.1, with **exit code 0** and `Build completed successfully (3579 jobs)`. Both new declarations report precisely `[propext, Classical.choice, Quot.sound]` under `#print axioms`. From the repository root in the Windows workspace with the preinstalled local toolchain, the equivalent command is:

```powershell
$repo = (Resolve-Path .).Path
Push-Location (Join-Path $repo 'lean/extraction')
try {
  & (Join-Path $repo '.lean/task-03/lean-4.33.1-windows/bin/lake.exe') build Extraction
} finally {
  Pop-Location
}
```

On a fresh machine, install the toolchain selected by `lean/extraction/lean-toolchain`, retrieve Mathlib caches and run `lake build Extraction` from that directory.

**Boundary:** The logarithmic estimate is standard and small. It has a genuine upstream consumer but does not independently validate the difficult theta lifts, covolume estimates, prime-pair density, final nonvanishing argument, or GRH. We did **not** locally compile the 175,187-module submitted archive.

## Other artifacts

- [Source-level dependency map and analytical hypotheses](arithmetic-handoff-audit.md)
- [Updated ranked experiments](next-research-experiments.md)
- [Source registry](../data/arithmetic-handoff.json)
- [Offline integrity tests](../tests/test_arithmetic_handoff.py)
- [Task specification](task-04.md)

The repository remains a research and verification project, not a completed GRH proof.
