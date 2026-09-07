# ChatGPT Slash Command Finder

A local Streamlit tool for **ChatGPT** that turns a plain-English goal into the most relevant `/codewords` from a curated library of **384 prompt shortcuts**.

Use it when you know what you want ChatGPT to do but you are not sure which slash-style prompt shortcut fits best. Describe the task, optionally filter by domain, and the app recommends the most relevant commands and ready-to-copy combinations for ChatGPT.

> These are user-defined prompt labels for ChatGPT, not official ChatGPT commands or hidden OpenAI features.

## What it does

- Free-text input: describe what you want ChatGPT to do.
- Recommends the most relevant slash-style prompt shortcuts for ChatGPT.
- Use-case filters for graphic design, photography, marketing, office work, business, education, engineering, web/UX, coding, and social media.
- Filters by the 13 library sections.
- Local relevance ranking; no API key is required.
- Suggested combinations of two or three codewords.
- A quick ChatGPT prompt ready to copy.
- Full searchable browser for all 384 commands.

## Quick start

Requirements: Python 3.10+.

```bash
git clone https://github.com/ergowareltd/chatgpt-prompt-shortcut-finder.git
cd chatgpt-prompt-shortcut-finder
python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually `http://localhost:8501`.

## Example

Input:

```text
Create an elegant premium advertisement for a red wine bottle on a black background with side lighting.
```

The app may recommend ChatGPT prompt shortcuts such as:

```text
/productshot
/lusso
/dark-premium
/editorial
```

It also suggests combinations such as:

```text
/productshot + /dark-premium + /editorial Create an elegant premium advertisement for a red wine bottle...
```

Copy the resulting line into ChatGPT and continue refining the request normally.

## Project structure

```text
.
├── app.py
├── finder_core.py
├── command_data.py
├── export_commands.py
├── build_command_data.py
├── tests/
│   └── test_core.py
├── docs/
│   └── ABOUT_CODEWORDS.md
├── .github/workflows/ci.yml
├── ATTRIBUTION.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
└── requirements-dev.txt
```

## Command library

The English catalog is embedded in `command_data.py` so the app is self-contained. To export it as readable JSON, run:

```bash
python export_commands.py
```

The 384 entries are organized into 13 sections:

1. Structure, engineering & internal views
2. How it works, flows & instructions
3. Connections, compatibility, comparison & anatomy
4. Photography, perspectives & lighting
5. Art, editorial, graphics & visual styles
6. Motion, time, practical use & annotations
7. Environment, wear & technical imaging
8. Visual learning, education & diagrams
9. Strategy, analysis & business
10. Product photography & advertising
11. Social media, branding & visual communication
12. Web, apps & interfaces
13. Writing, reasoning, marketing & coding

## How ranking works

The finder uses a lightweight local scoring engine based on:

- normalized keywords;
- intent expansion;
- use-case detection;
- category and section weighting;
- a small number of priority rules for common intents;
- string similarity.

There is no external model call, telemetry, or API key requirement.

## Tests

```bash
python -m pip install -r requirements-dev.txt
pytest -q
```

GitHub Actions runs the tests on Python 3.10 through 3.13.

## Attribution

The project includes visual codeword names inspired by a public visual codebook by John Savage, together with independently written descriptions and additional project-specific shortcuts. See [`ATTRIBUTION.md`](ATTRIBUTION.md).

## License

Software and original project documentation are released under the MIT License. See [`LICENSE`](LICENSE) and [`ATTRIBUTION.md`](ATTRIBUTION.md) for third-party references.
