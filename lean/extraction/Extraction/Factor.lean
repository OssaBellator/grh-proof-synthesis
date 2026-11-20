import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.NumberTheory.DirichletCharacter.Bounds

namespace Extraction

theorem factor_ne_zero {M : ℕ} (ψ : DirichletCharacter ℂ M) {s : ℂ} (hs : 0 < s.re) (p : ℕ)
    (hp : p.Prime) : (1 : ℂ) - ψ p * (p : ℂ) ^ (-s) ≠ 0 := by
  have hpReal : (1 : ℝ) < p := by exact_mod_cast hp.one_lt
  have hPower : ‖(p : ℂ) ^ (-s)‖ < 1 := by
    rw [Complex.norm_natCast_cpow_of_pos hp.pos, Complex.neg_re]
    exact Real.rpow_lt_one_of_one_lt_of_neg hpReal (neg_neg_of_pos hs)
  have hTerm : ‖ψ p * (p : ℂ) ^ (-s)‖ < ‖(1 : ℂ)‖ := by
    rw [norm_mul, norm_one]
    exact (mul_le_of_le_one_left (norm_nonneg _) (ψ.norm_le_one _)).trans_lt hPower
  exact sub_ne_zero.mpr (Ne.symm (ne_of_apply_ne norm hTerm.ne))

#print axioms factor_ne_zero

end Extraction
