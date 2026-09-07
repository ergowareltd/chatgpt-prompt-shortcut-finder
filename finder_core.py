from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from command_data import get_embedded_commands

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "create", "do", "for",
    "from", "give", "help", "how", "i", "in", "into", "is", "it", "make", "me", "my",
    "of", "on", "or", "please", "show", "that", "the", "this", "to", "use", "want", "with",
}

USE_CASES = {
    "Auto": [],
    "Graphic design": [5, 8, 10, 11],
    "Photography & images": [4, 5, 7, 10],
    "Marketing & advertising": [9, 10, 11, 13],
    "Office & productivity": [9, 13],
    "Business & strategy": [9, 13],
    "Education & training": [1, 2, 3, 8, 13],
    "Technical & engineering": [1, 2, 3, 7],
    "Web, UX & interfaces": [12],
    "Coding & development": [13],
    "Social media & content": [10, 11, 13],
}

INTENT_EXPANSIONS = {
    "photo": ["photography", "studio", "lighting", "cinematic", "productshot", "camera"],
    "photography": ["photo", "studio", "lighting", "cinematic", "productshot"],
    "product": ["productshot", "showcase", "advertising", "packaging", "hero"],
    "ad": ["advertising", "campaign", "showcase", "editorial", "marketing"],
    "advertising": ["ad", "campaign", "showcase", "editorial", "marketing"],
    "luxury": ["premium", "dark", "editorial", "chiaroscuro"],
    "social": ["instagram", "facebook", "linkedin", "carousel", "content", "viral"],
    "instagram": ["social", "post", "story", "carousel", "advertising"],
    "logo": ["brand", "branding", "identity", "design", "moodboard"],
    "brand": ["branding", "logo", "identity", "campaign", "style"],
    "marketing": ["strategy", "funnel", "customer", "campaign", "seo", "copywriter"],
    "seo": ["search", "copywriter", "content", "marketing"],
    "company": ["business", "strategy", "workflow", "process", "kpi", "roadmap"],
    "business": ["strategy", "workflow", "process", "kpi", "roadmap", "decision"],
    "strategy": ["roadmap", "decision", "matrix", "business", "priority"],
    "decision": ["matrix", "comparison", "proscons", "critical"],
    "compare": ["comparison", "sidebyside", "proscons", "featurematrix", "whichone"],
    "comparison": ["sidebyside", "proscons", "featurematrix", "whichone"],
    "explain": ["infographic", "diagram", "visualize", "learning", "flowchart", "eli5", "teacher"],
    "school": ["learning", "infographic", "teacher", "eli5", "flashcards", "conceptmap"],
    "study": ["learning", "cheatsheet", "flashcards", "mindmap", "summary"],
    "manual": ["instruction", "step", "checklist", "repair", "technical"],
    "technical": ["blueprint", "schematic", "cutaway", "exploded", "dimension"],
    "inside": ["cutaway", "insideview", "xray", "exploded", "crosssection", "seethrough"],
    "internal": ["cutaway", "insideview", "xray", "exploded", "crosssection", "seethrough"],
    "process": ["workflow", "flowchart", "roadmap", "stepsequence"],
    "web": ["website", "landing", "ux", "ui", "wireframe", "dashboard"],
    "website": ["landing", "wireframe", "ux", "ui"],
    "app": ["ui", "dashboard", "userflow", "saas"],
    "code": ["coding", "debug", "explain", "programming"],
    "python": ["code", "coding", "debug", "explain", "programming"],
    "bug": ["debug", "error", "fault", "problemresolution"],
    "error": ["debug", "fault", "problemresolution"],
    "email": ["copywriter", "professional", "writing"],
    "write": ["copywriter", "writing", "improve", "human", "expert"],
    "summary": ["brief", "cheatsheet"],
}

USE_CASE_HINTS = {
    "Graphic design": {"graphic", "design", "poster", "cover", "magazine", "packaging", "logo", "brand", "infographic"},
    "Photography & images": {"photo", "photography", "image", "portrait", "lighting", "cinematic", "studio", "product", "model"},
    "Marketing & advertising": {"marketing", "advertising", "campaign", "lead", "funnel", "seo", "copy", "ad"},
    "Office & productivity": {"office", "email", "summary", "document", "table", "outline", "productivity", "presentation"},
    "Business & strategy": {"business", "strategy", "company", "decision", "kpi", "roadmap", "priority", "process"},
    "Education & training": {"school", "study", "explain", "lesson", "education", "training", "learn", "teach"},
    "Technical & engineering": {"technical", "engineering", "internal", "mechanism", "assembly", "schematic", "dimension", "maintenance"},
    "Web, UX & interfaces": {"web", "website", "landing", "app", "dashboard", "ui", "ux", "wireframe"},
    "Coding & development": {"code", "python", "debug", "programming", "script", "error", "software", "bug"},
    "Social media & content": {"social", "instagram", "facebook", "linkedin", "tiktok", "post", "carousel", "viral"},
}

COMPLEMENTARY = {
    1: [2, 7, 8], 2: [1, 3, 8], 3: [1, 2, 8], 4: [5, 10, 11],
    5: [4, 10, 11], 6: [4, 5, 8], 7: [1, 2, 3], 8: [1, 2, 9, 13],
    9: [8, 10, 11, 13], 10: [4, 5, 11], 11: [5, 9, 10, 13],
    12: [9, 11, 13], 13: [8, 9, 11, 12],
}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("/", " ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> list[str]:
    return [t for t in normalize(text).split() if len(t) > 1 and t not in STOPWORDS]


def load_commands(path: str | Path | None = None) -> list[dict]:
    if path is None:
        rows = get_embedded_commands()
    else:
        with Path(path).open("r", encoding="utf-8") as f:
            rows = json.load(f)
    for row in rows:
        row["search_text"] = normalize(f"{row['command']} {row['description']} {row['category']}")
    return rows


def infer_use_cases(query: str) -> list[str]:
    q_tokens = set(tokens(query))
    scored = []
    for name, hints in USE_CASE_HINTS.items():
        overlap = len(q_tokens & hints)
        if overlap:
            scored.append((overlap, name))
    return [name for _, name in sorted(scored, key=lambda x: (-x[0], x[1]))]


def expand_query(query: str, selected_use_case: str) -> list[str]:
    q_tokens = tokens(query)
    expanded = list(q_tokens)
    for token in q_tokens:
        expanded.extend(INTENT_EXPANSIONS.get(token, []))
    if selected_use_case != "Auto":
        expanded.extend(tokens(selected_use_case))
    return list(dict.fromkeys(expanded))


def intent_priority_boost(row: dict, query: str) -> float:
    q = set(tokens(query))
    cmd = row["command"]
    boost = 0.0

    if q & {"python", "code", "programming", "script", "software"}:
        if q & {"error", "errors", "bug", "fix", "debug"} and cmd == "/debug":
            boost += 30
        if q & {"explain", "understand", "works"} and cmd == "/spiegacodice":
            boost += 24
        if q & {"write", "create", "generate"} and cmd == "/codice":
            boost += 22

    if q & {"product", "bottle", "package", "object"}:
        if q & {"photo", "photography", "studio"} and cmd == "/productshot":
            boost += 28
        if q & {"advertising", "ad", "campaign"} and cmd in {"/showcase", "/productshot", "/hero-product"}:
            boost += 20
        if q & {"luxury", "premium", "elegant"} and cmd in {"/lusso", "/dark-premium", "/editorial"}:
            boost += 18

    if q & {"infographic"} and cmd in {"/infographic", "/infografic"}:
        boost += 30
    if q & {"roadmap", "plan", "planning"} and cmd == "/roadmap":
        boost += 24
    if q & {"logo"} and cmd == "/logo-concept":
        boost += 30
    if q & {"cover", "magazine"} and cmd == "/magazinecover":
        boost += 28
    if q & {"inside", "internal", "section", "components"} and cmd in {"/cutaway", "/insideview", "/crosssection", "/explodedview"}:
        boost += 16
    return boost


def score_row(row: dict, query: str, query_tokens: list[str], boosted_sections: set[int]) -> float:
    cmd = normalize(row["command"])
    desc = normalize(row["description"])
    cat = normalize(row["category"])
    full = row["search_text"]
    score = 0.0

    for token in query_tokens:
        if token == cmd:
            score += 18
        elif token in cmd:
            score += 10
        if re.search(rf"\b{re.escape(token)}\b", desc):
            score += 4.5
        elif token in desc:
            score += 2.0
        if token in cat:
            score += 2.5

    nq = normalize(query)
    if nq and nq in full:
        score += 12
    if nq:
        score += 8 * SequenceMatcher(None, nq, cmd).ratio()
    if row["section"] in boosted_sections:
        score *= 1.22
    if len(cmd.split()) <= 2:
        score += 0.5
    return score


def rank_commands(
    rows: list[dict],
    query: str,
    use_case: str = "Auto",
    selected_categories: list[str] | None = None,
    top_n: int = 10,
) -> list[dict]:
    selected_categories = selected_categories or []
    candidates = rows

    if use_case != "Auto":
        allowed_sections = set(USE_CASES[use_case])
        candidates = [r for r in candidates if r["section"] in allowed_sections]
    if selected_categories:
        allowed_categories = set(selected_categories)
        candidates = [r for r in candidates if r["category"] in allowed_categories]

    inferred = infer_use_cases(query) if use_case == "Auto" else []
    boosted_sections: set[int] = set()
    for name in inferred[:2]:
        boosted_sections.update(USE_CASES[name])

    expanded = expand_query(query, use_case)
    scored = []
    for row in candidates:
        score = score_row(row, query, expanded, boosted_sections) + intent_priority_boost(row, query)
        if score > 0:
            item = dict(row)
            item["score_raw"] = score
            scored.append(item)

    scored.sort(key=lambda x: (-x["score_raw"], x["command"]))
    scored = scored[: max(top_n, 1)]

    if scored:
        max_score = scored[0]["score_raw"]
        min_score = scored[-1]["score_raw"]
        span = max(max_score - min_score, 1e-9)
        for index, row in enumerate(scored):
            relative = 62 + 36 * ((row["score_raw"] - min_score) / span) - index * 0.35
            row["match"] = int(max(35, min(98, round(relative))))
    return scored


def explain_match(row: dict, query: str) -> str:
    q = set(tokens(query))
    c = set(tokens(row["command"]))
    d = set(tokens(row["description"]))
    overlap_cmd = sorted(q & c)
    overlap_desc = sorted(q & d)
    if overlap_cmd:
        return "Direct command match: " + ", ".join(overlap_cmd[:3])
    if overlap_desc:
        return "Description matches: " + ", ".join(overlap_desc[:4])
    return f"Relevant to the “{row['category']}” section."


def build_combinations(results: list[dict], query: str, max_combos: int = 3) -> list[str]:
    if not results:
        return []
    combos: list[str] = []
    used: set[tuple[str, ...]] = set()
    for base in results[:4]:
        preferred_sections = COMPLEMENTARY.get(base["section"], [])
        partners = [
            r for r in results[1:10]
            if r["command"] != base["command"] and r["section"] in preferred_sections
        ]
        if not partners:
            partners = [r for r in results[1:8] if r["command"] != base["command"]]
        if not partners:
            continue
        parts = [base["command"], partners[0]["command"]]
        if len(partners) > 1 and partners[1]["section"] != partners[0]["section"]:
            parts.append(partners[1]["command"])
        key = tuple(parts)
        if key not in used:
            used.add(key)
            combos.append(" + ".join(parts) + " " + query.strip())
        if len(combos) >= max_combos:
            break
    return combos


def category_options_for_use_case(rows: list[dict], use_case: str) -> list[str]:
    if use_case == "Auto":
        return list(dict.fromkeys(r["category"] for r in rows))
    sections = set(USE_CASES[use_case])
    return list(dict.fromkeys(r["category"] for r in rows if r["section"] in sections))
