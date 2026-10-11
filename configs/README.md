# Configuration examples

Store only reviewed, non-secret, portable examples here. Every configuration should state its target version, purpose, validation test, rollback, and source.

Do not commit full OPNsense exports, Wazuh credential bundles, agent keys, certificates, private keys, environment files, or copied third-party configurations without checking their license.

Recommended future layout:

```text
configs/
├── opnsense/       # sanitized aliases and rule tables, not raw backups
├── sysmon/         # reviewed configuration and test notes
├── wazuh/          # local rules/decoders and validation records
└── linux/          # narrowly scoped audit/FIM examples
```
