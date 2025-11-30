from typing import Callable, Iterable, List, Optional, Sequence, Tuple

import mpmath
from mpmath import mp, pslq


def _mp_values(seq: Iterable[float]) -> List[mpmath.mpf]:
    """Convert an iterable to high-precision mpmath mpf values."""
    return [mp.mpf(val) for val in seq]


def algebraic_relation(
    target_fn: Callable[[], mpmath.mpf],
    degree: int,
    max_coeff: int,
    precision_dps: int,
) -> Tuple[Optional[Sequence[int]], Optional[mpmath.mpf], mpmath.mpf]:
    """
    Search for an integer relation a_0 + a_1*x + ... + a_deg*x^deg = 0.
    Returns (relation_coeffs or None, residual or None, target_value).
    """
    with mp.workdps(precision_dps):
        target = mp.mpf(target_fn())
        basis = [target**k for k in range(degree + 1)]
        relation = pslq(basis, maxcoeff=max_coeff)
        residual = sum(c * b for c, b in zip(relation, basis)) if relation else None
        return relation, residual, target


def linear_relation(
    values: Sequence[float],
    max_coeff: int,
    precision_dps: int,
) -> Tuple[Optional[Sequence[int]], Optional[mpmath.mpf], List[mpmath.mpf]]:
    """
    Search for c_0*v_0 + ... + c_n*v_n = 0 among the given values.
    Returns (relation_coeffs or None, residual or None, mp_values).
    """
    with mp.workdps(precision_dps):
        mp_values = _mp_values(values)
        relation = pslq(mp_values, maxcoeff=max_coeff)
        residual = sum(c * v for c, v in zip(relation, mp_values)) if relation else None
        return relation, residual, mp_values
