from __future__ import annotations

import base64
import gzip
import json
import sys
import textwrap
from pathlib import Path

SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("commands_384.json")
TARGET = Path(__file__).resolve().parent / "command_data.py"

rows = json.loads(SOURCE.read_text(encoding="utf-8"))
payload = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
encoded = base64.b64encode(gzip.compress(payload, compresslevel=9)).decode("ascii")
wrapped = "\n".join(textwrap.wrap(encoded, 120))

content = f'''from __future__ import annotations

import base64
import gzip
import json

DATA_GZIP_BASE64 = """{wrapped}"""


def get_embedded_commands() -> list[dict]:
    raw = gzip.decompress(base64.b64decode(DATA_GZIP_BASE64.encode("ascii")))
    return json.loads(raw.decode("utf-8"))
'''
TARGET.write_text(content, encoding="utf-8")
print(f"Embedded {{len(rows)}} commands into {{TARGET}}")
