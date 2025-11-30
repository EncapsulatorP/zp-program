# Z(p) Irrationality & Transcendence Explorer

[![CI](https://github.com/kugguk2022/zp-program/actions/workflows/ci.yml/badge.svg)](https://github.com/kugguk2022/zp-program/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Heuristic probes for algebraic structure of hard constants (odd zetas, polylog-type periods, and Schanuel-style tuples). We document the closed form for even cases, then run reproducible PSLQ scans—both algebraic (single number) and linear-independence (many numbers)—to gather numerical evidence where proofs are out of reach.

---

## Overview

- **Algebraic relation scans**: does a single constant satisfy a polynomial with small integer coefficients?
- **Linear-independence scans**: does a tuple of constants satisfy an integer linear relation?
- Targets include $$\zeta(3),\ \zeta(5),\ \zeta(7),\ \zeta(9)$$, Catalan, Euler–Mascheroni, and Schanuel-style tuples such as $$\{\pi, e, \ln 2\}$$.

---

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

---

## Experiments

### Algebraic relation scans (single number)
- `z_p/experiments/pslq_scan.py`: sweep odd primes and search for algebraic relations of $$Z(p)$$ itself.  
  Example:  
  ```bash
  python z_p/experiments/pslq_scan.py --pmin 3 --pmax 31 --prec 300 --deg 6 --height 2000 --processes 4 --timeout 30
  ```  
  Multiprocessing is used for prime sweeps; `--timeout` (seconds) skips slow outliers.
- `z_p/experiments/maximal_pslq_scan.py`: targeted probe for specific constants (e.g., $$\zeta(3), \zeta(5), \zeta(7), \zeta(9)$$, Catalan, Euler–Mascheroni). Run as-is for built-ins or call `run_maximal_scan` with your own bounds.

### Linear independence scans (multi-number)
- `z_p/experiments/linear_independence_scan.py`: searches for integer linear relations  
  $$c_0 + c_1 x_1 + \dots + c_n x_n = 0$$  
  Demos include:
  - Odd zetas: $$\{1, \zeta(3), \zeta(5), \zeta(7), \zeta(9)\}$$
  - Schanuel-ish trio: $$\{\pi, e, \ln 2\}$$
  - Sanity check: $$\sin^2 \theta + \cos^2 \theta - 1 = 0$$

---

## Reading the output
- **Algebraic scans:** a coefficient vector from PSLQ is a candidate polynomial; inspect the residual and re-run at higher precision to confirm stability. `None` means no relation within the chosen degree/height.
- **Linear-independence scans:** a printed linear combination signals dependence; otherwise the set appears independent up to the searched coefficient bound.

---

## Math snapshot
For odd primes $$p$$,
<p align="center">
  $$Z(p)=e^{\pi\,\zeta(p-1)/p}+1 = e^{c_p\pi^p}+1$$
</p>
with
<p align="center">
  $$c_p = (-1)^{\frac{p+1}{2}}\,\frac{2^{\,p-2} B_{p-1}}{p\,(p-1)!}\in\mathbb{Q}\setminus\{0\}$$
</p>
Even zetas (periods) give a sanity check; odd zetas and related periods remain open, making PSLQ evidence valuable.

---

## Repository map
```
z_p/
  zeta_even_reduction.md        # Derivation of c_p
  proof_sketch.md               # Conditional routes and barriers
  experiments/
    pslq_scan.py                # Z(p) algebraic scans across primes
    maximal_pslq_scan.py        # Single-constant algebraic scan
    linear_independence_scan.py # PSLQ search for linear relations
  utils/
    pslq_helpers.py             # Shared PSLQ helpers
tests/
  test_cp.py                    # Rational values of c_p for p=3,5,7
  test_linear_independence.py   # Integration tests for linear relations
.github/workflows/
  ci.yml                        # Python 3.11 CI: lint + tests
notebooks/
  odd_zeta_scan.ipynb           # Example PSLQ run on ζ(3)
requirements.txt
CONTRIBUTING.md
LICENSE
```

---

## Roadmap
- Broaden numeric coverage: raise precision/degree/height and log stability of hits.
- Extend independence experiments: add polylogarithms and other period candidates.
- Tighten docs: relate independence scans to Schanuel prerequisites; capture parameter choices in notebooks.

---

## Citation
If you use this work:
```
@software{Z(p)IrrationalityTranscendenceExplorer2025,
  title   = {Z(p) Irrationality & Transcendence Explorer},
  author  = {kugguk2022},
  year    = {2025},
  url     = {https://github.com/EncapsulatorP/zp-program}
}
```

---

## License
MIT — see `LICENSE`.
