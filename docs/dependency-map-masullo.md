# Masullo: source-grounded trace-formula dependency map

**Primary source:** [Alessandro Maria Masullo, *The Music of the Primes*](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf), 940 physical PDF pages, retrieved 20 November 2026 UTC; SHA-256: `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5`. Server Last-Modified: 20 November 2026, 18:18:35 GMT. Inspected page ranges: contents pp. 3–5, introductory material pp. 6–20 and 27–36, sampled pp. 433–434, main statement pp. 519–520, and terminal deductions pp. 521–522. **This is a sampling, not a review of the complete 940-page proof.**

The [20 November announcement by Ravi Vakil](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/) describes this as a proposed GRH proof. The manuscript's p. 6 author note acknowledges unfinished writing and known glitches. Status throughout is **author-proposed**, not independently verified.

| Node | Source location | Statement or mechanism | Suggested inputs and explicit references | Inspection status |
| --- | --- | --- | --- | --- |
| M0 | pp. 6–11 | Number fields F, idele classes, Hecke characters and L-functions are the general setting | Established definitions and analytic properties of Hecke L-functions are inputs | Selected introductory definitions inspected; conventions not audited fully |
| M1 | Intro pp. 11–14; Ch. 9 (§9.2, p. 403); §10.1 p. 434 | Weighted Schwartz/Hardy–Sobolev spaces and completions used to control spectral evaluation | Requires topology, completeness, continuity, and closure results | Intro and p. 434 sampled; proofs in Ch. 9 not audited |
| M2 | Contents: Chs. 4–7, pp. 155–380; intro pp. 12–16 | Periodic/orbital Schauder bases, structure theorems, poles and nuclearity | Proposed analytic infrastructure for trace decomposition | Mostly introduction and table-of-contents level; no verification of structure theorems |
| M3 | Contents: Chs. 8, 10–12, pp. 381–520; intro pp. 15–16, 27 | Orbital decomposition, geometric and spectral trace calculations, trace-norm limits | Depends on M1–M2 plus justified nuclearity, convergence, kernel restriction and limit interchanges | Only sampled; critical operator steps unaudited |
| M4 | §12.5, pp. 519–520, **Theorem 12.5.1.1** | A trace formula for test functions φ on the idele class group satisfying φ(C_F¹)=0, with zeros counted in a specified vertical strip | The text of the proof cites Theorems 11.3.2.1, 12.4.1.1 and 10.4.2.8 and Definition 10.4.3.7 | Statement and citation chain inspected, cited results **not** verified |
| M5 | Intro §1.4, pp. 27–32 | Described passage from restricted trace identities to stronger zero-location assertions via test-function families, normal-family arguments and analytic continuation | Needs **uniform** estimates as the test-function family and interval change, plus correct treatment of poles/trivial zeros | Narrative inspected, no complete deduction independently established |
| M6 | Ch. 13, pp. 521–522, **§13.3** | Intended main theorems locating Hecke L-function zeros | Refers to M4 and an unspecified “Theorem ??”, then an intended approximation argument | **Visible written gap:** Theorem 13.3.1.2 has no statement; footnotes say to insert it and to state/prove the main theorems |

## Explicit dependency chain versus conjectural arrows

The source explicitly cites results in support of Theorem 12.5.1.1 (M4); these exact citations are documented above. Most other edges, **M1 → M2 → M3 → M4 → M5 → M6**, are an inferred organizational reconstruction from the chapter structure and introduction, **not** independently proved implications.

**Two mandatory reconciliation questions:**

1. On **p. 519**, the author says the calculation is done in the special case **a = 1/2**, emphasizing the necessity of that choice. In the introduction, the proposed zero-location strategy discusses varying the localization interval/parameter. Establish which variable is held fixed and which can vary before concluding that the trace formula works on arbitrarily narrow strips. There is **no demonstrated contradiction** merely from these passages.
2. In **§1.7.2, around pp. 35–36**, Masullo says the trace formula requires **φ(C_F¹)=0** and that this restriction rules out nonzero positive autocorrelation tests of the form ψ * ψ*. This blocks a naïve plug-in of Weil positivity to the proposed trace formula; any hybrid needs a new theorem overcoming the mismatch.

## Visible missing terminal step

**Physical p. 522** prints Theorem 13.3.1.1 with additional vanishing conditions, then “Upon combining Theorem 13.3.1.1 and Theorem ??, we obtain ...”, followed by Theorem 13.3.1.2 **without a statement**. Its footnotes instruct the author to insert the statement and state/prove the main theorems. This demonstrates that the *written terminal argument at this location is incomplete*, not that the author's underlying ideas are necessarily false. It prevents promoting M6 to a proved theorem based on the available draft.

## Next tractable source-specific checks

- Verify the exact test-function restriction and its interaction with autocorrelation positivity (see [first-lemma triage](first-lemma-triage.md)).
- Pin down parameter a in §12.5 relative to the interval family in §1.4.
- Trace the finite-to-nuclear operator passage of Theorem 12.5.1.1, specifically every summation/integration exchange and operator-domain claim.
