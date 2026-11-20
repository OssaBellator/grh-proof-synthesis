# Alpöge–Claude: source narrative and dependency-audit map

**Primary source:** [Levent Alpöge, four-page author note](https://alpo.ge/remark.pdf), retrieved 20 November 2026 UTC; SHA-256: `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`. All four physical PDF pages were text-extracted and cross-checked with the displayed author note. Its dated timeline ends on 16 November 2026.

**Crucial limitation:** The source is a personal announcement and discovery timeline, **not an expository proof or the Lean declaration-dependency graph**. Its author warns in the p. 3 footnote that some compressed descriptions may require correction. All arrows below are candidate *narrative* connections; they are not established mathematical implications. The massive Lean archive was **not** downloaded or checked.

| Node | Source location | Author-described mechanism | Candidate input or dependency | Current verification status |
| --- | --- | --- | --- | --- |
| A1 | p. 1 | Analogy with Stepanov multiplicity in the function-field setting; an unspecified new Fourier-analytic toy argument | No precise theorem given | Narrative inspected; formal statement absent |
| A2 | pp. 3–4, timeline items 1–7 | Determinants, positivity-style claims, weighted von Mangoldt sums, and period constructions | Alleged analogue of the toy model A1 | The chronology is reported; hypotheses, constants, and mathematical links unknown |
| A3 | p. 1 and p. 4, items 8–10 | Iterated theta lifts among definite unitary groups, claimed increasing multiplicity m, and a proposed chain length roughly √X | Analogy with multiplicity A1; norms and divisibility estimates | No quantified iteration lemma or uniform error estimate is stated |
| A4 | p. 4, items 11–19 | Iwasawa towers, seesaw/Bessel periods, lift costs, integrality, trace-formula constructions, and extra averaging | A3 appears connected in the narrative | No explicit sufficient conditions or proved dependency edges available in this note |
| A5 | pp. 1, 4, timeline item 20 | Claimed RH and Dirichlet GRH, said to be formalized in Lean | Author associates this culmination with A2–A4 | First pass had only the announcement. Five pinned types and immediate proof terms have since been inspected. The analytic narrative still needs a declaration-level audit. |
| A6 | p. 1, footnote 1; p. 2 | Fourteen linked multipart Lean archive files, offered instead of a conventional proof paper | A5 requires a formal source audit | No local archive build. Sutherland reports independent compilation, module replay, a three-axiom audit and full-export nanoda acceptance. |

## Candidate graph

A1 (Stepanov/Fourier toy analogy) → A2 (determinants/prime sums) and A3 (iterated lifts) → A4 (norms, periods, integrality, averaging) → A5 (claimed GRH).

This diagram records a **reported research narrative**, not the actual term dependency graph. None of these arrows may be called a theorem before extracting exact Lean declarations and checking their hypotheses, axioms, and semantic correspondence to Dirichlet GRH.

## First formal-audit questions

1. What exact Lean declaration asserts Dirichlet GRH, and what family of L-functions does it cover?
2. Which hypotheses and imports support that declaration? Does the proof have any new axioms, sorry-like admissions, or trusted external computations?
3. Where is the **first statement** saying that m iterated lifts provide a quantified multiplicity gain, with all conductors, norms, and constants?
4. Where is the final analytic implication from the claimed arithmetic bound to the GRH zero statement?

The [entry-point map](entrypoint-lean-dependency-map.md) answers the declaration question from pinned source, including the principal-character guard. The [verification landscape](verification-landscape-2026-11-21.md) identifies Sutherland’s 19:45 UTC verdicts and Deicyde’s more limited CI scope. Quantified lift costs and the semantic audit remain open. The narrative edges A1–A5 retain their original status.
