#!/usr/bin/env python3
"""
Universal Lab Assistant
A comprehensive laboratory calculation tool for biochemistry, tissue culture,
molecular biology, and microbiology.
"""

from lib.menu import run_menu


if __name__ == "__main__":
    run_menu()


def convert_molarity(value, from_unit, to_unit):
    """
    Convert between molar units.
    
    Args:
        value: The value to convert
        from_unit: Source unit ('M' for Molar, 'mM' for millimolar)
        to_unit: Target unit ('M' for Molar, 'mM' for millimolar)
        
    Returns:
        float: The converted value
    """
    value = validate_positive_number(value)
    
    # Convert to molar first
    if from_unit == 'M':
        value_in_molar = value
    elif from_unit == 'mM':
        value_in_molar = value / 1000
    else:
        raise ValueError(f"Unknown molarity unit: {from_unit}")
    
    # Convert from molar to target unit
    if to_unit == 'M':
        return value_in_molar
    elif to_unit == 'mM':
        return value_in_molar * 1000
    else:
        raise ValueError(f"Unknown molarity unit: {to_unit}")


if __name__ == "__main__":
    run_menu()


# --- Old code below (deprecated) ---

def convert_mass(value, from_unit, to_unit):
    """
    Convert between mass units.
    
    Args:
        value: The value to convert
        from_unit: Source unit ('g' for grams, 'mg' for milligrams)
        to_unit: Target unit ('g' for grams, 'mg' for milligrams)
        
    Returns:
        float: The converted value
    """
    value = validate_positive_number(value)
    
    # Convert to grams first
    if from_unit == 'g':
        value_in_grams = value
    elif from_unit == 'mg':
        value_in_grams = value / 1000
    else:
        raise ValueError(f"Unknown mass unit: {from_unit}")
    
    # Convert from grams to target unit
    if to_unit == 'g':
        return value_in_grams
    elif to_unit == 'mg':
        return value_in_grams * 1000
    else:
        raise ValueError(f"Unknown mass unit: {to_unit}")


def convert_volume(value, from_unit, to_unit):
    """
    Convert between volume units.
    
    Args:
        value: The value to convert
        from_unit: Source unit ('L' for liters, 'µL' or 'uL' for microliters)
        to_unit: Target unit ('L' for liters, 'µL' or 'uL' for microliters)
        
    Returns:
        float: The converted value
    """
    value = validate_positive_number(value)
    
    # Normalize microliter notation
    from_unit = from_unit.replace('µ', 'u')
    to_unit = to_unit.replace('µ', 'u')
    
    # Convert to liters first
    if from_unit == 'L':
        value_in_liters = value
    elif from_unit == 'uL':
        value_in_liters = value / 1_000_000
    else:
        raise ValueError(f"Unknown volume unit: {from_unit}")
    
    # Convert from liters to target unit
    if to_unit == 'L':
        return value_in_liters
    elif to_unit == 'uL':
        return value_in_liters * 1_000_000
    else:
        raise ValueError(f"Unknown volume unit: {to_unit}")


def convert_concentration(value, from_unit, to_unit):
    """
    Convert between simple concentration units used in the lab.

    Supported units: 'ng/µL', 'ng/mL', 'pg/µL'
    """
    val = validate_positive_number(value)
    # Normalize micro symbol
    fu = from_unit.replace('µ', 'u')
    tu = to_unit.replace('µ', 'u')

    supported = {'ng/uL', 'ng/mL', 'pg/uL'}
    if fu not in supported:
        raise ValueError(f"Unsupported from-unit: {from_unit}")
    if tu not in supported:
        raise ValueError(f"Unsupported to-unit: {to_unit}")

    # Convert input to base unit ng/uL
    if fu == 'ng/uL':
        base = val
    elif fu == 'ng/mL':
        # 1 mL = 1000 µL
        base = val / 1000.0
    elif fu == 'pg/uL':
        # 1 ng = 1000 pg
        base = val / 1000.0

    # Convert base to target
    if tu == 'ng/uL':
        return base
    elif tu == 'ng/mL':
        return base * 1000.0
    elif tu == 'pg/uL':
        return base * 1000.0


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_history_entry(entry: dict):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def prompt_save(entry: dict):
    choice = input('Save this result to lab history? (y/n): ').strip().lower()
    if choice == 'y' or choice == 'yes':
        entry.setdefault('timestamp', datetime.now().isoformat())
        save_history_entry(entry)
        print('Saved to', HISTORY_FILE)
    else:
        print('Not saved.')


def display_history():
    history = load_history()
    if not history:
        print('\nNo history found.')
        return

    print('\n' + '=' * 80)
    print('LAB HISTORY')
    print('=' * 80)
    for i, e in enumerate(history, 1):
        ts = e.get('timestamp', '')
        module = e.get('module', '')
        status = e.get('status', 'completed')
        summary = e.get('summary', '')
        print(f"{i:>3}. [{status}] {ts} | {module} | {summary}")

    # Allow finalizing pending microbiology experiments
    idx = input('\nEnter history number to finalize a pending Microbiology experiment (or press Enter to return): ').strip()
    if not idx:
        return
    try:
        idxi = int(idx) - 1
        entry = history[idxi]
    except Exception:
        print('Invalid selection.')
        return

    if entry.get('module') != 'Microbiology' or entry.get('status') != 'pending':
        print('Selected entry is not a pending Microbiology experiment.')
        return

    final_N = input('Enter final bacterial count (N): ').strip()
    try:
        final_N_v = validate_positive_number(final_N)
        gens, dt = generation_time_calculator(entry['N0'], final_N_v, entry['time_elapsed'])
        entry['N'] = final_N_v
        entry['generations'] = gens
        entry['doubling_time'] = dt
        entry['status'] = 'completed'
        entry['completed_timestamp'] = datetime.now().isoformat()
        # write back
        history[idxi] = entry
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print('Pending experiment finalized and saved.')
    except ValueError as e:
        print('Error:', e)


def serial_dilution(starting_conc, dilution_factor, num_steps, final_volume, conc_unit='M', vol_unit='µL'):
    """
    Calculate serial dilution recipe.
    
    Args:
        starting_conc: Initial concentration of the sample
        dilution_factor: Dilution factor (e.g., 10 for 1:10 dilution)
        num_steps: Number of dilution steps
        final_volume: Final volume per tube
        conc_unit: Unit of concentration (default 'M')
        vol_unit: Unit of volume (default 'µL')
        
    Returns:
        list: List of tuples containing (step, concentration, sample_volume, diluent_volume)
    """
    starting_conc = validate_positive_number(starting_conc)
    dilution_factor = validate_positive_number(dilution_factor)
    num_steps = validate_positive_number(num_steps)
    final_volume = validate_positive_number(final_volume)
    
    if dilution_factor <= 1:
        raise ValueError("Dilution factor must be greater than 1")
    
    if int(num_steps) != num_steps or num_steps < 1:
        raise ValueError("Number of steps must be a positive integer")
    
    num_steps = int(num_steps)
    
    # Calculate sample volume for each dilution (1/dilution_factor of final volume)
    sample_volume = final_volume / dilution_factor
    diluent_volume = final_volume - sample_volume
    
    results = []
    for step in range(1, num_steps + 1):
        concentration = starting_conc / (dilution_factor ** step)
        results.append((step, concentration, sample_volume, diluent_volume))
    
    return results, starting_conc, sample_volume, diluent_volume, conc_unit, vol_unit


def tissue_culture_calculator(cells_counted, dilution_factor, seeding_density, total_volume_ml):
    """
    Calculate cell concentration and volume needed for tissue culture seeding.
    
    Uses hemocytometer counting method (4 squares counted).
    
    Args:
        cells_counted: Total number of cells counted in 4 squares of hemocytometer
        dilution_factor: Dilution factor used (e.g., 2 for 1:2 dilution with Trypan Blue)
        seeding_density: Desired number of cells per mL (e.g., 1e5 for 1 x 10^5 cells/mL)
        total_volume_ml: Total volume of new media in mL
        
    Returns:
        tuple: (cells_per_ml, total_cells_available, volume_to_pipet_ul)
    """
    cells_counted = validate_positive_number(cells_counted)
    dilution_factor = validate_positive_number(dilution_factor)
    seeding_density = validate_positive_number(seeding_density)
    total_volume_ml = validate_positive_number(total_volume_ml)
    
    # Hemocytometer formula: cells/mL = (cells counted / 4 squares) × dilution factor × 10,000
    # The 10,000 factor comes from the hemocytometer grid dimensions
    cells_per_ml = (cells_counted / 4) * dilution_factor * 10000
    
    # Total cells available in the original suspension
    # This would be cells_per_ml × original volume, but we calculate what's needed
    
    # Volume of cell suspension needed to achieve seeding density in total volume
    volume_needed_ml = (seeding_density * total_volume_ml) / cells_per_ml
    volume_needed_ul = volume_needed_ml * 1000  # Convert mL to µL
    
    # Total cells that will be in the flask after seeding
    total_cells_in_flask = seeding_density * total_volume_ml
    
    return cells_per_ml, total_cells_in_flask, volume_needed_ul


def display_tissue_culture():
    """Display tissue culture cell seeding calculations."""
    try:
        print("\n" + "=" * 70)
        print("TISSUE CULTURE CELL COUNTING & SEEDING CALCULATOR")
        print("=" * 70)
        print("\nHemocytometer Method (Count cells in 4 squares)")
        
        cells_counted = input("Number of cells counted (in 4 squares): ").strip()
        dilution_factor = input("Dilution factor (e.g., 2 for 1:2 with Trypan Blue) [2]: ").strip() or '2'
        seeding_density = input("Desired seeding density (e.g., 100000 for 1x10^5 cells/mL): ").strip()
        total_volume = input("Total volume of new media (mL) [10]: ").strip() or '10'
        
        cells_per_ml, total_cells, volume_pipet = tissue_culture_calculator(
            cells_counted, dilution_factor, seeding_density, total_volume
        )
        
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"\nCell Concentration (Hemocytometer):")
        print(f"  Cells counted in 4 squares: {cells_counted}")
        print(f"  Dilution factor: 1:{dilution_factor}")
        print(f"  Cell concentration: {cells_per_ml:.2e} cells/mL")
        print(f"                      {cells_per_ml:,.0f} cells/mL")
        
        print(f"\nSeeding Information:")
        print(f"  Desired seeding density: {float(seeding_density):.2e} cells/mL")
        print(f"  Total volume of new media: {total_volume} mL")
        print(f"  Total cells in flask after seeding: {total_cells:.2e} cells")
        print(f"                                      {total_cells:,.0f} cells")
        
        print(f"\nVolume to Pipet:")
        print(f"  Volume of cell suspension needed: {volume_pipet:.2f} µL")
        
        # Provide warnings if volume is too small or too large
        print(f"\n{'─' * 70}")
        if volume_pipet < 1:
            print(f"⚠ WARNING: Volume is less than 1 µL (very difficult to pipet accurately)")
            print(f"  Consider using a lower dilution factor or lower seeding density")
        elif volume_pipet > 1000:
            print(f"⚠ WARNING: Volume is greater than 1000 µL (1 mL)")
            print(f"  Consider using a smaller total volume or higher seeding density")
        else:
            print(f"✓ Volume is within reasonable pipetting range")
        
        print(f"{'─' * 70}\n")
        
    except ValueError as e:
        print(f"✗ Error: {e}\n")
    else:
        entry = {
            'timestamp': datetime.now().isoformat(),
            'module': 'Tissue Culture',
            'summary': f'{cells_per_ml:.2e} cells/mL, volume to pipet {volume_pipet:.2f} µL',
            'details': {
                'cells_counted_4_squares': float(cells_counted),
                'dilution_factor': float(dilution_factor),
                'cells_per_ml': cells_per_ml,
                'seeding_density_per_ml': float(seeding_density),
                'total_volume_ml': float(total_volume),
                'total_cells_in_flask': total_cells,
                'volume_to_pipet_ul': volume_pipet,
            },
            'status': 'completed'
        }
        prompt_save(entry)


def dna_normalization_calculator(current_conc, current_volume_ul, target_conc, conc_unit='ng/µL', fragment_bp=None):
    """
    Calculate how much TE buffer to add to a DNA extract to reach a target concentration.

    Supports concentrations in mass units (ng/µL) or molar units (nM).

    Args:
        current_conc: Current DNA concentration (numeric)
        current_volume_ul: Current volume of DNA extract (µL)
        target_conc: Desired target concentration (numeric)
        conc_unit: Unit of concentration for both current and target ('ng/µL' or 'nM')
        fragment_bp: Fragment length in base pairs (required if using molar units)

    Returns:
        tuple: (final_volume_ul, volume_te_to_add_ul)
    """
    current_conc = validate_positive_number(current_conc)
    current_vol = validate_positive_number(current_volume_ul)
    target_conc = validate_positive_number(target_conc)

    unit = conc_unit.replace('u', 'µ')

    # If concentrations are provided in molar units (nM), convert to ng/µL using fragment length
    if unit.lower() in ('nm', 'nm', 'nm', 'nm', 'nm', 'nm', 'nm'):
        unit = 'nM'

    if unit == 'nM':
        if fragment_bp is None:
            raise ValueError('Fragment length (bp) is required to convert between nM and ng/µL')
        bp = validate_positive_number(fragment_bp)
        # Molecular weight (g/mol) for double-stranded DNA ≈ 660 g/mol per bp
        mw = 660.0 * bp
        # Convert nM to ng/µL: ng/µL = nM * MW * 1e-6
        current_ng_per_ul = current_conc * mw * 1e-6
        target_ng_per_ul = target_conc * mw * 1e-6
    elif unit in ('ng/µL', 'ng/uL', 'ng/μL'):
        current_ng_per_ul = current_conc
        target_ng_per_ul = target_conc
    else:
        raise ValueError('Unsupported concentration unit. Use "ng/µL" or "nM"')

    if target_ng_per_ul <= 0:
        raise ValueError("Target concentration must be greater than 0")

    # Total mass of DNA (ng)
    total_dna_ng = current_ng_per_ul * current_vol

    # Final total volume required to reach target concentration (µL)
    final_volume_ul = total_dna_ng / target_ng_per_ul

    if final_volume_ul < current_vol - 1e-9:
        # Can't concentrate by adding buffer
        raise ValueError("Target concentration is higher than current concentration; concentration requires evaporation or concentration methods, not addition of TE.")

    volume_te_to_add_ul = final_volume_ul - current_vol
    return final_volume_ul, volume_te_to_add_ul


def display_dna_normalization():
    """Prompt user for DNA normalization inputs and display results."""
    try:
        print("\n" + "=" * 60)
        print("DNA NORMALIZATION (Molecular/Forensics)")
        print("=" * 60)
        conc_unit = input("Concentration unit for inputs (ng/µL or nM) [ng/µL]: ").strip() or 'ng/µL'
        current_conc = input(f"Current concentration ({conc_unit}): ").strip()
        current_vol = input("Current volume (µL): ").strip()
        target_conc = input(f"Target concentration ({conc_unit}): ").strip()
        fragment_bp = None
        if conc_unit.lower() == 'nM'.lower():
            fragment_bp = input("Fragment length in bp (required for molar units): ").strip()

        final_vol, vol_te = dna_normalization_calculator(current_conc, current_vol, target_conc, conc_unit, fragment_bp)

        print("\nResults:")
        print(f"  Input unit: {conc_unit}")
        print(f"  Current: {float(current_conc):.2f} {conc_unit}, {float(current_vol):.1f} µL")
        print(f"  Target: {float(target_conc):.2f} {conc_unit}")
        print(f"  Final total volume required: {final_vol:.2f} µL")
        print(f"  Volume of TE buffer to add: {vol_te:.2f} µL")
        if vol_te < 1:
            print("  ⚠ Note: Volume to add is <1 µL; this may be impractical to pipet accurately.")
        print("\n")
        entry = {
            'timestamp': datetime.now().isoformat(),
            'module': 'Molecular - DNA Normalization',
            'summary': f'Normalize to {float(target_conc):.2f} {conc_unit}',
            'details': {
                'input_unit': conc_unit,
                'current_conc': float(current_conc),
                'current_volume_ul': float(current_vol),
                'target_conc': float(target_conc),
                'final_volume_ul': final_vol,
                'volume_TE_to_add_ul': vol_te,
                'fragment_bp': fragment_bp
            },
            'status': 'completed'
        }
        prompt_save(entry)
    except ValueError as e:
        print(f"✗ Error: {e}\n")


def generation_time_calculator(N0, N, t):
    """
    Calculate number of generations and doubling time.

    Args:
        N0: Starting cell/bacteria count
        N: Final cell/bacteria count
        t: Total time elapsed (in hours, or user units)

    Returns:
        tuple: (generations, doubling_time)
    """
    N0_v = validate_positive_number(N0)
    N_v = validate_positive_number(N)
    t_v = validate_positive_number(t)

    if N_v <= N0_v:
        raise ValueError('Final count must be greater than starting count')

    import math
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
        N = input("Final number of cells (N) [leave blank to save a pending experiment]: ").strip()
        t = input("Total time elapsed (hours): ").strip()

        if not N:
            # save pending experiment
            entry = {
                'timestamp': datetime.now().isoformat(),
                'module': 'Microbiology',
                'summary': f'Pending experiment: N0={N0}, time={t}',
                'details': {
                    'N0': float(N0),
                    'time_elapsed': float(t)
                },
                'status': 'pending'
            }
            prompt_save(entry)
            return

        gens, dt = generation_time_calculator(N0, N, t)
        print(f"\nResults:")
        print(f"  Generations (n): {gens:.4f}")
        print(f"  Doubling time: {dt:.4f} (same time units as input)")
        print("\n")
        entry = {
            'timestamp': datetime.now().isoformat(),
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
        prompt_save(entry)
    except ValueError as e:
        print(f"✗ Error: {e}\n")


def display_serial_dilution():
    """Display serial dilution results in a formatted table."""
    try:
        print("\n" + "=" * 60)
        print("Serial Dilution Calculator")
        print("=" * 60)
        
        starting_conc = input("Starting concentration: ").strip()
        conc_unit = input("Concentration unit (e.g., M, mM, ng/mL) [M]: ").strip() or 'M'
        dilution_factor = input("Dilution factor (e.g., 10 for 1:10) [10]: ").strip() or '10'
        num_steps = input("Number of dilution steps [5]: ").strip() or '5'
        final_volume = input("Final volume per tube [100]: ").strip() or '100'
        vol_unit = input("Volume unit (e.g., µL, mL, L) [µL]: ").strip() or 'µL'
        
        results, start_conc, sample_vol, diluent_vol, conc_u, vol_u = serial_dilution(
            starting_conc, dilution_factor, num_steps, final_volume, conc_unit, vol_unit
        )
        
        print("\n" + "=" * 60)
        print("SERIAL DILUTION RECIPE")
        print("=" * 60)
        print(f"Starting Concentration: {start_conc} {conc_u}")
        print(f"Dilution Factor: 1:{dilution_factor}")
        print(f"Sample Volume per Tube: {sample_vol:.4g} {vol_u}")
        print(f"Diluent Volume per Tube: {diluent_vol:.4g} {vol_u}")
        print(f"Total Volume per Tube: {sample_vol + diluent_vol:.4g} {vol_u}")
        print("-" * 60)
        print(f"{'Step':<6} {'Concentration':<20} {'Sample':<15} {'Diluent':<15}")
        print(f"{'':6} {f'({conc_u})':<20} {f'({vol_u})':<15} {f'({vol_u})':<15}")
        print("-" * 60)
        
        for step, conc, sample, diluent in results:
            source = "Starting solution" if step == 1 else f"Tube {step-1}"
            print(f"{step:<6} {conc:<20.6g} {sample:<15.4g} {diluent:<15.4g}")
            if step == 1:
                print(f"       (From: {source})")
            else:
                print(f"       (From: {source})")
        
        print("-" * 60)
        print("\nInstructions:")
        print(f"1. For tube 1: Mix {sample_vol:.4g} {vol_u} of STARTING SOLUTION")
        print(f"               with {diluent_vol:.4g} {vol_u} of DILUENT")
        for step in range(2, int(num_steps) + 1):
            print(f"{step}. For tube {step}: Mix {sample_vol:.4g} {vol_u} of TUBE {step-1}")
            print(f"               with {diluent_vol:.4g} {vol_u} of DILUENT")
        
        # Offer to save recipe to lab history
        entry = {
            'timestamp': datetime.now().isoformat(),
            'module': 'Biochemistry - Serial Dilution',
            'summary': f'1:{dilution_factor} serial dilution, {num_steps} steps, {final_volume}{vol_u} per tube',
            'details': {
                'starting_concentration': start_conc,
                'concentration_unit': conc_u,
                'dilution_factor': dilution_factor,
                'num_steps': int(num_steps),
                'final_volume_per_tube': float(final_volume),
                'sample_volume': sample_vol,
                'diluent_volume': diluent_vol,
            },
            'status': 'completed'
        }
        prompt_save(entry)

        print("\n")
        
    except ValueError as e:
        print(f"✗ Error: {e}\n")


def interactive_converter():
    """Main menu for the Universal Lab Assistant."""
    def display_biochemistry():
        while True:
            print("\nBiochemistry — choose an option:")
            print("  1. Concentration conversion (ng/µL ↔ ng/mL ↔ pg/µL)")
            print("  2. Molarity conversion (M ↔ mM)")
            print("  3. Serial dilution calculator")
            print("  4. Back to main menu")
            choice = input("Select 1-3: ").strip()
            if choice == '1':
                try:
                    value = input("Enter value: ").strip()
                    from_u = input("From unit (ng/µL, ng/mL, pg/µL): ").strip()
                    to_u = input("To unit (ng/µL, ng/mL, pg/µL): ").strip()
                    res = convert_concentration(value, from_u, to_u)
                    print(f"\n✓ Result: {value} {from_u} = {res:.6g} {to_u}\n")
                except ValueError as e:
                    print(f"✗ Error: {e}\n")
            elif choice == '2':
                try:
                    value = input("Enter value: ").strip()
                    from_u = input("From unit (M/mM): ").strip()
                    to_u = input("To unit (M/mM): ").strip()
                    res = convert_molarity(value, from_u, to_u)
                    print(f"\n✓ Result: {value} {from_u} = {res:.6g} {to_u}\n")
                except ValueError as e:
                    print(f"✗ Error: {e}\n")
            elif choice == '3':
                display_serial_dilution()
            elif choice == '4':
                break
            else:
                print("Invalid choice — please select 1-4.")

    while True:
        print("\n" + "=" * 60)
        print("Universal Lab Assistant — Main Menu")
        print("=" * 60)
        print("  1. Biochemistry (Molarity & Dilutions)")
        print("  2. Tissue Culture (Cell Counting & Seeding)")
        print("  3. Molecular/Forensics (DNA Normalization)")
        print("  4. Microbiology (Generation Time)")
        print("  5. View Lab History")
        print("  6. Exit")
        choice = input("Select 1-6: ").strip()

        if choice == '1':
            display_biochemistry()
            continue
        elif choice == '2':
            display_tissue_culture()
            continue
        elif choice == '3':
            display_dna_normalization()
            continue
        elif choice == '4':
            display_generation_time()
            continue
        elif choice == '5':
            display_history()
            continue
        elif choice == '6' or choice.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            print("Invalid choice — please select 1-6.")


if __name__ == "__main__":
    interactive_converter()
