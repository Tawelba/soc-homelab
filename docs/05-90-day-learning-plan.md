# 90-day daily practice plan

## Daily cadence

Aim for 45–75 minutes. Spend 5 minutes stating the objective, 30–50 minutes doing the work, 10 minutes collecting evidence, and 5 minutes writing a reflection. On review days, fix documentation before adding new technology.

## Weeks 1–2: Foundations and design (days 1–14)

- Days 1–3: inventory host resources; learn virtualization, NAT, routing, and snapshots.
- Days 4–5: define scope, ethics, naming, addressing, and evidence rules.
- Days 6–9: install VirtualBox and OPNsense; build the three isolated networks.
- Days 10–12: create firewall objects, update rules, deny logs, and a network test matrix.
- Day 13: draw the as-built architecture and compare it with the design.
- Day 14: restore a snapshot, review notes, and publish a sanitized week-one summary.

**Deliverable:** architecture decision record, topology, IP plan, firewall matrix, and acceptance results.

## Weeks 3–4: Endpoints and hardening (days 15–28)

- Days 15–18: build and patch Windows; learn local accounts, services, firewall, and event logs.
- Days 19–21: build and patch Ubuntu; learn permissions, sudo, services, journal, and host firewall.
- Days 22–24: build Kali and prove default isolation.
- Days 25–26: establish clean snapshots and asset register.
- Day 27: review against CIS-style hardening concepts without blindly applying a benchmark.
- Day 28: run a recovery exercise and document gaps.

**Deliverable:** asset register, hardening checklist, recovery record, and revised diagram.

## Weeks 5–6: SIEM and telemetry (days 29–42)

- Days 29–32: install Wazuh, secure access, and understand its components.
- Days 33–35: enroll Windows, install Sysmon, and validate event flow.
- Days 36–38: enroll Ubuntu and validate auth, sudo, service, and FIM events.
- Days 39–40: add firewall logs or document a staged integration plan.
- Day 41: create a telemetry coverage matrix and health checks.
- Day 42: reboot each component and prove monitoring recovers.

**Deliverable:** telemetry map, agent-health evidence, event samples, and operations notes.

## Weeks 7–8: Detection engineering (days 43–56)

- Days 43–45: implement and test DET-001 and DET-002.
- Days 46–48: implement and test DET-004 and DET-005.
- Days 49–51: implement and test DET-006 with a narrow temporary rule.
- Days 52–53: test service-stop and agent-health use cases.
- Days 54–55: tune one noisy detection and document the tradeoff.
- Day 56: produce a coverage review with counts, gaps, and next priorities.

**Deliverable:** at least six validated detection records with positive/negative tests.

## Weeks 9–10: Incident response (days 57–70)

- Days 57–59: learn triage fields, severity, confidence, scope, and timelines.
- Days 60–62: investigate a failed-logon scenario and write IR-001.
- Days 63–65: investigate file/service changes and write IR-002.
- Days 66–67: correlate scan, firewall, endpoint, and SIEM records.
- Days 68–69: conduct a tabletop containment and recovery decision exercise.
- Day 70: review reports for evidence quality and unsupported claims.

**Deliverable:** two incident reports, one event timeline, and a lessons-learned note.

## Weeks 11–12: Engineering and automation (days 71–84)

- Days 71–73: use the readiness and repository-check scripts; improve error handling.
- Days 74–76: create a repeatable evidence-capture routine and checksum important artifacts.
- Days 77–79: back up sanitized configurations and test restoration.
- Days 80–82: review firewall rules, stale exceptions, agent health, and disk capacity.
- Days 83–84: write an operational runbook and monthly maintenance checklist.

**Deliverable:** repeatable checks, backup/restore evidence, and maintenance runbook.

## Days 85–90: Portfolio release

- Day 85: choose the three strongest stories: architecture, detection, and incident response.
- Day 86: turn each into a problem-action-evidence-result case study.
- Day 87: redact screenshots and replace unstable details with diagrams/tables.
- Day 88: ask a peer to follow one guide and record confusing steps.
- Day 89: fix gaps, run repository validation, and tag a release candidate.
- Day 90: publish the honest project status, lessons, limitations, and next roadmap.

**Deliverable:** sanitized repository, three case studies, skills matrix, and release notes.

## Weekly scorecard

| Measure | Target |
|---|---:|
| Practice sessions completed | 6 of 7 |
| New validated detection or control | 1+ |
| Recovery/negative test | 1 |
| Documentation updated | Every changed day |
| Unresolved critical safety issue | 0 |

Missing a day is not failure. Resume with the next numbered task and write what interrupted progress; reliability and honest reporting matter more than a perfect streak.
