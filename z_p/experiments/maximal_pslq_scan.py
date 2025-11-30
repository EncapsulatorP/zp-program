import mpmath
from mpmath import mp, pslq
import sys

def run_maximal_scan(target_name, target_value_func, max_degree=6, max_coeff=1000, precision_dps=200):
    """
    Scans for algebraic relations for a specific target constant.
    This checks if P(x) = 0 for a polynomial P with integer coefficients.
    """
    
    # 1. Set Precision (Vital for PSLQ to distinguish true zero from noise)
    mp.dps = precision_dps
    
    print(f"--- Scanning {target_name} ---")
    print(f"Precision: {mp.dps} digits")
    
    # 2. Generate the Target Value
    # We evaluate the function inside the high-precision context
    target = target_value_func()
    
    # 3. Construct the Basis Vector
    # To check if 'x' is algebraic of degree 'n', we feed PSLQ: [1, x, x^2, ... x^n]
    # If PSLQ finds a relation, it means a_0 + a_1*x + ... + a_n*x^n = 0
    basis = [target**k for k in range(max_degree + 1)]
    
    print(f"Basis constructed (Degree {max_degree}). Running PSLQ...")
    
    # 4. Run PSLQ Algorithm
    # maxcoeff limits the size of the integers allowed in the relation
    try:
        relation = pslq(basis, maxcoeff=max_coeff)
    except Exception as e:
        print(f"Error during PSLQ: {e}")
        return

    # 5. Interpret Results
    if relation:
        print(f"⚠️  POSSIBLE RELATION FOUND for {target_name}!")
        print(f"Coefficients: {relation}")
        print(f"Polynomial: ", end="")
        terms = []
        for i, coeff in enumerate(relation):
            if coeff == 0: continue
            term = f"{coeff}" if i == 0 else f"{coeff}*{target_name}^{i}"
            terms.append(term)
        print(" + ".join(terms) + " = 0\n")
        
        # Validation step: Compute the residual to see how close to zero it actually is
        residual = sum(c * (target**i) for i, c in enumerate(relation))
        print(f"Residual (error): {residual}")
        print("Note: If residual is very small (e.g. 1e-200), this might be real.")
        print("If this is Zeta(3), you likely just won a Fields Medal (or precision was too low).")
    else:
        print(f"✅ No relation found for {target_name} up to degree {max_degree}.")
        print("Evidence suggests this number is likely transcendental (or has very large coefficients).\n")

# --- Configuration for the "Maximal" Search ---

def scan_all():
    # We define a list of "hard" irrationals/transcendentals 
    # that standard generators fail to classify.
    
    targets = [
        # The famous Apery's Constant. Irrationality known, Transcendence unknown.
        ("Zeta(3)", lambda: mp.zeta(3)),
        
        # Zeta(5): Completely open problem.
        ("Zeta(5)", lambda: mp.zeta(5)),
        
        # Catalan's Constant: Open problem.
        ("Catalan", lambda: mp.catalan),
        
        # Euler-Mascheroni Constant: We don't even know if this is irrational!
        ("Euler-Gamma", lambda: mp.euler),
    ]

    for name, func in targets:
        run_maximal_scan(name, func, max_degree=10, max_coeff=10000, precision_dps=500)

if __name__ == "__main__":
    scan_all()