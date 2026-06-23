#!/usr/bin/env python3
"""
export_okf.py - Export a slice of the claude-obsidian wiki as an OKF v0.1 bundle.

Open Knowledge Format (OKF) v0.1:
  https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf

1. SELECT  wiki pages by domain + tag (curated, local-SEO/GBP focused).
2. COPY    them into a bundle dir, slugifying paths, preserving subfolders.
3. REWRITE Obsidian [[wikilinks]] -> bundle-relative markdown links [text](/path.md).
4. NORMALISE frontmatter (keep type, ensure title/description, add ISO timestamp,
   strip Obsidian wikilink syntax from related/sources).
5. GENERATE clean index.md per directory (root carries okf_version: "0.1").
6. WRITE   a root log.md noting the generation.

Usage:
  python3 export_okf.py --vault . --out okf/local-seo-gbp
  python3 export_okf.py --vault . --out okf/local-seo-gbp --dry-run
  python3 export_okf.py --vault . --out /tmp/share/local-seo-gbp --preset local-seo
"""
from __future__ import annotations
import argparse, datetime as dt, re, shutil, sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml --break-system-packages")

PRESETS = {
    "local-seo": {
        "bundle_name": "Local SEO & Google Business Profile",
        "domains": {"local-seo"},
        "tags": {
            "gbp", "google-business-profile", "business-profile",
            "local-seo", "local",
            "google-maps", "maps", "google-maps-platform", "ask-maps",
            "rank-in-maps", "onemap", "oneverymap",
            "reviews", "review", "citation", "citations",
            "local-landing-page", "local-guides", "gbp-spam",
            "geo", "geospatial-ai", "multilingual-seo", "localized",
            "map-pack", "local-pack",
        },
    },
}

SCAN_DIRS = ["wiki"]
SKIP_BASENAMES = {"_index", "index", "log", "hot", "dashboard", "overview"}
KEEP_EXTERNAL_LINKS_AS_TEXT = True
OKF_VERSION = "0.1"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def slugify(name: str) -> str:
    name = name.strip().strip('"').strip().replace("&", "and")
    name = re.sub(r"[^\w\s/.-]", "", name)
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"-{2,}", "-", name)
    return name.lower().strip("-")


def slug_relpath(relpath: Path) -> Path:
    parts = list(relpath.parts)
    parts[-1] = slugify(parts[-1][:-3]) + ".md"
    parts[:-1] = [slugify(p) for p in parts[:-1]]
    return Path(*parts)


def split_frontmatter(text: str):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return (fm if isinstance(fm, dict) else {}), text[m.end():]


def norm_tag(t: str) -> str:
    t = str(t).strip().strip('"').strip()
    for pref in ("domain/", "source/"):
        if t.lower().startswith(pref):
            t = t[len(pref):]
    return t.lower()


def first_sentence(body: str) -> str:
    for line in body.splitlines():
        s = line.strip()
        if not s or s[0] in "#>|-*" or s.startswith("```"):
            continue
        s = WIKILINK_RE.sub(lambda m: m.group(1).split("|")[-1], s)
        s = re.sub(r"[*_`]", "", s)
        m = re.match(r"(.+?[.!?])(\s|$)", s)
        return (m.group(1) if m else s).strip()[:200]
    return ""


def to_iso(value) -> str:
    if isinstance(value, dt.datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(value, dt.date):
        return value.strftime("%Y-%m-%dT00:00:00Z")
    s = str(value).strip().strip('"')
    return s + "T00:00:00Z" if re.match(r"^\d{4}-\d{2}-\d{2}$", s) else s


@dataclass
class Doc:
    abspath: Path
    relpath: Path
    fm: dict
    body: str
    basename: str
    selected: bool = False
    out_rel: Path = field(default=None)


def load_docs(vault: Path):
    docs = []
    for d in SCAN_DIRS:
        for p in sorted((vault / d).rglob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            fm, body = split_frontmatter(text)
            docs.append(Doc(p, p.relative_to(vault), fm, body, p.stem))
    return docs


def is_selected(doc: Doc, preset: dict) -> bool:
    if doc.basename in SKIP_BASENAMES:
        return False
    if norm_tag(doc.fm.get("domain", "")) in preset["domains"]:
        return True
    tags = doc.fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    return any(norm_tag(t) in preset["tags"] for t in tags)


def build_link_index(docs):
    by_relstem, by_basename = {}, {}
    for d in docs:
        relstem = str(d.relpath.with_suffix("")).replace("\\", "/").lower()
        by_relstem[relstem] = d
        parts = relstem.split("/")
        if len(parts) > 1:
            by_relstem.setdefault("/".join(parts[1:]), d)
        by_basename.setdefault(d.basename.lower(), []).append(d)
    return by_relstem, by_basename


def resolve_wikilink(target, src, by_relstem, by_basename):
    target = target.strip().split("#")[0].strip()
    if not target or target.lower().endswith(".canvas"):
        return None
    key = target.replace("\\", "/").lower()
    if key.endswith(".md"):
        key = key[:-3]
    if key in by_relstem:
        return by_relstem[key]
    base = key.split("/")[-1]
    cands = by_basename.get(base, [])
    if not cands:
        return None
    if len(cands) == 1:
        return cands[0]
    sel = [c for c in cands if c.selected]
    if len(sel) == 1:
        return sel[0]
    pool = sel or cands
    src_top = src.relpath.parts[1] if len(src.relpath.parts) > 1 else ""
    same = [c for c in pool if (c.relpath.parts[1] if len(c.relpath.parts) > 1 else "") == src_top]
    return (same or pool)[0]


def rewrite_body(doc, by_relstem, by_basename):
    def repl(m):
        target, _, alias = m.group(1).partition("|")
        display = alias.strip() or target.strip().split("/")[-1].split("#")[0].strip()
        tgt = resolve_wikilink(target, doc, by_relstem, by_basename)
        if tgt and tgt.selected and tgt.out_rel is not None:
            return f"[{display}](/{str(tgt.out_rel).replace(chr(92), '/')})"
        return display if KEEP_EXTERNAL_LINKS_AS_TEXT else f"[{display}]"
    return WIKILINK_RE.sub(repl, doc.body)


def _clean_fm_value(val, doc, by_relstem, by_basename):
    if isinstance(val, list):
        return [_clean_fm_value(v, doc, by_relstem, by_basename) for v in val]
    if isinstance(val, dict):
        return {k: _clean_fm_value(v, doc, by_relstem, by_basename) for k, v in val.items()}
    if isinstance(val, str):
        def repl(m):
            target, _, alias = m.group(1).partition("|")
            display = alias.strip() or target.strip().split("/")[-1].split("#")[0].strip()
            tgt = resolve_wikilink(target, doc, by_relstem, by_basename)
            if tgt and tgt.selected and tgt.out_rel is not None:
                return "/" + str(tgt.out_rel).replace("\\", "/")
            return display
        return WIKILINK_RE.sub(repl, val)
    return val


def normalise_frontmatter(doc, by_relstem, by_basename):
    fm = dict(doc.fm)
    fm.setdefault("type", "Concept")
    if not fm.get("title"):
        fm["title"] = doc.basename
    if not fm.get("description"):
        snip = first_sentence(doc.body)
        if snip:
            fm["description"] = snip
    ts = fm.get("timestamp") or fm.get("updated") or fm.get("created")
    if ts:
        fm["timestamp"] = to_iso(ts)
    return _clean_fm_value(fm, doc, by_relstem, by_basename)


def dump_concept(fm, body):
    y = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False).strip()
    return f"---\n{y}\n---\n\n{body.lstrip()}"


def _count_in(dirrel, selected):
    return sum(1 for d in selected if str(d.out_rel).startswith(str(dirrel) + "/"))


def write_indexes(out, selected):
    by_dir = {}
    for d in selected:
        by_dir.setdefault(d.out_rel.parent, []).append(d)
    all_dirs = set(by_dir)
    for d in list(all_dirs):
        for parent in d.parents:
            all_dirs.add(parent)
    for dirrel in sorted(all_dirs, key=lambda p: str(p)):
        target_dir = out / dirrel
        target_dir.mkdir(parents=True, exist_ok=True)
        is_root = (dirrel == Path("."))
        lines = []
        if is_root:
            lines += ["---", f'okf_version: "{OKF_VERSION}"', "---", ""]
        title = "Local SEO & GBP - OKF Bundle" if is_root else dirrel.name.replace("-", " ").title()
        lines += [f"# {title}", ""]
        subdirs = sorted({p for p in all_dirs if p.parent == dirrel and p != dirrel})
        if subdirs:
            lines += ["## Sections", ""]
            for sd in subdirs:
                lines.append(f"* [{sd.name.replace('-', ' ').title()}]({sd.name}/) - {_count_in(sd, selected)} concepts")
            lines.append("")
        here = sorted(by_dir.get(dirrel, []), key=lambda d: str(d.out_rel))
        if here:
            lines += ["## Concepts", ""]
            for d in here:
                desc = d.fm.get("description", "")
                line = f"* [{d.fm.get('title', d.basename)}]({d.out_rel.name})"
                if desc:
                    line += f" - {desc}"
                lines.append(line)
            lines.append("")
        (target_dir / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_log(out, n, preset_name):
    today = dt.date.today().isoformat()
    txt = ("# Bundle Update Log\n\n"
           f"## {today}\n"
           f"* **Initialization**: Generated OKF v{OKF_VERSION} bundle from the claude-obsidian "
           f"wiki (preset `{preset_name}`), {n} concepts, via export_okf.py.\n")
    (out / "log.md").write_text(txt, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Export wiki slice as an OKF bundle.")
    ap.add_argument("--vault", default=".")
    ap.add_argument("--out", required=True)
    ap.add_argument("--preset", default="local-seo", choices=list(PRESETS))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    out = Path(args.out)
    if not out.is_absolute():
        out = vault / out
    preset = PRESETS[args.preset]

    docs = load_docs(vault)
    for d in docs:
        d.selected = is_selected(d, preset)
    selected = [d for d in docs if d.selected]

    for d in selected:
        rel = Path(*d.relpath.parts[1:]) if len(d.relpath.parts) > 1 else d.relpath
        d.out_rel = slug_relpath(rel)

    print(f"Preset: {args.preset}  |  scanned {len(docs)} docs  |  selected {len(selected)}")
    if args.dry_run:
        for d in sorted(selected, key=lambda d: str(d.out_rel)):
            print(f"  {d.relpath}  ->  {d.out_rel}")
        return

    # Overwrite-in-place; some mounts disallow deletion, so don't hard-fail on rmtree.
    try:
        if out.exists():
            shutil.rmtree(out)
    except (PermissionError, OSError):
        pass
    out.mkdir(parents=True, exist_ok=True)

    by_relstem, by_basename = build_link_index(docs)
    for d in selected:
        fm = normalise_frontmatter(d, by_relstem, by_basename)
        body = rewrite_body(d, by_relstem, by_basename)
        target = out / d.out_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(dump_concept(fm, body), encoding="utf-8")

    write_indexes(out, selected)
    write_log(out, len(selected), args.preset)
    print(f"Bundle written to: {out}")
    print(f"Concepts: {len(selected)}  |  directories: {len({d.out_rel.parent for d in selected})}")


if __name__ == "__main__":
    main()
