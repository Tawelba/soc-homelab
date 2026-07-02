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