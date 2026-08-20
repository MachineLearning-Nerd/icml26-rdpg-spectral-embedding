# Claim evidence — RDPG Spectral Embedding

Paper: On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models
Paper record: arXiv 2601.06014v1, OpenReview wIMGGV9l1i
Repository scope: clean-room NumPy finite-diagnostic audit

## C1 — trailing eigenvector delocalization

Paper anchor: Theorem 3.1's bounded-entry or delocalization behavior for eigenvectors after the signal rank.

Production path: repro/src/verify_rdpg.py generates a Bernoulli RDPG with n = 200, r = 2, and rho = 0.3. It calls trailing_eigenvector_delocalization, selects five trailing eigenvectors, and compares their largest absolute entry with the displayed r squared square-root-log bound.

Observed result: maximum entry is 0.2550 and the displayed bound is 0.6517; the local threshold check passes.

Verdict: VERIFIED_FINITE_DIAGNOSTIC. One small instance does not reproduce the theorem's assumptions or proof.

## C2 — over-specification rate

Paper anchor: Theorem 3.2's slower over-specification rate relative to correct specification.

Production path: repro/src/verify_rdpg.py calls over_specification_rate and correct_specification_rate at n in {50, 100, 200, 400}, fits log-log slopes, and requires the over-specified slope to be less negative than the correct-specification slope.

Observed result: both slopes are -0.2343202846, so the required strict comparison fails.

Verdict: FINITE_CHECK_FAILED. This is a limitation of the one-seed, four-size proxy and is not treated as a disproof of the asymptotic theorem.

## C3 — under-specification inconsistency

Paper anchor: under-specification can retain a non-vanishing error lower bound.

Production path: the verifier generates rank-3 RDPGs at the four sizes, embeds at dimension 2, compares the estimate with the first two columns of the latent matrix, fits the log-log error slope, and requires the slope to be greater than -0.3.

Observed result: errors are 0.4039, 0.3466, 0.3116, and 0.2716 with slope -0.1871, so the local plateau proxy passes.

Verdict: VERIFIED_FINITE_DIAGNOSTIC. The first-two-columns target is a bounded helper proxy, not the full-rank lower-bound target.

## C4 — correct-specification ASE rate

Paper anchor: correctly specified ASE error decreases at the claimed scale.

Production path: the verifier runs correct_specification_rate at the four sizes with seed 42, fits a log-log slope, and requires it to be below -0.2.

Observed result: the slope is -0.2348 and passes the local convergence threshold.

Verdict: VERIFIED_FINITE_DIAGNOSTIC. This does not establish an exact n to the power minus one-half exponent or theorem constant.

## C5 — binary-network extension

Paper anchor: the binary-network extension conjecture.

Production path: the verifier reruns correct_specification_rate with seed 99. The RDPG generator samples a Bernoulli adjacency matrix, so the route checks a narrow binary graph setting.

Observed result: the slope is -0.2227 and passes the local threshold.

Verdict: VERIFIED_FINITE_DIAGNOSTIC. It does not cover all binary-network assumptions or regimes.

## C6 — finite simulation ordering

Paper anchor: simulations show over-specification worse than correct specification and under-specification worst.

Production path: the verifier compares stored over-specification, correct-specification, and under-specification errors pointwise. It requires over-specification to exceed 0.8 times the correct error and under-specification to exceed the correct error.

Observed result: both ordering checks pass.

Verdict: VERIFIED_FINITE_DIAGNOSTIC. This checks the selected finite simulation ordering, not the full asymptotic result.
