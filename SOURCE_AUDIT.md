# Source audit

## Paper record

- Title: On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models
- Authors: Roddy Taing and Keith Levin
- arXiv: 2601.06014v1
- OpenReview: wIMGGV9l1i
- Paper URL: https://arxiv.org/abs/2601.06014v1

The repository is a clean-room NumPy audit. It contains no author implementation and does not claim to reproduce the paper's theorem proofs.

## Claim-to-source mapping

| Claim | Paper anchor | Local producer or record |
| --- | --- | --- |
| C1 | trailing eigenvector delocalization | repro/src/verify_rdpg.py and repro/src/rdpg.py::trailing_eigenvector_delocalization |
| C2 | over-specification rate | repro/src/verify_rdpg.py and repro/src/rdpg.py::over_specification_rate |
| C3 | under-specification inconsistency | repro/src/verify_rdpg.py and repro/src/rdpg.py::estimation_error |
| C4 | correct-specification ASE rate | repro/src/verify_rdpg.py and repro/src/rdpg.py::correct_specification_rate |
| C5 | binary extension | repro/src/verify_rdpg.py with seed 99 |
| C6 | finite simulation ordering | repro/src/verify_rdpg.py |

## Scope and divergence audit

- All diagnostics use small finite RDPG simulations and NumPy eigendecompositions.
- C2's failure is preserved as a protocol result, not upgraded to theorem falsification.
- C3 compares a dimension-2 estimate with the first two coordinates of a rank-3 latent matrix.
- C4 and C5 use slope thresholds rather than a formal rate proof.
- C6 uses the stored finite error arrays and does not rerun a paper-scale experiment.
- The default RNG seed is 42, with separate seeded routes for C4 and C5.
- No current live-judge score is available or claimed.

## Attribution audit

The paper authors remain the authors of the paper and its claims. MachineLearning-Nerd applies only to this independent audit repository, its documentation, its branch normalization, and its reachable commit history.
