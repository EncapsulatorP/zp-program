# Contributing

Thanks for helping extend the Z(p) experimental toolkit. Please keep the scope tight: high-precision PSLQ probes, documentation, and tests.

## Workflow
- Create/activate a virtualenv and install deps: `pip install -r requirements.txt`.
- Run tests before submitting: `pytest -q`.
- Prefer small, focused PRs with clear descriptions of what you changed and why.

## Precision guidance
- Use `mp.workdps` to scope precision changes.
- When scanning, start with moderate bounds (e.g., degree ≤10, height ≤10k) and only increase after recording prior outcomes.
- For long runs, document chosen precision/degree/height in notebooks or README snippets.

## Code style
- Reuse shared helpers in `z_p/utils/pslq_helpers.py` for algebraic and linear PSLQ calls.
- Keep scripts and notebooks reproducible: fixed seeds/angles when applicable, explicit arguments for bounds/precision.
- Add comments only where intent is non-obvious.

## Tests
- Add or update tests alongside code changes. Favor parameterized pytest cases to cover multiple precisions/bounds.
- Keep runtime reasonable; prefer small max_coeff and precision in tests that check for “no relation found.”

## Documentation
- Update `README.md` and relevant notebooks when you add new experiment modes or parameters.
- Note any heuristics or caveats explicitly; results here are numerical hints, not proofs.
