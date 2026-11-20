import Mathlib.NumberTheory.DirichletCharacter.Basic
import Mathlib.Data.Complex.Basic

namespace Extraction

theorem stage1_prim (N₀ : ℕ) (hN : 0 < N₀) (ξ : DirichletCharacter ℂ N₀) :
    ∃ ξ' : (Σ N : ℕ, DirichletCharacter ℂ (N + 1)), ξ'.2.IsPrimitive ∧ ξ'.1 + 1 ≤ N₀ ∧
      ∀ n : ℕ, n.Coprime N₀ → ξ'.2 (n : ZMod (ξ'.1 + 1)) = ξ (n : ZMod N₀) := by
  let _ : NeZero N₀ := ⟨Nat.ne_of_gt hN⟩
  have hdiv := ξ.conductor_dvd_level
  have hagree (n : ℕ) (hn : n.Coprime N₀) :
      ξ.primitiveCharacter (n : ZMod ξ.conductor) = ξ (n : ZMod N₀) := by
    let u := ZMod.unitOfCoprime n hn
    calc
      ξ.primitiveCharacter (n : ZMod ξ.conductor) =
          (ξ.primitiveCharacter.changeLevel hdiv) (u : ZMod N₀) := by
        rw [DirichletCharacter.changeLevel_eq_cast_of_dvd, show (u : ZMod N₀) = n from
          ZMod.coe_unitOfCoprime n hn, ZMod.cast_natCast hdiv]
      _ = ξ (n : ZMod N₀) := by
        rw [DirichletCharacter.changeLevel_primitiveCharacter, ZMod.coe_unitOfCoprime]
  have package (c : ℕ) (hc : c ≠ 0) (χ : DirichletCharacter ℂ c) (hp : χ.IsPrimitive)
      (hle : c ≤ N₀) (h : ∀ n : ℕ, n.Coprime N₀ → χ (n : ZMod c) = ξ (n : ZMod N₀)) :
      ∃ θ : (Σ N : ℕ, DirichletCharacter ℂ (N + 1)), θ.2.IsPrimitive ∧ θ.1 + 1 ≤ N₀ ∧
        ∀ n : ℕ, n.Coprime N₀ → θ.2 (n : ZMod (θ.1 + 1)) = ξ (n : ZMod N₀) := by
    cases c with
    | zero => exact (hc rfl).elim
    | succ k => exact ⟨⟨k, χ⟩, hp, hle, h⟩
  exact package ξ.conductor ξ.conductor_ne_zero ξ.primitiveCharacter ξ.primitiveCharacter_isPrimitive
    (Nat.le_of_dvd hN hdiv) hagree

#print axioms stage1_prim

end Extraction
