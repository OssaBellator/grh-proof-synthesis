# First-lemma triage: find a *real* interface, not a cosmetic simplification

**Decision (first pass, 21 November 2026):** Investigate the **autocorrelation obstruction to a positivity-based hybrid** before trying to combine theta lifts and localized traces. It is explicitly motivated by Masullo §1.7.2 (around pp. 35–36) and provides an immediate falsification test for a tempting but unjustified synthesis.

This is a **small standard lemma**, not a new proof of GRH and not one of Masullo's major technical results. Its importance is diagnostic: it identifies a precise incompatibility that an actual bridge theorem would need to overcome.

| Priority | Candidate | Source connection | What can actually be checked now | Unresolved bottleneck |
| --- | --- | --- | --- | --- |
| **1** | Autocorrelation at the identity is a squared L² norm | Masullo §1.7.2: requirement φ(C_F¹)=0 and rejection of Weil-style positivity test functions | A short analytic argument and a two-element finite toy checked in Lean | Find any **new** positive test class compatible with the restricted trace formula, or prove that no direct bridge is possible |
| 2 | Uniform passage from a trace formula with fixed parameter a=1/2 to an adjustable localization interval | Masullo §1.4 versus §12.5 (pp. 27–32 and 519) | Write down all parameters and their quantifiers; test a finite trace model | Need actual uniform estimates and exchange-of-limit hypotheses from the manuscript |
| 3 | Accumulated cost of m iterated lifts is controlled uniformly in the relevant conductor/X parameter | Alpöge p. 4, timeline 8–10 and 14 | A finite telescoping/sum bound is easy once per-step estimates are stated | The source note **does not supply** the needed inequality or its constants; must first inspect the Lean archive |

## Priority-1 precise lemma (standard mathematics)

Let G be a locally compact **abelian** group with Haar measure μ and identity e. Let ψ : G → ℂ be a continuous compactly supported function. Set

- ψ*(g) = conjugate(ψ(g⁻¹))
- φ = ψ ∗ ψ*, with convolution (f ∗ h)(x) = ∫_G f(y) h(y⁻¹x) dμ(y).

Then

**φ(e) = ∫_G |ψ(g)|² dμ(g) ≥ 0.**

Consequently, if H ≤ G is a subgroup containing e and φ vanishes on H, then ψ = 0 (as a function, using continuity and the full support of Haar measure). The only such autocorrelation φ is the zero function.

**Proof:** At x=e, ψ*(y⁻¹)=conjugate(ψ(y)), so the convolution integrand is |ψ(y)|². Haar integration makes the result nonnegative, and a continuous nonnegative function with zero integral must vanish everywhere on G.

### Two-element toy case and falsification

For the additive group ℤ/2ℤ and a real function with values (a,b), φ(0)=a²+b²; therefore φ(0)=0 forces a=b=0. The checked Lean file uses **natural numbers** instead, proving only the implication a·a+b·b=0 ⇒ a=b=0. It does **not** formalize complex convolution, Haar integration, or the manuscript's operator spaces.

The conjugate-involution hypothesis matters. If we replace ψ* by ψ for complex values, choose (ψ(0),ψ(1))=(1,i). Then (ψ∗ψ)(0)=1²+i²=0 although ψ is nonzero. This is a direct finite counterexample to a careless positivity assertion.

## What exactly this does—and does not—establish

This standard lemma explains the incompatibility Masullo himself notes between the restriction φ(C_F¹)=0 and autocorrelation positivity tests. It **does not** show Masullo's trace formula is wrong. It **does not** refute non-Weil methods of deriving GRH. It **does** mean that a putative synthesis invoking Weil positivity must prove a different interface.

The previous finite trace-additivity toy is retained as an additional verified syntax/checker smoke test: tr(A+B)=tr(A)+tr(B) for two diagonal entries. That identity does not justify any infinite-dimensional trace/sum interchange.

## Acceptance criteria for the next nontrivial lemma

A meaningful M2 result would be an **explicit source-derived boundedness or trace-limit lemma** with precise spaces, norms, convergence mode, and hypotheses, together with either a proof or a counterexample. This priority-1 lemma is only the first interface sanity check. The project's more substantial next target is parameter uniformity in Masullo's §12.5 and the corresponding theorem statements in the source.
