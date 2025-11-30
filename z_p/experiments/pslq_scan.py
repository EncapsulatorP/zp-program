"""PSLQ scans for Z(p) = exp(c_p*pi**p) + 1.

Example:
  python z_p/experiments/pslq_scan.py --pmin 3 --pmax 31 --prec 300 --deg 6 --height 2000
"""
import argparse
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, TimeoutError

import mpmath as mp
import sympy as sp

from z_p.utils.pslq_helpers import algebraic_relation

def c_p_rational(p: int) -> sp.Rational:
    assert p % 2 == 1 and p >= 3
    B = sp.bernoulli(p-1)  # Rational for p-1 even > 0
    Bn, Bd = B.as_numer_denom()
    sign = -1 if (((p + 1) // 2) % 2) == 1 else 1  # (-1)^{(p+1)/2}
    num = sign * (2 ** (p - 2)) * Bn
    den = p * sp.factorial(p - 1) * Bd
    return sp.Rational(num, den)

def Z_of_p(p: int, prec: int = 300) -> mp.mpf:
    with mp.workdps(prec):
        cp = c_p_rational(p)
        exponent = mp.mpf(int(cp.p)) / mp.mpf(int(cp.q)) * (mp.pi ** p)  # cp.p, cp.q are ints
        return mp.e ** exponent + 1


def _scan_prime(p: int, prec: int, deg: int, height: int):
    """Worker to scan a single prime."""
    relation, residual, _ = algebraic_relation(
        lambda: Z_of_p(p, prec=prec),
        degree=deg,
        max_coeff=height,
        precision_dps=prec,
    )
    return {
        "p": p,
        "cp": c_p_rational(p),
        "relation": relation,
        "residual": residual,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmin", type=int, default=3)
    ap.add_argument("--pmax", type=int, default=31)
    ap.add_argument("--prec", type=int, default=300)
    ap.add_argument("--deg", type=int, default=6)
    ap.add_argument("--height", type=int, default=2000)
    ap.add_argument(
        "--processes",
        type=int,
        default=max(1, multiprocessing.cpu_count() // 2),
        help="Number of worker processes for the prime sweep.",
    )
    ap.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Optional per-prime timeout (seconds). If exceeded, the prime is reported as timed out.",
    )
    args = ap.parse_args()

    print("# Z(p) PSLQ scan\n# Columns: p, c_p (rational), PSLQ_relation (or None)\n")
    primes = list(range(args.pmin, args.pmax + 1, 2))
    with ProcessPoolExecutor(max_workers=args.processes) as executor:
        future_to_prime = {
            executor.submit(_scan_prime, p, args.prec, args.deg, args.height): p
            for p in primes
        }
        # Enforce optional per-prime timeout while still letting other primes run in parallel.
        for future, p in list(future_to_prime.items()):
            try:
                result = future.result(timeout=args.timeout)
            except TimeoutError:
                print(f"p={p:2d}  TIMEOUT (>{args.timeout}s)")
                continue
            except Exception as e:
                print(f"p={p:2d}  ERROR: {e}")
                continue

            rel = result["relation"]
            cp = result["cp"]
            residual = result["residual"]
            if rel:
                print(f"p={p:2d}  c_p={cp}  PSLQ={rel}  residual={residual}")
            else:
                print(f"p={p:2d}  c_p={cp}  PSLQ=None")

if __name__ == "__main__":
    main()
