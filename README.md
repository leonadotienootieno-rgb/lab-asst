# Universal Lab Assistant

Universal Lab Assistant is a lightweight command-line toolkit for laboratory calculations aimed at biochemists, microbiologists, and forensic scientists. It bundles common lab utilities (concentration conversions, serial dilutions, hemocytometer cell counting and seeding, DNA normalization, and microbial generation time calculations) into a simple, modular Python application.

**Current Modules**
- **Biochemistry**: [biochem.py](biochem.py) — molarity, mass, volume and concentration conversions; serial dilution recipes.
- **Tissue Culture**: [culture.py](culture.py) — hemocytometer-based cell concentration and seeding volume calculations.
- **Molecular / Forensics**: [forensics.py](forensics.py) — DNA normalization (calculate TE to add to reach a target concentration; supports `ng/µL` and `nM` with fragment length).
- **Microbiology**: [micro.py](micro.py) — generation-time calculator (number of generations and doubling time) and pending-experiment support.
- **Storage**: [storage.py](storage.py) — JSON-backed lab history save/load and pending-experiment finalization.
- **Utilities**: [utils.py](utils.py) — input validation and shared constants (standard concentration unit: `ng/µL`).
- **Entry point**: [main.py](main.py) — interactive main menu and orchestration of modules.

**Why the modular structure?**
- Separation of concerns: calculation logic is kept separate from user interaction and storage.
- Testability: each module can be imported and unit-tested independently.
- Maintainability: adding new laboratory domains or features is straightforward.

**Directory layout**
```
/home/user/biochem/
├── main.py           # CLI entry point
├── biochem.py        # Biochemistry helpers
├── culture.py        # Tissue culture helpers
├── micro.py          # Microbiology helpers
├── forensics.py      # DNA normalization
├── storage.py        # JSON history management
├── utils.py          # Shared utilities & constants
└── lab_history.json  # Lab log (created at runtime)
```

**Run the app**
Make sure you have Python 3 installed. From the project root run:

```bash
python3 main.py
```

Follow the interactive menu to perform calculations. After each computation you will be prompted whether to save the result to the lab history (`lab_history.json`).

If you want, I can add a small test suite, a `requirements.txt`, or a short example workflow demonstrating a typical use-case (serial dilution -> DNA normalization -> save result). Would you like that next?