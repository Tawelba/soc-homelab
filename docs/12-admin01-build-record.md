# admin01 management VM build record

**Build date:** 2026-07-15  
**Asset:** `admin01`  
**Role:** LAN-side administration and acceptance testing  
**Status:** Baseline configured, validated, and snapshotted

## Virtual machine configuration

| Setting | Implemented value |
|---|---|
| Operating system | Debian 13.6 with Xfce |
| CPU | 2 vCPU |
| Memory | 2 GB |
| Disk | 16 GB maximum, dynamically allocated VDI |
| Network | VirtualBox Internal Network `LAB-LAN` |
| Hostname | `admin01` |
| Domain | `cyberlab.test` |
| Administrator account | `labadmin`; password kept private and excluded from documentation |

## Network configuration

| Field | Value |
|---|---|
| Interface | `enp0s3` |
| IPv4 address | `10.10.10.50/24` |
| Default gateway | `10.10.10.1` |
| DNS server | `10.10.10.1` |
| Connected subnet | `10.10.10.0/24` |

The VM has no bridged or physical home-LAN adapter. Its only network attachment is `LAB-LAN`, and all routed access passes through `fw01`.

## Acceptance results

- IPv4 internet routing passed with four of four replies from `1.1.1.1`.
- Public DNS resolution and reachability passed with zero packet loss.
- LAN-to-DMZ and LAN-to-ATTACK probes were blocked with 100% packet loss.
- OPNsense Live View correlated all eight denied ICMP probes to the intended labeled block rules.
- The active IPv4 address remained `10.10.10.50/24`, with default route through `10.10.10.1`.
- `sudo apt update` reached the official Debian repositories and completed without errors; all packages were current.

See [NET-001](../evidence/2026-07-15_NET-001_lan-firewall-acceptance.md) and [NET-002](../evidence/2026-07-15_NET-002_admin01-update-path.md) for the sanitized test records.

## Recovery observation

The VM stopped accepting keyboard input during firewall setup. A hard reset did not restore it cleanly and left the VirtualBox process stuck while stopping. An `admin01`-only cold power cycle terminated the stuck process without interrupting `fw01`. Debian then booted from the existing virtual disk, reached the graphical login screen, and accepted keyboard input normally. No disk repair or reinstallation was required.

## Baseline snapshot

| Field | Value |
|---|---|
| Snapshot name | `admin01-baseline-2026-07-15` |
| Snapshot type | Cold snapshot; VM powered off |
| Snapshot date | 2026-07-15 |
| Captured state | Debian baseline after LAN firewall acceptance and successful `apt update` |

Snapshots are recovery points, not backups. Because this lab uses a storage-saver profile, future snapshots should be limited to meaningful milestones and removed only after their replacement has been verified.

## Remaining work

- [x] Start `admin01` from the new baseline and confirm it reaches the Debian graphical login screen.
- [ ] Add only the administration and evidence tools required by later exercises.
- [ ] Establish a separate backup/export process for critical lab configuration and sanitized documentation.
