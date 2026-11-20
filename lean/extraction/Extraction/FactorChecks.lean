import Extraction.Factor

namespace Extraction

example : (1 : ℂ) - (1 : DirichletCharacter ℂ 1) (2 : ℕ) *
    (2 : ℂ) ^ (-(1 : ℂ)) ≠ 0 := by
  exact factor_ne_zero (1 : DirichletCharacter ℂ 1) (s := 1) (by simp) 2 (by decide)

-- Even the weaker premise 0 ≤ s.re is insufficient.
example : (1 : ℂ) - (1 : DirichletCharacter ℂ 1) (2 : ℕ) *
    (2 : ℂ) ^ (-(0 : ℂ)) = 0 := by
  rw [MulChar.one_apply (isUnit_of_subsingleton _)]
  simp

example (s : ℂ) : (1 : ℂ) - (1 : DirichletCharacter ℂ 6) (2 : ℕ) *
    (2 : ℂ) ^ (-s) = 1 := by
  have h : ¬ IsUnit ((2 : ℕ) : ZMod 6) := by
    rw [ZMod.isUnit_iff_coprime]
    decide
  rw [MulChar.map_nonunit _ h, zero_mul, sub_zero]

end Extraction
