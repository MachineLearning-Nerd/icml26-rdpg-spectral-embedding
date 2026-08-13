# Status - icml26-rdpg-spectral-embedding

- **Paper:** On the Effect of Misspecifying the Embedding Dimension in Low-rank Network Models ([arXiv 2601.06014v1](https://arxiv.org/abs/2601.06014v1), OpenReview wIMGGV9l1i)
- **Repository:** `MachineLearning-Nerd/icml26-rdpg-spectral-embedding`
- **Owner:** MachineLearning-Nerd
- **State:** DOCUMENTED - local gate reports 5/6 finite diagnostics passing and 0/6 paper claims independently verified; C2 is not verified by the included finite slope protocol.

## Claim status

- C1, C3, C4, C5, and C6 pass the current NumPy audit.
- C2 fails because the observed over-specification slope (`-0.2343`) is equal to the correct-specification slope (`-0.2343`) in the four-size run.
- The failed finite check is recorded as an audit limitation, not as a disproof of the paper's asymptotic theorem.

## Files

- `repro/src/rdpg.py` - RDPG generation, ASE, alignment, and rate helpers.
- `repro/src/verify_rdpg.py` - deterministic claim verifier.
- `outputs/verdict.json` and `outputs/verify_run.log` - recorded evidence.
- `docs/` is not used in this repository; the paper is cited by arXiv link in `README.md`.

## Publication state

The GitHub mirror is renamed and published with a clean `main` branch, branch audit, citation, thank-you note, and explicit finite-scope limitations.
