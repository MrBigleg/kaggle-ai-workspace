# OKF v0.1 — condensed reference

Source: https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf (SPEC.md)
Community tooling: https://github.com/xSAVIKx/okf-skills

OKF is an open, vendor-neutral format for knowledge: a directory of Markdown files with YAML frontmatter. No schema registry, no required tooling. If you can `cat` a file you can read it; if you can `git clone` you can ship it.

## Terms

- **Bundle** — self-contained directory tree of concept docs. Unit of distribution.
- **Concept** — one markdown document = one unit of knowledge.
- **Concept ID** — the file path within the bundle minus `.md` (e.g. `concepts/local-seo.md` -> `concepts/local-seo`).

## Concept document

Frontmatter (`---` delimited YAML) + markdown body.

Frontmatter keys:
- `type` — **REQUIRED**, non-empty string. Not centrally registered; be descriptive. Consumers must tolerate unknown types.
- `title` — recommended display name.
- `description` — recommended one-line summary (used in index snippets / search).
- `resource` — optional canonical URI of the underlying asset (omit for abstract concepts).
- `tags` — optional list.
- `timestamp` — optional ISO-8601 last-modified.
- Producers MAY add any extra keys; consumers MUST preserve unknown keys and MUST NOT reject unknown ones.

Conventional body headings (use when applicable): `# Schema`, `# Examples`, `# Citations`.

## Cross-linking

- Standard markdown links. **Absolute (bundle-relative)** preferred: begin with `/`, e.g. `[customers](/tables/customers.md)`.
- A link asserts an untyped relationship; the prose conveys the kind.
- Consumers MUST tolerate broken links (may be not-yet-written knowledge).

## Reserved filenames (any level)

- `index.md` — directory listing for progressive disclosure. **No frontmatter**, EXCEPT the bundle-root `index.md` MAY carry a single `okf_version` key. Body is sections of `* [Title](url) - description` bullets.
- `log.md` — optional chronological update history, newest first, ISO date headings.

These two names MUST NOT be used for concept documents.

## Conformance (v0.1)

A bundle is conformant if:
1. Every non-reserved `.md` has a parseable YAML frontmatter block.
2. Every frontmatter block has a non-empty `type`.
3. `index.md` / `log.md` follow their structures when present.

Consumers treat everything else as soft guidance and MUST NOT reject a bundle for: missing optional fields, unknown `type` values, unknown extra keys, broken cross-links, or missing `index.md`.

Bundles MAY declare `okf_version: "0.1"` in the root `index.md` frontmatter (the only place frontmatter is allowed in an index).

## Verification snippet

Run from vault root, pointing `B` at the bundle. Must print `CONFORMANT v0.1: True`.

```python
import re, yaml
from pathlib import Path
B = Path("okf/local-seo-gbp")
FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
RESERVED = {"index.md", "log.md"}
ids = {str(p.relative_to(B).with_suffix("")).replace("\\","/")
       for p in B.rglob("*.md") if p.name not in RESERVED}
fail_fm=[]; fail_type=[]; idx_fm=[]; root_ok=False; broken=0; resid=0
LINK=re.compile(r"\]\((/[^)]+\.md)\)")
for p in sorted(B.rglob("*.md")):
    rel=str(p.relative_to(B)).replace("\\","/"); txt=p.read_text(encoding="utf-8")
    resid += len(re.findall(r"\[\[", txt))
    if p.name=="index.md":
        m=FM.match(txt)
        if m and rel=="index.md":
            root_ok = list((yaml.safe_load(m.group(1)) or {}).keys())==["okf_version"]
        elif m: idx_fm.append(rel)
        continue
    if p.name=="log.md": continue
    m=FM.match(txt)
    if not m: fail_fm.append(rel); continue
    try: fm=yaml.safe_load(m.group(1)) or {}
    except Exception: fail_fm.append(rel); continue
    if not str(fm.get("type","")).strip(): fail_type.append(rel)
    for mm in LINK.finditer(txt):
        if mm.group(1).lstrip("/")[:-3] not in ids: broken+=1
ok = not fail_fm and not fail_type and not idx_fm and root_ok and resid==0
print("fm_fail",fail_fm[:3],"type_fail",fail_type[:3],"idx_fm",idx_fm[:3])
print("root_ok",root_ok,"broken_inbundle",broken,"residual_wikilinks",resid)
print("CONFORMANT v0.1:", ok)
```
