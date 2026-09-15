# skill-spec

**The spec-discipline layer for AI agent skills.** Your agent has skills. Do they have contracts?

A template + linter that turns any existing `SKILL.md` folder into a **falsifiable, auditable unit**: explicit input/output contract, numbered non-skippable procedure, acceptance criteria you can actually check, guard rails, and honest limits.

> [answer-contract](https://github.com/chenhz01/answer-contract) disciplines what your agent *answers*; skill-spec disciplines the *skills* it runs. Install both and the whole chain is covered.

## Why

Spec-first development proved itself at scale — [github/spec-kit](https://github.com/github/spec-kit) (130k+ stars) showed that specs beat vibes. [agent-skills](https://github.com/tech-leads-club/agent-skills) reported that **13.4% of marketplace skills have severe vulnerabilities** — most skill collections grow by accretion, and nobody can say what a given skill promises, what "done" means, or where its red lines are.

Existing solutions audit *new* skills entering a marketplace. **skill-spec is the upgrade path for the skills you already have** — the legacy folder, the orphaned script, the skill that "worked when I wrote it."

## What's in the box

| File | What it does |
|---|---|
| [`SPEC_TEMPLATE.md`](SPEC_TEMPLATE.md) | Six-section contract skeleton: Purpose · Interface · Procedure · Acceptance · Guards · Honest limits |
| [`tools/spec_lint.py`](tools/spec_lint.py) | Zero-dependency Python linter: scans skill folders, checks contract completeness and falsifiable acceptance criteria |
| [`tools/spec_gen.py`](tools/spec_gen.py) | Draft generator: writes a six-section SPEC.md draft (DRAFT-flagged, TODO-marked) from a skill's SKILL.md — a starting point for human judgment, never a finished contract |
| [`examples/`](examples/) | A fully worked, desensitized example spec |
| [`tests/`](tests/) | Three fixtures — pass / fail / warn — the linter's own acceptance test |

## Install (60 seconds)

Single file linter. Zero dependencies. No network calls, no telemetry.

```bash
git clone https://github.com/chenhz01/skill-spec.git
python skill-spec/tools/spec_lint.py path/to/your/skills/    # scan a collection
python skill-spec/tools/spec_lint.py path/to/one-skill/      # scan one skill
```

Exit code `0` = all contracts pass; `1` = at least one FAIL. Wire it into CI or a pre-commit hook.

## Add a spec to an existing skill (three steps)

1. Copy [`SPEC_TEMPLATE.md`](SPEC_TEMPLATE.md) next to the skill's `SKILL.md`, rename it `SPEC.md`.
2. Fill the six sections — the two that take real thought are **Acceptance** (every claim must be answerable with yes/no or a number) and **Honest limits** (what it can't do, stated plainly).
3. Run the linter. Fix every ❌. Ship when it's green — then re-run it whenever the skill changes.

A skill without a spec isn't wrong; it's unaudited. The linter tells you which one is which.

## Drafting specs at scale (v0.2.0)

481 skills missing specs is not a hand-writing job. `spec_gen.py` drafts them:

```bash
python skill-spec/tools/spec_gen.py path/to/skills/ --dry-run   # see the backlog, write nothing
python skill-spec/tools/spec_gen.py path/to/one-skill/          # write a DRAFT SPEC.md next to SKILL.md
```

Every draft is flagged `DRAFT` with TODO markers and never overwrites an existing SPEC.md. The draft fills in what can be inferred (name, description, structure hints); the human fills in what must be judged — acceptance criteria, red lines, honest limits. Draft → review → `spec_lint` green, in that order.

## The five checks

1. **Frontmatter** — `SKILL.md` exists and declares `name` / `description`.
2. **Spec present** — `SPEC.md` exists (warn if missing; the whole point is fixing that).
3. **Six sections** — Purpose, Interface, Procedure, Acceptance, Guards, Honest limits all present.
4. **Falsifiable acceptance** — the Acceptance section contains checkable assertions (`[ ]` checkboxes, quantified thresholds, `N/N` coverage statements). "Works well" fails; "6/6 directories scanned, totals match `du -sh`" passes.
5. **Honest limits declared** — the skill states what it cannot do and the evidence status of its claims.

## Authorship

Produced through human-AI collaboration: the template and linter were drafted by an AI coding agent during a real internal migration — retrofitting a legacy skill collection with specs, one at a time, starting with a production scouting skill — then reviewed, edited, and approved by a human maintainer.

## Dogfooded against 482 real skills

Before release, the linter ran against its own author's collection: **482 skills scanned, coverage 482/482** — 481 flagged for missing specs (that's the migration backlog, made visible in one command) and 1 with a complete spec. That first run caught **three real bugs** the fixtures had missed: Chinese section headers not recognized, a regex capture group truncating section bodies, and a header variant (`已知局限`) not matching. All three were fixed and promoted to regression fixtures — the pass / fail / warn / bilingual set in [`tests/`](tests/) is exactly that battle record.

Then the generator ran on the full backlog: **481 DRAFT specs written in one pass** (481/481 written, 0 existing specs touched). Re-lint after drafting: **482/482 pass, 0 warnings** — every skill in the collection now has a structurally complete contract. Honest boundary: lint-green means *structurally complete*, not *human-reviewed*; every draft carries a DRAFT banner requiring review before it counts as audited. Two more real defects were found and fixed during the batch run itself (a Windows console crash on unencodable characters, and a broken-pipe exit code when output is piped).

## License

MIT — use it, fork it, wire it into your CI. Attribution appreciated, not required.

<a href="https://github.com/chenhz01/skill-spec">canary: CANARY-ZS-SP-20260915-3F7C21A9</a>
