# Primary sources and provenance

**Snapshot date:** 2026-11-21. URLs below were discovered from the public announcements; availability and contents can change. Do not confuse finding a URL with independently checking every page or source file.

| ID | Source | Link | Role | Initial status |
| --- | --- | --- | --- | --- |
| A-NOTE | Levent Alpöge, announcement note, 20 Nov 2026 | https://alpo.ge/remark.pdf | Primary statement of claim, rough chronology and proposed mechanisms | Reported; formal artifact audit pending |
| A-LEAN | Lean archive linked from the original note | See A-NOTE and its archive references | Primary formal evidence | Acquisition, hash, build, axiom and theorem audit pending |
| M-ANN | Ravi Vakil, *Hurried Announcement: Alessandro Masullo GRH*, 20 Nov 2026 | https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/ | Announcement and status context | Reported |
| M-PDF | Alessandro Masullo, *The Music of the Primes* | https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf | Primary manuscript | Section-by-section audit pending |

## Source-acquisition protocol

For each upstream release, record in a future `sources.lock.json`:
- retrieval URL, UTC retrieval time, source owner and artifact license;
- byte length, SHA-256 checksum, release/commit if available;
- exact notation for theorem to be checked and relevant page or Lean declaration;
- compiler and Mathlib/Lean versions for a formal artifact;
- independent reproducibility receipt (machine, commands, exit status, log hash);
- any untrusted code or scripts in third-party archives, reviewed before execution.

**Do not automatically execute downloaded proof archives.** Prefer inspecting code and dependency manifests before running anything in a sandbox.

## Verification cautions

- A claim of 'the generalized Riemann hypothesis' may refer to different families of L-functions. This project defaults to **Dirichlet GRH** and explicitly marks any extension.
- A successful Lean build alone can establish only that a precise term typechecks under that kernel and its accepted axioms/imports.
- For handwritten proofs, distinguish a strategy outline from a fully quantified proof.
- Point to source locations rather than paraphrasing a conjectured step as a fact.

## Primary PDF checksums (20 November 2026 UTC retrieval)

The checksums below were independently recomputed in the local Code workspace on 21 November 2026. The PDFs themselves are in ignored local storage and are not committed to GitHub.

| Artifact | Size | Pages | SHA-256 |
| --- | ---: | ---: | --- |
| Alpöge note | 245,114 bytes | 4 | `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d` |
| Masullo draft | 6,756,996 bytes | 940 | `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5` |

See [machine-readable source lock](../data/sources.lock.json). This verifies downloaded artifact identity **only**, not mathematical correctness.

## Second pass, 20 November UTC / 21 November Brisbane

The initial-status table above records the first pass. The two original PDFs still returned the locked SHA-256 values. Sutherland subsequently documented a source build, module replay, axiom lists and nanoda acceptance. Deicyde published successful archive and challenge CI jobs. The landscape records their different cutoffs, the hashes we recomputed on small files, and which large hashes come solely from the operators. [Dated landscape](verification-landscape-2026-11-21.md) · [public run records and source revisions](../data/reproductions.json)

Exact raw URLs, byte counts and SHA-256 values for Main, Statements, the immediate wrappers and official Mathlib definitions are in the [entry-point source inventory](entrypoint-lean-dependency-map.md#artifact-identity-and-external-checks). The paper’s August v2 and the November submission have separate provenance. [Alpöge–Furman revision history](https://arxiv.org/abs/2608.13637v2)
