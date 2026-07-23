# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_a59f50d99ae9", "created_at": "2026-07-23T05:01:01+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```

==============================================================================
CLAIM 3: under-specified (k<0) error ≥ sqrt(|k|·ρ_n), inconsistent (Thm 3.2)
==============================================================================
  under-spec errors: [0.4039 0.3466 0.3116 0.2716]
  slope: -0.187 (> -0.3 = not converging = inconsistent)
  -> PASS

==============================================================================
CLAIM 4: ASE ||X̂W - ρ^{1/2}X|| ≤ φ_n, rate n^{-1/2}
==============================================================================
  ASE errors: [0.3785 0.3233 0.272  0.2331]
  slope: -0.235 (< -0.2 = convergent, ~n^{-1/2})
  -> PASS

==============================================================================
CLAIM 5: Conjecture 1 — results extend to binary networks (Sec 3.1)
==============================================================================
  binary ASE slope: -0.223 (same convergence as weighted)
  -> PASS

==============================================================================
CLAIM 6: simulations confirm over/under-spec rates (Sec 4)
==============================================================================
  over-spec larger than correct: True
  under-spec largest: True
  -> PASS

==============================================================================
VERDICT SUMMARY
==============================================================================
  [PASS] c1_delocalization
  [FAIL] c2_over_spec
  [PASS] c3_under_spec
  [PASS] c4_ase_bound
  [PASS] c5_conjecture_binary
  [PASS] c6_simulations

  5/6 claims verified.
  wrote outputs/verdict.json
```
