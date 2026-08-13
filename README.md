# ICML 2026 Reproduction: RDPG Spectral Embedding

Independent, claim-by-claim reproduction audit of **[On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models](https://arxiv.org/abs/2601.06014)** by Roddy Taing and Keith Levin.

This repository studies adjacency spectral embedding (ASE) for a random dot product graph (RDPG) when the embedding dimension is too small, correct, or too large. The included audit is a small NumPy/CPU sanity check. It is not a full proof verification or a paper-scale reproduction.

## What the paper does

An RDPG uses latent node positions `X` to define a probability matrix such as

```text
P = rho_n X X^T
```

The adjacency spectral embedding estimates latent positions from the leading eigenvectors of the observed adjacency matrix. The paper analyzes what happens when the chosen embedding dimension `d` differs from the true latent rank `r`:

- **Under-specification (`d < r`):** the paper proves lower bounds on estimation error, so consistency can fail.
- **Correct specification (`d = r`):** standard ASE consistency and error-rate behavior apply.
- **Over-specification (`d > r`):** consistency still holds, but at a slower rate than with the correct dimension.
- **Non-signal eigenvectors:** the paper develops a delocalization result for eigenvectors associated with the noise-only part of a low-rank signal-plus-noise matrix.

The paper also reports synthetic experiments supporting these statements. This repository contains only lightweight matrix simulations; it does not contain the paper's complete theorem proofs, every assumption-matched experiment, or a full reproduction of its figures.

## Reproduction verdict

The local gate records **5/6 claims verified**. C2 is the one failed finite-simulation check and is intentionally called out below. A failed finite proxy is not by itself a disproof of the paper's theorem, but it means this repository does not support that claim under the included protocol.

| Claim | Paper/reproduction claim | Evidence in this repository | Verdict |
|---|---|---|---|
| C1 | Trailing/non-signal eigenvectors are delocalized (Theorem 3.1) | One RDPG instance with `n=200`, `r=2`, `rho=0.3`; maximum of five selected trailing eigenvector entries `0.2550` versus bound `0.6517`; the verifier accepts `< 3x` the bound | **VERIFIED, FINITE SANITY CHECK** |
| C2 | Over-specification has a slower `n^(-1/4)`-type rate than correct specification (Theorem 3.2) | Four sizes `[50, 100, 200, 400]`; observed over-spec slope `-0.2343` equals the correct-spec slope `-0.2343`, so the gate condition `slope_over > slope_correct` fails | **NOT VERIFIED IN THIS PROTOCOL** |
| C3 | Under-specification is inconsistent / has a non-vanishing error lower bound | Rank-3 graph embedded in dimension 2; proxy errors `[0.4039, 0.3466, 0.3116, 0.2716]` with log-log slope `-0.1871`, which passes the repository's plateau threshold | **VERIFIED, PROXY SCOPE** |
| C4 | Correctly specified ASE error decreases at the claimed scale | Four-size correct-specification run gives slope `-0.2348`, passing the verifier's convergence threshold `< -0.2` | **VERIFIED, RATE PROXY ONLY** |
| C5 | The binary-network extension conjecture is supported | Bernoulli adjacency RDPG diagnostic gives slope `-0.2227` under the same small-size protocol | **VERIFIED, LIMITED BINARY DIAGNOSTIC** |
| C6 | Simulations show over-specification is worse than correct specification and under-specification is worst | Pointwise comparisons require over-spec error to be at least `0.8x` correct-spec error and under-spec error to exceed correct-spec error | **VERIFIED, FINITE SIMULATION** |

### Why C2 is not a clean theorem reproduction

The included C2 check uses one seed, four small graph sizes, one extra embedding dimension, and a simple log-log slope comparison. Its observed slopes are identical, so the code correctly records a failed gate condition. A larger, assumption-matched experiment could still support the paper's asymptotic theorem; this repository does not infer that result from the failed small proxy.

## How each claim is produced

The executable audit is [`repro/src/verify_rdpg.py`](repro/src/verify_rdpg.py), supported by [`repro/src/rdpg.py`](repro/src/rdpg.py). It uses NumPy and writes [`outputs/verdict.json`](outputs/verdict.json).

1. **C1 - delocalization:** generate a symmetric Bernoulli RDPG adjacency matrix, eigendecompose it, select five eigenvectors after the top `r` directions, and compare their largest absolute entries with `r^2 sqrt(log(n+2))/sqrt(n)`. The acceptance threshold is three times the displayed bound.
2. **C2 - over-specification:** for `n in {50, 100, 200, 400}`, generate an RDPG, embed once at `d=r+1` and once at `d=r`, Procrustes-align the estimates, fit log-log slopes, and require the over-specified slope to be less negative than the correct slope. The recorded run fails this requirement.
3. **C3 - under-specification:** generate rank-3 graphs and embed them at dimension 2. The verifier compares the selected two-coordinate target proxy and checks that the error slope is greater than `-0.3`. This is a finite inconsistency diagnostic, not a direct evaluation of every rank-3 lower-bound assumption.
4. **C4 - correct specification:** reuse the correct-dimension ASE path and require the four-size error slope to be below `-0.2`. The check supports decreasing error but does not establish an exact `n^(-1/2)` exponent or theorem constant.
5. **C5 - binary conjecture:** rerun the correct-specification rate diagnostic with a separate RNG seed. Since `generate_rdpg` already samples a Bernoulli adjacency matrix, this checks a narrow binary graph instance rather than all binary-network settings.
6. **C6 - ordering simulation:** compare the stored over-, correct-, and under-specified errors pointwise. This tests the finite ordering used by the local gate, not the complete asymptotic result.

## Reproduce the local audit

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install numpy
python3 repro/src/verify_rdpg.py
```

Expected result for the recorded protocol: C1, C3, C4, C5, and C6 pass; C2 fails the slope comparison.

## Repository contents

| Path | Purpose |
|---|---|
| [`repro/src/rdpg.py`](repro/src/rdpg.py) | RDPG generator, adjacency spectral embedding, Procrustes error, and rate helpers |
| [`repro/src/verify_rdpg.py`](repro/src/verify_rdpg.py) | Claim-by-claim deterministic audit |
| [`outputs/verdict.json`](outputs/verdict.json) | Structured metrics and per-claim verdicts |
| [`outputs/verify_run.log`](outputs/verify_run.log) | Recorded gate output |
| [`publication_gate.json`](publication_gate.json) | Local publication-gate metadata |
| [`GATE_READY.md`](GATE_READY.md) | Gate receipt and limitations |
| [`STATUS.md`](STATUS.md) | Ownership and current status |
| [`branch-audit.md`](branch-audit.md) | Legacy-to-clean branch mapping and final branch contract |

## Branches

The source repository had one branch, `master`. It is normalized to `main`; there are no `orx/*` branches in this repository.

| Clean branch | Former ref | Purpose |
|---|---|---|
| [`main`](https://github.com/MachineLearning-Nerd/icml26-rdpg-spectral-embedding/tree/main) | `master` | Default documented reproduction audit |

See [`branch-audit.md`](branch-audit.md) for the source tip and verification contract.

## Citation

If this audit helps your work, please cite the paper:

```bibtex
@article{taing2026misspecifying,
  title         = {On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models},
  author        = {Taing, Roddy and Levin, Keith},
  journal       = {arXiv preprint arXiv:2601.06014},
  year          = {2026},
  doi           = {10.48550/arXiv.2601.06014}
}
```

## Thank you

Thank you to **Roddy Taing and Keith Levin** for developing a careful account of how embedding-dimension misspecification changes spectral-network estimation. The distinction between under-specification, over-specification, and noise-eigenvector behavior is valuable for reproducibility and practice.

## Attribution and limitations

- Documentation, branch normalization, and verification-audit commits are attributed to **MachineLearning-Nerd**.
- This is a clean-room NumPy audit, not the authors' official implementation.
- The finite checks do not replace theorem proofs and do not cover all RDPG assumptions, sparsity regimes, ranks, dimensions, or graph distributions.
- C2 is not supported by the included run; C3, C4, and C5 are deliberately labeled as proxy or limited diagnostics.
- The under-specification helper compares the two-dimensional estimate with `X[:, :2]` from a rank-3 latent matrix, so it should not be read as a complete reproduction of the full-rank lower-bound target.
