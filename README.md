# Z(p) Irrationality & Transcendence Program

[![CI](https://github.com/kugguk2022/zp-program/actions/workflows/ci.yml/badge.svg)](https://github.com/kugguk2022/zp-program/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Focused, reproducible experiments around
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\displaystyle Z(p)=e^{\pi\,\zeta(p-1)/p}+1 \qquad (p\ \text{odd prime})" alt="Z(p) definition" />
</p>
We keep the scope narrow, document the exact rational coefficient <img src="https://latex.codecogs.com/svg.latex?c_p" alt="c_p" />, explain why transcendence here is difficult, and ship executable PSLQ probes for both single-number algebraicity and multi-number linear independence. Everything here is heuristic evidence, not proof.

---

## What this repo is
- Expresses <img src="https://latex.codecogs.com/svg.latex?Z(p)=e^{c_p\pi^p}+1" alt="Z(p)" /> with a closed form for the rational <img src="https://latex.codecogs.com/svg.latex?c_p" alt="c_p" />.
- Provides two complementary probes:
  - **Algebraic relation scans**: does one constant satisfy a low-degree polynomial with small integer coefficients?
  - **Linear independence scans**: are several constants tied by a rational linear relation?
- Targets open cases such as odd zeta values, Catalan, Euler–Mascheroni, and Schanuel-style tuples.
- Outputs are reproducible scripts; results are numerical hints only.

---

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

---

## Experiments and scripts

### Algebraic relation scans (single number)
- `z_p/experiments/pslq_scan.py`: sweep odd primes and search for algebraic relations of `Z(p)` itself.  
  Example: `python z_p/experiments/pslq_scan.py --pmin 3 --pmax 31 --prec 300 --deg 6 --height 2000 --processes 4 --timeout 30`  
  Prime sweeps use multiprocessing; set `--timeout` (seconds) to skip outliers.
- `z_p/experiments/maximal_pslq_scan.py`: “maximal” probe for one constant at a time (e.g., `zeta(3)`, `zeta(5)`, `zeta(7)`, `zeta(9)`, Catalan, Euler–Mascheroni). Run it as a script to scan the built-in targets, or adapt `run_maximal_scan` for your own constant and bounds.

### Linear independence scans (many numbers)
- `z_p/experiments/linear_independence_scan.py`: searches for integer linear relations  
  <p align="center"><img src="https://latex.codecogs.com/svg.latex?c_0+c_1x_1+\dots+c_nx_n=0" alt="linear relation" /></p>
  across a user-provided dictionary of constants. The script ships three demonstrations:
  1. **Odd zetas**: checks `{1, ζ(3), ζ(5), ζ(7), ζ(9)}` for a relation (conjectured independent).
  2. **Schanuel-ish trio**: checks `{π, e, ln 2}` (expected independent).
  3. **Sanity check**: finds the known relation `sin^2 θ + cos^2 θ - 1 = 0`.
  Run: `python z_p/experiments/linear_independence_scan.py`. Tune `max_coeff` and `precision_dps` to widen the search.

---

## Reading the output
- **Algebraic scans**: a non-empty coefficient vector from PSLQ is a candidate polynomial; check the printed residual at higher precision before taking it seriously. `None` means no relation up to the requested degree and coefficient bound.
- **Linear independence scans**: a relation prints as a signed combination of your basis (including the implicit `1`). If none is found, the set looks linearly independent over `Q` within the searched coefficient size.

---

## Math snapshot
Using the classical even-zeta formula
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\displaystyle \zeta(2k)=\frac{(-1)^{k+1} B_{2k}(2\pi)^{2k}}{2(2k)!}" alt="Even zeta formula" />
</p>
and <img src="https://latex.codecogs.com/svg.latex?k=(p-1)/2" alt="k=(p-1)/2" />, we obtain
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\displaystyle \frac{\pi\,\zeta(2k)}{p}=(-1)^{k+1}\frac{2^{\,2k-1}B_{2k}}{(2k)!\,(2k+1)}\,\pi^{2k+1}=c_p\pi^{p}" alt="Derivation of c_p" />
</p>
so <img src="https://latex.codecogs.com/svg.latex?Z(p)=e^{c_p\pi^{p}}+1" alt="Z(p) formula" /> with
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\displaystyle c_p = (-1)^{\frac{p+1}{2}}\,\frac{2^{\,p-2} B_{p-1}}{p\,(p-1)!}\in\mathbb{Q}\setminus\{0\}" alt="c_p boxed formula" />
</p>

**Sanity checks**
| p | <img src="https://latex.codecogs.com/svg.latex?c_p" alt="c_p" /> | Reason |
|---|---|---|
| 3 | <img src="https://latex.codecogs.com/svg.latex?1/18" alt="1/18" /> | <img src="https://latex.codecogs.com/svg.latex?\pi\zeta(2)/3=\pi^3/18" alt="c_3 reason" /> |
| 5 | <img src="https://latex.codecogs.com/svg.latex?1/450" alt="1/450" /> | <img src="https://latex.codecogs.com/svg.latex?\pi\zeta(4)/5=\pi^5/450" alt="c_5 reason" /> |
| 7 | <img src="https://latex.codecogs.com/svg.latex?1/6615" alt="1/6615" /> | <img src="https://latex.codecogs.com/svg.latex?\pi\zeta(6)/7=\pi^7/6615" alt="c_7 reason" /> because <img src="https://latex.codecogs.com/svg.latex?\zeta(6)=\pi^6/945" alt="zeta(6)" /> |

---

## Why this is hard
- **Lindemann–Weierstrass**: guarantees transcendence of <img src="https://latex.codecogs.com/svg.latex?e^{\alpha}" alt="e^alpha" /> for algebraic nonzero <img src="https://latex.codecogs.com/svg.latex?\alpha" alt="alpha" />, but <img src="https://latex.codecogs.com/svg.latex?c_p\pi^p" alt="c_p pi^p" /> is not known to be algebraic.
- **Gelfond–Schneider**: handles algebraic bases/exponents; <img src="https://latex.codecogs.com/svg.latex?\pi^p" alt="pi^p" /> sits outside its scope.
- **Linear forms in logarithms**: about logarithms of algebraic numbers, again missing <img src="https://latex.codecogs.com/svg.latex?\pi" alt="pi" />.

Bottom line: unconditional transcendence of <img src="https://latex.codecogs.com/svg.latex?e^{c_p\pi^p}" alt="e^(c_p pi^p)" /> needs tools we do not yet have.

---

## Coverage ladder (toward a “maximal” generator)
1. Rational numbers (easy).
2. Algebraic numbers (roots of polynomials): probed via the PSLQ algebraic scans.
3. Periods (e.g., <img src="https://latex.codecogs.com/svg.latex?\pi" alt="pi" />, <img src="https://latex.codecogs.com/svg.latex?\log 2" alt="log 2" />, odd zetas?): probed via linear-independence scans for relations among periods.
4. Computable but unknown status numbers (e.g., Euler–Mascheroni): generate and test heuristically.
5. Uncomputable constants (e.g., Chaitin’s <img src="https://latex.codecogs.com/svg.latex?\Omega" alt="Omega" />): out of scope.

---

## Schanuel perspective
Schanuel’s conjecture requires that the chosen numbers are linearly independent over <img src="https://latex.codecogs.com/svg.latex?\mathbb{Q}" alt="Q" />. The linear-independence scanner supplies heuristic checks of that prerequisite: if `{1, x_1, …, x_n}` has no relation up to your coefficient bound, you have numerical support for applying Schanuel-style implications to that tuple.

---

## Repository map
```
z_p/
  zeta_even_reduction.md   # Derivation of c_p
  proof_sketch.md          # Conditional routes, barriers, plan
  experiments/
    pslq_scan.py           # Z(p) algebraic scans across primes
    maximal_pslq_scan.py   # Algebraic scan for a single hard constant
    linear_independence_scan.py  # PSLQ search for integer linear relations
  utils/
    pslq_helpers.py        # Shared PSLQ helpers (algebraic + linear)
tests/
  test_cp.py               # Rational values of c_p for p=3,5,7
  test_linear_independence.py  # Integration tests for linear relations
.github/workflows/
  ci.yml                   # Python 3.11 CI: lint + tests
notebooks/
  odd_zeta_scan.ipynb      # Example PSLQ run on ζ(3)
requirements.txt
CONTRIBUTING.md
LICENSE
```

---

## Roadmap
- Broaden numeric coverage: raise precision, degree, and coefficient bounds for both scans; log stability of hits.
- Extend independence experiments: add polylogarithms and other period candidates.
- Document conditional routes crisply in `proof_sketch.md`, including Schanuel/Four-Exponentials setups.
- Add more unit checks (e.g., additional primes, symmetry tests) as the scripts grow.

---

## Testing
```bash
pytest -q
```
The suite currently verifies <img src="https://latex.codecogs.com/svg.latex?c_3=1/18" alt="c3" />, <img src="https://latex.codecogs.com/svg.latex?c_5=1/450" alt="c5" />, and <img src="https://latex.codecogs.com/svg.latex?c_7=1/6615" alt="c7" />.

---

## License
MIT — see `LICENSE`.
