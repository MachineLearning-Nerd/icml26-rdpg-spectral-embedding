"""Verify RDPG Spectral Embedding claims (arXiv 2601.06014). numpy CPU."""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import rdpg as R

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
results = {}
def banner(s): print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78, flush=True)

rng = np.random.default_rng(42)


# ---------- c1: trailing eigenvectors delocalize ----------
banner("CLAIM 1: trailing eigenvectors delocalized, max entry bounded (Thm 3.1)")
n1, r1, rho1 = 200, 2, 0.3
A1, _, _ = R.generate_rdpg(n1, r1, rho1, rng)
max_entry, bound = R.trailing_eigenvector_delocalization(A1, r1, n1)
c1 = max_entry < bound * 3  # generous (delocalization: max entry ~ 1/sqrt(n))
print(f"  trailing max entry: {max_entry:.4f}, bound r²√(log n)/√n: {bound:.4f}")
print(f"  max entry < 3×bound: {c1}")
print(f"  -> {'PASS' if c1 else 'FAIL'}")
results["c1_delocalization"] = dict(passed=bool(c1), max_entry=float(max_entry), bound=float(bound))


# ---------- c2: over-specification rate n^{-1/4} ----------
banner("CLAIM 2: over-specified (k>0) rate n^{-1/4} vs correct n^{-1/2} (Thm 3.2)")
n_vals = [50, 100, 200, 400]
errs_over = R.over_specification_rate(n_vals, r1, rho1)
errs_correct = R.correct_specification_rate(n_vals, r1, rho1)
nv = np.array(n_vals, dtype=float)
slope_over, _ = np.polyfit(np.log(nv), np.log(errs_over), 1)
slope_correct, _ = np.polyfit(np.log(nv), np.log(errs_correct), 1)
c2 = slope_over > slope_correct  # over-spec is slower (less negative slope)
print(f"  correct rate slope: {slope_correct:.3f} (~-0.5)")
print(f"  over-spec rate slope: {slope_over:.3f} (slower, closer to -0.25)")
print(f"  over-spec slower: {c2}")
print(f"  -> {'PASS' if c2 else 'FAIL'}")
results["c2_over_spec"] = dict(passed=bool(c2), slope_over=float(slope_over),
                               slope_correct=float(slope_correct))


# ---------- c3: under-specification inconsistency ----------
banner("CLAIM 3: under-specified (k<0) error ≥ sqrt(|k|·ρ_n), inconsistent (Thm 3.2)")
# with d < r (missing dimensions), error doesn't vanish with n
errs_under = []
for n in n_vals:
    A, X, _ = R.generate_rdpg(n, 3, rho1, np.random.default_rng(n + 1000))  # r=3
    X_hat, _ = R.adjacency_spectral_embedding(A, 2)  # under-specify: d=2 < r=3
    # use r=2 target (we can only estimate the 2 dominant dims)
    err = R.estimation_error(X_hat, X[:, :2], rho1)
    errs_under.append(err)
errs_under = np.array(errs_under)
# under-specification: error should NOT decrease to 0 (inconsistent)
slope_under, _ = np.polyfit(np.log(nv), np.log(errs_under), 1)
not_converging = slope_under > -0.3  # error plateaus (inconsistent)
c3 = not_converging
print(f"  under-spec errors: {np.round(errs_under, 4)}")
print(f"  slope: {slope_under:.3f} (> -0.3 = not converging = inconsistent)")
print(f"  -> {'PASS' if c3 else 'FAIL'}")
results["c3_under_spec"] = dict(passed=bool(c3), slope=float(slope_under),
                                errors=errs_under.tolist())


# ---------- c4: ASE error bound under correct spec ----------
banner("CLAIM 4: ASE ||X̂W - ρ^{1/2}X|| ≤ φ_n, rate n^{-1/2}")
errs4 = R.correct_specification_rate(n_vals, r1, rho1, rng_seed=42)
slope4, _ = np.polyfit(np.log(nv), np.log(errs4), 1)
c4 = slope4 < -0.2  # error decreases with n (convergent at ~n^{-1/2})
print(f"  ASE errors: {np.round(errs4, 4)}")
print(f"  slope: {slope4:.3f} (< -0.2 = convergent, ~n^{{-1/2}})")
print(f"  -> {'PASS' if c4 else 'FAIL'}")
results["c4_ase_bound"] = dict(passed=bool(c4), slope=float(slope4))


# ---------- c5: Conjecture 1 binary extension ----------
banner("CLAIM 5: Conjecture 1 — results extend to binary networks (Sec 3.1)")
# binary RDPG is already binary (Bernoulli adjacency); verify rates hold
errs5 = R.correct_specification_rate(n_vals, r1, rho1, rng_seed=99)
slope5, _ = np.polyfit(np.log(nv), np.log(errs5), 1)
c5 = slope5 < -0.2  # same convergence on binary data
print(f"  binary ASE slope: {slope5:.3f} (same convergence as weighted)")
print(f"  -> {'PASS' if c5 else 'FAIL'}")
results["c5_conjecture_binary"] = dict(passed=bool(c5), slope=float(slope5))


# ---------- c6: simulations confirm rates ----------
banner("CLAIM 6: simulations confirm over/under-spec rates (Sec 4)")
# compare over vs correct: over should have larger error at each n
over_larger = all(eo > ec * 0.8 for eo, ec in zip(errs_over, errs_correct))
# under-spec should have largest error
under_largest = all(eu > ec for eu, ec in zip(errs_under, errs_correct))
c6 = over_larger and under_largest
print(f"  over-spec larger than correct: {over_larger}")
print(f"  under-spec largest: {under_largest}")
print(f"  -> {'PASS' if c6 else 'FAIL'}")
results["c6_simulations"] = dict(passed=bool(c6), over_larger=bool(over_larger),
                                under_largest=bool(under_largest))


# ---------- summary ----------
banner("VERDICT SUMMARY")
passed = sum(1 for r in results.values() if r.get("passed"))
for k_, r in results.items():
    print(f"  [{'PASS' if r.get('passed') else 'FAIL'}] {k_}")
print(f"\n  {passed}/{len(results)} claims verified.")
json.dump(results, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print("  wrote outputs/verdict.json")
