# Reproduction report

## Executive result

This repository provides a transparent finite-diagnostic audit of embedding-dimension misspecification in RDPGs. Five of six finite diagnostics pass; C2's small slope comparison fails. Because these checks are scoped proxies, the audit records zero of six paper claims as independently verified.

## Results

| Claim | Result | Boundary |
| --- | --- | --- |
| C1 | maximum trailing entry 0.2550 versus displayed bound 0.6517 | one n = 200 diagnostic |
| C2 | failed; both slopes are -0.2343 | one seed and four graph sizes |
| C3 | slope -0.1871 passes the local plateau threshold | rank-3 to dimension-2 proxy |
| C4 | slope -0.2348 passes the local convergence threshold | four-size finite rate proxy |
| C5 | binary slope -0.2227 passes | narrow Bernoulli RDPG diagnostic |
| C6 | over/correct/under ordering passes | stored finite errors |

## Interpretation

The outputs support the recorded finite behavior in the selected RDPG simulations. They do not reproduce the paper's theorem proofs, all assumptions, asymptotic constants, full network regimes, or complete experiment suite. C2's failed finite comparison is a reason to keep the audit inconclusive, not a reason to declare the paper's theorem false.

## Publication boundary

The repository is suitable as an explicitly partial audit when its finite scope and C2 limitation remain visible. It is not suitable for a claim of complete paper reproduction, theorem verification, or a current competition score.
