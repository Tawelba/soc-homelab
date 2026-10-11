# KALI-002 - Kali baseline acceptance

**Validation date:** 2026-07-31  
**Status:** Passed; cold snapshot pending  
**Environment:** Authorized, isolated home lab

## Objective

Validate the lean `kali-01` operating-system baseline, ATTACK-segment infrastructure access, time synchronization, storage use, and VirtualBox guest integration before creating a recovery snapshot.

## Implemented baseline

| Field | Validated value |
|---|---|
| Hostname | `kali-01` |
| Interface | `eth0` — `UP` |
| IPv4 address | `10.10.30.10/24` |
| Gateway | `10.10.30.1` |
| DNS | `10.10.30.1` |
| Time zone | `Africa/Accra` |
| NTP server observed | `162.159.200.1` |
| Root filesystem | 28 GB total; 7.4 GB used; 19 GB available |
| Guest integration | `virtualbox-guest-utils.service` active |
| Installed profile | Xfce and Kali Top 10 tools |

## Firewall validation

Initial DNS and NTP probes timed out and were correlated with OPNsense default-deny logging. The following ATTACK-interface rules were added above blocking rules:

1. Pass IPv4 TCP/UDP from `ATTACK net` to `ATTACK address`, destination port 53.
2. Pass IPv4 UDP from `ATTACK net` to any, source port any and destination port 123.

Both rules have logging enabled. After correction and application:

- DNS resolution for `kali.org` returned IPv4 addresses.
- Kali synchronized time successfully (`NTPSynchronized=yes`).
- The observed NTP packet count increased to 2.
- Repository metadata refresh completed without persistent warning or error output.

## Installation recovery evidence

The installer twice stopped at `Starting up the partitioner` while PAE/NX was disabled. The VDI was visible as a 30 GB SATA disk and the VirtualBox log contained no storage failure. PAE/NX was enabled during a `kali-01`-only maintenance action; the installer then reached disk selection and completed successfully.

The other lab VMs remained running throughout the Kali-only recovery. The Manager UI required a restart, but no `VirtualBoxVM.exe` process belonging to `fw01`, `admin01`, `ubuntu-01`, or `siem01` was terminated.

## Result

**Pass.** `kali-01` is current, storage-conscious, time-synchronized, integrated with VirtualBox, and connected only to the isolated ATTACK segment. Snapshot creation remains the final baseline action.
