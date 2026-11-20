# Proof obligations and audit gates

This is a checklist of questions **to resolve**, not a list of accomplished facts.

## Common target and definitions

- [ ] Identify a formal, fully quantified Dirichlet GRH statement.
- [ ] Check that completed/noncompleted L-functions, trivial zeros, and principal-character poles are treated consistently.
- [ ] Identify the exact relationship between each source's asserted theorem and the target.
- [ ] Check every use of analytic continuation, functional equation and zero symmetry.
- [ ] Verify no intermediate proposition assumes GRH, equivalent positivity, or desired cancellation.

## Alpöge–Claude: formal and arithmetic

- [ ] Identify the exact upstream Lean artifact and hash its files.
- [ ] Reproduce a build with **pinned Lean and Mathlib versions** and a clean package cache.
- [ ] Enumerate axioms and imports used by the final GRH theorem, including `sorryAx`, `axiom`, `unsafe`, `opaque`, `native_decide`, and foreign-code/trust boundaries as applicable.
- [ ] Independently check the **semantic equivalence** between the terminal Lean proposition and standard Dirichlet GRH.
- [ ] Locate and state the theta-lift iteration lemma with all length, norm, error and conductor parameters.
- [ ] Check uniformity of implicit constants; verify that iteration costs do not swamp the saving.
- [ ] Extract one small dependency-minimal lemma and reproduce it without the giant imported environment.

## Masullo: functional analysis and traces

- [ ] Fix precise definitions and topology of the modified Hardy–Sobolev spaces.
- [ ] Check the claimed density/completeness properties and whether they change as localization windows shrink.
- [ ] Specify orbital Schauder bases and their convergence in the required operator topologies.
- [ ] Define operators and domains; justify any trace or determinant identity.
- [ ] Audit convergence and all exchanges of limits, sums, integrals and traces.
- [ ] Check that zero-isolation/localization neither assumes nor implies the conclusion circularly.
- [ ] Locate a **finished** theorem deducing the critical-line conclusion, not just a stated program or placeholder.
- [ ] Reduce one significant trace or basis identity to a checkable independent lemma.

## Potential synthesis

- [ ] Identify a common intermediate object, not merely overlapping mathematical vocabulary.
- [ ] Type-check the *mathematical interface*: spaces, operators, normalization, local/global parameters.
- [ ] Prove the bridge on a toy model and list exactly which features fail in the Dirichlet case.
- [ ] Show that error estimates remain uniform in the limit and no GRH-equivalent property was assumed.
- [ ] Conduct a second independent review of every proposed synthesis step.

## Completion bar

No claim may be promoted to 'established' inside the research ledger without a verifiable artifact and an independently explained mathematical meaning. Disputed claims should keep their dispute history.
