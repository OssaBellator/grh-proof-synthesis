# Task 01 execution report — 21 November 2026

## How this pass was run

Codex CLI 0.163.0 ran noninteractively from this repository, with `danger-full-access` sandbox mode and approval setting `never`, as requested. The requested `gpt-6.2` model was **rejected** by the ChatGPT-backed Codex account, so the completed run used the CLI's supported default **gpt-6.1-terra**. It performed a source-inspection and documentation task; this was not a professional mathematical peer review.

## Deliverables

- [Alpöge–Claude dependency map](dependency-map-alpoge.md): source-reported timeline separated from the **uninspected** formal Lean dependency graph.
- [Masullo dependency map](dependency-map-masullo.md): sampled chapter inputs, named trace-formula references, source restrictions and the incomplete terminal write-up on p. 522.
- [First-lemma triage](first-lemma-triage.md): prioritizes the source-specific autocorrelation restriction as an interface sanity check; lists parameter uniformity and theta-lift costs as the next mathematical bottlenecks.
- [Technique matrix](technique-matrix.md) and [claim ledger](../data/claims.json): claims and unresolved verification obligations.
- [Lean toy file](../lean/ToyLemma.lean): two elementary arithmetic toy identities, not GRH or a genuine trace theorem.

## Source coverage

Downloaded and checked hashes for both primary PDFs. Alpöge's four-page note was text-extracted in full. Masullo's 940-page draft was sampled, including introduction, contents, the trace-formula statement (pp. 519–520), and the visible incomplete terminal theorem (p. 522). The full 940-page proof was **not** checked, and the multipart Lean archive was **not** downloaded or executed.

The PDFs and intermediate text files are stored in a locally ignored `.source-tmp/` directory. They are **not** part of the public repository.

## Verification

- Research claims metadata validator: passed (8 structurally valid entries).
- Four Python regression tests: passed.
- Lean 4.35.0: `lean lean/ToyLemma.lean` passed.
- Minimal MCP Lean provider `lean.file.check`: passed (exit code 0, no diagnostics).

These checks do **not** establish any part of GRH.

## Open questions

1. Audit the exact Dirichlet GRH Lean declaration, assumptions, and final dependency graph.
2. Determine whether Masullo's trace parameter `a=1/2` can be reconciled with the introduction's variable localization scheme.
3. Identify the missing terminal zero-location theorem and full written proof in a later revised draft.
4. Find a precisely stated, nontrivial bridge lemma only after resolving the incompatibility between the restricted test space and Weil positivity.
