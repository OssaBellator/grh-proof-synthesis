import Extraction.Factor
import Mathlib.NumberTheory.LSeries.Nonvanishing

namespace Extraction

open DirichletCharacter

-- The four local definitions in pinned Statements.lean.
def RiemannZetaZerosOnLine : Prop :=
  ∀ s : ℂ, riemannZeta s = 0 → (¬∃ n : ℕ, s = -2 * ((n : ℂ) + 1)) → s ≠ 1 → s.re = 1 / 2

def DirichletLNonvanishingRightOfHalf : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0

def DirichletLZerosOnLine : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2

def PrimitiveDirichletLZerosOnLine : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N), χ.IsPrimitive →
    ∀ s : ℂ, 0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2

theorem zeta_statement_iff : RiemannZetaZerosOnLine ↔ RiemannHypothesis := Iff.rfl

theorem pole_guard_iff {N : ℕ} (χ : DirichletCharacter ℂ N) (s : ℂ) :
    ¬ (χ ≠ 1 ∨ s ≠ 1) ↔ χ = 1 ∧ s = 1 := by
  classical
  simp only [not_or, not_ne_iff]

example {N : ℕ} [NeZero N] {χ : DirichletCharacter ℂ N} (h : χ ≠ 1) :
    LFunction χ 1 ≠ 0 := LFunction_apply_one_ne_zero h

example {s : ℂ} (hs : s ≠ 1) (hre : s.re = 1) :
    LFunction (1 : DirichletCharacter ℂ 1) s ≠ 0 :=
  LFunction_ne_zero_of_re_eq_one _ hre (Or.inr hs)

private theorem strip_ne_one {s : ℂ} (h : s.re < 1) : s ≠ 1 := by
  rintro rfl
  simp at h

private theorem gammaFactor_ne_zero {N : ℕ} [NeZero N] (χ : DirichletCharacter ℂ N)
    {s : ℂ} (hs : 0 < s.re) : gammaFactor χ s ≠ 0 := by
  rcases χ.even_or_odd with h | h
  · rw [h.gammaFactor_def]
    exact Complex.Gammaℝ_ne_zero_of_re_pos hs
  · rw [h.gammaFactor_def]
    apply Complex.Gammaℝ_ne_zero_of_re_pos
    simpa only [Complex.add_re, Complex.one_re] using add_pos hs zero_lt_one

private theorem reflect_zero {N : ℕ} [NeZero N] {χ : DirichletCharacter ℂ N}
    (hχ : χ.IsPrimitive) {s : ℂ} (hs0 : 0 < s.re) (hs1 : s.re < 1)
    (hz : LFunction χ s = 0) : LFunction χ⁻¹ (1 - s) = 0 := by
  have hs : s ≠ 0 := by
    rintro rfl
    simp at hs0
  have ht : (1 : ℂ) - s ≠ 0 := sub_ne_zero.mpr (Ne.symm (strip_ne_one hs1))
  rw [LFunction_eq_completed_div_gammaFactor χ s (Or.inl hs), div_eq_zero_iff] at hz
  have hCompleted := hz.resolve_right (gammaFactor_ne_zero χ hs0)
  have hInv : (χ⁻¹).IsPrimitive := by
    simpa only [isPrimitive_def, conductor_inv] using hχ
  rw [LFunction_eq_completed_div_gammaFactor _ _ (Or.inl ht),
    hInv.completedLFunction_one_sub s, inv_inv, hCompleted, mul_zero, zero_div]

theorem primitive_strip_of_half_plane (h : DirichletLNonvanishingRightOfHalf) :
    PrimitiveDirichletLZerosOnLine := by
  intro N _ χ hχ s hs0 hs1 hz
  rcases lt_trichotomy s.re (1 / 2) with hleft | hline | hright
  · have ht : 1 / 2 < ((1 : ℂ) - s).re := by
      rw [Complex.sub_re, Complex.one_re]
      linarith
    have ht1 : (1 : ℂ) - s ≠ 1 := by
      intro eq
      have hRe := congrArg Complex.re eq
      rw [Complex.sub_re, Complex.one_re] at hRe
      linarith
    exact (h N χ⁻¹ (1 - s) ht (Or.inr ht1) (reflect_zero hχ hs0 hs1 hz)).elim
  · exact hline
  · exact (h N χ s hright (Or.inr (strip_ne_one hs1)) hz).elim

theorem all_strip_of_primitive_strip (h : PrimitiveDirichletLZerosOnLine) :
    DirichletLZerosOnLine := by
  intro N _ χ s hs0 hs1 hz
  let : NeZero χ.conductor := ⟨χ.conductor_ne_zero⟩
  have hProduct := LFunction_changeLevel χ.conductor_dvd_level
    χ.primitiveCharacter (Or.inr (strip_ne_one hs1))
  rw [χ.changeLevel_primitiveCharacter, hz] at hProduct
  have hFactors : (∏ p ∈ N.primeFactors, (1 - χ.primitiveCharacter p * (p : ℂ) ^ (-s))) ≠ 0 :=
    Finset.prod_ne_zero_iff.mpr fun p hp =>
      factor_ne_zero χ.primitiveCharacter hs0 p (Nat.prime_of_mem_primeFactors hp)
  exact h χ.conductor χ.primitiveCharacter χ.primitiveCharacter_isPrimitive s hs0 hs1
    ((mul_eq_zero.mp hProduct.symm).resolve_right hFactors)

theorem half_plane_of_all_strip (h : DirichletLZerosOnLine) :
    DirichletLNonvanishingRightOfHalf := by
  intro N _ χ s hHalf hGuard
  by_cases hs : s.re < 1
  · intro hz
    have hpos : 0 < s.re := by linarith
    exact hHalf.ne' (h N χ s hpos hs hz)
  · exact LFunction_ne_zero_of_one_le_re χ hGuard (le_of_not_gt hs)

theorem all_strip_iff_half_plane :
    DirichletLZerosOnLine ↔ DirichletLNonvanishingRightOfHalf :=
  ⟨half_plane_of_all_strip, fun h => all_strip_of_primitive_strip (primitive_strip_of_half_plane h)⟩

theorem primitive_strip_iff_all_strip :
    PrimitiveDirichletLZerosOnLine ↔ DirichletLZerosOnLine := by
  refine ⟨all_strip_of_primitive_strip, ?_⟩
  intro h N _ χ _ s
  exact h N χ s

theorem zeta_of_all_strip (h : DirichletLZerosOnLine) : RiemannHypothesis := by
  intro s hz hTrivial hOne
  by_cases hs : 0 < s.re
  · by_cases hs1 : s.re < 1
    · exact h 1 1 s hs hs1 (by simpa only [LFunction_modOne_eq] using hz)
    · exact (riemannZeta_ne_zero_of_one_le_re (le_of_not_gt hs1) hz).elim
  · have hs0 : s ≠ 0 := by
      rintro rfl
      rw [riemannZeta_zero] at hz
      norm_num at hz
    have hGamma : Complex.Gammaℝ s ≠ 0 := by
      intro hg
      obtain ⟨n, hn⟩ := Complex.Gammaℝ_eq_zero_iff.mp hg
      cases n with
      | zero => exact hs0 (by simpa using hn)
      | succ n => exact hTrivial ⟨n, by push_cast at hn; linear_combination hn⟩
    have hCompleted : completedRiemannZeta s = 0 := by
      rw [riemannZeta_def_of_ne_zero hs0, div_eq_zero_iff] at hz
      exact hz.resolve_right hGamma
    have ht : 1 ≤ ((1 : ℂ) - s).re := by
      rw [Complex.sub_re, Complex.one_re]
      linarith
    have ht0 : (1 : ℂ) - s ≠ 0 := sub_ne_zero.mpr hOne.symm
    have hReflected : riemannZeta (1 - s) = 0 := by
      rw [riemannZeta_def_of_ne_zero ht0, completedRiemannZeta_one_sub, hCompleted, zero_div]
    exact (riemannZeta_ne_zero_of_one_le_re ht hReflected).elim

#print axioms pole_guard_iff
#print axioms all_strip_iff_half_plane
#print axioms primitive_strip_iff_all_strip
#print axioms zeta_statement_iff
#print axioms zeta_of_all_strip

end Extraction
