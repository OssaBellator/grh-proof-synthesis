-- These are toy finite models only. They do NOT prove a GRH implication.
-- Finite diagonal-sum additivity in the two-entry Nat model.
theorem toy_diagonal_sum (a b c d : Nat) :
    (a + b) + (c + d) = (a + c) + (b + d) := by
  simp [Nat.add_comm, Nat.add_left_comm]

-- On the two-element additive group, the autocorrelation at the identity
-- is a*a + b*b for a real-valued function (a,b); Nat is used here as
-- a no-dependencies, nonnegative toy model.
-- Zero identity autocorrelation forces the function to vanish.
theorem toy_autocorrelation_zero (a b : Nat)
    (h : a * a + b * b = 0) : a = 0 ∧ b = 0 := by
  simpa [Nat.add_eq_zero_iff, Nat.mul_eq_zero] using h
