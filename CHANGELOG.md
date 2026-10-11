# Changelog

All notable project changes will be documented here. This project uses status-based learning releases rather than claiming unverified production readiness.

## [Unreleased]

### Planned

- Complete host capacity decision and software asset register
- Build and validate the segmented OPNsense network
- Enroll the approved Linux endpoints in Wazuh and validate telemetry
- Complete the first six detection exercises

### Changed

- Installed and validated a lean Kali Linux 2026.2 `kali-01` workstation on `LAB-ATTACK` with static address `10.10.30.10/24`, Xfce, and the Top 10 tool collection
- Recovered two repeatable installer partitioner stalls with a Kali-only cold power-off and verified PAE/NX enablement while leaving all other VM processes active
- Added logged ATTACK-interface DNS and NTP exceptions; correlated initial default-deny events in OPNsense Live View and validated DNS, repository access, and NTP synchronization
- Verified the Kali baseline at 7.4 GB used with 19 GB available and confirmed `virtualbox-guest-utils.service` active after reboot
- Added the `kali-01` build record and portfolio-safe KALI-002 baseline acceptance evidence; cold snapshot remains pending
- Downloaded and SHA-256 verified the official Kali Linux 2026.2 AMD64 installer ISO; recorded the exact local and published hashes in KALI-001 before VM creation
- Added a living all-in-one build guide that consolidates the verified lab workflow through DET-001 while preserving the original phased guide and individual build records
- Added a portfolio-ready A4 PDF edition with template-inspired curved-edge, fused-color teaching callouts, section banners, command blocks, architecture, troubleshooting, glossary, and evidence references; pending Kali steps are explicitly marked in progress
- Installed the Wazuh 4.14 all-in-one central stack on Ubuntu Server 24.04.4 LTS `siem01` at `10.10.10.10/24`
- Validated the Wazuh indexer, manager, Filebeat, dashboard, API listener, local HTTPS, and remote dashboard access
- Replaced the generated dashboard administrator credential through a private handoff and the official Wazuh password-management tool; no credential was recorded
- Disabled the Wazuh APT repository after installation to prevent accidental component upgrades
- Enabled a default-deny UFW policy on `siem01`, limiting SSH and dashboard access to `admin01` and staging agent ports 1514/1515 only for `admin01` and `ubuntu-01`
- Created the cold pre-install recovery point `siem01-clean-os-2026-07-30`
- Created the cold post-install recovery point `siem01-wazuh-baseline-2026-07-30` after service, firewall, SSH, and dashboard validation
- Added a logged OPNsense exception from `ubuntu-01` to `siem01` for Wazuh TCP 1514–1515 above the DMZ-to-LAN block
- Verified the DMZ Wazuh exception permits TCP 1514/1515 while TCP 443 to the dashboard remains blocked
- Installed and enabled Wazuh agents on `admin01` and `ubuntu-01`; the dashboard reported two active agents and zero disconnected agents
- Validated DET-001 with one authorized nonexistent-user SSH attempt; Wazuh produced rule 5710 at level 5 with the correct agent, source IP, and attempted username
- Added a portfolio-safe DET-001 report that distinguishes the true-positive detection from its benign authorized context
- Installed checksum-verified Ubuntu Server 24.04.4 LTS as `ubuntu-01` on `LAB-DMZ` with static address `10.10.20.10/24` and OpenSSH
- Implemented a logged DMZ minimum-access policy for firewall DNS, outbound NTP, HTTP, and HTTPS, with explicit DMZ-to-LAN and DMZ-to-ATTACK blocks
- Added a logged single-host SSH exception from `admin01` (`10.10.10.50`) to `ubuntu-01` (`10.10.20.10`) above the broader LAN-to-DMZ block
- Passed DMZ acceptance tests for DNS, NTP, HTTP, HTTPS, LAN isolation, ATTACK isolation, default deny, narrow SSH access, and non-SSH LAN blocking
- Correlated DMZ NTP passes and unapproved ICMP blocks in OPNsense Live View using source `10.10.20.10`
- Recovered a frozen `ubuntu-01` guest with an authorized ubuntu-only cold power cycle after console input and SSH stopped responding; `fw01` and `admin01` remained running
- Created the cold recovery point `ubuntu-01-baseline-2026-07-30` after DMZ acceptance testing
- Built Debian 13 `admin01` on `LAB-LAN` with static address `10.10.10.50/24` for firewall administration
- Renamed OPNsense OPT1 and OPT2 to DMZ and ATTACK
- Applied logged LAN-to-DMZ and LAN-to-ATTACK block rules above the IPv4 LAN allow rule
- Disabled the default IPv6 LAN allow rule for the current IPv4-only phase
- Recovered an unresponsive `admin01` input session with an admin01-only cold power cycle while leaving `fw01` running
- Passed LAN-side firewall acceptance tests for internet access, DNS, DMZ isolation, ATTACK isolation, and logged-rule correlation
- Verified `admin01` retained its isolated `10.10.10.50/24` address and completed `apt update` through OPNsense without repository errors
- Created the cold recovery point `admin01-baseline-2026-07-15` after acceptance testing and documented the management VM build and input-recovery incident
- Confirmed the post-snapshot `admin01` boot reached the Debian graphical login screen while `fw01` remained running

## [0.1.0] — 2026-07-14

### Added

- Project charter, safety boundaries, architecture, and capacity profiles
- Phased build and acceptance guide
- Monitoring, detection, incident response, and operations documentation
- 90-day daily practice plan and portfolio publishing guide
- Evidence, change, incident, asset, and case-study templates
- Windows readiness, log-creation, and repository validation scripts

### Changed

- Added a 75–100 GB storage-saver deployment with dynamic disks, short SIEM retention, one endpoint at a time, and a 20 GB safety floor
- Validated the 32 GB, 12-thread host for the storage-saver profile and isolated the project from existing training VMs
- Installed checksum-verified OPNsense 26.1.6 to `fw01` using a 20 GB dynamic ZFS disk and documented installer troubleshooting
- Set the firewall password through a private operator handoff, detached the installer, and validated the first disk boot into OPNsense 26.1.6_2
- Corrected the automatic interface assignment, configured three isolated IPv4 gateways, and validated the VirtualBox NAT path with zero packet loss
