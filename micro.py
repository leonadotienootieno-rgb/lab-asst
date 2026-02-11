"""Microbiology module: generation time and cell doubling calculations."""
import math
from utils import validate_positive_number


def generation_time_calculator(N0, N, t):
    """Calculate number of generations and doubling time."""
    N0_v = validate_positive_number(N0)
    N_v = validate_positive_number(N)
    t_v = validate_positive_number(t)

    if N_v <= N0_v:
        raise ValueError('Final count must be greater than starting count')

    generations = math.log(N_v / N0_v, 2)
    doubling_time = t_v / generations
    return generations, doubling_time


def display_generation_time():
    """Prompt user for microbiology generation time inputs and display results."""
    try:
        print("\n" + "=" * 60)
        print("MICROBIOLOGY — GENERATION TIME CALCULATOR")
        print("=" * 60)
        N0 = input("Starting number of cells (N0): ").strip()
        N = input("Final number of cells (N) [leave blank to save pending]: ").strip()
        t = input("Total time elapsed (hours): ").strip()

        if not N:
            # Save pending experiment
            return {
                'module': 'Microbiology',
                'summary': f'Pending experiment: N0={N0}, time={t}',
                'details': {
                    'N0': float(N0),
                    'time_elapsed': float(t)
                },
                'status': 'pending'
            }

        gens, dt = generation_time_calculator(N0, N, t)
        print(f"\nResults:")
        print(f"  Generations (n): {gens:.4f}")
        print(f"  Doubling time: {dt:.4f} (same time units as input)")
        print("\n")
        
        return {
            'module': 'Microbiology',
            'summary': f'N0={N0} -> N={N} in {t}',
            'details': {
                'N0': float(N0),
                'N': float(N),
                'time_elapsed': float(t),
                'generations': gens,
                'doubling_time': dt
            },
            'status': 'completed'
        }
        
    except ValueError as e:
        print(f"✗ Error: {e}\n")
        return None
