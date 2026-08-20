# Status — RDPG Spectral Embedding

Paper: On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models
Paper record: arXiv 2601.06014v1, OpenReview wIMGGV9l1i
Authors: Roddy Taing and Keith Levin
Repository: MachineLearning-Nerd/icml26-rdpg-spectral-embedding
Audit date: 2026-08-20
Audit state: INCONCLUSIVE_C1_C3_C4_C5_C6_FINITE_DIAGNOSTICS_VERIFIED_C2_FINITE_CHECK_FAILED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE

## Outcome

Five of six finite diagnostics pass. C2 fails its four-size slope comparison because the over-specification slope and correct-specification slope are both -0.2343. Zero of six paper claims are independently verified because the available checks are deliberately scoped proxies rather than complete theorem and experiment reproductions.

| Claim | Finite audit result | Evidence boundary |
| --- | --- | --- |
| C1 | VERIFIED_FINITE_DIAGNOSTIC | One bounded trailing-eigenvector check |
| C2 | FINITE_CHECK_FAILED | Four sizes, one seed, and a slope comparison |
| C3 | VERIFIED_FINITE_DIAGNOSTIC | Rank-3 to dimension-2 finite proxy |
| C4 | VERIFIED_FINITE_DIAGNOSTIC | Four-size correct-specification rate proxy |
| C5 | VERIFIED_FINITE_DIAGNOSTIC | Separate seeded Bernoulli RDPG diagnostic |
| C6 | VERIFIED_FINITE_DIAGNOSTIC | Finite error-ordering comparison |

The evidence package contains ten scoped diagnostic points out of a twelve-point six-claim ledger. This is an evidence-package count, not a live judge score. No current score is claimed.

## Evidence boundary

C2's finite failure is retained as evidence about this protocol, not as a theorem falsification. C3's target proxy uses the first two columns of a rank-3 latent matrix, C4 checks convergence rather than an exact theorem constant, C5 covers a narrow binary RDPG setup, and C6 checks the stored finite ordering only.

## Files

- repro/src/rdpg.py — RDPG generation, ASE, alignment, and rate helpers
- repro/src/verify_rdpg.py — deterministic diagnostic producer
- outputs/verdict.json and outputs/verify_run.log — recorded evidence
- CLAIM_EVIDENCE.md — claim production paths and boundaries
- REPORT.md — interpretation and publication boundary
