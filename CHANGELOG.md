# Changelog

All notable changes to skill-spec. Small, regular releases.

## [0.4.0] - 2026-09-16

- Added `tools/spec_evidence.py`: per-run evidence black box — `gen` writes an unchecked acceptance checklist per execution, `check` exits 0 only when every item is ticked with real evidence
- Full-cycle acceptance verified: gen (6 items) → check 0/6 UNAUDITED (exit 1) → tick → check 6/6 AUDITED (exit 0)

## [0.3.0] - 2026-09-16

- Full-backlog dogfood run: 481 DRAFT specs generated in one pass (481/481 written, 0 existing specs touched); post-draft lint 482/482 pass
- `spec_gen.py`: Windows stdout hardening (`errors="replace"`) and control-character sanitize extended (`\x7f`, U+2028/U+2029, BOM)
- README Dogfooded section updated with batch-run results and the honest lint-green ≠ human-reviewed boundary

## [0.2.0] - 2026-09-16

- Added `tools/spec_gen.py`: SPEC.md draft generator (DRAFT-flagged, TODO-marked, never overwrites existing specs, `--dry-run` backlog mode)
- Bilingual section headers (English / Chinese) in `spec_lint.py`, promoted from dogfooding
- New regression fixture: bilingual-skill (Chinese headers)
- Dogfood release: 482-skill scan, 3 real bugs found and fixed (CN headers, capture-group truncation, header variant)

## [0.1.0] - 2026-09-15

- Initial release: six-section SPEC template + zero-dependency spec_lint.py (5 checks, fixtures verified) + worked example + MIT
