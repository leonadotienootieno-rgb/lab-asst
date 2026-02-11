"""Storage module: JSON history management."""
import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'lab_history.json')
REAGENTS_FILE = os.path.join(os.path.dirname(__file__), 'reagents.json')


def load_history():
    """Load lab history from JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_history_entry(entry: dict):
    """Save a single entry to lab history."""
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def prompt_save(entry: dict):
    """Prompt user to save an entry to lab history."""
    choice = input('Save to lab history? (y/n): ').strip().lower()
    if choice in ('y', 'yes'):
        entry.setdefault('timestamp', datetime.now().isoformat())
        save_history_entry(entry)
        print(f'✓ Saved to {HISTORY_FILE}')
    else:
        print('Not saved.')


def load_reagents():
    """Load reagent pricing from JSON file."""
    if not os.path.exists(REAGENTS_FILE):
        return {}
    try:
        with open(REAGENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_reagents(reagents: dict):
    """Save reagent pricing to JSON file."""
    with open(REAGENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reagents, f, indent=2, ensure_ascii=False)


def update_reagent_price(name: str, price_per_unit: float, unit: str = 'uL'):
    """Add or update a reagent price. Unit should be 'uL' or 'mL'."""
    reagents = load_reagents()
    reagents[name] = {
        'price_per_unit': float(price_per_unit),
        'unit': unit
    }
    save_reagents(reagents)


def get_reagent_price(name: str):
    """Return reagent pricing dict or None if not found."""
    reagents = load_reagents()
    return reagents.get(name)


def compute_cost_for_volume(name: str, volume_ul: float):
    """Compute cost for given reagent name and volume in µL.

    Returns cost as float or None if reagent not found.
    """
    info = get_reagent_price(name)
    if not info:
        return None
    price = float(info.get('price_per_unit', 0.0))
    unit = info.get('unit', 'uL')
    if unit == 'uL':
        return price * float(volume_ul)
    elif unit == 'mL':
        # convert µL to mL
        return price * (float(volume_ul) / 1000.0)
    else:
        # unknown unit, assume per µL
        return price * float(volume_ul)


def display_history():
    """Display lab history and finalize pending experiments."""
    from micro import generation_time_calculator
    from utils import validate_positive_number
    
    history = load_history()
    if not history:
        print('\nNo history found.')
        return

    print('\n' + '=' * 80)
    print('LAB HISTORY')
    print('=' * 80)
    total_spend = 0.0
    for i, e in enumerate(history, 1):
        ts = e.get('timestamp', '')
        module = e.get('module', '')
        status = e.get('status', 'completed')
        summary = e.get('summary', '')
        cost = e.get('details', {}).get('estimated_cost')
        if cost:
            try:
                total_spend += float(cost)
            except Exception:
                pass
        print(f"{i:>3}. [{status}] {ts} | {module} | {summary}")
        if cost:
            print(f"       Estimated cost: ${float(cost):.2f}")

    idx = input('\nEnter number to finalize pending Microbiology experiment (or press Enter): ').strip()
    if not idx:
        print('\n' + '-' * 40)
        print(f"Total Project Spend (from history): ${total_spend:.2f}")
        return
    try:
        idxi = int(idx) - 1
        entry = history[idxi]
    except Exception:
        print('Invalid selection.')
        return

    if entry.get('module') != 'Microbiology' or entry.get('status') != 'pending':
        print('Not a pending Microbiology experiment.')
        return

    final_N = input('Enter final bacterial count (N): ').strip()
    try:
        final_N_v = validate_positive_number(final_N)
        gens, dt = generation_time_calculator(
            entry['details']['N0'],
            final_N_v,
            entry['details']['time_elapsed']
        )
        entry['details']['N'] = final_N_v
        entry['details']['generations'] = gens
        entry['details']['doubling_time'] = dt
        entry['status'] = 'completed'
        entry['completed_timestamp'] = datetime.now().isoformat()
        
        history[idxi] = entry
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print('✓ Pending experiment finalized and saved.')
    except ValueError as e:
        print(f'Error: {e}')
