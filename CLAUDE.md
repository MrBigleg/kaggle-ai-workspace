# 001_Kaggle — Project Workspace

Scaffolding ground for experiments and agents. Several projects here touch **OKF** (Open Knowledge Format), so this file points to where to learn it. The reference material is **contained in this folder** (`_okf-reference/`) so it works with nothing else mounted.

## Learn OKF (Open Knowledge Format)

OKF v0.1 is an open, vendor-neutral format for representing knowledge: a directory of Markdown files with YAML frontmatter, cross-linked, git-friendly. The only hard rule for a conformant document is a non-empty `type` field in its frontmatter. No schema registry, no required tooling — if you can `cat` a file you can read it.

### Where to read up (all local unless noted)

| Resource | Location | Use it for |
|----------|----------|------------|
| **Condensed spec + conformance check** | `_okf-reference/okf-spec-summary.md` | Read this first. Quick reference + a ready-to-run Python validator. |
| **Reference producer** | `_okf-reference/export_okf.py` | A working OKF bundle generator (select → rewrite links → normalise frontmatter → index/log). Study the structure; the selection presets assume an Obsidian vault. |
| **Reference consumer** | `_okf-reference/viz_okf.py` | Renders any OKF bundle to a self-contained interactive `viz.html`. Source-agnostic — runs on any bundle. |
| Official spec (v0.1) | https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf (`SPEC.md`) | The authoritative upstream definition. |
| Community tooling | https://github.com/xSAVIKx/okf-skills | Connectors, MCP server, enrichment guidance, `okf-viz`. |

### Conformance essentials (the short version)

A bundle is a directory tree of `.md` files. To be OKF v0.1 conformant:

1. Every non-reserved `.md` has a parseable YAML frontmatter block with a non-empty `type`.
2. Reserved filenames: `index.md` (directory listing, no frontmatter — except the bundle-root `index.md` may carry only `okf_version: "0.1"`) and `log.md` (update history).
3. Cross-links are standard markdown, bundle-relative preferred: `[text](/path/to/concept.md)`.
4. Recommended frontmatter beyond `type`: `title`, `description`, `resource`, `tags`, `timestamp` (ISO-8601). Producers may add any extra keys; consumers must tolerate unknown keys, types, and broken links.

### Validate a bundle

```bash
# edit the bundle path inside the snippet, then:
python3 -c "$(sed -n '/^```python/,/^```/p' _okf-reference/okf-spec-summary.md | sed '1d;$d')"
```

Or copy the Python block from `_okf-reference/okf-spec-summary.md`. It must print `CONFORMANT v0.1: True`.

> Requires Python 3 + PyYAML (`pip install pyyaml --break-system-packages`).
