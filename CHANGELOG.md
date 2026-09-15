# Changelog

All notable changes to skill-spec. Small, regular releases.

## [0.2.0] - 2026-09-16

- Added `tools/spec_gen.py`: SPEC.md draft generator (DRAFT-flagged, TODO-marked, never overwrites existing specs, `--dry-run` backlog mode)
- Bilingual section headers (English / Chinese) in `spec_lint.py`, promoted from dogfooding
- New regression fixture: bilingual-skill (Chinese headers)
- Dogfood release: 482-skill scan, 3 real bugs found and fixed (CN headers, capture-group truncation, header variant)

## [0.1.0] - 2026-09-15

- Initial release: six-section SPEC template + zero-dependency spec_lint.py (5 checks, fixtures verified) + worked example + MIT
