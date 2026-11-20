# Task 01: primary-source dependency maps and the first checkable lemma

User objective: derive a rigorous, attributable dependency graph for the Alpöge–Claude (Lean, RH/GRH) and Alessandro Maria Masullo (trace/functional analysis, GRH) proposals announced 20 November 2026. Identify the **smallest high-value bottleneck lemma** to investigate before any hybrid synthesis. The proposed proofs are NOT presumed correct.

Run through the Codex CLI using the user's requested full-access mode, but **confine actual edits to this repository**.

Primary source anchors:
- https://alpo.ge/remark.pdf (four-page note; Lean archive is linked as 14 multipart downloads)
- https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/
- https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf

Read existing `docs/` and `data/claims.json` first, then:

1. Retrieve/inspect the author notes and at least meaningful intro/table of contents/theorem citations from Masullo. Record exact page ranges and definitions and assess gaps. If a source cannot be accessed or a quote checked, mark it unverified. Do **not** download/compile the huge Alpöge Lean archive at this stage.
2. Write `docs/dependency-map-alpoge.md` and `docs/dependency-map-masullo.md` as two graph-like tables. Nodes with IDs, source location, statement or named mechanism, input dependencies, status. Distinguish *source narrative* vs *formal theorem dependency*; explicitly state when the latter cannot be inferred from a four-page note.
3. Write `docs/first-lemma-triage.md`: rank three **small independently provable** bottleneck lemmas based on mathematical relevance, source grounding, missing infrastructure, falsifiability and tractability. Choose a single first lemma. Write its precise theorem statement with all hypotheses, and at least one toy case or falsification test. Avoid ambiguous function-space claims or unproved continuity.
4. If feasible, produce a `lean/ToyLemma.lean` **minimal** verified toy lemma in plain Lean 4 and document the actual kernel-check command and results; it need not claim novelty or connect to GRH on its own. Use lean provider via Minimal MCP when available; if provider unavailable, lean CLI is installed. Do not waste time bootstrapping massive Mathlib just for a trivial statement.
5. Make narrow, evidence-based amendments to `docs/technique-matrix.md` and `data/claims.json`, preserving current statuses unless new source inspection supports promotion. Do not overclaim.
6. Run metadata tests, any minimal Lean test, and summarize exactly what passed or was not run. Do not push automatically.

Stop after meaningful M1 dependency maps, M2 first lemma triage and limited reproducible proof-of-concept, even if substantial open issues remain. Final report should state source coverage, limitations and files changed.
