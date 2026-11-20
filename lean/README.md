# Lean formalization area

There is **no claimed GRH proof in this repository**.

A future Lean subproject must:
1. Pin the Lean toolchain and Mathlib revision.
2. Declare the *precise* theorem to prove and link to its standard analytic definition.
3. Audit imports, axioms, holes, custom kernel behavior and external automation.
4. Check a small lemma end-to-end before importing any enormous proof archive.
5. Provide a clean-rebuild script and explain the difference between kernel acceptance and semantic review.

Do not add placeholder `by sorry` theorems to a file presented as verified.
