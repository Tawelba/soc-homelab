# Project governance

## Milestones

| Milestone | Exit criteria | Status |
|---|---|---|
| M0 Design | Scope, topology, IP plan, safety policy, and capacity decision reviewed | Validated |
| M1 Network | OPNsense and isolated zones pass connectivity matrix | Planned |
| M2 Visibility | Wazuh and two agents survive reboot and report expected events | Planned |
| M3 Detections | Six use cases pass positive and negative tests | Planned |
| M4 Response | Two incident exercises and one restore test completed | Planned |
| M5 Portfolio | Sanitized case studies pass peer and repository review | Planned |

Update this table only when the linked evidence exists.

## Decision log

| ID | Decision | Reason | Revisit trigger |
|---|---|---|---|
| ADR-001 | VirtualBox for the first release | Lowest entry cost on a desktop | Dedicated hardware acquired |
| ADR-002 | OPNsense NAT WAN; no bridging | Containment over convenience | Never for vulnerable targets |
| ADR-003 | Wazuh all-in-one | Fits beginner operations and small scale | Resource or availability needs grow |
| ADR-004 | Defer Active Directory | Keep first build understandable | Core milestones complete |

## Risk register

| Risk | Likelihood | Impact | Control |
|---|---|---|---|
| Lab traffic reaches unintended network | Low | High | NAT-only WAN, internal networks, stop conditions |
| Host resources are exhausted | Medium | Medium | Capacity profile, staged VM operation, disk checks |
| Secrets enter Git history | Medium | High | `.gitignore`, repository scan, manual review, rotation plan |
| Tool updates invalidate steps | Medium | Medium | Link current vendor docs and record versions/dates |
| Snapshots are mistaken for backups | Medium | Medium | Separate configs/docs and perform restore tests |
| Portfolio overstates progress | Medium | Medium | Status vocabulary and evidence-linked milestone gates |

## Change control

Use the change template for firewall policy, agent configuration, new services, logging scope, and resource allocation. Low-risk documentation corrections can be committed directly but still require link and repository validation.
