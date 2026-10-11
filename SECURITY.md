# Security and responsible-use policy

## Authorized use only

Run exercises only in this isolated lab or on another system for which you have explicit written authorization. The presence of a public IP, hostname, or open service is not permission to test it.

## Lab containment rules

1. Use hypervisor **NAT** for the OPNsense WAN; do not use bridged networking.
2. Attach vulnerable targets only to named internal networks.
3. Do not configure inbound port forwarding from the host or home router.
4. Stop the exercise immediately if traffic reaches an unintended network.
5. Snapshot clean states before experiments and restore them afterward.
6. Use harmless simulations and test files; do not store live malware here.

## Never commit

- Passwords, API tokens, private keys, recovery codes, or cookies
- Public IP addresses, real internal addressing, MAC addresses, or device serials
- Personal names, email addresses, usernames, browser data, or document contents
- Raw packet captures, unredacted dashboards, VM disks, or configuration backups

Before publishing, run `scripts/windows/Test-Repository.ps1` and manually review every screenshot. Automated checks reduce risk but cannot prove an artifact is safe.

## Reporting a problem

If a repository artifact exposes sensitive information, remove it from the current tree, rotate the affected secret, and purge it from Git history before publishing. Treat a committed secret as compromised even if the repository was private.
