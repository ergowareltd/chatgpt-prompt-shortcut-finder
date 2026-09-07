from __future__ import annotations

import json
from pathlib import Path

from command_data import get_embedded_commands

OUTPUT = Path(__file__).resolve().parent / "commands_384.json"
OUTPUT.write_text(json.dumps(get_embedded_commands(), ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Exported {len(get_embedded_commands())} commands to {OUTPUT}")
