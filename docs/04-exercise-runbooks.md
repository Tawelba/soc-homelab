# Safe exercise runbooks

Every run starts with the checklist in `00-scope-safety.md` and ends by removing temporary access and restoring a clean state when appropriate.

## Exercise 1 — Failed Windows logons

**Objective:** validate Windows authentication telemetry and alert triage.

1. Create a disposable local user on `win11-01` and document the start time.
2. At the console, attempt several incorrect passwords at a slow manual pace.
3. Log in successfully, confirm the activity in Wazuh, and correlate relevant events.
4. Record the account, endpoint, event timestamps, rule, and why the activity was benign.
5. Remove the disposable account.

**Success:** evidence shows failures and success in sequence, without exposing a password or real username.

## Exercise 2 — Linux file integrity

**Objective:** confirm that an approved directory change is visible.

1. Configure file-integrity monitoring for a dedicated path such as `/opt/lab-fim`.
2. Create, modify, rename, and delete a harmless text file.
3. Find each event and compare recorded metadata.
4. Explain any delay and the difference between scheduled and real-time monitoring.

**Success:** all four operations are accounted for and the monitored scope is intentionally narrow.

## Exercise 3 — Internal scan detection

**Objective:** correlate a permitted Kali scan with firewall and endpoint evidence.

1. Approve one target and a small port range.
2. Add a temporary OPNsense rule from `kali-01` to that target/range with logging enabled.
3. Run a low-rate version-detection scan only against the approved IP and ports.
4. Compare Kali output, OPNsense logs, target logs, and Wazuh alerts.
5. Delete the temporary rule and prove access is blocked again.

**Success:** the timeline identifies source, destination, ports, policy change, detection result, and rollback.

## Exercise 4 — Service interruption

**Objective:** practice operational response without causing damage.

1. Select a non-critical test web service on `ubuntu-01`.
2. Record health, stop the service, wait only long enough to observe telemetry, and restart it.
3. Triage the alert and write a short root-cause statement.

**Success:** downtime is bounded, service recovery is verified, and monitoring captured both stop and start.

## Exercise 5 — EICAR handling

Use the industry-standard EICAR anti-malware test string only from its official source and only inside the Windows lab VM. It is not malware, but endpoint tools intentionally treat it like a threat. Do not disable host protection or transfer the file through shared folders.

**Success:** prevention/quarantine and Wazuh telemetry are documented, then the VM is returned to a clean state.

## Experiment record

For every exercise, copy `templates/daily-lab-log.md` and include:

- hypothesis and expected signals;
- exact scope and temporary rule;
- sanitized commands or UI actions;
- observations from at least two sources;
- result, limitation, cleanup, and next step.
