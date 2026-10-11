# Architecture and capacity plan

## Recommended deployment

Use VirtualBox on a personal computer for the first build. The design is hypervisor-neutral, so it can later move to Proxmox or another dedicated host without changing the learning objectives.

### Capacity profiles

| Profile | Host requirement | Concurrent VMs | Operating approach |
|---|---:|---|---|
| Storage-saver | 4 cores, 16 GB RAM, 75–100 GB free SSD | OPNsense + Wazuh + one endpoint | Dynamic disks; rotate Windows, Ubuntu, and Kali; short log retention |
| Lean | 4 cores, 16 GB RAM, 120–200 GB free SSD | OPNsense + Wazuh + one endpoint | Run Windows, Ubuntu, and Kali one at a time |
| Recommended | 8 cores, 32 GB RAM, 350 GB free SSD | All five | Best beginner experience |
| Expanded | 12+ cores, 64 GB RAM, 750 GB free SSD | All five plus AD and sensors | Future phase, not required initially |

Do not allocate all host resources. Reserve at least 4 GB RAM, two logical CPU threads, and 15% free disk space for the host.

### VM inventory

| VM | vCPU | RAM | Disk | Network adapters | Purpose |
|---|---:|---:|---:|---|---|
| `fw01` | 2 | 3 GB | 20 GB dynamic ceiling | NAT + three internal | Routing and policy enforcement |
| `siem01` | 4 | 8 GB | 80 GB | LAB-LAN | Wazuh all-in-one |
| `win11-01` | 2 | 4–6 GB | 64 GB | LAB-LAN | Windows telemetry and hardening |
| `ubuntu-01` | 2 | 2 GB | 30 GB | LAB-DMZ | Linux server and service monitoring |
| `kali-01` | 2 | 2–4 GB | 40 GB | LAB-ATTACK | Authorized telemetry generation |

Vendor requirements change; confirm current minimums in official documentation before allocating resources.

## Storage-saver deployment

The disk figures in the VM inventory are **virtual maximums**, not space that must be consumed on day one. Select dynamically allocated VDI disks so each file grows only as data is written. Do not select fixed-size disks.

Start with only three VMs:

| VM | Dynamic virtual maximum | Expected initial host use | Rule |
|---|---:|---:|---|
| `fw01` | 20 GB | 3–5 GB | Keep permanently; installer required the larger logical ceiling |
| `siem01` | 50 GB | 20–30 GB | Monitor growth; use short lab retention |
| One endpoint | 30–50 GB | 10–30 GB | Keep only the endpoint needed for the current phase |

This starts around 35–65 GB of actual host usage, although updates, logs, and snapshots make it grow. Add Ubuntu, Kali, and Windows sequentially; export or remove a replaceable VM before adding another if free space approaches the safety floor.

Storage rules for this profile:

- Keep at least **20 GB host free space** at all times. Stop the lab below that floor.
- Keep one clean snapshot per active VM and delete obsolete snapshots through VirtualBox after validating the replacement. Snapshots can consume more space than expected.
- Delete ISO installers after the VM and checksum/source record are validated; they can be downloaded again.
- Configure short Wazuh index retention suitable for a disposable two-agent lab and export only the small sanitized evidence needed for the portfolio.
- Do not place live VM disk files inside a OneDrive-synchronized folder. Use a local nonsynchronized VM directory.

Wazuh currently recommends 50 GB for 1–25 agents when retaining 90 days of indexed alerts. This lab uses far fewer agents and a shorter retention window, but storage must still be monitored; the 50 GB dynamic disk remains the safe virtual ceiling.

## Address plan

| Zone | Hypervisor network | CIDR | Gateway | Static assignments |
|---|---|---|---|---|
| User/monitoring | `LAB-LAN` | `10.10.10.0/24` | `10.10.10.1` | Wazuh `.10`, Windows `.20` |
| Server DMZ | `LAB-DMZ` | `10.10.20.0/24` | `10.10.20.1` | Ubuntu `.10` |
| Attack simulation | `LAB-ATTACK` | `10.10.30.0/24` | `10.10.30.1` | Kali `.10` |

Use DHCP only during the first boot if necessary. Move infrastructure systems to static addresses or static reservations before installing agents.

## Trust model and traffic policy

Default policy is deny between zones. Add only the flows below:

| Source | Destination | Service | Reason |
|---|---|---|---|
| Managed lab hosts | OPNsense | DNS, NTP | Basic infrastructure |
| Wazuh agents | `siem01` | Current Wazuh agent enrollment/telemetry ports | Central monitoring |
| Admin endpoint | OPNsense/Wazuh | HTTPS | Management |
| Lab zones | Internet | DNS, HTTP/S, NTP | Updates; disable during risky exercises |
| Kali | Named target only | Exercise-specific | Temporary simulation rule |

Never use an `any-to-any` inter-zone rule. Document the owner, purpose, creation date, and removal condition for every exception.

## Design decisions

- **VirtualBox first:** accessible on common desktop hardware and supports isolated internal networks.
- **OPNsense as choke point:** makes segmentation and network evidence visible.
- **Wazuh all-in-one:** reduces operational overhead while exposing SIEM/XDR concepts.
- **No Active Directory initially:** identity infrastructure is valuable but adds too many failure modes for the first build.
- **Snapshots are not backups:** export sanitized configuration and keep repository documentation separately.

## Future enhancements

After the 90-day baseline, consider an Active Directory domain, Zeek or Suricata network telemetry, vulnerability management, infrastructure-as-code, and a dedicated Proxmox host. Add one capability at a time with acceptance tests.
