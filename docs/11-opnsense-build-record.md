# OPNsense firewall build record

**Build date:** 2026-07-15  
**Asset:** `fw01`  
**Status:** Base network, LAN isolation, and DMZ minimum-access policy configured and validated

## Source verification

| Field | Value |
|---|---|
| Product | OPNsense Community Edition |
| Installation image | `OPNsense-26.1.6-dvd-amd64.iso.bz2` |
| Source | Official OPNsense Leaseweb mirror |
| Published SHA-256 | `6ba3633d9c0f96d82c792015a45f4b8aac45ea8fa2bdba3c5e534d0c90a4f08c` |
| Observed SHA-256 | `6ba3633d9c0f96d82c792015a45f4b8aac45ea8fa2bdba3c5e534d0c90a4f08c` |
| Verification | Pass — exact match before extraction |

The 26.1.6 image is a stable installation base. The first disk boot reported OPNsense `26.1.6_2` (amd64). The system will be updated through OPNsense's supported update mechanism after initial network validation.

## Virtual machine configuration

| Setting | Implemented value |
|---|---|
| VM name | `fw01` |
| Guest type | FreeBSD 64-bit |
| CPU | 2 vCPU |
| Memory | 3 GB |
| Disk | 20 GB maximum, dynamically allocated VDI |
| Filesystem | ZFS, single-disk stripe |
| Boot media | Verified OPNsense DVD ISO |
| Clipboard / drag-and-drop | Disabled |
| USB / audio | Disabled |

The disk ceiling was raised from 12 GB to 20 GB after the installer kept confirmation disabled at the smaller size. Because the VDI is dynamic, this did not reserve 20 GB on the host. At the end of system cloning, the physical VDI remained under 2 GB.

## Network adapters

| VirtualBox adapter | Attachment | OPNsense assignment | Address / purpose |
|---|---|---|---|
| 1 | NAT | WAN (`em0`) | DHCP; observed `10.0.2.15/24` for controlled updates |
| 2 | Internal Network `LAB-LAN` | LAN (`em1`) | `10.10.10.1/24`; user and monitoring zone |
| 3 | Internal Network `LAB-DMZ` | DMZ (`em2`) | `10.10.20.1/24`; server zone |
| 4 | Internal Network `LAB-ATTACK` | ATTACK (`em3`) | `10.10.30.1/24`; authorized simulation zone |

OPNsense's initial auto-assignment reversed the intended WAN and LAN roles. Each FreeBSD interface was matched to its VirtualBox adapter by observed MAC address, then the roles were corrected explicitly. MAC addresses are intentionally omitted from the public build record.

## Installation observations

- All four Intel PRO/1000 virtual adapters were detected.
- The UFS installer path repeatedly returned a false minimum-size error even after the virtual disk was expanded.
- Restarting the installer and using its default ZFS path succeeded.
- Only the new blank `fw01` virtual disk (`ada0`) was selected at the destructive confirmation screen.
- File cloning, verification, and target preparation completed successfully.
- The root password was set privately by the operator and was not recorded in the repository.
- The VM was halted cleanly, the installation ISO was detached, and the first boot from the installed disk completed successfully.
- The first installed console reported OPNsense `26.1.6_2`, temporary LAN `em0` at `192.168.1.1/24`, and WAN `em1` with no address displayed.
- Interface mapping was corrected to WAN `em0`, LAN `em1`, DMZ `em2`, and attack zone `em3`.
- LAN, DMZ, and attack-zone gateway addresses were configured statically; DHCP servers and IPv6 tracking were left disabled on the isolated zones for this IPv4-first build.
- The first LAN management client, Debian 13 `admin01` at `10.10.10.50/24`, reached the OPNsense web interface through `LAB-LAN`.
- OPT1 and OPT2 were renamed to DMZ and ATTACK in the web interface.
- Two logged, first-match IPv4 rules were placed above the general LAN allow rule: block `LAN network` to `DMZ network`, and block `LAN network` to `ATTACK network`.
- The default IPv6 LAN-to-any allow rule was disabled because this phase is intentionally IPv4-only. The IPv4 LAN-to-any rule remains enabled for controlled updates.
- During setup, `admin01` stopped accepting keyboard input. An admin01-only cold power cycle recovered the VM; `fw01` remained running and unchanged. Debian then booted from its existing virtual disk and accepted keyboard input normally.
- WAN received `10.0.2.15/24` from VirtualBox NAT and reached the NAT gateway at `10.0.2.2` with three of three ICMP replies and zero packet loss.
- Existing training VMs and physical disks were not modified.

## LAN-side acceptance results

On 2026-07-15, `admin01` completed the following checks:

- Public IPv4 reachability: four of four replies from `1.1.1.1`, zero packet loss.
- DNS plus public reachability: a public hostname resolved and returned four of four replies, zero packet loss.
- LAN to DMZ: four probes to `10.10.20.1` were blocked, 100% packet loss.
- LAN to ATTACK: four probes to `10.10.30.1` were blocked, 100% packet loss.
- OPNsense Live View recorded all eight denied ICMP probes against the intended labeled rules.

Detailed sanitized results are in [NET-001](../evidence/2026-07-15_NET-001_lan-firewall-acceptance.md).

The follow-up update-path test confirmed that `admin01` retained `10.10.10.50/24`, used `10.10.10.1` as its default gateway, reached the official Debian repositories, and completed `apt update` without errors. See [NET-002](../evidence/2026-07-15_NET-002_admin01-update-path.md).

On 2026-07-29, `ubuntu-01` validated the DMZ minimum-access policy. DNS, NTP, HTTP, and HTTPS succeeded; DMZ traffic to LAN and ATTACK was blocked; and unapproved ICMP internet traffic remained subject to default deny. A single logged SSH rule allowed `admin01` to administer `ubuntu-01`, while ICMP from the same LAN host remained blocked. See [NET-003](../evidence/2026-07-29_NET-003_dmz-minimum-access.md).

## Remaining acceptance work

- [x] User privately sets the root password in the VM console.
- [x] Complete installation and shut down/reboot.
- [x] Detach the installation ISO and boot from the virtual disk.
- [x] Validate interface mapping and assign WAN, LAN, DMZ, and attack interfaces.
- [x] Replace the temporary LAN address with `10.10.10.1/24`.
- [x] Configure DMZ `10.10.20.1/24` and attack zone `10.10.30.1/24`.
- [x] Rename OPT1 to DMZ and OPT2 to ATTACK in the web interface.
- [x] Add logged LAN-to-DMZ and LAN-to-ATTACK block rules above the IPv4 LAN allow rule.
- [x] Disable the unused default IPv6 LAN allow rule for the IPv4-first build.
- [x] Verify LAN-side IPv4 internet access and DNS resolution from `admin01`.
- [x] Verify and log LAN-to-DMZ and LAN-to-ATTACK denials from `admin01`.
- [x] Verify a lab client can update through OPNsense without receiving a physical home-LAN address.
- [x] Verify bidirectional LAN/DMZ isolation and DMZ-to-ATTACK blocking after deploying the DMZ client.
- [ ] Repeat ATTACK-zone source testing after the ATTACK client is deployed.
- [ ] Take a clean installed-firewall snapshot only after acceptance tests pass.
