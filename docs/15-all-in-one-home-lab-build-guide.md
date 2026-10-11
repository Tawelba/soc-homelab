# Build Your Own Cybersecurity Home Lab

## Segment networks, centralize Wazuh telemetry, validate detections, and document the work

**Document type:** Additive all-in-one build guide  
**Status:** Living guide - verified through DET-001; Kali build in progress  
**Last updated:** 2026-07-31  
**Audience:** Beginner SOC analysts, cybersecurity analysts, blue-team learners, and junior security engineers

This guide brings the existing architecture, build records, acceptance tests, recovery notes, and detection evidence into one beginner-friendly sequence. The detailed source records remain authoritative and are not replaced by this document.

| Guide field | Value |
|---|---|
| Best for | SOC analyst, security analyst, blue team, SIEM, and junior cybersecurity engineering roles |
| You will build | An isolated OPNsense network, Debian management workstation, Ubuntu DMZ server, Wazuh SIEM, monitored agents, Kali simulation workstation, and portfolio evidence |
| Level | Beginner; no prior SIEM or firewall administration assumed |
| Host used | Windows host, 32 GB RAM, hardware virtualization enabled |
| Hypervisor | Oracle VirtualBox |
| Storage approach | Dynamic disks, milestone snapshots, 20 GB host free-space stop threshold |
| Current verified result | OPNsense segmentation, Wazuh central stack, two active agents, and DET-001 failed SSH authentication detection |

::: warning
### READ THIS BEFORE YOU BUILD

Use this lab only against systems you own or have explicit permission to test. Never bridge the ATTACK network to a physical network, never forward public ports into the lab, and stop immediately if a target resolves outside `10.10.0.0/16`. Passwords, API keys, browser cookies, private MAC addresses, and raw unredacted screenshots do not belong in the repository.
:::

## How this guide works

Every major step uses the same callout types:

::: action
### WHAT YOU'RE DOING

The plain-language outcome and exact action for the step.
:::

::: why
### WHY IT MATTERS

The engineering or analyst skill demonstrated by the step.
:::

::: expect
### WHAT YOU SHOULD SEE

The observable acceptance result used to decide whether the step passed.
:::

::: warning
### HEADS UP

A safety boundary, common mistake, or recovery warning.
:::

::: concept
### NEW CONCEPT

A short explanation of terminology when it first appears.
:::

::: mindset
### ANALYST MINDSET

How to explain the decision, evidence, or trade-off in an interview.
:::

## The big picture: from isolated VMs to a working SOC loop

The lab follows the same operational loop used by a small defensive security team:

1. **Isolate.** Put systems into trust zones and deny unapproved paths.
2. **Collect.** Send endpoint and firewall telemetry to one monitoring platform.
3. **Detect.** Match activity against rules and validate alerts with controlled tests.
4. **Triage.** Confirm who, what, where, when, and whether the activity succeeded.
5. **Recover.** Use clean shutdowns, snapshots, and documented rollback points.
6. **Publish.** Share sanitized evidence that proves the result without exposing secrets.

```text
VirtualBox NAT -> fw01 OPNsense
                   |-- LAB-LAN    10.10.10.0/24 -> admin01, siem01
                   |-- LAB-DMZ    10.10.20.0/24 -> ubuntu-01
                   `-- LAB-ATTACK 10.10.30.0/24 -> kali-01 (in progress)

admin01 + ubuntu-01 -> Wazuh agents -> siem01 -> Threat Hunting -> DET-001 report
```

::: mindset
### ANALYST MINDSET

The project is not simply a collection of virtual machines. Its value is the evidence chain: an intentional action occurs on an endpoint, the endpoint records it, Wazuh analyzes it, the analyst verifies the fields, and the result becomes a defensible report.
:::

# Part 0 - Scope, capacity, and guardrails

## STEP 01 - Confirm the host is ready

::: action
### WHAT YOU'RE DOING

Confirm hardware virtualization, RAM, logical processors, and free storage before allocating any virtual disks. Run the repository readiness script as a normal Windows user:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\windows\Test-LabReadiness.ps1
```
:::

::: why
### WHY IT MATTERS

Resource exhaustion causes frozen guests, corrupt shutdowns, and misleading network failures. Capacity planning is part of security engineering because monitoring systems are only useful when they remain stable.
:::

::: expect
### WHAT YOU SHOULD SEE

The implemented host has 32 GB RAM and hardware virtualization enabled. Live VM files are stored under `D:\CyberLab-VMs`, outside the OneDrive repository.
:::

## STEP 02 - Adopt the storage-saver profile

::: action
### WHAT YOU'RE DOING

Use dynamically allocated VDI disks and stop adding data if drive `D:` approaches 20 GB free. Keep snapshots only at meaningful milestones. Delete verified, replaceable installer ISOs after the VM is stable if capacity becomes tight.
:::

| VM | Implemented or planned maximum | Memory | vCPU |
|---|---:|---:|---:|
| `fw01` | 20 GB dynamic | 3 GB | 2 |
| `admin01` | 16 GB dynamic | 2 GB | 2 |
| `ubuntu-01` | 30 GB dynamic | 2 GB | 2 |
| `siem01` | 50 GB dynamic | 8 GB | 4 |
| `kali-01` | 30 GB dynamic, planned | 3 GB | 2 |

::: warning
### HEADS UP - A VIRTUAL MAXIMUM IS NOT RESERVED SPACE

A 50 GB dynamic VDI grows only as blocks are written. Snapshots create differencing disks that also grow, so configured disk size alone does not describe real host consumption.
:::

## STEP 03 - Record safety stop conditions

::: action
### WHAT YOU'RE DOING

Before every exercise, identify the source VM, destination VM, lab IP, temporary firewall rule, expected alert, evidence to capture, and rollback point.
:::

::: expect
### WHAT YOU SHOULD SEE

Every target is inside the documented ranges, no VM receives a physical home-LAN address, and OPNsense remains the only system with a VirtualBox NAT-facing adapter.
:::

# Part 1 - Build the segmented OPNsense network

## STEP 04 - Create the isolated VirtualBox networks

::: action
### WHAT YOU'RE DOING

Use these exact Internal Network names wherever a VM attaches to a lab zone:

| Zone | VirtualBox network | CIDR | Gateway |
|---|---|---|---|
| Management and monitoring | `LAB-LAN` | `10.10.10.0/24` | `10.10.10.1` |
| Server DMZ | `LAB-DMZ` | `10.10.20.0/24` | `10.10.20.1` |
| Attack simulation | `LAB-ATTACK` | `10.10.30.0/24` | `10.10.30.1` |
:::

::: concept
### NEW CONCEPT - INTERNAL NETWORK

A VirtualBox Internal Network is a private virtual switch. It does not connect directly to the Windows host network or physical home LAN. Routing between zones occurs only through `fw01`.
:::

## STEP 05 - Create and install `fw01`

::: action
### WHAT YOU'RE DOING

Create the OPNsense VM with four adapters in this order:

1. NAT -> WAN
2. Internal Network `LAB-LAN` -> LAN
3. Internal Network `LAB-DMZ` -> DMZ
4. Internal Network `LAB-ATTACK` -> ATTACK

Use 2 vCPU, 3 GB RAM, and a 20 GB dynamically allocated disk. Install from the checksum-verified OPNsense DVD image, select only the new blank virtual disk, set the root password privately, detach the ISO, and boot from disk.
:::

::: warning
### HEADS UP - VERIFY INTERFACE MAPPING

Automatic assignment initially reversed WAN and LAN in this build. Match interfaces to VirtualBox adapters before applying addresses. Never publish the VM MAC addresses.
:::

::: expect
### WHAT YOU SHOULD SEE

OPNsense `26.1.6_2` boots with WAN on VirtualBox NAT and the three static IPv4 gateways on LAN, DMZ, and ATTACK.
:::

## STEP 06 - Apply deny-by-default inter-zone policy

::: action
### WHAT YOU'RE DOING

Rename OPT1 to DMZ and OPT2 to ATTACK. Disable the unused default IPv6 LAN allow rule for this IPv4-first phase. Place logged LAN-to-DMZ and LAN-to-ATTACK block rules above the general IPv4 LAN allow rule.
:::

::: why
### WHY IT MATTERS

Firewall rules use first-match evaluation. A narrow block or allow must appear above a broader rule or it will never be reached.
:::

::: expect
### WHAT YOU SHOULD SEE

LAN internet and DNS tests pass, while probes from LAN to DMZ and ATTACK fail and appear as labeled blocks in OPNsense Live View.
:::

## STEP 07 - Build a minimum-access DMZ policy

::: action
### WHAT YOU'RE DOING

Permit only the required DMZ services: DNS to the firewall, outbound NTP, HTTP, and HTTPS. Explicitly block and log DMZ-to-LAN and DMZ-to-ATTACK traffic. Add narrow exceptions above broader blocks only when a validated service requires them.
:::

::: expect
### WHAT YOU SHOULD SEE

`ubuntu-01` resolves names, synchronizes time, and reaches package repositories. DMZ probes to LAN, ATTACK, and unapproved internet services remain blocked. See `NET-003` for the verified results.
:::

# Part 2 - Build the LAN management workstation

## STEP 08 - Install `admin01`

::: action
### WHAT YOU'RE DOING

Install Debian 13.6 with Xfce using 2 vCPU, 2 GB RAM, and a 16 GB dynamic disk. Attach only `LAB-LAN`. Configure:

```text
Hostname: admin01
Address:  10.10.10.50/24
Gateway:  10.10.10.1
DNS:      10.10.10.1
User:     labadmin
```

Keep the password private.
:::

::: why
### WHY IT MATTERS

A dedicated management workstation creates a known source for firewall and dashboard access. It also makes source-based allow rules meaningful and testable.
:::

::: expect
### WHAT YOU SHOULD SEE

`admin01` reaches OPNsense, resolves public names, updates from official Debian repositories, and cannot reach the DMZ or ATTACK zone until an exception is approved.
:::

## STEP 09 - Create the management baseline

::: action
### WHAT YOU'RE DOING

After acceptance testing, shut down cleanly and create the cold snapshot `admin01-baseline-2026-07-15`.
:::

::: warning
### HEADS UP - CONSOLE INPUT FREEZES

This VM once stopped accepting keyboard input. An `admin01`-only cold power cycle recovered it without interrupting `fw01`. Always isolate recovery actions to the affected VM and preserve unrelated running systems.
:::

# Part 3 - Build the Ubuntu DMZ server

## STEP 10 - Install `ubuntu-01`

::: action
### WHAT YOU'RE DOING

Install checksum-verified Ubuntu Server 24.04.4 LTS using 2 vCPU, 2 GB RAM, and a 30 GB dynamic disk. Attach only `LAB-DMZ`. Configure:

```text
Hostname: ubuntu-01
Address:  10.10.20.10/24
Gateway:  10.10.20.1
DNS:      10.10.20.1
User:     labadmin
Service:  OpenSSH
```
:::

::: expect
### WHAT YOU SHOULD SEE

Gateway, DNS, HTTP, HTTPS, and NTP tests pass. The system receives no physical-LAN address.
:::

## STEP 11 - Allow one management path

::: action
### WHAT YOU'RE DOING

On the LAN interface, place a logged TCP 22 pass rule from `10.10.10.50` to `10.10.20.10/32` above the broader LAN-to-DMZ block.
:::

::: expect
### WHAT YOU SHOULD SEE

SSH from `admin01` succeeds, while ICMP from the same source remains blocked. This proves the exception permits one service instead of bypassing segmentation.
:::

## STEP 12 - Snapshot and document recovery

::: action
### WHAT YOU'RE DOING

After the DMZ acceptance tests, create the cold snapshot `ubuntu-01-baseline-2026-07-30`.
:::

::: warning
### HEADS UP - FROZEN GUEST RECOVERY

`ubuntu-01` once stopped accepting console input and SSH timed out. Keyboard recapture and ACPI shutdown failed, so an authorized VM-only cold power cycle restored it. Record recovery events because troubleshooting discipline is portfolio evidence too.
:::

# Part 4 - Deploy the Wazuh central server

## STEP 13 - Install the `siem01` operating-system baseline

::: action
### WHAT YOU'RE DOING

Create `siem01` with 4 vCPU, 8 GB RAM, and a 50 GB dynamically allocated disk. Attach only `LAB-LAN`. Install Ubuntu Server 24.04.4 LTS and configure:

```text
Hostname: siem01
Address:  10.10.10.10/24
Gateway:  10.10.10.1
DNS:      10.10.10.1
User:     labadmin
Service:  OpenSSH
```

Update the operating system, verify time synchronization and disk space, enable SSH, detach the ISO, shut down, and create `siem01-clean-os-2026-07-30`.
:::

::: why
### WHY IT MATTERS

The pre-application snapshot separates operating-system recovery from Wazuh recovery. If the central stack fails, the installation can be repeated without reinstalling Ubuntu.
:::

## STEP 14 - Install Wazuh all-in-one

::: action
### WHAT YOU'RE DOING

Use the current official Wazuh quickstart. The verified installation used the Wazuh 4.14 assistant:

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```

Store the generated administrator password privately. Do not include it in screenshots or documentation.
:::

::: expect
### WHAT YOU SHOULD SEE

The installer reports completion and provides an HTTPS dashboard URL. The following services report `active`:

```bash
systemctl is-active wazuh-indexer wazuh-manager filebeat wazuh-dashboard
```
:::

## STEP 15 - Secure Wazuh administration

::: action
### WHAT YOU'RE DOING

Change the Wazuh `admin` credential privately with the official password-management tool. Use a masked shell variable so the password does not enter shell history. Disable the Wazuh APT repository after installation to prevent accidental component upgrades.
:::

::: warning
### HEADS UP - WAZUH PASSWORD POLICY

The password must be 8 to 64 characters and include uppercase, lowercase, a number, and one of `. * + ? -`. Never post a password into a chat or evidence file. Any exposed value must be considered compromised and replaced.
:::

## STEP 16 - Apply the `siem01` host firewall

::: action
### WHAT YOU'RE DOING

Stage all rules before enabling UFW. Use default deny inbound and allow outbound. Permit only:

| Source | TCP port | Purpose |
|---|---:|---|
| `10.10.10.50` | 22 | SSH administration |
| `10.10.10.50` | 443 | Wazuh dashboard |
| `10.10.10.50` | 1514, 1515 | `admin01` agent telemetry and enrollment |
| `10.10.20.10` | 1514, 1515 | `ubuntu-01` agent telemetry and enrollment |

Review with `sudo ufw show added`, then enable and validate a new SSH connection and dashboard session.
:::

::: expect
### WHAT YOU SHOULD SEE

UFW reports active, a new SSH connection from `admin01` succeeds, local and remote HTTPS return `HTTP/1.1 302 Found`, and the dashboard loads at `https://10.10.10.10/`.
:::

## STEP 17 - Create the Wazuh baseline

::: action
### WHAT YOU'RE DOING

After service, firewall, SSH, and dashboard validation, create the cold snapshot `siem01-wazuh-baseline-2026-07-30`.
:::

::: warning
### HEADS UP - FIRST BOOT MAY APPEAR FROZEN

`siem01` intermittently paused at `Begin: Loading essential drivers ...` after a cold snapshot. The installer ISO was already detached. A VM-only cold power cycle followed by a second boot reached the login prompt. Do not restore or delete snapshots during this recovery.
:::

### Part 4 acceptance checkpoint

::: status
### CENTRAL MONITORING BASELINE VERIFIED

| Control | Verified result |
|---|---|
| Core services | Wazuh indexer, manager, Filebeat, and dashboard active |
| Management access | New SSH session and HTTPS dashboard access from `admin01` passed |
| Host firewall | UFW active with default-deny inbound policy |
| DMZ exposure | Only Wazuh agent TCP 1514/1515 staged for `ubuntu-01` |
| Update control | Wazuh APT repository disabled after installation |
| Recovery | Cold baseline snapshot created and successfully boot-validated |
:::

::: mindset
### ANALYST MINDSET

The checkpoint proves more than successful installation: the service is reachable only through approved paths, has a tested recovery point, and has evidence for each security control.
:::

# Part 5 - Enroll endpoints and validate the detection pipeline

## STEP 18 - Permit DMZ agent traffic

::: action
### WHAT YOU'RE DOING

On OPNsense DMZ rules, place a logged IPv4 TCP pass rule from `10.10.20.10/32` to `10.10.10.10/32`, destination ports 1514 through 1515, above the DMZ-to-LAN block.
:::

::: expect
### WHAT YOU SHOULD SEE

From `ubuntu-01`, TCP 1514 and 1515 succeed while TCP 443 remains blocked. This proves the dashboard was not exposed to the DMZ.
:::

## STEP 19 - Enroll `ubuntu-01` and `admin01`

::: action
### WHAT YOU'RE DOING

Use **Agents management -> Summary -> Deploy new agent** in the Wazuh dashboard. Generate Linux DEB x86_64 commands with manager `10.10.10.10` and unique names `ubuntu-01` and `admin01`. Enable each service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now wazuh-agent
```
:::

::: expect
### WHAT YOU SHOULD SEE

The Wazuh dashboard reports `Active: 2` and `Disconnected: 0`.
:::

## STEP 20 - Run DET-001: failed SSH authentication

::: action
### WHAT YOU'RE DOING

From `admin01`, generate one controlled failed login using a nonexistent account:

```bash
ssh invaliduser@10.10.20.10
```

Submit one dummy password, stop after the first denial, then inspect Wazuh Threat Hunting with `agent.name is ubuntu-01`.
:::

::: expect
### WHAT YOU SHOULD SEE

The verified event showed:

| Field | Value |
|---|---|
| Agent | `ubuntu-01` |
| Rule ID | `5710` |
| Rule level | `5` |
| Description | `sshd: Attempt to login using a non-existent user` |
| Source IP | `10.10.10.50` |
| Source user | `invaliduser` |

The complete sanitized report is `evidence/2026-07-31_DET-001_failed-ssh-login.md`.
:::

::: mindset
### ANALYST MINDSET

The alert is a true positive for the behavior but a benign positive in operational context because the test was authorized. One failed login is not a brute-force attack. Accurate classification is more valuable than exaggerating severity.
:::

# Part 6 - Build the Kali simulation workstation

## STEP 21 - Download and verify Kali

::: status
### CURRENT STATUS - IN PROGRESS

Kali Linux 2026.2 installer AMD64 is being downloaded from the official Kali image service. The VM has not yet been created, so the steps in this part remain pending until verified during execution.
:::

::: action
### WHAT YOU'RE DOING

Save the official installer as:

```text
D:\CyberLab-VMs\ISO\kali-linux-2026.2-installer-amd64.iso
```

Download the matching official `SHA256SUMS`, calculate the local SHA-256 hash, and require an exact match before attaching the ISO.
:::

## STEP 22 - Create `kali-01`

::: action
### WHAT YOU'RE DOING

Create the VM with:

| Setting | Planned value |
|---|---|
| Name | `kali-01` |
| Type | Linux / Debian 64-bit |
| vCPU | 2 |
| Memory | 3072 MB |
| Disk | 30 GB VDI, dynamically allocated |
| Network | Adapter 1 only: Internal Network `LAB-ATTACK` |
| 3D acceleration | Disabled |

Do not attach NAT, bridged, host-only, shared-folder, or second network adapters.
:::

## STEP 23 - Install and configure Kali

::: action
### WHAT YOU'RE DOING

Install the default Xfce desktop and create a non-root daily account. Configure the final static address:

```text
Hostname: kali-01
Address:  10.10.30.10/24
Gateway:  10.10.30.1
DNS:      10.10.30.1
```

Keep the account password private and detach the ISO before the first installed-disk boot.
:::

## STEP 24 - Validate ATTACK-zone isolation

::: action
### WHAT YOU'RE DOING

Before adding any temporary exercise rule, test that Kali cannot reach OPNsense management, `admin01`, `siem01`, or `ubuntu-01`. Confirm the blocks in OPNsense Live View using source `10.10.30.10`.
:::

::: expect
### WHAT YOU SHOULD SEE

Unapproved paths fail and are logged. Kali receives no physical home-LAN address and cannot reach the Wazuh dashboard.
:::

## STEP 25 - Update, harden, and snapshot Kali

::: action
### WHAT YOU'RE DOING

Create the narrowest temporary ATTACK-zone egress rules needed for DNS, NTP, HTTP, and HTTPS updates. Apply updates, confirm the daily user is non-root, remove unneeded access, shut down cleanly, and create one cold baseline snapshot. Record the snapshot name and host free space.
:::

::: warning
### HEADS UP - KALI IS A TOOLBOX, NOT AUTHORIZATION

Installing Kali does not broaden the lab scope. Every test still requires a named source, named target, temporary rule, expected detection, and removal condition.
:::

# Part 7 - Operate, recover, and publish

## STEP 26 - Start and stop the lab safely

::: action
### WHAT YOU'RE DOING

Recommended startup order:

1. `fw01`
2. `siem01`
3. `admin01`
4. The one endpoint needed for the exercise

Recommended shutdown order:

1. Endpoints
2. `admin01`
3. `siem01`
4. `fw01`

Use guest shutdown commands or ACPI shutdown first. Use a cold power cycle only for an unresponsive VM and document why.
:::

## STEP 27 - Maintain recovery points

| Snapshot | Verified purpose |
|---|---|
| `admin01-baseline-2026-07-15` | Validated Debian management baseline |
| `ubuntu-01-baseline-2026-07-30` | Validated Ubuntu DMZ baseline |
| `siem01-clean-os-2026-07-30` | Clean Ubuntu state before Wazuh |
| `siem01-wazuh-baseline-2026-07-30` | Validated Wazuh and UFW state |

::: concept
### NEW CONCEPT - SNAPSHOT VS BACKUP

A snapshot depends on the original VM disk and is useful for short rollback. It is not an independent backup. Keep sanitized documentation and configuration exports outside the live VM directory.
:::

## STEP 28 - Validate evidence before publishing

::: action
### WHAT YOU'RE DOING

Run:

```powershell
.\scripts\windows\Test-Repository.ps1
```

Review screenshots manually, keep raw evidence under the ignored `evidence/raw/` path, and publish only cropped, sanitized artifacts.
:::

## STEP 29 - Explain the project to hiring teams

::: why
### WHY IT MATTERS

Hiring teams need evidence of decisions and outcomes, not only screenshots of installed tools. Lead with segmentation, least privilege, telemetry coverage, detection validation, troubleshooting, and recovery.
:::

**SOC analyst version**

> Built an isolated VirtualBox SOC lab with OPNsense segmentation and Wazuh monitoring, enrolled Linux endpoints, validated least-privilege firewall paths, and triaged an SSH authentication alert using endpoint and network evidence.

**Cybersecurity engineering version**

> Designed a three-zone virtual security architecture, implemented deny-by-default routing and host firewalls, deployed a storage-conscious Wazuh SIEM, documented recovery controls, and produced reproducible acceptance and detection evidence.

# Appendix A - Current asset and address register

| Asset | Role | Zone | Address | Current state |
|---|---|---|---|---|
| `fw01` | OPNsense firewall | All zones | `.1` gateway on each zone | Operational |
| `admin01` | Management workstation | LAN | `10.10.10.50` | Operational; Wazuh agent active |
| `siem01` | Wazuh central server | LAN | `10.10.10.10` | Operational |
| `ubuntu-01` | DMZ Linux server | DMZ | `10.10.20.10` | Operational; Wazuh agent active |
| `kali-01` | Simulation workstation | ATTACK | `10.10.30.10` | ISO download in progress; VM pending |
| `win11-01` | Future Windows endpoint | LAN | `10.10.10.20` planned | Not built |

# Appendix B - Minimum approved traffic matrix

| Source | Destination | Service | State |
|---|---|---|---|
| LAN managed systems | Internet through OPNsense | Controlled updates | Allowed |
| `admin01` | `fw01` | HTTPS management | Allowed |
| `admin01` | `siem01` | SSH 22, HTTPS 443, Wazuh 1514/1515 | Allowed |
| `admin01` | `ubuntu-01` | SSH 22 only | Allowed and logged |
| `ubuntu-01` | OPNsense / Internet | DNS, NTP, HTTP, HTTPS | Allowed and logged as configured |
| `ubuntu-01` | `siem01` | Wazuh TCP 1514/1515 | Allowed and logged |
| `ubuntu-01` | Wazuh dashboard TCP 443 | HTTPS | Blocked |
| DMZ | LAN / ATTACK | Any unapproved service | Blocked and logged |
| ATTACK | LAN / DMZ | Any service without an exercise rule | Blocked and logged |

# Appendix C - When something breaks

| Symptom | Most likely cause and safe response |
|---|---|
| Guest pauses at `Loading essential drivers` | Wait at least three minutes. If unchanged and the ISO is detached, power-cycle only that VM and retry the boot. |
| Keyboard does not respond in a VM | Release and recapture input. Try SSH if approved. If both console and SSH fail, use a VM-only cold recovery and document it. |
| SSH says host authenticity cannot be established | Compare the presented ED25519 SHA-256 fingerprint with the server's local host-key fingerprint before accepting. |
| VirtualBox console will not paste | Linux TTY clipboard integration is limited. Use SSH from `admin01`; inside Linux terminals paste with `Ctrl+Shift+V`. |
| Wazuh password tool rejects a value | Confirm the variable is non-empty and the policy includes uppercase, lowercase, number, and `. * + ? -`. Never reveal the password while troubleshooting. |
| Dashboard says no API is available | Allow services time to restart, verify `wazuh-manager`, and retry before changing firewall rules. |
| Firefox displays a blank screen or TLS EOF error | Verify local and remote HTTPS with `curl -kI`. If both return 302, close all Firefox windows and retry a clean session. |
| Wazuh dashboard is unreachable after UFW | Verify the source IP, staged TCP 443 rule, listening socket, and remote curl before disabling UFW. |
| Agent is disconnected | Check agent service status, TCP 1514/1515, OPNsense ordering, UFW source rule, manager address, and system time. |
| Host storage approaches 20 GB free | Stop adding data, shut down nonessential VMs, review snapshots and verified installer ISOs, and do not expand disks. |

# Appendix D - Plain-English glossary

| Term | Meaning |
|---|---|
| SIEM | A platform that centralizes security telemetry, detects activity, and supports investigation. |
| Wazuh manager | The component that receives agent events and applies decoders and rules. |
| Wazuh indexer | The search and storage component for alerts and security data. |
| Wazuh dashboard | The HTTPS interface for monitoring, threat hunting, and administration. |
| Agent | Lightweight endpoint software that collects and forwards telemetry. |
| DMZ | A restricted server zone separated from trusted management systems. |
| Default deny | Traffic is blocked unless a specific rule permits it. |
| First match | The first applicable firewall rule decides the result. |
| Telemetry | Security-relevant data such as authentication, process, service, and network events. |
| True positive | The detected behavior genuinely occurred. Context can still make it authorized or benign. |
| Benign positive | A valid detection caused by planned or harmless activity. |
| False positive | A rule incorrectly identifies behavior that did not meet the intended detection condition. |
| Triage | Validate, scope, enrich, assess, respond, document, and improve an alert. |
| Snapshot | A dependent rollback point for a VM, not an independent backup. |

# Appendix E - Evidence and source records

This guide summarizes, but does not replace, the following detailed records:

- `docs/00-scope-safety.md`
- `docs/01-architecture.md`
- `docs/02-build-guide.md`
- `docs/11-opnsense-build-record.md`
- `docs/12-admin01-build-record.md`
- `docs/13-ubuntu01-build-record.md`
- `docs/14-siem01-build-record.md`
- `evidence/2026-07-15_NET-001_lan-firewall-acceptance.md`
- `evidence/2026-07-15_NET-002_admin01-update-path.md`
- `evidence/2026-07-29_NET-003_dmz-minimum-access.md`
- `evidence/2026-07-31_DET-001_failed-ssh-login.md`

## Official vendor references

- OPNsense documentation: `https://docs.opnsense.org/`
- VirtualBox documentation: `https://www.virtualbox.org/wiki/Documentation`
- Wazuh quickstart: `https://documentation.wazuh.com/current/quickstart.html`
- Wazuh Linux agent guide: `https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html`
- Kali downloads: `https://www.kali.org/get-kali/`
- Kali VirtualBox guide: `https://www.kali.org/docs/virtualization/install-virtualbox-guest-vm/`

Always recheck vendor requirements, commands, ports, and supported versions before repeating the build at a later date.
