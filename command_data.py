from __future__ import annotations

import base64
import gzip
import json

from command_chunk_1 import CHUNK as C1
from command_chunk_2 import CHUNK as C2
from command_chunk_3 import CHUNK as C3
from command_chunk_4 import CHUNK as C4
from command_chunk_5 import CHUNK as C5


def get_embedded_commands() -> list[dict]:
    payload = base64.b64decode(C1 + C2 + C3 + C4 + C5)
    return json.loads(gzip.decompress(payload).decode("utf-8"))
