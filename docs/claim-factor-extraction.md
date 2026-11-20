# A Mathlib extraction of `Claim.factor_ne_zero`

The extracted theorem keeps the original binders and uses two Mathlib modules for character norms and complex powers. It passed a Lean 4.33.1 build and local kernel replay. The source uses the theorem to pass from a zero of an imprimitive Dirichlet L-function to a zero of its inducing primitive character. [Extraction](../lean/extraction/Extraction/Factor.lean) · [Pinned source, lines 7–33](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean#L7-L33)

## Source declaration and consumer

The declaration at physical lines 7–8 has this type. The name is `Claim.factor_ne_zero` in the source and `Extraction.factor_ne_zero` here.

```lean
theorem factor_ne_zero {M : ℕ} (ψ : DirichletCharacter ℂ M) {s : ℂ} (hs : 0 < s.re) (p : ℕ)
    (hp : p.Prime) : (1 : ℂ) - ψ p * (p : ℂ) ^ (-s) ≠ 0
```

`M` and `s` are implicit. The explicit arguments are `ψ`, `hs`, `p` and `hp`. The character uses the multiplicative character structure on `ZMod M`, and the two occurrences of `p` use its casts into `ZMod M` and `ℂ`. The exponent is complex. There is no extra typeclass premise on the modulus, and no condition that `ψ` be primitive or that `p` be coprime to the modulus. The source proof obtains equality of the product with one by linear combination, bounds the product norm by the power norm and derives a contradiction. [Exact raw source](https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean)

`Claim.prim_zero` (lines 23–33) assumes `[NeZero N]`, `[NeZero χ.conductor]`, an open-strip point and `LFunction χ s = 0`. It uses `LFunction_changeLevel` with `Or.inr hs`, where `hs : s ≠ 1` follows from `s.re < 1`. After rewriting the induced character and its zero, a zero product would give either a primitive L-function zero or a vanishing factor at some `p ∈ N.primeFactors`. At line 33 it rules out the latter by calling `factor_ne_zero _ hs0 p (Nat.prime_of_mem_primeFactors hp)`. Here `_ = χ.primitiveCharacter` and `M = χ.conductor`. The two `NeZero` instances serve the L-function comparison. `Claim.strip` uses `prim_zero` in its left-of-line branch at line 67. [Pinned consumer, lines 23–33 and 59–73](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean#L23-L73)

## Independent proof

For a prime natural $p$, we have $p>1$. With $\sigma=\Re(s)>0$ and the real logarithm of the positive base, $|p^{-s}|=p^{-\sigma}<1$. Also $|\psi(p)|\le 1$. On a unit the character has norm one, and on a nonunit it is zero. Thus $|\psi(p)p^{-s}|<|1|$. Strict inequality of norms implies the two complex numbers differ, so their difference is nonzero. In Lean the proof uses `Complex.norm_natCast_cpow_of_pos`, `Real.rpow_lt_one_of_one_lt_of_neg`, `DirichletCharacter.norm_le_one`, and `norm_mul`, then turns unequal norms directly into unequal terms with `ne_of_apply_ne`. The imported character bound includes the degenerate modulus allowed by the source binder. [Power lemmas](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/SpecialFunctions/Pow/Real.lean#L340-L360) · [Character bounds](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/NumberTheory/DirichletCharacter/Bounds.lean#L23-L35)

| Case | Value or conclusion |
| --- | --- |
| Principal mod 1, $p=2$, $s=1$ | $1-2^{-1}=1/2\ne0$. The Lean control checks nonvanishing. |
| Principal mod 1, $p=2$, $s=0$ | $1-1=0$. This refutes the statement with $0\le\Re(s)$ in place of strict positivity. The Lean control checks equality to zero. |
| Principal mod 6, $p=2$ | The character value at $2$ is zero since $2$ is a nonunit, so the factor equals one at every $s$. The Lean control checks this identity. |
| $s=it$ with real $t$ | For a unit input, the subtracted term has norm one, so the strict norm bound is unavailable. For the principal mod-1 character the factor vanishes exactly when $t\log p\in 2\pi\mathbb Z$, since $p^{-it}=e^{-it\log p}$. For a nonunit input the factor is still one. This boundary description is analytic. |

The factor proof uses neither conductor reduction nor L-function nonvanishing. The [semantic audit](semantic-audit-dirichlet.md) applies the factor lemma in a separate conditional reduction. The [Task 03 run report](codex-task-03-result.md) records commands, source hashes, Lean build status, and the output of `#print axioms`. The three explicit controls are in [FactorChecks.lean](../lean/extraction/Extraction/FactorChecks.lean).
