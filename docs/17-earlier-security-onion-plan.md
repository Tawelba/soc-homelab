# Earlier repository plan — historical

This was the repository overview before the Wazuh/OPNsense lab snapshot was added on 11 October 2026. It is retained as an earlier proposal, not evidence that the listed tools were deployed. The current implementation is described in the root README and dated build records.

# SOC Homelab 🛡️

A home Security Operations Center (SOC) laboratory built for practicing threat detection, incident response, and security monitoring.

## Architecture

- **SIEM Platform**: Security Onion
- **Log Sources**: Sysmon, Apache logs, Windows Event Logs
- **Detection Rules**: Custom Sigma rules + Suricata signatures
- **Attack Simulation**: Atomic Red Team

## Tools Used

- Security Onion (SIEM + NSM)
- Wireshark / tcpdump
- Suricata IDS/IPS
- Elasticsearch / Kibana
- Sigma (rule format)

## Labs Completed

*Coming soon*

## Getting Started

1. Install Security Onion on a VM (minimum 8GB RAM, 4 cores)
2. Configure log sources
3. Deploy detection rules
4. Run attack simulations with Atomic Red Team

## Resources

- [Security Onion Documentation](https://docs.securityonion.net/)
- [Sigma Rules Repository](https://github.com/SigmaHQ/sigma)
- [Atomic Red Team](https://atomicredteam.io/)
