import mpmath
from mpmath import mp, pslq

def scan_linear_independence(constants_dict, max_coeff=1000, precision_dps=600):
    """
    Checks for integer linear relations among a set of constants.
    Equation: c_0*x_0 + c_1*x_1 + ... + c_n*x_n = 0
    """
    mp.dps = precision_dps
    
    # 1. Prepare the Basis
    # We convert the dictionary of {name: function} into lists of names and values
    names = list(constants_dict.keys())
    # Note: We usually include '1' in the basis to handle non-homogeneous relations
    # (e.g., x + y = 5 is x + y - 5*1 = 0)
    names.insert(0, "1")
    
    print(f"--- Scanning for Linear Relations ---")
    print(f"Basis: {names}")
    print(f"Precision: {mp.dps} digits")

    # Evaluate functions
    values = [mp.mpf(1.0)] 
    for name in names[1:]:
        val = constants_dict[name]()
        values.append(val)
    
    # 2. Run PSLQ
    try:
        relation = pslq(values, maxcoeff=max_coeff)
    except Exception as e:
        print(f"Error: {e}")
        return

    # 3. Analyze Results
    if relation:
        print("\n⚠️  RELATION FOUND!")
        print("Equation found:")
        
        terms = []
        for coeff, name in zip(relation, names):
            if coeff == 0: continue
            sign = "+" if coeff > 0 else "-"
            abs_coeff = abs(coeff)
            # Formatting to look pretty (e.g., " - 5*Zeta(3)")
            terms.append(f"{sign} {abs_coeff}*{name}")
            
        # Join and clean up leading "+"
        equation_str = " ".join(terms)
        if equation_str.startswith("+ "):
            equation_str = equation_str[2:]
            
        print(f"{equation_str} = 0")
        
        # Calculate residual
        residual = sum(c * v for c, v in zip(relation, values))
        print(f"Residual: {residual}")
    else:
        print(f"\n✅ No linear relation found among these constants.")
        print(f"They appear linearly independent (up to coeff size {max_coeff}).")

# --- Experiments ---

def run_experiments():
    
    # Experiment 1: The Odd Zeta Test (The "Holy Grail" search)
    # Conjecture: These are all linearly independent over Q.
    odd_zetas = {
        "Zeta(3)": lambda: mp.zeta(3),
        "Zeta(5)": lambda: mp.zeta(5),
        "Zeta(7)": lambda: mp.zeta(7),
        "Zeta(9)": lambda: mp.zeta(9)
    }
    scan_linear_independence(odd_zetas, max_coeff=10000)

    print("-" * 30)

    # Experiment 2: The Schanuel-ish Test
    # Checking relation between e, pi, and ln(2).
    # Expected: No relation (Independence).
    mixed_transcendentals = {
        "Pi": lambda: mp.pi,
        "e": lambda: mp.e,
        "ln(2)": lambda: mp.log(2)
    }
    scan_linear_independence(mixed_transcendentals)

    print("-" * 30)
    
    # Experiment 3: Sanity Check (We force a relation to prove it works)
    # We know that sin^2 + cos^2 = 1. Let's see if it finds 1*s + 1*c - 1*1 = 0
    theta = mp.mpf(1.2345)
    sanity_check = {
        "Sin^2": lambda: mp.sin(theta)**2,
        "Cos^2": lambda: mp.cos(theta)**2
    }
    # Note: '1' is automatically added by the function
    scan_linear_independence(sanity_check)

if __name__ == "__main__":
    run_experiments()