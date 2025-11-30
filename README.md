# Z(p) Irrationality & Transcendence Explorer

[![CI](https://github.com/kugguk2022/zp-program/actions/workflows/ci.yml/badge.svg)](https://github.com/kugguk2022/zp-program/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A heuristic probe into the algebraic structure of hard constants.**

This project moves beyond known values to explore the **arithmetic nature of odd zeta values, polylogarithms, and period integrals**. We provide reproducible PSLQ scripts to search for algebraic relations and linear dependencies where theoretical proofs are currently impossible.

---

## 🧭 Overview

We aim to generate and classify "maximal" subsets of irrational numbers by probing their properties:

1.  **Algebraic Relation Scans:** Is a constant $$\alpha$$ a root of a polynomial with integer coefficients?
2.  **Linear Independence Scans:** Is a set $$\{1, \alpha, \beta, \gamma\}$$ linearly dependent over $\mathbb{Q}$?

While we document the classical derivation for even zeta values (where $$Z(p)$$ is known transcendental), the core value of this repo is applying these heuristic probes to **open problems** like $$\zeta(3)$$, $$\zeta(5)$$, and Schanuel-type conjectures.

---

## 🚀 Quick Start

```bash
# Set up environment
python -m venv .venv 
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Verify installation
pytest -q
````

-----

## 🔬 Experiments

### 1\. Algebraic Relation Scans (Single Number)

Checks if a single number (like `Zeta(5)`) satisfies a polynomial equation $$P(x) = 0$$.

  * **`z_p/experiments/pslq_scan.py`**: Sweeps odd primes to check $$Z(p)$$ itself.
  * **`z_p/experiments/maximal_pslq_scan.py`**: A targeted probe for specific constants.
      * *Targets:* $$\zeta(3), \zeta(5)$$, Catalan's Constant, Euler-Mascheroni.
      * *Usage:* Run directly to scan these built-in targets.

### 2\. Linear Independence Scans (Multi-Number)

Checks if a group of numbers satisfies a linear equation:

$$c_0 + c_1 x_1 + c_2 x_2 + \dots + c_n x_n = 0$$

  * **`z_p/experiments/linear_independence_scan.py`**:
      * **Odd Zetas:** Checks $$\{1, \zeta(3), \zeta(5), \zeta(7), \zeta(9)\}$$ (Conjectured independent).
      * **Schanuel Set:** Checks $$\{\pi, e, \ln(2)\}$$ (Expected independent).
      * **Sanity Check:** Validates against a known relation ($$\sin^2 + \cos^2 - 1 = 0$$) to prove the tool works.

-----

## 🧮 Math Snapshot

### The Known Case (Even Zetas)

For odd primes $$p$$, we define:

$$ Z(p) = e^{\\pi \\zeta(p-1)/p} + 1 $$

Using Euler's formula for even zeta values $$\zeta(2k)$$, we derive the exact rational coefficient $$c_p$$:

$$c\_p = (-1)^{\\frac{p+1}{2}} \\frac{2^{p-2} B\_{p-1}}{p (p-1)\!}$$

Since $$c_p$$ is rational and $$\pi$$ is transcendental (Lindemann), $$Z(p)$$ is transcendental. This serves as our **calibration ground**.

### The Open Case (Odd Zetas & Periods)

For values like $$\zeta(3)$$ or combinations like $$e + \pi$$, no such closed forms exist.

  * **Lindemann–Weierstrass** does not apply (exponents are not algebraic).
  * **Gelfond–Schneider** does not apply ($$\pi$$ is not algebraic).
  * **Schanuel's Conjecture** suggests independence but is unproven.

**This is where our heuristic scans provide value.**

-----

## 📊 Reading the Output

### Algebraic Scans

  * `POSSIBLE RELATION FOUND`: The tool found coefficients such that $$\sum a_i x^i \approx 0$$.
      * *Action:* Check the **residual**. If it is $$10^{-100}$$ or smaller, verify with higher precision.
  * `None`: No relation found up to the specified Degree and Height.
      * *Meaning:* Evidence that the number is likely transcendental (or the defining polynomial is massive).

### Linear Independence

  * `RELATION FOUND`: The numbers are linearly dependent (e.g., $$2x - 3y = 0$$).
  * `No linear relation found`: The set appears linearly independent.
      * *Significance:* This is a computational verification of the prerequisites for Schanuel's Conjecture.

-----

## 📦 Repository Map

```text
z_p/
  zeta_even_reduction.md      # Math derivation for the solved (even) cases
  proof_sketch.md             # Theoretical background & conditional proofs
  experiments/
    pslq_scan.py              # General scanner for Z(p)
    maximal_pslq_scan.py      # TARGETED scanner for hard open constants
    linear_independence_scan.py  # Multi-variable independence checker
tests/
  test_cp.py                  # Unit tests for rational coefficients
```

-----

## 🛣️ Roadmap

1.  **Refine Heuristics:** Increase bit-precision and polynomial degree limits for deeper scans of $$\zeta(5)$$.
2.  **Expand Scope:** Add generalized Polylogarithms $$Li_s(z)$$ to the generator.
3.  **Documentation:** Formalize the link between "Linear Independence Scans" and the conditions required for Schanuel’s Conjecture.

-----

## License

MIT — see `LICENSE`.

## Citation
If you use this work in your research, please cite:
```
@software{Z(p) Irrationality & Transcendence Explorer Program 2025, 
-title={Z(p) Irrationality & Transcendence Explorer},
-author={kugguk2022},
-year={2025}, 
-url={[https://github.com/kugguk2022/lotteries](https://github.com/EncapsulatorP/zp-program/)} }
```

```
