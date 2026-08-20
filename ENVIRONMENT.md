# Environment and rerun contract

## Runtime

- Intended runtime: CPU
- Python: standard virtual environment
- Numerical dependency: NumPy
- Main random generator seed: 42
- Separate correct-specification seeds: 42 and 99

## Protocol

- C1 uses n = 200, r = 2, rho = 0.3, and five trailing eigenvectors.
- C2, C4, C5, and C6 use n in {50, 100, 200, 400}.
- C2 compares d = r + 1 with d = r.
- C3 generates rank-3 graphs and embeds at d = 2.
- C4 uses seed 42; C5 uses seed 99.

## Local rerun

Create an isolated environment and run:

    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install numpy
    python3 repro/src/verify_rdpg.py

The producer writes outputs/verdict.json. The committed output and run log are the evidence snapshot checked by verify_final.py.

## Missing inputs

Theorem proofs, assumption-matched asymptotic sweeps, complete paper-scale synthetic experiments, and any author-side executable pipeline are not present. Those inputs are required for a full paper reproduction and are outside this repository's finite diagnostic contract.
