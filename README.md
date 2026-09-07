# ChatGPT Slash Command Finder

[![CI](https://github.com/ergowareltd/chatgpt-prompt-shortcut-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/ergowareltd/chatgpt-prompt-shortcut-finder/actions/workflows/ci.yml)

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

Requirements:

- Python 3.10+
- pip
- A modern web browser

Clone the repository:

```bash
git clone https://github.com/ergowareltd/chatgpt-prompt-shortcut-finder.git
cd chatgpt-prompt-shortcut-finder
python -m venv .venv
```

Activate the environment.

### Windows

```powershell
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

You can also use the included startup scripts:

### Windows

```text
run_windows.bat
```

### macOS / Linux

```bash
./run_unix.sh
```

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

It can also suggest combinations such as:

```text
/productshot + /dark-premium + /editorial Create an elegant premium advertisement for a red wine bottle...
```

Copy the resulting line into ChatGPT and continue refining the request normally.

## Project structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── ABOUT_CODEWORDS.md
├── tests/
│   └── test_core.py
├── app.py
├── finder_core.py
├── command_data.py
├── command_chunk_1.py
├── command_chunk_2.py
├── command_chunk_3.py
├── command_chunk_4.py
├── command_chunk_5.py
├── export_commands.py
├── build_command_data.py
├── run_windows.bat
├── run_unix.sh
├── requirements.txt
├── requirements-dev.txt
├── ATTRIBUTION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── .gitignore
└── README.md
```

## Command library

The command catalog contains **384 entries** organized into 13 sections.

The compressed catalog data is stored across:

```text
command_chunk_1.py
command_chunk_2.py
command_chunk_3.py
command_chunk_4.py
command_chunk_5.py
```

`command_data.py` loads and reconstructs the embedded catalog when the application starts.

To export the complete catalog as readable JSON, run:

```bash
python export_commands.py
```

The 384 entries are organized into these sections:

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
- priority rules for common intents;
- string similarity.

There is no external model call, telemetry, or API key requirement.

The recommendation process runs locally.

## Tests

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the tests:

```bash
python -m pytest -q
```

The current test suite checks, among other things:

- that the library contains 384 unique commands;
- product photography recommendations;
- roadmap-related queries;
- Python debugging queries.

GitHub Actions automatically runs the test suite on:

- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

## Development

To verify the application manually:

```bash
python -m streamlit run app.py
```

To run the automated tests:

```bash
python -m pytest -q
```

Contributions are welcome. See:

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

## About the slash-style codewords

The `/codewords` used by this project are mnemonic prompt labels designed to make prompting faster and easier.

They are not:

- official ChatGPT slash commands;
- hidden ChatGPT features;
- OpenAI system commands;
- special API instructions.

They work because the codeword is combined with a normal natural-language request that describes the user's intended task.

See [`docs/ABOUT_CODEWORDS.md`](docs/ABOUT_CODEWORDS.md) for more information.

## Attribution

The project includes visual codeword names inspired by a public visual codebook by John Savage, together with independently written descriptions and additional project-specific shortcuts.

See [`ATTRIBUTION.md`](ATTRIBUTION.md) for details and third-party references.

## Privacy

The application runs locally and does not require:

- an OpenAI API key;
- a ChatGPT account connection;
- external AI API calls;
- telemetry.

## License

Software and original project documentation are released under the MIT License.

See:

- [`LICENSE`](LICENSE)
- [`ATTRIBUTION.md`](ATTRIBUTION.md)

for licensing and third-party reference information.