# GRH Proof Synthesis

**Open research project · Started 21 November 2026 · Status: preliminary**

An independent, public, reproducible effort to **audit, compare, simplify, and (where justified) combine** two newly announced approaches to the **Generalized Riemann Hypothesis for Dirichlet L-functions**:

1. **Levent Alpöge / Claude:** a claimed Lean-formalized RH/GRH argument, with a proposed number-theoretic/automorphic route.
2. **Alessandro Masullo:** a proposed GRH argument using functional analysis, spectral methods, and trace formulas.

**Neither announcement is treated here as a settled proof.** This repository does not claim to prove RH or GRH. It is not affiliated with the authors.

## Research question

Can independently verified pieces of these arguments be reduced to a small number of conventional, checkable lemmas—possibly revealing a shared mechanism, a simpler proof, or an obstruction?

We prioritize **reconstructing both arguments independently before combining them**. A superficially plausible hybrid is not a substitute for a sound theorem.


## First evidence-backed pass (21 November 2026)

The [task report](docs/codex-task-01-result.md) documents Codex CLI's source-inspection run and tests. Its [Alpöge dependency map](docs/dependency-map-alpoge.md) is a *narrative audit map*, not an extracted Lean proof graph. The [Masullo dependency map](docs/dependency-map-masullo.md) records the trace-formula prerequisites and a visible gap in the manuscript's written terminal theorem on p. 522. The [first-lemma triage](docs/first-lemma-triage.md) prioritizes the incompatibility between Masullo's restricted test functions and autocorrelation positivity. A tiny [Lean toy check](lean/ToyLemma.lean) passed, but no part of RH or GRH was proved.

## First milestones

- **M0 — Source control:** identify originals, versions, licenses, formal theorem statements, build environments, and dependencies; preserve links and hashes.
- **M1 — Proof-obligation map:** express each proposal as a dependency graph from established mathematics to its final asserted theorem. Record missing steps and unresolved definitions.
- **M2 — Minimal core:** select the smallest independently checkable lemma from each approach; reproduce it with a conventional proof or a genuinely audited Lean proof.
- **M3 — Simplification:** eliminate redundant constructions and quantify exactly which hypotheses each lemma uses.
- **M4 — Bridge investigation:** test narrowly stated interfaces between multiplicity/amplification, trace localization, and positivity. Record counterexamples and failed attempts.
- **M5 — Alternatives (later):** only after M0–M4, compare other routes (spectral, approximation, Hilbert-space density, cancellation).

See [research plan](docs/research-plan.md), [proof obligations](docs/proof-obligations.md), and the [claim ledger](data/claims.json).

## What counts as evidence?

| Level | Meaning |
| --- | --- |
| Announced | An author or intermediary has asserted a claim. |
| Source-inspected | We identified the precise statement in a versioned primary source. |
| Reproduced | Another researcher ran a documented computational or formal check. |
| Audited | The statement, hypotheses, axioms, dependencies, and proof steps were independently inspected. |
| Established | The mathematical community has robust, reproducible support for the stated theorem. |

These levels are **not interchangeable**. In particular, “Lean compiles” does not itself show that the formal theorem matches informal GRH, that no assumptions bypass the result, or that the mathematical interpretation is correct.

## Reproduce the repository's checks

Requires Python 3.11+; no third-party Python packages.

```sh
python tools/validate_claims.py
python -m unittest discover -s tests -v
```

These checks validate the **research metadata**, not any GRH proof.

## Layout

```text
data/claims.json             versioned claim/evidence ledger
docs/sources.md              primary-source entry points and acquisition plan
docs/proof-obligations.md    explicit mathematical and formal audit gates
docs/research-plan.md        phased plan and stop conditions
docs/technique-matrix.md     candidate connections; no assumed bridge
docs/alternatives-backlog.md deferred research ideas
lean/README.md               safe formalization policy
tools/validate_claims.py     metadata validator
tests/                       regression tests for metadata
```

## Research rules

1. Every substantive assertion must point to an exact source or be labeled a conjecture.
2. Never report a theorem as proved merely because it is typechecked, cited, or numerically illustrated.
3. Record hypotheses, quantifiers, normalization, and zero-set conventions exactly; distinguish Dirichlet GRH from broader ERH claims.
4. Publish negative results and reproducible counterexamples as first-class outputs.
5. Respect upstream authorship and licenses; **do not mirror giant Lean archives or manuscripts** unless permission/licensing and provenance are clear.
6. Keep independent mathematical verification separate from AI-generated suggestions.

## Original entry points

- [Alpöge's original note](https://alpo.ge/remark.pdf)
- [Ravi Vakil's announcement of Masullo's work](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/)
- [Masullo's manuscript](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf)

These links are sources for claims **about the announcements**, not endorsements.

## Contribute

Open a focused issue or pull request with the exact theorem statement, source location/version, assumptions, proof sketch or reproducible commands, and an explicit verification status. See [CONTRIBUTING.md](CONTRIBUTING.md).

Released under the MIT license for this project's original text and code. Upstream mathematical manuscripts and formalizations retain their own copyright.
