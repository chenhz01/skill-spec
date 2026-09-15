#!/usr/bin/env python3
"""spec_gen.py — draft SPEC.md files for skills that lack one.

Reads a skill's SKILL.md (frontmatter, description, structure) and generates a
six-section SPEC.md draft. Every draft is marked DRAFT and carries TODO markers:
a draft is a starting point for human judgment, never a finished contract.

Usage:
    python spec_gen.py <skill-dir>                  # write SPEC.md next to SKILL.md
    python spec_gen.py <skill-dir> --out <dir>      # write the draft elsewhere (safe preview)
    python spec_gen.py <collection-dir> --dry-run   # list skills missing SPEC.md (writes nothing)
    python spec_gen.py <collection-dir> --out <dir> # batch drafts into one output dir

Safety: never overwrites an existing SPEC.md (skip with a note; --force to override).
Zero dependencies. No network calls.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
HEADER_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def parse_skill(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm = FRONTMATTER_RE.match(text)
    name = desc = ""
    if fm:
        block = fm.group(1)
        m = re.search(r"^name\s*:\s*(.+)$", block, re.MULTILINE)
        name = m.group(1).strip().strip("\"'") if m else ""
        m = re.search(r"^description\s*:\s*(.+)$", block, re.MULTILINE)
        desc = m.group(1).strip().strip("\"'") if m else ""
    if not name:
        name = skill_md.parent.name
    # first markdown H1 as fallback context
    h1 = HEADER_RE.search(text[fm.end():] if fm else text)
    title = h1.group(1).strip() if h1 else name
    # headings inventory (structure hints for the human filling TODOs)
    headings = re.findall(r"^##\s+(.+)$", text[fm.end():] if fm else text, re.MULTILINE)
    return {"name": name, "description": desc, "title": title, "headings": headings[:12]}


def first_sentence(text: str) -> str:
    m = re.search(r"^(.{10,}?[.。!!?？])\s", text + " ")
    return m.group(1).strip() if m else text.strip()


def draft_spec(info: dict) -> str:
    purpose = first_sentence(info["description"]) if info["description"] else "TODO: one paragraph — the problem this skill solves, for whom, and what it is NOT for."
    headings_list = "\n".join(f"  - {h}" for h in info["headings"]) or "  - TODO: none detected"
    today = date.today().isoformat()
    return f"""# SPEC: {info['name']}

> Status: DRAFT (auto-generated {today} by spec-gen — human review required before removing this banner) · Version: 0.0-draft
> Source of truth for behavior: SKILL.md ("{info['title']}")
> canary: TODO

## 1. Purpose (Why)

{purpose}

Non-goals: TODO — state what this skill must not be used for.

## 2. Interface (What goes in, what comes out)

```
inputs:
  - type: TODO  # e.g. text | file | url | none
    schema: TODO
outputs:
  - type: TODO  # e.g. report | code change | log entry
    schema: TODO
confidence: TODO  # how output confidence is scored, and the downgrade rule
degraded: TODO    # what "running degraded" looks like — explicit placeholder, never fabrication
```

Detected SKILL.md structure (hints for filling this in):
{headings_list}

## 3. Procedure (Steps that cannot be skipped)

1. TODO — numbered, ordered, no jumps; each step produces an artifact, calls a verifiable source, or gates on a check.

## 4. Acceptance (Falsifiable)

- [ ] TODO — every assertion must be answerable with yes/no or a number
- [ ] TODO — coverage stated as `N/N <units>`; partial pass is a named, visible state
- Quantified thresholds where applicable: `<metric> <op> <value>`

## 5. Guards (Red lines)

- Irreversible or outward-facing actions (TODO: list them) require explicit human confirmation.
- Must never: TODO — hard stops for this skill.
- On repeated failure: stop after 3 attempts and report — never loop.

## 6. Honest limits

- Cannot: TODO — capabilities it lacks, environments it fails in.
- Evidence status: TODO — executed and verified / produced-but-unverified / protocol-level estimate.
- Known failure modes: TODO.
"""


def sanitize(text: str) -> str:
    """Strip control characters that crash Windows console writes."""
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u2028\u2029\ufeff]", "", text)


def main() -> int:
    # Windows console / pipe writes can raise OSError 22 on unencodable
    # characters; replace instead of crash.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description="draft SPEC.md files for skills lacking one")
    ap.add_argument("path", type=Path, help="a skill directory or a collection directory")
    ap.add_argument("--out", type=Path, help="write drafts here instead of next to each SKILL.md (safe preview)")
    ap.add_argument("--dry-run", action="store_true", help="list skills missing SPEC.md; write nothing")
    ap.add_argument("--force", action="store_true", help="overwrite existing SPEC.md (default: never)")
    args = ap.parse_args()

    if not args.path.exists():
        print(f"error: path not found: {args.path}", file=sys.stderr)
        return 1

    root = args.path
    skill_dirs = [root] if (root / "SKILL.md").exists() else sorted(p.parent for p in root.rglob("SKILL.md"))
    if not skill_dirs:
        print(f"no SKILL.md found under {root}")
        return 1

    missing = [d for d in skill_dirs if not (d / "SPEC.md").exists()]
    if args.dry_run:
        print(f"dry-run: {len(missing)}/{len(skill_dirs)} skill(s) missing SPEC.md")
        for d in missing:
            info = parse_skill(d / "SKILL.md")
            print(f"  - {d.name}: {sanitize(info['description'])[:70] or sanitize(info['title'])[:70]}")
        return 0

    written = skipped = 0
    for d in missing:
        info = parse_skill(d / "SKILL.md")
        content = draft_spec(info)
        target = (args.out / d.name / "SPEC.md") if args.out else (d / "SPEC.md")
        if target.exists() and not args.force:
            print(f"  SKIP {target} (exists)")
            skipped += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        print(f"  WROTE {target}")
        written += 1

    existing = len(skill_dirs) - len(missing)
    print(f"\nsummary: {written} draft(s) written, {skipped} skipped, "
          f"{existing} already had a SPEC.md (untouched)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
