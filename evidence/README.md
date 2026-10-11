# Evidence index

Only sanitized, portfolio-safe evidence belongs in version control. Keep originals in `evidence/raw/`, which Git ignores.

Use this naming convention:

`YYYY-MM-DD_<exercise-or-change-id>_<artifact>.<ext>`

Example: `2026-07-20_DET-001_failed-logon-alert.png`

For each committed artifact, link it from a daily log, change record, detection record, or incident report. Crop to the relevant fields and redact personal data, tokens, addresses outside the documented lab ranges, MAC addresses, and browser/UI clutter. Prefer text or JSON excerpts where they are easier to audit than screenshots.

## Current acceptance records

- [NET-001 — LAN firewall acceptance](2026-07-15_NET-001_lan-firewall-acceptance.md)
- [NET-002 — admin01 update path](2026-07-15_NET-002_admin01-update-path.md)
- [NET-003 — DMZ minimum-access firewall acceptance](2026-07-29_NET-003_dmz-minimum-access.md)
- [DET-001 — Failed SSH login detection](2026-07-31_DET-001_failed-ssh-login.md)
- [KALI-001 - Kali installer ISO verification](2026-07-31_KALI-001_iso-verification.md)
- [KALI-002 — Kali baseline acceptance](2026-07-31_KALI-002_baseline-acceptance.md)
