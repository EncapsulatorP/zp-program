import mpmath as mp
import pytest

from z_p.utils.pslq_helpers import linear_relation


@pytest.mark.parametrize(
    ("precision_dps", "max_coeff"),
    [
        (60, 200),
        (90, 500),
    ],
)
def test_conjectured_independence_odd_zetas(precision_dps, max_coeff):
    """{1, zeta(3), zeta(5)} should not return a small linear relation."""
    values = [mp.mpf(1), mp.zeta(3), mp.zeta(5)]
    relation, residual, _ = linear_relation(values, max_coeff=max_coeff, precision_dps=precision_dps)
    assert relation is None
    assert residual is None


@pytest.mark.parametrize("precision_dps", [50, 80])
def test_known_relation_sqrt_scaling(precision_dps):
    """sqrt(8) - 2*sqrt(2) = 0 should be detected (constant term unused)."""
    root2 = mp.sqrt(2)
    values = [mp.mpf(1), root2, mp.sqrt(8)]
    relation, residual, _ = linear_relation(values, max_coeff=10, precision_dps=precision_dps)
    assert relation is not None
    # relation should involve the last two entries with ratio 2:1 (up to sign)
    assert {abs(int(c)) for c in relation if c != 0} <= {1, 2}
    assert mp.fabs(residual) < mp.mpf("1e-20")
