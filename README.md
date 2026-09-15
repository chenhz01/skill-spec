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

## The five checks

1. **Frontmatter** — `SKILL.md` exists and declares `name` / `description`.
2. **Spec present** — `SPEC.md` exists (warn if missing; the whole point is fixing that).
3. **Six sections** — Purpose, Interface, Procedure, Acceptance, Guards, Honest limits all present.
4. **Falsifiable acceptance** — the Acceptance section contains checkable assertions (`[ ]` checkboxes, quantified thresholds, `N/N` coverage statements). "Works well" fails; "6/6 directories scanned, totals match `du -sh`" passes.
5. **Honest limits declared** — the skill states what it cannot do and the evidence status of its claims.

## Authorship

Produced through human-AI collaboration: the template and linter were drafted by an AI coding agent during a real internal migration — retrofitting a large legacy skill collection with specs, one at a time, starting with a production scouting skill — then reviewed, edited, and approved by a human maintainer. The linter shipped only after its own fixtures (pass / fail / warn / strict) all behaved as specified.

## License

MIT — use it, fork it, wire it into your CI. Attribution appreciated, not required.

<a href="https://github.com/chenhz01/skill-spec">canary: CANARY-ZS-SP-20260915-3F7C21A9</a>
