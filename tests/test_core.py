from finder_core import load_commands, rank_commands


def test_library_has_384_unique_commands():
    rows = load_commands()
    assert len(rows) == 384
    assert len({r["command"] for r in rows}) == 384


def test_product_photo_query_prioritizes_productshot():
    rows = load_commands()
    results = rank_commands(rows, "professional studio product photo of a perfume bottle", top_n=10)
    commands = [r["command"] for r in results]
    assert "/productshot" in commands[:5]


def test_roadmap_query_returns_roadmap():
    rows = load_commands()
    results = rank_commands(rows, "30 day marketing roadmap", top_n=10)
    commands = [r["command"] for r in results]
    assert "/roadmap" in commands[:5]


def test_python_bug_query_returns_debug():
    rows = load_commands()
    results = rank_commands(rows, "fix a Python bug and explain the error", top_n=10)
    commands = [r["command"] for r in results]
    assert "/debug" in commands[:5]
