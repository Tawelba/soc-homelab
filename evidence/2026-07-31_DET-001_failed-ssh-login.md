# DET-001 — Failed SSH login detection

**Exercise date:** 2026-07-31  
**Dashboard timestamp:** `Jul 31, 2026 @ 00:54:22.410`  
**Status:** Validated  
**Environment:** Authorized, isolated home lab

## Executive summary

A single controlled SSH login attempt used a deliberately nonexistent account from the management workstation `admin01` against the DMZ server `ubuntu-01`. The Wazuh agent on `ubuntu-01` collected the authentication event and sent it to `siem01`, where the default ruleset generated authentication-failure alerts. The reviewed alert identified the correct endpoint, source address, attempted username, and SSH behavior. No valid account was used or compromised, and no containment action was required. The exercise validates the lab's endpoint-to-SIEM detection path.

## Objective and authorization

Validate that Wazuh detects and presents a failed SSH authentication event from a monitored Linux server without performing password guessing or sustained brute-force activity.

The test was limited to lab systems owned by the operator:

| Asset | Role | Address |
|---|---|---|
| `admin01` | Authorized test source and management workstation | `10.10.10.50` |
| `ubuntu-01` | Monitored DMZ target | `10.10.20.10` |
| `siem01` | Wazuh manager, indexer, and dashboard | `10.10.10.10` |

## Test procedure

From `admin01`, the operator initiated one SSH connection using the nonexistent account `invaliduser`:

```bash
ssh invaliduser@10.10.20.10
```

One dummy password was submitted. The attempt was stopped after the first `Permission denied` response. No real credential was entered, and the test was not repeated.

## Alert evidence

Wazuh Threat Hunting displayed three authentication-failure alerts associated with the controlled attempt. The most recent reviewed event contained:

| Field | Observed value |
|---|---|
| Timestamp | `Jul 31, 2026 @ 00:54:22.410` |
| Agent | `ubuntu-01` |
| Rule ID | `5710` |
| Wazuh rule level | `5` |
| Rule description | `sshd: Attempt to login using a non-existent user` |
| Source IP | `10.10.10.50` |
| Source user | `invaliduser` |
| Authentication-failure alert count | `3` |

The Wazuh rule level describes the alert's detection priority; it is not, by itself, the incident severity assigned by the analyst.

## Analysis

### Facts

- The source address matches `admin01`, the authorized management workstation.
- The destination agent is `ubuntu-01`, the intended monitored endpoint.
- The attempted username matches the deliberately nonexistent test account.
- Rule 5710 describes the exact behavior performed during the exercise.
- The dashboard received the event through the approved Wazuh TCP 1514–1515 path.

### Assessment

The alert is a true positive for failed SSH authentication and a benign positive in operational context because the activity was planned and authorized. Confidence is high because the time, source, target, username, and rule description agree with the test procedure.

This single attempt must not be characterized as a brute-force attack. A production analyst would look for repetition, multiple usernames, unusual source systems, successful logins after failures, or activity outside an approved change window before escalating.

## Response decision

| Decision area | Outcome |
|---|---|
| Analyst severity | Low — authorized validation activity |
| Confidence | High |
| Containment | Not required |
| Credential reset | Not required; no real credential was used |
| Endpoint recovery | Not required |
| Final disposition | Benign positive / detection validated |

## Validation result

```text
Controlled action
  -> ubuntu-01 SSH authentication log
  -> Wazuh agent collection
  -> encrypted agent communication to siem01
  -> Wazuh rule 5710
  -> visible Threat Hunting alert
```

**Result: Pass.** The lab detected the intended event and exposed sufficient fields for basic triage and attribution.

## Limitations and next improvements

- This exercise validated one default rule, not correlation for repeated failures.
- No screenshot is included yet; any future screenshot must exclude credentials, cookies, unrelated browser content, and non-lab addresses.
- A later exercise should test repeated failures from the isolated ATTACK network and compare single-event detection with threshold-based correlation.
- Alert retention must be tuned to the storage-conscious capacity plan before generating higher event volumes.

