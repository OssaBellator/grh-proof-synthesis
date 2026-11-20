# Lean formalization area

**No proof of RH or GRH is asserted in this directory.**

The installed Minimal MCP **Lean 4 Verifier** was checked with Lean **4.35.0** (commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`).

## Current toy checks

[**ToyLemma.lean**](ToyLemma.lean) has two elementary, deliberately limited results:

1. Additivity of a diagonal sum with two pairs of natural numbers, a basic finite-trace sanity check.
2. The two-element *nonnegative* autocorrelation obstruction: if a·a+b·b=0 for natural numbers, then a=b=0.

The second toy is motivated by Masullo's test-function restriction φ(C_F¹)=0 and the fact that an autocorrelation at the identity is a squared L² norm. It **does not** formalize a complex convolution algebra, Haar measure, arbitrary L² functions, Masullo's topology, or a GRH implication.

The following commands **were run and passed** on 21 November 2026:

```powershell
$env:ELAN_TOOLCHAIN = 'leanprover/lean4:v4.35.0'
lean lean/ToyLemma.lean
```

The Minimal MCP provider capability `lean.file.check` was also run on `lean/ToyLemma.lean` and exited 0 without diagnostics. The environment variable is process-local.

## Pinned Mathlib extraction

[`extraction/`](extraction/) pins Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. It contains the independent Euler-factor proof, three controls and conditional implications among the headline predicates. See the [Task 03 run report](../docs/codex-task-03-result.md) for commands and receipts.

## Requirements before any serious formalization

1. Pin the Lean toolchain and, if introduced, the Mathlib commit.
2. State the exact proposed theorem, including quantifiers, normalizations, and zero conventions.
3. Audit imports, axioms, admissions, custom trusted code and external automation.
4. Select a **source-specific** lemma, not merely an elementary syntactic demo.
5. Publish clean build instructions and a separate mathematical semantics audit.

Never use `sorry` or `admit` in a file labeled as formally verified.
