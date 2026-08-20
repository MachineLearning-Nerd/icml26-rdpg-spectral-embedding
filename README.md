# ICML 2026 Reproduction Audit: RDPG Spectral Embedding

Independent, claim-by-claim evidence audit of [On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models](https://arxiv.org/abs/2601.06014v1) by Roddy Taing and Keith Levin.

Repository: [MachineLearning-Nerd/icml26-rdpg-spectral-embedding](https://github.com/MachineLearning-Nerd/icml26-rdpg-spectral-embedding)

## Executive result

The clean-room audit passes five finite NumPy diagnostics and records one finite diagnostic failure:

- C1, C3, C4, C5, and C6 pass under the included bounded protocol.
- C2 fails because its observed over-specification slope equals the correct-specification slope in the four-size run.
- The failed finite proxy is not treated as a disproof of the paper's asymptotic theorem.
- These finite checks are evidence about the audited diagnostics; they are not counted as independent verification of the six paper-level claims.
- The dossier therefore records 5/6 finite diagnostics, 0/6 paper claims independently verified, and no current competition score.

The full status is in [STATUS.md](STATUS.md), the claim-to-evidence production paths are in [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md), and the machine-readable boundary is in [claims.json](claims.json) and [reproduction_verdicts.json](reproduction_verdicts.json).

## What the paper does

An RDPG uses latent node positions X to define a probability matrix such as P = rho_n X X transpose. Adjacency spectral embedding estimates latent positions from leading eigenvectors of the observed adjacency matrix.

The paper studies what happens when the selected embedding dimension d differs from the true latent rank r:

- Under-specification, d < r, can produce a non-vanishing error lower bound.
- Correct specification, d = r, gives the standard ASE consistency and rate behavior.
- Over-specification, d > r, remains consistent but can have a slower rate.
- Eigenvectors associated with the noise-only part of a low-rank signal-plus-noise matrix are analyzed through a delocalization result.

The paper also reports synthetic experiments. This repository contains only lightweight NumPy/CPU simulations; it does not reproduce the paper's theorem proofs, every assumption-matched experiment, or the full figure set.

This repository is an independent audit, not the authors' official implementation.

## Claim ledger

| Claim | Paper-level statement | Audit evidence | Boundary |
| --- | --- | --- | --- |
| C1 | Trailing/non-signal eigenvectors are delocalized | One n = 200, r = 2 RDPG instance and a bounded-entry check | VERIFIED_FINITE_DIAGNOSTIC |
| C2 | Over-specification has a slower n to the power minus one-quarter rate | Four sizes, one extra dimension, and log-log slope comparison | FINITE_CHECK_FAILED |
| C3 | Under-specification is inconsistent or has a non-vanishing error lower bound | Rank-3 graph embedded in dimension 2; finite slope proxy | VERIFIED_FINITE_DIAGNOSTIC |
| C4 | Correctly specified ASE error decreases at the claimed scale | Four-size correct-specification rate proxy | VERIFIED_FINITE_DIAGNOSTIC |
| C5 | The binary-network extension is supported | Separate seeded Bernoulli RDPG rate diagnostic | VERIFIED_FINITE_DIAGNOSTIC |
| C6 | Simulations order over-, correct-, and under-specification | Pointwise comparison of stored finite errors | VERIFIED_FINITE_DIAGNOSTIC |

The local C2 failure is a limitation of the included protocol. It does not establish that the paper's theorem is false.

## How each claim is produced

The executable producer is [repro/src/verify_rdpg.py](repro/src/verify_rdpg.py), supported by [repro/src/rdpg.py](repro/src/rdpg.py). It uses NumPy with deterministic seeds and writes [outputs/verdict.json](outputs/verdict.json).

1. C1 generates a symmetric Bernoulli RDPG adjacency matrix, eigendecomposes it, selects five eigenvectors after the top r directions, and checks the largest entry against r squared times the square root of log(n) divided by square root of n. The local acceptance threshold is three times the displayed bound.
2. C2 generates RDPGs at n in {50, 100, 200, 400}, embeds once at d = r + 1 and once at d = r, Procrustes-aligns the estimates, fits log-log slopes, and requires the over-specified slope to be less negative than the correct slope. The recorded run fails this comparison because both slopes are -0.2343.
3. C3 generates rank-3 graphs and embeds them at dimension 2. The verifier compares the selected two-coordinate target proxy and checks that its error slope is greater than -0.3. This is a finite inconsistency diagnostic, not a complete lower-bound reproduction.
4. C4 reuses the correct-dimension ASE path and requires the four-size error slope to be below -0.2. This supports decreasing error but does not establish an exact exponent or theorem constant.
5. C5 reruns the correct-specification rate diagnostic with a separate seed. The generated adjacency matrices are Bernoulli, so this is a narrow binary graph check rather than all binary-network settings.
6. C6 compares the stored over-, correct-, and under-specified errors pointwise. This tests the finite ordering used by the local gate, not the complete asymptotic result.

## Why C2 is not a theorem disproof

The C2 route uses one seed, four small graph sizes, one extra embedding dimension, and a simple log-log slope comparison. Its observed slopes are identical, so the code correctly records a failed gate condition. A larger, assumption-matched experiment could still support the paper's asymptotic theorem; this repository does not infer that result from the failed small proxy.

## Reproduce the local audit

Create an isolated environment and run:

    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install numpy
    python3 repro/src/verify_rdpg.py

Expected result: C1, C3, C4, C5, and C6 pass; C2 fails the recorded slope comparison. The committed output is the evidence snapshot checked by verify_final.py.

## Repository contents

| Path | Purpose |
| --- | --- |
| [repro/src/rdpg.py](repro/src/rdpg.py) | RDPG generator, ASE, Procrustes error, and rate helpers |
| [repro/src/verify_rdpg.py](repro/src/verify_rdpg.py) | Deterministic claim diagnostic producer |
| [outputs/verdict.json](outputs/verdict.json) | Raw metrics and per-diagnostic results |
| [outputs/verify_run.log](outputs/verify_run.log) | Recorded producer output |
| [publication_gate.json](publication_gate.json) | Conservative finite-diagnostic gate |
| [GATE_READY.md](GATE_READY.md) | Gate receipt and limitations |
| [STATUS.md](STATUS.md) | Current reproduction boundary |
| [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) | Claim-by-claim evidence production ledger |
| [SOURCE_AUDIT.md](SOURCE_AUDIT.md) | Paper/source/implementation mapping |
| [ENVIRONMENT.md](ENVIRONMENT.md) | Runtime and rerun contract |
| [REPORT.md](REPORT.md) | Interpretation and publication boundary |
| [branch-audit.md](branch-audit.md) | Legacy branch mapping and clean branch contract |
| [verify_final.py](verify_final.py) | Static final-state verifier |

## Branches

The source repository contained one legacy branch, master. It is normalized to main. There are no master or orx branches in the published repository.

| Clean branch | Former ref | Purpose |
| --- | --- | --- |
| [main](https://github.com/MachineLearning-Nerd/icml26-rdpg-spectral-embedding/tree/main) | master | Default documented reproduction audit |

## Citation

If this audit is useful, please cite the paper:

    @article{taing2026misspecifying,
      title         = {On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models},
      author        = {Taing, Roddy and Levin, Keith},
      journal       = {arXiv preprint arXiv:2601.06014},
      year          = {2026},
      doi           = {10.48550/arXiv.2601.06014}
    }

Repository citation metadata is also provided in [CITATION.cff](CITATION.cff).

## Thank you

Thank you to Roddy Taing and Keith Levin for developing a careful account of how embedding-dimension misspecification changes spectral-network estimation. The distinction between under-specification, over-specification, and noise-eigenvector behavior is valuable for reproducibility and practice.

## Attribution and limitations

- The paper authors remain the authors of the paper and its claims.
- Documentation, branch normalization, and audit commits are attributed to MachineLearning-Nerd.
- This is a clean-room NumPy audit, not the authors' official implementation.
- The finite checks do not replace theorem proofs and do not cover all RDPG assumptions, sparsity regimes, ranks, dimensions, or graph distributions.
- C2 is not supported by the included run; C3, C4, and C5 are deliberately labeled as proxy or limited diagnostics.
- The under-specification helper compares the two-dimensional estimate with the first two columns of a rank-3 latent matrix, so it should not be read as a complete reproduction of the full-rank lower-bound target.
