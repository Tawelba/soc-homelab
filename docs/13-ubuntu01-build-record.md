# ubuntu-01 DMZ server build record

**Validation date:** 2026-07-29  
**Asset:** `ubuntu-01`  
**Role:** DMZ Linux server and minimum-access firewall test host  
**Status:** Installed, networked, validated, and snapshotted

## Source verification

| Field | Value |
|---|---|
| Operating system | Ubuntu Server 24.04.4 LTS |
| Installation image | Ubuntu Server 24.04.4 LTS ISO |
| Published SHA-256 | `e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433` |
| Observed SHA-256 | `e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433` |
| Verification | Pass — exact match before installation |

## Virtual machine configuration

| Setting | Implemented value |
|---|---|
| CPU | 2 vCPU |
| Memory | 2 GB |
| Disk | 30 GB maximum, dynamically allocated VDI |
| Network | VirtualBox Internal Network `LAB-DMZ` only |
| Hostname | `ubuntu-01` |
| Administrator account | `labadmin`; password kept private |
| Remote administration | OpenSSH server |

The dynamic disk sets a maximum size and does not reserve 30 GB immediately. The VM has no bridged or direct home-LAN adapter.

## Network configuration

| Field | Value |
|---|---|
| Interface | `enp0s3` |
| IPv4 address | `10.10.20.10/24` |
| Default gateway | `10.10.20.1` |
| DNS server | `10.10.20.1` |
| Connected subnet | `10.10.20.0/24` |

All routed traffic passes through `fw01`. OPNsense permits only the services required for a basic managed server: DNS to the firewall, outbound NTP, outbound HTTP, outbound HTTPS, and SSH from the single management host `admin01`.

## Minimum-access policy

The implemented DMZ policy is evaluated from top to bottom:

1. Allow logged IPv4 TCP/UDP DNS from `DMZ network` to `DMZ address` on port 53.
2. Block and log IPv4 traffic from `DMZ network` to `LAN network`.
3. Block and log IPv4 traffic from `DMZ network` to `ATTACK network`.
4. Allow and log IPv4 UDP from `DMZ network` to any destination on port 123.
5. Allow and log IPv4 TCP from `DMZ network` to any destination on port 80.
6. Allow and log IPv4 TCP from `DMZ network` to any destination on port 443.
7. Deny all other traffic through OPNsense's default-deny policy.

The LAN policy includes one exception above the broader LAN-to-DMZ block:

- Allow and log IPv4 TCP from `10.10.10.50` to `10.10.20.10/32` on SSH port 22.

## Acceptance results

- DNS resolution returned public IPv4 and IPv6 records for `archive.ubuntu.com`.
- HTTP and HTTPS requests to `archive.ubuntu.com` each returned `HTTP/1.1 200 OK`.
- `timedatectl status` reported `System clock synchronized: yes` and `NTP service: active`.
- DMZ probes to `admin01` (`10.10.10.50`) and the ATTACK gateway (`10.10.30.1`) each produced 100% packet loss.
- An ICMP probe to `1.1.1.1` produced 100% packet loss, demonstrating that the web rules did not create a general internet allow.
- SSH from `admin01` to `ubuntu-01` succeeded and presented the Ubuntu 24.04.4 LTS login banner.
- A ping from `admin01` to `ubuntu-01` still produced 100% packet loss, proving that the SSH exception did not bypass the broader LAN-to-DMZ block.
- OPNsense Live View showed logged NTP passes and default-deny ICMP blocks for source `10.10.20.10`.

See [NET-003](../evidence/2026-07-29_NET-003_dmz-minimum-access.md) for the detailed test record.

## Recovery observation

After the initial acceptance tests, the local console stopped accepting keyboard input and SSH timed out. Releasing and recapturing the VirtualBox keyboard did not recover the guest, and an ACPI shutdown signal received no response. An authorized `ubuntu-01`-only cold power cycle restored the VM while `fw01` and `admin01` remained running. Ubuntu booted from its existing disk, retained `10.10.20.10`, and accepted login normally.

## Baseline snapshot

| Field | Value |
|---|---|
| Snapshot name | `ubuntu-01-baseline-2026-07-30` |
| Snapshot type | Cold snapshot; VM powered off |
| Snapshot date | 2026-07-30 |
| Validation basis | Installation, addressing, minimum-access policy, SSH administration, isolation, and firewall-log tests passed |

This is the single retained recovery point for `ubuntu-01`. Future changes are written to a growing differencing disk, so additional snapshots will be limited to meaningful milestones and available host space will be checked before major updates.

## Remaining work

- [x] Take one storage-conscious baseline snapshot after confirming available host space.
- [ ] Apply controlled operating-system updates through the validated DNS/HTTP/HTTPS policy.
- [ ] Install only the server and telemetry components required by later exercises.
- [ ] Establish a separate backup/export process for critical configuration and sanitized evidence.
