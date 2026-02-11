#!/usr/bin/env python3
"""
Universal Lab Assistant - Main Entry Point
Professional modular laboratory calculation tool.
"""

from biochem import convert_molarity, convert_concentration, convert_mass, convert_volume, serial_dilution
from culture import display_tissue_culture
from micro import display_generation_time
from forensics import display_dna_normalization, display_normalize_dna_forensics
from storage import display_history, prompt_save, compute_cost_for_volume, load_reagents, update_reagent_price
from datetime import datetime


def display_biochemistry():
    """Biochemistry submenu."""
    while True:
        print("\nBiochemistry — choose an option:")
        print("  1. Concentration conversion (ng/µL ↔ ng/mL ↔ pg/µL)")
        print("  2. Molarity conversion (M ↔ mM)")
        print("  3. Serial dilution calculator")
        print("  4. Back to main menu")
        choice = input("Select 1-4: ").strip()
        
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
            print("Invalid choice — select 1-4.")


def display_forensics():
    """Molecular/Forensics submenu."""
    while True:
        print("\nMolecular/Forensics — choose an option:")
        print("  1. DNA Normalization (complex calculator)")
        print("  2. Quick Forensic DNA Normalization (with pre-dilution check)")
        print("  3. Back to main menu")
        choice = input("Select 1-3: ").strip()
        
        if choice == '1':
            entry = display_dna_normalization()
            if entry:
                prompt_save(entry)
        
        elif choice == '2':
            entry = display_normalize_dna_forensics()
            if entry:
                prompt_save(entry)
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice — select 1-3.")



def display_serial_dilution():
    """Serial dilution recipe display with history save."""
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
        
        results, start_conc, sample_vol, diluent_vol, _, _ = serial_dilution(
            starting_conc, dilution_factor, num_steps, final_volume, conc_unit, vol_unit
        )
        
        print("\n" + "=" * 60)
        print("SERIAL DILUTION RECIPE")
        print("=" * 60)
        print(f"Starting Concentration: {start_conc} {conc_unit}")
        print(f"Dilution Factor: 1:{dilution_factor}")
        print(f"Sample Volume per Tube: {sample_vol:.4g} {vol_unit}")
        print(f"Diluent Volume per Tube: {diluent_vol:.4g} {vol_unit}")
        print(f"Total Volume per Tube: {sample_vol + diluent_vol:.4g} {vol_unit}")
        print("-" * 60)
        print(f"{'Step':<6} {'Concentration':<20} {'Sample':<15} {'Diluent':<15}")
        print(f"{'':6} {f'({conc_unit})':<20} {f'({vol_unit})':<15} {f'({vol_unit})':<15}")
        print("-" * 60)
        
        for step, conc, sample, diluent in results:
            source = "Starting solution" if step == 1 else f"Tube {step-1}"
            print(f"{step:<6} {conc:<20.6g} {sample:<15.4g} {diluent:<15.4g}")
            print(f"       (From: {source})")
        
        print("-" * 60)
        print("\nInstructions:")
        print(f"1. For tube 1: Mix {sample_vol:.4g} {vol_unit} of STARTING SOLUTION")
        print(f"               with {diluent_vol:.4g} {vol_unit} of DILUENT")
        for step in range(2, int(num_steps) + 1):
            print(f"{step}. For tube {step}: Mix {sample_vol:.4g} {vol_unit} of TUBE {step-1}")
            print(f"               with {diluent_vol:.4g} {vol_unit} of DILUENT")
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'module': 'Biochemistry - Serial Dilution',
            'summary': f'1:{dilution_factor} dilution, {num_steps} steps, {final_volume}{vol_unit}/tube',
            'details': {
                'starting_concentration': start_conc,
                'concentration_unit': conc_unit,
                'dilution_factor': dilution_factor,
                'num_steps': int(num_steps),
                'final_volume_per_tube': float(final_volume),
                'sample_volume': sample_vol,
                'diluent_volume': diluent_vol,
            },
            'status': 'completed'
        }
        # Ask user which diluent reagent to cost (optional)
        diluent_name = input('Diluent reagent name for cost estimate [TE Buffer]: ').strip() or 'TE Buffer'
        try:
            total_diluent_ul = float(diluent_vol) * int(num_steps)
            cost = compute_cost_for_volume(diluent_name, total_diluent_ul)
        except Exception:
            cost = None
        if cost is not None:
            print(f"Estimated diluent cost ({diluent_name}): ${cost:.2f}")
            entry['details']['estimated_cost'] = cost
            entry['details']['diluent_reagent'] = diluent_name

        prompt_save(entry)
        print()
        
    except ValueError as e:
        print(f"✗ Error: {e}\n")


def display_settings():
    """Settings submenu: manage reagent prices."""
    while True:
        print("\nSettings — Reagent Pricing")
        reagents = load_reagents()
        if reagents:
            print("Current reagents and prices:")
            for name, info in reagents.items():
                unit = info.get('unit', 'uL')
                price = info.get('price_per_unit', 0.0)
                print(f"  - {name}: ${price:.4g} per {unit}")
        else:
            print("No reagents configured yet.")
        print("\n  1. Add / Update reagent price")
        print("  2. Back to main menu")
        choice = input("Select 1-2: ").strip()
        if choice == '1':
            name = input('Reagent name: ').strip()
            if not name:
                print('Name required.')
                continue
            price = input('Price per unit (numeric): ').strip()
            unit = input("Unit ('uL' or 'mL') [uL]: ").strip() or 'uL'
            try:
                update_reagent_price(name, float(price), unit)
                print(f"✓ Saved price for {name}.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            break
        else:
            print('Invalid choice.')


def run_main_menu():
    """Main interactive menu."""
    while True:
        print("\n" + "=" * 60)
        print("Universal Lab Assistant — Main Menu")
        print("=" * 60)
        print("  1. Biochemistry (Molarity & Dilutions)")
        print("  2. Tissue Culture (Cell Counting & Seeding)")
        print("  3. Molecular/Forensics (DNA Normalization)")
        print("  4. Microbiology (Generation Time)")
        print("  5. View Lab History")
        print("  6. Settings")
        print("  7. Exit")
        choice = input("Select 1-7: ").strip()

        if choice == '1':
            display_biochemistry()
        
        elif choice == '2':
            entry = display_tissue_culture()
            if entry:
                prompt_save(entry)
        
        elif choice == '3':
            display_forensics()
        
        elif choice == '4':
            entry = display_generation_time()
            if entry:
                prompt_save(entry)
        
        elif choice == '5':
            display_history()
        
        elif choice == '6':
            display_settings()

        elif choice == '7' or choice.lower() == 'exit':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice — select 1-6.")


if __name__ == "__main__":
    run_main_menu()
