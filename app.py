from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from finder_core import (
    USE_CASES,
    build_combinations,
    category_options_for_use_case,
    explain_match,
    infer_use_cases,
    load_commands,
    normalize,
    rank_commands,
)

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="ChatGPT Slash Command Finder", page_icon="/", layout="wide")


@st.cache_data
def get_rows() -> list[dict]:
    return load_commands()


rows = get_rows()
categories_all = list(dict.fromkeys(r["category"] for r in rows))

st.title("ChatGPT Slash Command Finder")
st.caption(
    "Describe what you want ChatGPT to do and get the most relevant /codewords from a 384-command library. "
    "The ranking engine runs locally and does not require an API key."
)

with st.sidebar:
    st.header("Filters")
    use_case = st.selectbox(
        "Use case",
        list(USE_CASES.keys()),
        index=0,
        help="Auto infers the domain from your text. Other options restrict the search to relevant guide sections.",
    )
    available_categories = category_options_for_use_case(rows, use_case)
    selected_categories = st.multiselect(
        "Library sections",
        available_categories,
        placeholder="All compatible sections",
    )
    top_n = st.slider("Number of results", 5, 25, 10)
    st.divider()
    st.caption("Match percentages are relative relevance scores, not probabilities.")

st.subheader("1. What do you want ChatGPT to do?")
query = st.text_area(
    "Describe the result you want",
    placeholder=(
        "Examples: create a premium ad for a wine bottle; explain photosynthesis to a student; "
        "compare two marketing strategies; show the inside of an engine; fix a Python error..."
    ),
    height=110,
    label_visibility="collapsed",
)

example_cols = st.columns(4)
examples = [
    "Premium product advertisement",
    "Simple educational infographic",
    "30-day marketing roadmap",
    "Show the inside of an object",
]
for col, example in zip(example_cols, examples):
    if col.button(example, use_container_width=True):
        st.session_state["example_query"] = example

if st.session_state.get("example_query") and not query:
    query = st.session_state["example_query"]

search_clicked = st.button("Find ChatGPT commands", type="primary", use_container_width=True)

if query.strip() and (search_clicked or query):
    results = rank_commands(rows, query, use_case, selected_categories, top_n)
    inferred = infer_use_cases(query) if use_case == "Auto" else []
    if inferred:
        st.caption("Automatically detected use cases: " + " · ".join(inferred[:3]))

    st.subheader("2. Recommended ChatGPT prompt shortcuts")
    if not results:
        st.warning("No commands matched the current filters. Broaden the sections or switch to Auto.")
    else:
        for row in results:
            with st.container(border=True):
                c1, c2, c3 = st.columns([1.25, 5.3, 1.1])
                with c1:
                    st.markdown(f"### `{row['command']}`")
                with c2:
                    st.write(row["description"])
                    st.caption(f"{row['category']} · {explain_match(row, query)}")
                with c3:
                    st.metric("Match", f"{row['match']}%")

        st.subheader("3. Ready-to-try combinations")
        combinations = build_combinations(results, query)
        for combo in combinations or [f"{results[0]['command']} {query}"]:
            st.code(combo, language=None)

        st.subheader("4. Quick ChatGPT prompt")
        st.code(f"{results[0]['command']} {query.strip()}", language=None)

st.divider()
with st.expander("Browse the complete 384-command ChatGPT prompt library"):
    browse_category = st.selectbox("Section", ["All"] + categories_all, key="browse_cat")
    browse_search = st.text_input("Search command or description", key="browse_search")
    browse = rows
    if browse_category != "All":
        browse = [r for r in browse if r["category"] == browse_category]
    if browse_search.strip():
        needle = normalize(browse_search)
        browse = [r for r in browse if needle in r["search_text"]]
    dataframe = pd.DataFrame(
        [{"Command": r["command"], "Description": r["description"], "Section": r["category"]} for r in browse]
    )
    st.dataframe(dataframe, use_container_width=True, hide_index=True, height=480)

st.caption(
    "These /codewords are user-defined ChatGPT prompt shortcuts, not an official catalog of ChatGPT commands. "
    "The app treats them as operational labels for building faster, more consistent prompts."
)
