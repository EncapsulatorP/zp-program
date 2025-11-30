import mpmath
from mpmath import mp

from z_p.utils.pslq_helpers import algebraic_relation


def run_maximal_scan(
    target_name,
    target_value_func,
    max_degree=6,
    max_coeff=1000,
    precision_dps=200,
):
    """
    Scan for an algebraic relation for a single target constant.
    Checks if a_0 + a_1*x + ... + a_n*x^n = 0.
    """
    print(f"--- Scanning {target_name} ---")
    print(f"Precision: {precision_dps} digits")

    relation, residual, target = algebraic_relation(
        target_value_func,
        degree=max_degree,
        max_coeff=max_coeff,
        precision_dps=precision_dps,
    )

    if relation:
        print("POSSIBLE RELATION FOUND!")
        print(f"Coefficients: {relation}")
        terms = []
        for i, coeff in enumerate(relation):
            if coeff == 0:
                continue
            term = f"{coeff}" if i == 0 else f"{coeff}*{target_name}^{i}"
            terms.append(term)
        print("Polynomial: " + " + ".join(terms) + " = 0")
        print(f"Residual (error): {residual}")
        print("Re-run at higher precision to check if this stabilizes.")
    else:
        print(f"No relation found for {target_name} up to degree {max_degree}.")
        print("Evidence suggests transcendence or very large coefficients.\n")


# --- Configuration for the "Maximal" Search ---

def scan_all():
    # "Hard" constants where status is open or only partially known.
    targets = [
        ("Zeta(3)", lambda: mp.zeta(3)),
        ("Zeta(5)", lambda: mp.zeta(5)),
        ("Zeta(7)", lambda: mp.zeta(7)),
        ("Zeta(9)", lambda: mp.zeta(9)),
        ("Catalan", lambda: mp.catalan),
        ("Euler-Gamma", lambda: mp.euler),
    ]

    for name, func in targets:
        run_maximal_scan(name, func, max_degree=10, max_coeff=10000, precision_dps=500)


if __name__ == "__main__":
    scan_all()
