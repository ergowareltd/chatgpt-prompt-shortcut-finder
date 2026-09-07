# Contributing

Contributions are welcome.

## Local setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest -q
python -m streamlit run app.py
```

## Adding or editing a command

The catalog is embedded in `command_data.py`. For substantial catalog changes, export the JSON with `python export_commands.py`, edit the exported data, then run `python build_command_data.py commands_384.json` to regenerate the embedded payload. Each record contains:

```json
{
  "command": "/example",
  "description": "One concise English description.",
  "category": "Section name",
  "section": 1
}
```

Keep command names unique. Add or update a test when changing ranking behavior.

## Pull requests

Keep pull requests focused, explain the user-facing change, and make sure `pytest -q` passes.
