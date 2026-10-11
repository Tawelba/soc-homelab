# kali-01 ATTACK workstation build record

**Validation date:** 2026-07-31  
**Asset:** `kali-01`  
**Role:** Authorized security-testing workstation on the isolated ATTACK segment  
**Status:** Operating-system baseline installed and validated; cold snapshot pending

## Virtual machine configuration

| Setting | Implemented value |
|---|---|
| CPU | 2 vCPU |
| Memory | 3,072 MB |
| Disk | 30 GB maximum, dynamically allocated VDI |
| Network | VirtualBox Internal Network `LAB-ATTACK` only |
| Operating system | Kali Linux 2026.2 AMD64 |
| Desktop and tools | Xfce with the Top 10 tool collection |
| Firmware | Legacy BIOS |
| Processor feature | PAE/NX enabled |
| Display | VMSVGA, 128 MB video memory, 3D acceleration disabled |
| Administrator account | `labadmin`; password kept private |

The installer ISO passed SHA-256 verification before attachment. See [KALI-001](../evidence/2026-07-31_KALI-001_iso-verification.md).

## Network configuration

| Field | Value |
|---|---|
| IPv4 address | `10.10.30.10/24` |
| Default gateway | `10.10.30.1` |
| DNS server | `10.10.30.1` |
| Connected subnet | `10.10.30.0/24` (`LAB-ATTACK`) |

The workstation has no bridged adapter and cannot directly join the home LAN. OPNsense remains the only lab component with an external NAT path.

## Installation profile

- Used the graphical installer from the checksum-verified Kali 2026.2 installer ISO.
- Applied a static IPv4 configuration on `LAB-ATTACK`.
- Used guided partitioning on only the 30 GB `sda` VirtualBox disk.
- Selected one partition for all files, appropriate for this storage-conscious workstation.
- Installed GRUB to `/dev/sda`.
- Selected Xfce and the Top 10 tool collection instead of the larger default/everything collections.
- Completed the first disk boot and logged in as `labadmin`.
- Confirmed that Kali repositories were current: zero packages upgraded, installed, removed, or held back.

## Partitioner recovery

The graphical installer stopped twice at `Starting up the partitioner`. Read-only checks confirmed that the checksum-verified ISO, 30 GB VDI, SATA controller, free host capacity, CPU, memory, and display configuration were present and no VirtualBox disk I/O failure was logged.

The VM differed from Kali's published VirtualBox guidance because PAE/NX was disabled. After a `kali-01`-only cold power-off, PAE/NX was changed from disabled to enabled. The VirtualBox Settings processor panel became unresponsive, so only the Manager process was restarted; the four running VM processes were left active. The powered-off Kali configuration was backed up, changed, and verified before boot.

After PAE/NX was enabled, the installer loaded the disk-selection screen and completed partitioning and installation. This is recorded as an evidence-based remediation rather than proof that PAE/NX was the sole underlying cause.

## ATTACK firewall services

OPNsense uses logged, narrowly scoped rules above blocking rules:

| Source | Destination | Port/protocol | Purpose |
|---|---|---|---|
| `ATTACK net` | `ATTACK address` | 53 TCP/UDP | DNS through OPNsense |
| `ATTACK net` | Any | 123 UDP | External NTP synchronization |

The NTP rule uses source port `any` and destination port `123`. OPNsense Live View initially correlated NTP traffic with the `Default deny/state violation rule`; correcting and applying the pass rule allowed synchronization.

## Acceptance results

- `eth0` reported `UP` with `10.10.30.10/24`.
- Four ICMP probes to gateway `10.10.30.1` passed.
- DNS resolution through `10.10.30.1` passed after the ATTACK DNS rule was applied.
- `sudo apt update` completed without persistent warnings or repository errors.
- Full upgrade reported zero outstanding package actions.
- Time zone is `Africa/Accra`.
- NTP synchronization passed against `162.159.200.1`, with `NTPSynchronized=yes` and packet count 2.
- Root filesystem reported 28 GB total, 7.4 GB used, and 19 GB available.
- `virtualbox-guest-x11` was already at the newest version.
- `virtualbox-guest-utils.service` reported `active` after reboot.

See [KALI-002](../evidence/2026-07-31_KALI-002_baseline-acceptance.md) for the portfolio-safe acceptance record.

## Remaining work

- [ ] Create and validate the cold `kali-01` operating-system baseline snapshot.
- [ ] Test ATTACK-to-LAN and ATTACK-to-DMZ segmentation without scanning unrelated systems.
- [ ] Install only the additional tools required by approved lab exercises.
- [ ] Decide whether to enroll Kali in Wazuh for attacker-side telemetry.
- [ ] Run the first authorized Kali-to-DMZ detection exercise and preserve sanitized evidence.
