[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

Write-Host 'Cybersecurity Home Lab - Host Readiness' -ForegroundColor Cyan

$inventoryAvailable = $true
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $computer = Get-CimInstance Win32_ComputerSystem
    $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
    $systemDrive = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$($os.SystemDrive)'"

    $ramGb = [math]::Round($computer.TotalPhysicalMemory / 1GB, 1)
    $freeGb = [math]::Round($systemDrive.FreeSpace / 1GB, 1)
    $logicalProcessors = $cpu.NumberOfLogicalProcessors
    $operatingSystem = $os.Caption
    $virtualization = if ($null -ne $cpu.VirtualizationFirmwareEnabled) {
        $cpu.VirtualizationFirmwareEnabled
    } else {
        'Unknown (check Task Manager > Performance > CPU)'
    }
} catch {
    $inventoryAvailable = $false
    $systemDriveName = if ($env:SystemDrive) { $env:SystemDrive.TrimEnd(':') } else { 'C' }
    $drive = Get-PSDrive -Name $systemDriveName -ErrorAction SilentlyContinue
    $ramGb = 'Unavailable'
    $freeGb = if ($drive) { [math]::Round($drive.Free / 1GB, 1) } else { 'Unavailable' }
    $logicalProcessors = [Environment]::ProcessorCount
    $operatingSystem = [Environment]::OSVersion.VersionString
    $virtualization = 'Unknown (check Task Manager > Performance > CPU)'
    Write-Warning 'Detailed hardware inventory was blocked. The partial result below is safe to use; verify RAM and virtualization manually.'
}

$profile = if (-not $inventoryAvailable) {
    'Manual assessment required'
} elseif ($ramGb -ge 32 -and $freeGb -ge 350 -and $logicalProcessors -ge 8) {
    'Recommended'
} elseif ($ramGb -ge 16 -and $freeGb -ge 120 -and $logicalProcessors -ge 4) {
    'Lean'
} elseif ($ramGb -ge 16 -and $freeGb -ge 75 -and $logicalProcessors -ge 4) {
    'Storage-saver - dynamic disks, short retention, one endpoint at a time'
} else {
    'Below storage-saver profile - free space or reduce scope before building'
}

[pscustomobject]@{
    ComputerName           = $env:COMPUTERNAME
    OperatingSystem        = $operatingSystem
    LogicalProcessors      = $logicalProcessors
    MemoryGB               = $ramGb
    SystemDriveFreeGB      = $freeGb
    FirmwareVirtualization = $virtualization
    SuggestedProfile       = $profile
} | Format-List

Write-Host 'Keep this output private: the computer name may identify you.' -ForegroundColor Yellow
