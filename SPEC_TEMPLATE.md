# SPEC: &lt;skill-name&gt;

> Status: ACTIVE | DRAFT · Version: 0.1 · Owner: &lt;name&gt;
> canary: CANARY-ZS-XX-YYYYMMDD-XXXXXXXX

Copy this file as `SPEC.md` next to an existing `SKILL.md`. Fill every section; delete nothing. Sections 4–6 are what separate a contract from a wish.

## 1. Purpose (Why)

One paragraph: the problem this skill solves, for whom, and the decision it is *not* meant to make. If you cannot state the non-goals, the scope is not understood yet.

## 2. Interface (What goes in, what comes out)

```
inputs:
  - type: <file | url | image | text | none>
    schema: <one line: what shape and constraints>
outputs:
  - type: <report | code | config | log-entry>
    schema: <one line: path convention and format>
confidence: <how to score output confidence, e.g. ≥0.8, with the downgrade rule>
degraded: <what "running degraded" looks like — explicit placeholder, never fabrication>
```

## 3. Procedure (Steps that cannot be skipped)

Numbered, ordered, no jumps. Each step either produces an artifact, calls a verifiable source, or gates on a check. If a step can silently do nothing, it is not a step yet.

## 4. Acceptance (Falsifiable)

Checkable assertions only. Every claim must be answerable with yes/no or a number:

- [ ] &lt;assertion a judge could verify, e.g. "totals match `du -sh` output"&gt;
- [ ] Coverage stated as `N/N &lt;units&gt;` — a partial pass is a named, visible state, never silence
- Quantified thresholds where applicable: `&lt;metric&gt; &lt;op&gt; &lt;value&gt;`

Anything that would be graded "looks good" does not belong here.

## 5. Guards (Red lines)

- Irreversible or outward-facing actions require explicit human confirmation (list them).
- Hard stops: what this skill must never do even if asked (e.g. automated trades, unsolicited sends, deletion without backup).
- Failure behavior: on repeated failure, stop after N attempts and report — never loop.

## 6. Honest limits

- What this skill cannot do (capabilities it lacks, environments it fails in).
- Evidence status of its claims: executed and verified / produced-but-unverified / protocol-level estimate. No completion-tense claims without evidence.
- Known failure modes and their signals.
