"""Forensics/Molecular module: DNA normalization."""
from utils import validate_positive_number
from storage import compute_cost_for_volume


def normalize_dna(initial_conc, target_conc=0.1, target_total_volume=15):
    """
    Calculate DNA volume and TE buffer volume for forensic DNA normalization.
    
    Args:
        initial_conc: Starting DNA concentration (ng/µL)
        target_conc: Target concentration (default 0.1 ng/µL, typical for forensics)
        target_total_volume: Final total volume needed (default 15 µL, typical for PCR)
    
    Returns:
        dict with 'dna_volume_ul', 'te_volume_ul', 'needs_predilution', 'message'
    
    Raises:
        ValueError: If inputs are invalid or target concentration is impossible.
    """
    initial_conc = validate_positive_number(initial_conc)
    target_conc = validate_positive_number(target_conc)
    target_total_volume = validate_positive_number(target_total_volume)
    
    if target_conc <= 0:
        raise ValueError("Target concentration must be > 0")
    
    # Calculate required DNA volume using dilution equation: C1*V1 = C2*V2
    # initial_conc * dna_volume = target_conc * target_total_volume
    dna_volume_ul = (target_conc * target_total_volume) / initial_conc
    te_volume_ul = target_total_volume - dna_volume_ul
    
    # Safety check for accurate pipetting
    needs_predilution = dna_volume_ul < 1.0
    
    message = ""
    if needs_predilution:
        message = (
            f"⚠ PRE-DILUTION RECOMMENDED: Required DNA volume is {dna_volume_ul:.3f} µL "
            f"(< 1 µL). This is below typical pipette accuracy. "
            f"Consider pre-diluting the DNA sample first, then normalizing."
        )
    
    return {
        'dna_volume_ul': dna_volume_ul,
        'te_volume_ul': te_volume_ul,
        'needs_predilution': needs_predilution,
        'message': message
    }


def dna_normalization_calculator(current_conc, current_volume_ul, target_conc, conc_unit='ng/µL', fragment_bp=None):
    """Calculate how much TE buffer to add to reach target DNA concentration."""
    current_conc = validate_positive_number(current_conc)
    current_vol = validate_positive_number(current_volume_ul)
    target_conc = validate_positive_number(target_conc)

    unit = conc_unit.replace('u', 'µ')

    if unit.lower() == 'nm':
        if fragment_bp is None:
            raise ValueError('Fragment length (bp) is required for nM conversions')
        bp = validate_positive_number(fragment_bp)
        mw = 660.0 * bp  # Molecular weight for dsDNA
        current_ng_per_ul = current_conc * mw * 1e-6
        target_ng_per_ul = target_conc * mw * 1e-6
    elif unit in ('ng/µL', 'ng/uL', 'ng/μL'):
        current_ng_per_ul = current_conc
        target_ng_per_ul = target_conc
    else:
        raise ValueError('Use "ng/µL" or "nM"')

    if target_ng_per_ul <= 0:
        raise ValueError("Target concentration must be > 0")

    total_dna_ng = current_ng_per_ul * current_vol
    final_volume_ul = total_dna_ng / target_ng_per_ul

    if final_volume_ul < current_vol - 1e-9:
        raise ValueError("Cannot concentrate by dilution; use evaporation instead")

    volume_te_to_add_ul = final_volume_ul - current_vol
    return final_volume_ul, volume_te_to_add_ul


def display_dna_normalization():
    """Display DNA normalization calculator."""
    try:
        print("\n" + "=" * 60)
        print("DNA NORMALIZATION (Molecular/Forensics)")
        print("=" * 60)
        conc_unit = input("Concentration unit (ng/µL or nM) [ng/µL]: ").strip() or 'ng/µL'
        current_conc = input(f"Current concentration ({conc_unit}): ").strip()
        current_vol = input("Current volume (µL): ").strip()
        target_conc = input(f"Target concentration ({conc_unit}): ").strip()
        fragment_bp = None
        if conc_unit.lower() == 'nm':
            fragment_bp = input("Fragment length in bp: ").strip()

        final_vol, vol_te = dna_normalization_calculator(current_conc, current_vol, target_conc, conc_unit, fragment_bp)

        print("\nResults:")
        print(f"  Input unit: {conc_unit}")
        print(f"  Current: {float(current_conc):.2f} {conc_unit}, {float(current_vol):.1f} µL")
        print(f"  Target: {float(target_conc):.2f} {conc_unit}")
        print(f"  Final total volume: {final_vol:.2f} µL")
        print(f"  TE buffer to add: {vol_te:.2f} µL")
        # Attempt to estimate cost using TE Buffer pricing if available
        try:
            cost = compute_cost_for_volume('TE Buffer', vol_te)
        except Exception:
            cost = None
        if cost is not None:
            print(f"  Estimated cost (TE Buffer): ${cost:.2f}")
        if vol_te < 1:
            print("  ⚠ Volume <1 µL; may be difficult to pipet accurately")
        print("\n")
        
        details = {
            'input_unit': conc_unit,
            'current_conc': float(current_conc),
            'current_volume_ul': float(current_vol),
            'target_conc': float(target_conc),
            'final_volume_ul': final_vol,
            'volume_TE_to_add_ul': vol_te,
            'fragment_bp': fragment_bp,
            'estimated_cost': cost if cost is not None else None
        }
        return {
            'module': 'Molecular - DNA Normalization',
            'summary': f'Normalize to {float(target_conc):.2f} {conc_unit}',
            'details': details,
            'status': 'completed'
        }
    except ValueError as e:
        print(f"✗ Error: {e}\n")
        return None


def display_normalize_dna_forensics():
    """Interactive forensic DNA normalization with pre-dilution check."""
    try:
        print("\n" + "=" * 60)
        print("FORENSIC DNA NORMALIZATION")
        print("=" * 60)
        print("Calculate volumes for forensic DNA samples.")
        print("Default: target 0.1 ng/µL in 15 µL (typical for PCR)\n")
        
        initial_conc = input("Initial DNA concentration (ng/µL): ").strip()
        target_conc = input("Target concentration (ng/µL) [0.1]: ").strip() or '0.1'
        target_volume = input("Target total volume (µL) [15]: ").strip() or '15'
        
        result = normalize_dna(float(initial_conc), float(target_conc), float(target_volume))
        
        print("\nResults:")
        print(f"  DNA volume to use: {result['dna_volume_ul']:.3f} µL")
        print(f"  TE buffer to add: {result['te_volume_ul']:.3f} µL")
        try:
            cost = compute_cost_for_volume('TE Buffer', result['te_volume_ul'])
        except Exception:
            cost = None
        if cost is not None:
            print(f"  Estimated cost (TE Buffer): ${cost:.2f}")
        print(f"  Total final volume: {float(target_volume):.1f} µL")
        
        if result['needs_predilution']:
            print(f"\n{result['message']}")
        else:
            print(f"\n✓ Volume is within acceptable pipetting range (≥1 µL)")
        
        print()
        
        details = {
            'initial_concentration_ng_ul': float(initial_conc),
            'target_concentration_ng_ul': float(target_conc),
            'target_total_volume_ul': float(target_volume),
            'dna_volume_ul': result['dna_volume_ul'],
            'te_buffer_volume_ul': result['te_volume_ul'],
            'needs_predilution': result['needs_predilution'],
            'estimated_cost': cost if cost is not None else None
        }
        return {
            'module': 'Molecular - Forensic DNA Normalization',
            'summary': f'{result["dna_volume_ul"]:.3f} µL DNA + {result["te_volume_ul"]:.3f} µL TE',
            'details': details,
            'status': 'completed'
        }
    except ValueError as e:
        print(f"✗ Error: {e}\n")
        return None

