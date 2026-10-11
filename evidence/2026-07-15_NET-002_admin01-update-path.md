# NET-002 — admin01 update-path acceptance test

**Date:** 2026-07-15  
**Asset:** `admin01`  
**Purpose:** Confirm that the management VM remains on the isolated lab network while obtaining Debian repository metadata through OPNsense.

## Network identity

- Active interface: `enp0s3`
- Lab IPv4 address: `10.10.10.50/24`
- Default route: `10.10.10.1` through `enp0s3`
- Connected route: `10.10.10.0/24`, source `10.10.10.50`
- No physical home-network IPv4 address was present.
- An automatic `fe80::/64` link-local address was present; no routed IPv6 access was configured.

## Repository test

`sudo apt update` successfully contacted:

- `security.debian.org` for Debian security metadata
- `deb.debian.org` for the Debian release and update metadata

The command fetched 90.7 kB of metadata and completed with `All packages are up to date.` No unreachable-source, DNS, routing, or signature errors were observed.

## Conclusion

`admin01` can use the controlled OPNsense IPv4 egress path for Debian maintenance while remaining addressed only on `LAB-LAN`.
