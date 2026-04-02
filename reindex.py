#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["urllib3"]
# ///
"""Update README.md badges and INDEX.md language listing."""

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
YIT = ROOT / "YIT.tex"
README = ROOT / "README.md"
INDEX = ROOT / "INDEX.md"

ISO_NAMES_URL = "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Name_Index.tab"
ISO_TYPES_URL = "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab"
CLCR_URL = "https://www.kreativekorp.com/clcr/json.php"

HEADERS = {"User-Agent": "yoneda-in-tongues/1.0"}


def fetch_iso_names():
    """Fetch ISO 639-3 code-to-name mapping from the Name Index."""
    names = {}
    req = urllib.request.Request(ISO_NAMES_URL, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        for line in resp.read().decode("utf-8").splitlines()[1:]:
            fields = line.split("\t")
            if len(fields) >= 2:
                code, print_name = fields[0], fields[1]
                if code not in names:  # keep first (primary) name
                    names[code] = print_name
    return names


def fetch_iso_main():
    """Fetch ISO 639-3 main table: Ref_Name and Language_Type.

    Language_Type: L(iving), H(istorical), E(xtinct), A(ncient), C(onstructed), S(pecial)
    """
    names = {}
    types = {}
    req = urllib.request.Request(ISO_TYPES_URL, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        for line in resp.read().decode("utf-8").splitlines()[1:]:
            fields = line.split("\t")
            if len(fields) >= 7:
                code = fields[0]
                types[code] = fields[5]   # Language_Type
                names[code] = fields[6]   # Ref_Name
    return names, types


def fetch_clcr():
    """Fetch CLCR registry: names and metadata."""
    names = {}
    with urllib.request.urlopen(CLCR_URL) as resp:
        for entry in json.loads(resp.read()):
            if entry.get("long"):
                names[entry["long"]] = entry["name"]
            if entry.get("short"):
                names[entry["short"]] = entry["name"]
    return names


def parse_sections():
    """Parse YIT.tex to get sections and their input paths."""
    sections = []
    current = None
    for line in YIT.read_text().splitlines():
        m = re.match(r"^%%% (.+)$", line)
        if m:
            current = m.group(1)
            sections.append((current, []))
            continue
        m = re.match(r"^\\?(?:cjkbreak)?\\input\{(.+)\}$", line)
        if m:
            if current is None:
                current = "Other"
                sections.append((current, []))
            sections[-1][1].append(m.group(1))
    return sections


def parse_contributors(path):
    """Extract contributors from a src file."""
    tex_path = (ROOT / path).with_suffix(".tex")
    if not tex_path.exists():
        return "", True
    text = tex_path.read_text()
    contributors = ""
    for line in text.splitlines():
        if line.startswith("% contributors:"):
            contributors = line.removeprefix("% contributors:").strip()
            break
    is_stub = "\\tran" not in text or all(
        line.lstrip().startswith("%") for line in text.splitlines() if "\\tran" in line
    )
    return contributors, is_stub


def code_from_path(path):
    """Extract the ISO/CLCR code from a src path."""
    rel = path.removeprefix("src/")
    if "/" in rel:
        return rel.split("/")[0]
    return rel


def clean_registry_name(name):
    """Strip noisy SIL qualifiers from registry names."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()


def resolve_name(path, iso_ref_names, iso_alt_names, clcr_names):
    """Resolve a human-readable language name from the file path.

    Prefers Ref_Name from the main ISO table, falls back to Name Index, then CLCR.
    """
    rel = path.removeprefix("src/")
    if "/" in rel:
        code, script = rel.split("/", 1)
        raw = iso_ref_names.get(code) or iso_alt_names.get(code) or clcr_names.get(code) or code
        return f"{clean_registry_name(raw)} ({script})"
    if rel.startswith("art-x-"):
        raw = clcr_names.get(rel) or rel
        return clean_registry_name(raw)
    raw = iso_ref_names.get(rel) or iso_alt_names.get(rel) or clcr_names.get(rel) or rel
    return clean_registry_name(raw)


def resolve_code(path):
    """Get the display code for a path."""
    rel = path.removeprefix("src/")
    if "/" in rel:
        code, script = rel.split("/", 1)
        return f"{code}/{script}"
    return rel


TYPE_LABELS = {
    "L": "Living",
    "H": "Historical",
    "E": "Extinct",
    "A": "Ancient",
    "C": "Constructed",
    "S": "Special",
}


def resolve_type(path, iso_types):
    """Resolve the language type from ISO 639-3 data."""
    code = code_from_path(path)
    if code.startswith("art-x-"):
        return "Constructed"
    t = iso_types.get(code, "")
    return TYPE_LABELS.get(t, "")


def linkify_contributors(contributors):
    """Turn @handle into [&#64;handle](https://github.com/handle)."""
    if not contributors:
        return ""
    parts = [c.strip() for c in contributors.split(",")]
    linked = []
    for part in parts:
        if part.startswith("@"):
            handle = part[1:]
            linked.append(f"[@{handle}](https://github.com/{handle})")
        else:
            linked.append(part)
    return ", ".join(linked)


BADGE_COLORS = {
    "Living": "green",
    "Historical": "orange",
    "Ancient": "red",
    "Extinct": "black",
    "Constructed": "blue",
}


def generate_badges(entries, iso_types):
    """Generate one shields.io badge per language type, deduplicating by code."""
    seen = set()
    counts = {}
    for path, _ in entries:
        code = code_from_path(path)
        if code in seen:
            continue
        seen.add(code)
        t = resolve_type(path, iso_types) or "Unknown"
        counts[t] = counts.get(t, 0) + 1

    badges = []
    for t in ["Living", "Historical", "Ancient", "Extinct", "Constructed"]:
        n = counts.get(t, 0)
        color = BADGE_COLORS.get(t, "lightgray")
        label = f"{t} languages"
        badge_label = label.replace(" ", "_").replace("-", "--")
        badges.append(f"[![{label}](https://img.shields.io/badge/{badge_label}-{n}-{color})](INDEX.md)")
    return " ".join(badges)


def generate_table(entries, iso_ref_names, iso_alt_names, iso_types, clcr_names):
    """Generate a single markdown table sorted by code."""
    entries.sort(key=lambda e: e[0])
    lines = [
        "| Code | Language | Type | Contributors |",
        "| --- | --- | --- | --- |",
    ]
    for path, contributors in entries:
        code = resolve_code(path)
        file_path = path + ".tex" if "/" not in path.removeprefix("src/") or path.count("/") == 2 else path + ".tex"
        code_link = f"[`{code}`]({file_path})"
        name = resolve_name(path, iso_ref_names, iso_alt_names, clcr_names)
        lang_type = resolve_type(path, iso_types)
        contrib_linked = linkify_contributors(contributors)
        lines.append(f"| {code_link} | {name} | {lang_type} | {contrib_linked} |")
    return "\n".join(lines)


def update_readme(badges):
    """Update README.md badges."""
    text = README.read_text()

    # Match any line that's only shields.io badges (possibly wrapped in links)
    badge_re = re.compile(r"^(?:\[?!\[[^\]]*\]\(https://img\.shields\.io/badge/[^\)]+\)[^\n]*)+$", re.MULTILINE)
    if badge_re.search(text):
        text = badge_re.sub(badges, text)
    else:
        # Insert after the main header line
        text = re.sub(r"(^# [^\n]+\n)", rf"\1\n{badges}\n", text)

    README.write_text(text)


def update_index(table):
    """Write INDEX.md with the language listing."""
    INDEX.write_text(f"# Languages\n\n{table}\n")


def main():
    print("Fetching ISO 639-3 name index...")
    iso_alt_names = fetch_iso_names()
    print(f"  {len(iso_alt_names)} names loaded.")

    print("Fetching ISO 639-3 code table...")
    iso_ref_names, iso_types = fetch_iso_main()
    print(f"  {len(iso_types)} entries loaded.")

    print("Fetching CLCR registry...")
    clcr_names = fetch_clcr()
    print(f"  {len(clcr_names)} codes loaded.")

    sections = parse_sections()

    entries = []
    for _, paths in sections:
        for path in paths:
            contributors, is_stub = parse_contributors(path)
            if not is_stub:
                entries.append((path, contributors))

    badges = generate_badges(entries, iso_types)
    table = generate_table(entries, iso_ref_names, iso_alt_names, iso_types, clcr_names)
    update_readme(badges)
    update_index(table)

    n_total = len(entries)
    n_constructed = sum(1 for p, _ in entries if resolve_type(p, iso_types) == "Constructed")
    n_natural = n_total - n_constructed
    print(f"Natural: {n_natural}, Constructed: {n_constructed}, Total: {n_total}")
    print("README.md and INDEX.md updated.")


if __name__ == "__main__":
    main()
