"""Biochemistry module: molarity, mass, volume, and concentration conversions, serial dilutions."""
from utils import validate_positive_number


def convert_molarity(value, from_unit, to_unit):
    """Convert between molar units (M, mM)."""
    value = validate_positive_number(value)
    
    if from_unit == 'M':
        value_in_molar = value
    elif from_unit == 'mM':
        value_in_molar = value / 1000
    else:
        raise ValueError(f"Unknown molarity unit: {from_unit}")
    
    if to_unit == 'M':
        return value_in_molar
    elif to_unit == 'mM':
        return value_in_molar * 1000
    else:
        raise ValueError(f"Unknown molarity unit: {to_unit}")


def convert_mass(value, from_unit, to_unit):
    """Convert between mass units (g, mg)."""
    value = validate_positive_number(value)
    
    if from_unit == 'g':
        value_in_grams = value
    elif from_unit == 'mg':
        value_in_grams = value / 1000
    else:
        raise ValueError(f"Unknown mass unit: {from_unit}")
    
    if to_unit == 'g':
        return value_in_grams
    elif to_unit == 'mg':
        return value_in_grams * 1000
    else:
        raise ValueError(f"Unknown mass unit: {to_unit}")


def convert_volume(value, from_unit, to_unit):
    """Convert between volume units (L, µL)."""
    value = validate_positive_number(value)
    
    from_unit = from_unit.replace('µ', 'u')
    to_unit = to_unit.replace('µ', 'u')
    
    if from_unit == 'L':
        value_in_liters = value
    elif from_unit == 'uL':
        value_in_liters = value / 1_000_000
    else:
        raise ValueError(f"Unknown volume unit: {from_unit}")
    
    if to_unit == 'L':
        return value_in_liters
    elif to_unit == 'uL':
        return value_in_liters * 1_000_000
    else:
        raise ValueError(f"Unknown volume unit: {to_unit}")


def convert_concentration(value, from_unit, to_unit):
    """Convert between concentration units (ng/µL, ng/mL, pg/µL)."""
    val = validate_positive_number(value)
    fu = from_unit.replace('µ', 'u')
    tu = to_unit.replace('µ', 'u')

    supported = {'ng/uL', 'ng/mL', 'pg/uL'}
    if fu not in supported:
        raise ValueError(f"Unsupported from-unit: {from_unit}")
    if tu not in supported:
        raise ValueError(f"Unsupported to-unit: {to_unit}")

    # Convert to base unit ng/µL
    if fu == 'ng/uL':
        base = val
    elif fu == 'ng/mL':
        base = val / 1000.0
    elif fu == 'pg/uL':
        base = val / 1000.0

    # Convert from base to target
    if tu == 'ng/uL':
        return base
    elif tu == 'ng/mL':
        return base * 1000.0
    elif tu == 'pg/uL':
        return base * 1000.0


def serial_dilution(starting_conc, dilution_factor, num_steps, final_volume, conc_unit='M', vol_unit='µL'):
    """Calculate serial dilution recipe."""
    starting_conc = validate_positive_number(starting_conc)
    dilution_factor = validate_positive_number(dilution_factor)
    num_steps = validate_positive_number(num_steps)
    final_volume = validate_positive_number(final_volume)
    
    if dilution_factor <= 1:
        raise ValueError("Dilution factor must be greater than 1")
    
    if int(num_steps) != num_steps or num_steps < 1:
        raise ValueError("Number of steps must be a positive integer")
    
    num_steps = int(num_steps)
    sample_volume = final_volume / dilution_factor
    diluent_volume = final_volume - sample_volume
    
    results = []
    for step in range(1, num_steps + 1):
        concentration = starting_conc / (dilution_factor ** step)
        results.append((step, concentration, sample_volume, diluent_volume))
    
    return results, starting_conc, sample_volume, diluent_volume, conc_unit, vol_unit
