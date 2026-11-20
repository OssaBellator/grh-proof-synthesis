import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Mathlib.Tactic.Linarith

namespace Extraction

open Filter

-- Exact type from UpperTheory.Top.log_sq_le_rpow in DivinNOfHypV.lean.
theorem log_sq_le_rpow {eps : ℝ} (h : 0 < eps) :
    ∃ x0 : ℝ, ∀ x ≥ x0, Real.log x ^ 2 ≤ x ^ eps := by
  have eventuallyBound :
      ∀ᶠ x : ℝ in atTop, ‖Real.log x‖ ≤ 1 * ‖x ^ (eps / 2)‖ :=
    (isLittleO_log_rpow_atTop (half_pos h)).bound one_pos
  apply eventually_atTop.mp
  filter_upwards [eventually_ge_atTop (1 : ℝ), eventuallyBound] with x hx hb
  have hxPos : 0 < x := zero_lt_one.trans_le hx
  have hlog : 0 ≤ Real.log x := Real.log_nonneg hx
  have hrpow : 0 ≤ x ^ (eps / 2) := Real.rpow_nonneg hxPos.le _
  simp only [Real.norm_eq_abs, abs_of_nonneg hlog, abs_of_nonneg hrpow, one_mul] at hb
  calc
    Real.log x ^ 2 ≤ (x ^ (eps / 2)) ^ 2 := pow_le_pow_left₀ hlog hb _
    _ = x ^ eps := by
      rw [pow_two, ← Real.rpow_add hxPos, add_halves]

-- At eps = 0, take x = exp (max x0 2) past any proposed threshold.
theorem log_sq_not_eventually_le_one :
    ¬ ∃ x0 : ℝ, ∀ x ≥ x0, Real.log x ^ 2 ≤ x ^ (0 : ℝ) := by
  rintro ⟨x0, hx0⟩
  let t : ℝ := max x0 2
  have ht : 2 ≤ t := le_max_right _ _
  have hxt : t ≤ Real.exp t := by linarith [Real.add_one_le_exp t]
  have hx := hx0 (Real.exp t) ((le_max_left x0 2).trans hxt)
  rw [Real.log_exp, Real.rpow_zero] at hx
  nlinarith

#print axioms log_sq_le_rpow
#print axioms log_sq_not_eventually_le_one

end Extraction
