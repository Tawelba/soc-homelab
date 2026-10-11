# Scope, ethics, and safety

## Charter

The lab exists to develop entry-level cybersecurity engineering and SOC skills in a controlled environment. It is designed for defensive monitoring, system administration, detection validation, and incident-response practice. It is not a platform for attacking public systems.

## In scope

- OPNsense firewall policy, DHCP, DNS, and network logs
- A Windows evaluation VM used as an employee-style endpoint
- An Ubuntu Server VM used as an internal application target
- A Wazuh all-in-one deployment and endpoint agents
- A Kali VM used only to generate approved lab telemetry
- Benign tests such as failed logons, port scans within the lab, service changes, file-integrity events, and EICAR test-file handling

## Out of scope

- Home-router changes, public port forwarding, or exposure of vulnerable services
- Testing neighbors, employers, schools, cloud accounts, or internet targets without authorization
- Persistence outside disposable VMs, destructive payloads, credential theft, phishing real users, or denial of service
- Collection or publication of real personal data

## Stop conditions

Immediately stop and investigate if:

- a target resolves to an address outside `10.10.0.0/16`;
- OPNsense logs show exercise traffic leaving its WAN interface;
- an internal VM receives a physical-LAN address;
- the host security product alerts on an unexpected artifact;
- a snapshot or backup cannot be restored as expected.

## Pre-exercise checklist

- [ ] Target and source are identified by lab name and lab IP.
- [ ] Written objective and expected alert are recorded.
- [ ] Required firewall rule is narrow and temporary.
- [ ] Clean snapshots exist and are labeled.
- [ ] No shared clipboard/folders are required for the exercise.
- [ ] A rollback method is known.

## Evidence handling

Capture the minimum evidence needed to prove the result. Prefer a cropped alert, sanitized event fields, a short command excerpt, and a written conclusion. Store raw material under the ignored `evidence/raw/` path, then create a redacted copy for version control.
