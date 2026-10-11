# Monitoring and detection engineering

## Telemetry map

| Source | Minimum data | Questions it should answer |
|---|---|---|
| OPNsense | allowed/blocked connections, DHCP, DNS | Which zones communicated? What was denied? |
| Windows | Security log, Defender, PowerShell, Sysmon | Who logged on? What executed or changed? |
| Ubuntu | authentication, sudo, systemd, package and file-integrity events | Who administered the server? What changed? |
| Wazuh | agent status, rule alerts, vulnerability/configuration findings | Is coverage healthy? Which events require triage? |

## Detection-as-code workflow

For each detection:

1. State the threat behavior in plain language.
2. Identify the required data source and fields.
3. Generate one benign positive test.
4. Generate or observe a negative test.
5. Save the query/rule, result, timestamp, and screenshots.
6. Explain false positives and tuning choices.
7. Map to MITRE ATT&CK only after validating the behavior.

## Initial detection backlog

| ID | Use case | Test | Expected evidence |
|---|---|---|---|
| DET-001 | Repeated Windows authentication failures | Several wrong passwords on a lab account | Source, account, count, time window |
| DET-002 | New Windows local user | Create then remove a disposable user | Actor, target account, host |
| DET-003 | Suspicious PowerShell shape | Run a harmless encoded-string demonstration | Process command line and parent |
| DET-004 | Linux sudo authentication failure | Enter a wrong sudo password | User, host, result, timestamp |
| DET-005 | Monitored file changed | Edit a file in the designated test directory | Path, action, before/after metadata |
| DET-006 | Internal port scan | Scan only the approved target from Kali | Source, destination, ports, firewall evidence |
| DET-007 | Security service stopped | Stop and immediately restart a lab service | Service name, actor, duration |
| DET-008 | Agent stopped reporting | Shut down an endpoint during a planned window | Last seen, health status, recovery |

## Alert-triage method

Use the same sequence every time:

1. **Validate:** is the alert real, duplicated, or a parsing error?
2. **Scope:** which host, user, process, address, and time window are involved?
3. **Enrich:** compare endpoint, identity, and firewall evidence.
4. **Assess:** expected administration, benign anomaly, or suspicious activity?
5. **Contain:** in exercises, describe the least-disruptive response; do not improvise destructive action.
6. **Document:** create an incident report with evidence and confidence level.
7. **Improve:** tune the rule, logging, or runbook and retest.

## Coverage metrics

Track these weekly:

- agent reporting rate: active agents / expected agents;
- test success rate: detections producing the intended alert / detections tested;
- median triage time for exercises;
- false-positive notes resolved;
- systems with verified time synchronization;
- restore tests passed.

With only a few hosts, publish counts alongside percentages so metrics remain honest.
