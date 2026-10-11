# NET-001 — LAN firewall acceptance test

**Date:** 2026-07-15  
**Source asset:** `admin01` (`10.10.10.50/24`)  
**Firewall:** `fw01` (OPNsense `26.1.6_2`)  
**Scope:** IPv4 internet access, DNS resolution, and LAN isolation from DMZ and ATTACK

## Results

| Test | Observation | Result |
|---|---|---|
| Internet routing | `ping -c 4 1.1.1.1`: 4 transmitted, 4 received, 0% loss | Pass |
| DNS and internet | `ping -c 4 procrastination-fix.com`: resolved to `188.114.97.4`; 4 transmitted, 4 received, 0% loss | Pass |
| LAN to DMZ gateway | `ping -c 4 10.10.20.1`: 4 transmitted, 0 received, 100% loss | Pass — blocked as designed |
| LAN to ATTACK gateway | `ping -c 4 10.10.30.1`: 4 transmitted, 0 received, 100% loss | Pass — blocked as designed |
| Firewall logging | Live View showed four ICMP blocks for each isolated destination from `10.10.10.50` | Pass |

## Log correlation

OPNsense Live View correlated the failed pings with the intended first-match rules:

- `10.10.10.50` → `10.10.20.1`, ICMP, action `block`, label `Block LAN to DMZ`
- `10.10.10.50` → `10.10.30.1`, ICMP, action `block`, label `Block LAN to Attack`

This confirms the denials were enforced and logged by the configured LAN rules, rather than being caused only by an unavailable destination.

## Conclusion

`admin01` retained controlled IPv4 internet and DNS access while OPNsense blocked and logged LAN traffic to both isolated networks. Full bidirectional inter-zone testing remains pending until DMZ and ATTACK clients are deployed.
