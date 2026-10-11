# NET-003 — DMZ minimum-access firewall acceptance

**Date:** 2026-07-29  
**DMZ asset:** `ubuntu-01` (`10.10.20.10/24`)  
**Management asset:** `admin01` (`10.10.10.50/24`)  
**Firewall:** `fw01` (OPNsense `26.1.6_2`)  
**Scope:** DMZ egress allowlisting, inter-zone isolation, and narrow SSH administration

## Policy under test

| Interface | Action | Source | Destination | Protocol / port | Logging |
|---|---|---|---|---|---|
| DMZ | Pass | `DMZ network` | `DMZ address` | TCP/UDP 53 | Enabled |
| DMZ | Block | `DMZ network` | `LAN network` | IPv4 any | Enabled |
| DMZ | Block | `DMZ network` | `ATTACK network` | IPv4 any | Enabled |
| DMZ | Pass | `DMZ network` | any | UDP 123 | Enabled |
| DMZ | Pass | `DMZ network` | any | TCP 80 | Enabled |
| DMZ | Pass | `DMZ network` | any | TCP 443 | Enabled |
| LAN | Pass | `10.10.10.50` | `10.10.20.10/32` | TCP 22 | Enabled |

The LAN SSH exception was placed above the existing logged LAN-to-DMZ block. All unlisted DMZ traffic remained subject to default deny.

## Results

| Test | Observation | Result |
|---|---|---|
| DNS | `resolvectl query archive.ubuntu.com` returned multiple IPv4 and IPv6 addresses | Pass |
| HTTP | `curl -I --max-time 15 http://archive.ubuntu.com/` returned `HTTP/1.1 200 OK` | Pass |
| HTTPS | `curl -I --max-time 15 https://archive.ubuntu.com/` returned `HTTP/1.1 200 OK` | Pass |
| NTP | `timedatectl status` showed synchronized clock and active NTP service | Pass |
| DMZ to LAN | `ping -c 4 10.10.10.50`: 4 transmitted, 0 received, 100% loss | Pass — blocked |
| DMZ to ATTACK | `ping -c 4 10.10.30.1`: 4 transmitted, 0 received, 100% loss | Pass — blocked |
| DMZ unapproved internet traffic | `ping -c 4 1.1.1.1`: 4 transmitted, 0 received, 100% loss | Pass — default deny |
| Management SSH | `ssh labadmin@10.10.20.10` from `admin01` reached Ubuntu 24.04.4 LTS | Pass |
| Non-SSH LAN to DMZ | `ping -c 4 10.10.20.10` from `admin01`: 4 transmitted, 0 received, 100% loss | Pass — blocked |

## Log correlation

OPNsense Live View used the active filter:

`src contains 10.10.20.10`

The filtered view showed:

- Green UDP pass entries to public port 123 destinations labeled `Allow DMZ NTP outbound`.
- Red ICMP blocks to `1.1.1.1` labeled `Default deny / state violation rule`.

The successful application tests, failed isolation probes, and firewall log actions agree with the intended first-match policy.

## Recovery event

During testing, `ubuntu-01` stopped accepting console input and became unreachable over SSH. Keyboard recapture and ACPI shutdown did not recover it. An authorized cold power cycle affected only `ubuntu-01`; `fw01` and `admin01` remained running. The VM booted normally, retained `10.10.20.10`, and the interrupted isolation tests then completed successfully.

## Conclusion

The DMZ server can resolve names, synchronize time, and use web repositories without receiving unrestricted network access. Inter-zone isolation remains enforced in both directions, while a single logged management path permits SSH from `admin01` to `ubuntu-01`.
