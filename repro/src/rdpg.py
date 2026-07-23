"""Clean-room RDPG Spectral Embedding (arXiv 2601.06014). numpy CPU.

Random Dot Product Graph: P = ρ_n * X X^T, X ∈ R^{n×r}.
Adjacency Spectral Embedding (ASE): top-r eigenvectors of adjacency matrix A.
Over-specification (k>0 extra dims): rate n^{-1/4} (slower than n^{-1/2}).
Under-specification (k<0 missing dims): error ≥ sqrt(|k|ρ_n) (inconsistent).
"""
from __future__ import annotations
import numpy as np


def generate_rdpg(n, r, rho, rng):
    """Generate RDPG: latent X ~ Uniform, P = rho * X @ X^T, A ~ Bernoulli(P)."""
    X = rng.uniform(0.5, 1.0, (n, r))
    P = rho * X @ X.T
    P = np.clip(P, 0, 1)
    A = (rng.random((n, n)) < P).astype(float)
    A = np.triu(A, 1) + np.triu(A, 1).T  # symmetric
    return A, X, P


def adjacency_spectral_embedding(A, d):
    """ASE: top-d eigenvectors of A scaled by sqrt(eigenvalues)."""
    evals, evecs = np.linalg.eigh(A)
    # top-d by absolute eigenvalue
    idx = np.argsort(np.abs(evals))[::-1][:d]
    return evecs[:, idx] * np.sqrt(np.abs(evals[idx])), evals[idx]


def estimation_error(X_hat, X_true, rho):
    """Procrustes-aligned estimation error ||X_hat W - ρ^{1/2} X_true||_F / sqrt(n)."""
    n, r = X_true.shape
    X_target = np.sqrt(rho) * X_true
    # Procrustes alignment: W = argmin ||X_hat W - X_target|| via SVD
    U, _, Vt = np.linalg.svd(X_hat[:, :r].T @ X_target)
    W = U @ Vt
    err = np.linalg.norm(X_hat[:, :r] @ W - X_target, 'fro') / np.sqrt(n)
    return err


def trailing_eigenvector_delocalization(A, r, n):
    """Theorem 3.1: trailing eigenvectors (associated with ~0 eigenvalues) have
    max entry magnitude bounded by r^2 * (log n)^{1/2} / n^{1/2}."""
    evals, evecs = np.linalg.eigh(A)
    trailing_idx = np.argsort(np.abs(evals))[r:][:5]  # 5 trailing eigenvectors
    max_entries = [np.max(np.abs(evecs[:, i])) for i in trailing_idx]
    bound = r**2 * np.sqrt(np.log(n + 2)) / np.sqrt(n)
    return max(max_entries), bound


def over_specification_rate(n_vals, r, rho, rng_seed=0):
    """Measure ASE error with d=r+k (over-specified, k>0) across n.
    Expected rate: n^{-1/4} (slower than correct n^{-1/2})."""
    errs = []
    for n in n_vals:
        rng = np.random.default_rng(rng_seed + n)
        A, X, _ = generate_rdpg(n, r, rho, rng)
        X_hat, _ = adjacency_spectral_embedding(A, r + 1)  # over-specify by 1
        err = estimation_error(X_hat, X, rho)
        errs.append(err)
    return errs


def correct_specification_rate(n_vals, r, rho, rng_seed=0):
    """ASE error with d=r (correctly specified). Expected rate: n^{-1/2}."""
    errs = []
    for n in n_vals:
        rng = np.random.default_rng(rng_seed + n)
        A, X, _ = generate_rdpg(n, r, rho, rng)
        X_hat, _ = adjacency_spectral_embedding(A, r)
        err = estimation_error(X_hat, X, rho)
        errs.append(err)
    return errs
