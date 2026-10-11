# Operations and troubleshooting

## Start and stop order

Start: `fw01` → `siem01` → endpoint needed for the session → `kali-01` only when required.

Stop: finish evidence and cleanup → `kali-01` → endpoints → `siem01` → `fw01`. Use guest shutdown, not forced power-off, unless testing failure recovery.

## Before every session

- Confirm host disk and memory headroom.
- On the storage-saver profile, do not start the lab with less than 20 GB of host free space.
- Confirm `fw01` interfaces and system time.
- Confirm Wazuh services and agent health.
- Re-read the exercise scope and expected alerts.
- Confirm clean snapshots and raw evidence location.

## Weekly maintenance

- Apply updates in a documented window and snapshot only after validation.
- Review firewall rules, temporary exceptions, blocked traffic, and admin access.
- Check Wazuh index/disk utilization and agent last-seen status.
- Remove obsolete snapshots and downloaded installers only after confirming they are replaceable; never delete VM files manually while VirtualBox owns them.
- Review time synchronization on every VM.
- Export a sanitized configuration inventory and test one evidence link.

## Troubleshooting sequence

Use layers and change one variable at a time:

1. **Power/resource:** VM running, RAM/disk available, no paused state.
2. **Link:** correct named internal adapter, adapter enabled, expected virtual NIC.
3. **Address:** IP, prefix, gateway, and DNS match the address plan.
4. **Route/policy:** OPNsense route and rule exist; inspect deny logs.
5. **Service:** process listening on expected interface/port; host firewall permits it.
6. **Application:** credentials, certificate, configuration, and application logs.
7. **Telemetry:** endpoint produced event, agent read it, manager received it, rule matched it.

## Common failures

| Symptom | Likely cause | Safe check |
|---|---|---|
| VM gets a home-router address | Bridged adapter selected | Power off and correct adapter before continuing |
| Internet works but zones cannot communicate | Expected deny policy or missing narrow rule | Inspect live firewall log by source/destination |
| Agent is disconnected | time, DNS/IP, service, or blocked telemetry port | Check clock, service health, then exact flow |
| Dashboard unavailable | resource pressure or component failure | Check VM resources and service logs locally |
| No alert after test | missing data, wrong field, rule threshold, or delay | Trace endpoint event through the pipeline |
| Snapshot restore breaks identity | duplicate/stale agent enrollment | Document re-enrollment and update the baseline |

## Recovery priorities

1. Preserve documentation and sanitized configurations.
2. Restore network containment.
3. Restore OPNsense and Wazuh.
4. Rebuild endpoints from official media if integrity is uncertain.
5. Revalidate every acceptance test before resuming exercises.

Never weaken the home computer's security controls to make the lab work. If host protection objects, isolate the cause and redesign the exercise.
