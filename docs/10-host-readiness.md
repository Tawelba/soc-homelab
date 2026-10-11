# Host readiness record

**Assessment date:** 2026-07-15  
**Decision:** Approved for the storage-saver deployment

## Sanitized capacity evidence

| Check | Observed | Requirement | Result |
|---|---:|---:|---|
| Installed memory | 32 GB | 16 GB minimum | Pass |
| Logical processors | 12 | 4 minimum | Pass |
| Firmware virtualization | Enabled | Enabled | Pass |
| Dedicated VM volume free space | Approximately 90 GB | 75 GB storage-saver minimum | Pass with controls |
| VirtualBox | 7.2.12 | Current supported 7.2 release | Pass |

The computer name, physical serial numbers, MAC addresses, and other identifying values are deliberately excluded.

## Storage decision

- New project VMs will use `D:\CyberLab-VMs`.
- VM disks will be dynamically allocated VDI files.
- At least 20 GB must remain free on `D:`.
- Only OPNsense, Wazuh, and one endpoint will normally run or be retained as active project VMs at the same time.
- Existing training VMs are outside this project and will not be modified, deleted, or presented as project evidence.
- Every new-VM wizard must explicitly show `D:\CyberLab-VMs` before creation; this avoids relying on a user-profile-specific global default.

## Risks and controls

| Risk | Control |
|---|---|
| Dynamic disks grow unexpectedly | Check free space before and after each session |
| Wazuh indexes consume the volume | Short lab retention and weekly disk review |
| Snapshots accumulate | One validated clean snapshot per active VM |
| Old training VMs confuse evidence | Unique project names and separate storage folder |
| VM files synchronize to cloud storage | Keep live VM disks outside OneDrive |

## Next acceptance gate

The image, installation, disk boot, interface mapping, isolated-zone addresses, and WAN-to-NAT-gateway connectivity have been validated. The next gate is a small LAN client that can reach OPNsense without obtaining a physical home-network address; it will also enable web-interface naming and policy checks. See the [OPNsense build record](11-opnsense-build-record.md).
