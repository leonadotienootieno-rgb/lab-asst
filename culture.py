"""Tissue Culture module: cell counting and seeding calculations."""
from utils import validate_positive_number


def tissue_culture_calculator(cells_counted, dilution_factor, seeding_density, total_volume_ml):
    """Calculate cell concentration and volume needed for tissue culture seeding."""
    cells_counted = validate_positive_number(cells_counted)
    dilution_factor = validate_positive_number(dilution_factor)
    seeding_density = validate_positive_number(seeding_density)
    total_volume_ml = validate_positive_number(total_volume_ml)
    
    cells_per_ml = (cells_counted / 4) * dilution_factor * 10000
    volume_needed_ml = (seeding_density * total_volume_ml) / cells_per_ml
    volume_needed_ul = volume_needed_ml * 1000
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
        
        # Return results for saving to history
        return {
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
        
    except ValueError as e:
        print(f"✗ Error: {e}\n")
        return None
