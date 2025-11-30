import mpmath
from mpmath import mp

from z_p.utils.pslq_helpers import linear_relation


def scan_linear_independence(constants_dict, max_coeff=1000, precision_dps=600):
    """
    Checks for integer linear relations among a set of constants.
    Equation: c_0*x_0 + c_1*x_1 + ... + c_n*x_n = 0
    """
    names = list(constants_dict.keys())
    names.insert(0, "1")  # include constant term

    print(f"--- Scanning for Linear Relations ---")
    print(f"Basis: {names}")
    print(f"Precision: {precision_dps} digits")

    with mp.workdps(precision_dps):
        values = [mp.mpf(1.0)] + [constants_dict[name]() for name in names[1:]]

    relation, residual, mp_values = linear_relation(
        values, max_coeff=max_coeff, precision_dps=precision_dps
    )

    if relation:
        print("\nRELATION FOUND!")
        terms = []
        for coeff, name in zip(relation, names):
            if coeff == 0:
                continue
            sign = "+" if coeff > 0 else "-"
            abs_coeff = abs(coeff)
            terms.append(f"{sign} {abs_coeff}*{name}")

        equation_str = " ".join(terms)
        if equation_str.startswith("+ "):
            equation_str = equation_str[2:]

        print(f"{equation_str} = 0")
        print(f"Residual: {residual}")
    else:
        print(f"\nNo linear relation found among these constants.")
        print(f"They appear linearly independent (up to coeff size {max_coeff}).")


def run_experiments():
    # Experiment 1: The Odd Zeta Test
    odd_zetas = {
        "Zeta(3)": lambda: mp.zeta(3),
        "Zeta(5)": lambda: mp.zeta(5),
        "Zeta(7)": lambda: mp.zeta(7),
        "Zeta(9)": lambda: mp.zeta(9),
    }
    scan_linear_independence(odd_zetas, max_coeff=10000)

    print("-" * 30)

    # Experiment 2: Schanuel-ish trio
    mixed_transcendentals = {
        "Pi": lambda: mp.pi,
        "e": lambda: mp.e,
        "ln(2)": lambda: mp.log(2),
    }
    scan_linear_independence(mixed_transcendentals)

    print("-" * 30)

    # Experiment 3: Sanity check (sin^2 + cos^2 = 1)
    theta = mp.mpf(1.2345)
    sanity_check = {
        "Sin^2": lambda: mp.sin(theta) ** 2,
        "Cos^2": lambda: mp.cos(theta) ** 2,
    }
    scan_linear_independence(sanity_check)


if __name__ == "__main__":
    run_experiments()
