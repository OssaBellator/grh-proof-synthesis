# Technique matrix — candidate research interfaces, not proved bridges

| Theme | Alpöge–Claude proposal | Masullo proposal | Exact comparison task |
| --- | --- | --- | --- |
| Arithmetic/spectral object | Automorphic lifts, periods and prime sums in the author's timeline | Test functions on idele classes, nuclear operators, trace formulas, and Hecke L-function zeros | Establish whether both constructions give distributions with the **same** normalization |
| Localization | Multiplicity analogue from theta-lift iteration, with suggested chain length √X | Hardy–Sobolev topology and zero sums restricted to spectral strips | Identify the parameter range and error estimates; avoid conflating the two mechanisms |
| Cancellation | Claimed arithmetic divisibility, averaging, and determinants | Claimed orbital decomposition and trace localization | Derive exact inequalities with domains, norms, and **uniform constants** |
| Positivity | A positivity/determinant argument is mentioned in the source timeline | Masullo explicitly says **Weil positivity is not used** and restricts φ(C_F¹)=0 | The autocorrelation obstruction must be addressed before hypothesizing a positive trace identity |
| Terminal verification | Exact Lean declaration and axiom graph not yet inspected | Written terminal chapter has an incomplete theorem statement | Require complete final theorem statement and independent semantic/proof audit |

## Hypothesis H-1 (speculative only)

One might hope for an intermediate arithmetic distribution or trace identity to connect the two programs. **No such interface is yet constructed.**

Minimum tasks:

1. State and normalize the exact Dirichlet/Hecke L-function target and its explicit-formula distribution D_χ(f).
2. Extract source lemmas, with all quantifiers, from the actual Lean archive and the precise Masullo theorems.
3. Identify the test-function spaces, domains, and parameter dependencies of each proposed result.
4. Explicitly address Masullo's restriction φ(C_F¹)=0 and its incompatibility with nonzero Weil-autocorrelation tests.
5. Prove an intermediary bounded map or equality **without** GRH-equivalent assumptions or unjustified limit exchanges.
6. Test it in a finite model and search for counterexamples before claiming any GRH implication.

## Important source-inspected observations (21 November 2026)

- **Alpöge**, [author note](https://alpo.ge/remark.pdf), p. 3 footnote and pp. 3–4: his chronology is an explicitly provisional, compressed narrative. It cannot substitute for a Lean declaration graph.
- **Masullo**, [manuscript](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf), §1.7.2, around pp. 35–36: the test-function restriction excludes nonzero positivity autocorrelations in that setting.
- **Masullo**, §12.5, p. 519: the trace calculation specifies **a=1/2** and calls this choice necessary, whereas the introductory zero-location strategy discusses variable localization. Their relationship must be checked before extrapolation.
- **Masullo**, Chapter 13, p. 522: the putative terminal zero-location theorem still includes an absent statement, unresolved theorem reference, and instructions to finish proof text. This proves the **written presentation here is incomplete**, not that its underlying mathematical ideas are refuted.

See the [Masullo dependency map](dependency-map-masullo.md), [Alpöge dependency map](dependency-map-alpoge.md), and [lemma triage](first-lemma-triage.md).

## Simplification metric

Prefer a reduction that removes hypotheses, dependencies, or analytical limits **while retaining a complete proof**. Record external lemmas, nontrivial estimates, constants lacking uniformity proofs, and unresolved exchanges of limits. A shorter explanation is not, by itself, mathematical verification.
