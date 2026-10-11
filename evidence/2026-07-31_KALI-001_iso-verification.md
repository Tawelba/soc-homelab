# KALI-001 - Kali installer ISO verification

**Verification date:** 2026-07-31  
**Status:** Passed  
**Environment:** Authorized, isolated home lab

## Objective

Verify the integrity of the Kali Linux installer before attaching it to a new virtual machine. This prevents installation from a damaged or substituted image.

## Artifact

| Field | Verified value |
|---|---|
| Filename | `kali-linux-2026.2-installer-amd64.iso` |
| Local storage location | `D:\CyberLab-VMs\ISO\` |
| File size | `4,802,531,328` bytes |
| Hash algorithm | SHA-256 |
| Local SHA-256 | `6dbefacc95e3b556c19c48e8bae39b8b505e2d3a1aba0bfb7ab62b036c3d2ba3` |
| Official SHA-256 | `6dbefacc95e3b556c19c48e8bae39b8b505e2d3a1aba0bfb7ab62b036c3d2ba3` |
| Official checksum source | `https://old.kali.org/kali-images/kali-2026.2/SHA256SUMS` |

## Verification procedure

The local hash was calculated on the Windows host:

```powershell
Get-FileHash -LiteralPath 'D:\CyberLab-VMs\ISO\kali-linux-2026.2-installer-amd64.iso' -Algorithm SHA256
```

The resulting value was compared character-for-character with the entry for the same filename in Kali's official `SHA256SUMS` file.

## Result

**Pass.** The local and official SHA-256 values match exactly. The ISO is approved for attachment to `kali-01`.

## Capacity checkpoint

The D: volume reported approximately `120.73 GB` free after the ISO download. This is above the lab's `20 GB` stop threshold and supports creation of the planned `30 GB` dynamically allocated virtual disk. Dynamic allocation limits initial host-space consumption but does not reserve capacity.

