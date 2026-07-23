# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_9771e7a9e24c", "created_at": "2026-07-23T05:01:00+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Under the random dot product graph (RDPG) model where P = rho_n * X X^T for latent positions X in R^(n x r), Theorem 3.1 shows trailing eigenvectors associated with zero eigenvalues delocalize, with maximum entry magnitude bounded by r^2 (log n)^(4+6*gamma) / sqrt(n) (Theorem 3.1).
2. Theorem 3.2 shows that when the embedding dimension is over-specified (k>0 extra dimensions), consistent estimation of the latent positions still holds but only at the slower rate n^(-1/4), compared to the n^(-1/2) rate achieved under correct specification (Theorem 3.2).
3. Theorem 3.2 also shows that when the embedding dimension is under-specified (k<0), there is a fundamental lower bound on estimation error of order sqrt(|k| * rho_n), which need not vanish as the network size grows, proving inconsistency (Theorem 3.2).
4. Under correct specification, the adjacency spectral embedding satisfies ||X_hat_{1:r} W - rho_n^{1/2} X_{1:r}||_{2,infty} <~ phi_n, typically achieving the n^{-1/2} rate; over-specification adds an error term of order sqrt(sigma^2 k) * r^2 (log n)^(5+6*gamma) / n^{1/4} (Section 3).
5. Section 3.1 states Conjecture 1, extending the over-/under-specification results from weighted networks to binary networks under relaxed variance conditions (Section 3.1, Conjecture 1).
6. Section 4 presents simulation experiments across multiple noise distributions confirming the theoretical over- and under-specification rates (Section 4).
