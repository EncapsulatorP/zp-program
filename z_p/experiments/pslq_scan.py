"""PSLQ scans for Z(p) = exp(c_p*pi**p) + 1.

Example:
  python z_p/experiments/pslq_scan.py --pmin 3 --pmax 31 --prec 300 --deg 6 --height 2000
"""
import argparse
import mpmath as mp
from mpmath import pslq
import sympy as sp

def c_p_rational(p: int) -> sp.Rational:
    assert p % 2 == 1 and p >= 3
    B = sp.bernoulli(p-1)  # Rational for p-1 even > 0
    Bn, Bd = B.as_numer_denom()
    sign = -1 if (((p + 1) // 2) % 2) == 1 else 1  # (-1)^{(p+1)/2}
    num = sign * (2 ** (p - 2)) * Bn
    den = p * sp.factorial(p - 1) * Bd
    return sp.Rational(num, den)

def Z_of_p(p: int, prec: int = 300) -> mp.mpf:
    mp.mp.dps = prec
    cp = c_p_rational(p)
    exponent = mp.mpf(int(cp.p)) / mp.mpf(int(cp.q)) * (mp.pi ** p)  # cp.p, cp.q are ints
    return mp.e ** exponent + 1

def try_pslq(x: mp.mpf, deg: int, height: int):
    # Integer relation among [1, x, x^2, ..., x^deg] using mpmath.pslq
    vec = [mp.mpf(x) ** i for i in range(deg + 1)]
    return pslq(vec, maxcoeff=height)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmin", type=int, default=3)
    ap.add_argument("--pmax", type=int, default=31)
    ap.add_argument("--prec", type=int, default=300)
    ap.add_argument("--deg", type=int, default=6)
    ap.add_argument("--height", type=int, default=2000)
    args = ap.parse_args()

    print("# Z(p) PSLQ scan\n# Columns: p, c_p (rational), PSLQ_relation (or None)\n")
    for p in range(args.pmin, args.pmax + 1, 2):
        try:
            cp = c_p_rational(p)
            z = Z_of_p(p, prec=args.prec)
            rel = try_pslq(z, args.deg, args.height)
            print(f"p={p:2d}  c_p={cp}  PSLQ={rel}")
        except Exception as e:
            print(f"p={p:2d}  ERROR: {e}")

if __name__ == "__main__":
    main()
