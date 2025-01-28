<#
.SYNOPSIS
Backup and restore MSSQL database with target database renaming
#>

param (
    [string]$sourceServer,
    [string]$sourceDB,
    [string]$targetServer,
    [string]$targetDB,
    [string]$sqlUser,
    [string]$sqlPass
)

# Load SQL Server Module
try {
    Import-Module SqlServer -ErrorAction Stop
}
catch {
    Write-Host "##vso[task.logissue type=error]SQL Server module not installed"
    exit 1
}

# Backup file path
$backupPath = "$env:AGENT_TEMPDIRECTORY\$sourceDB-$(Get-Date -Format 'yyyyMMddHHmmss').bak"

try {
    # Step 1: Backup Source Database
    Write-Host "##[section]Backing up source database: $sourceDB"
    Backup-SqlDatabase `
        -ServerInstance $sourceServer `
        -Database $sourceDB `
        -BackupFile $backupPath `
        -Credential (New-Object System.Management.Automation.PSCredential ($sqlUser, (ConvertTo-SecureString $sqlPass -AsPlainText -Force))) `
        -CompressionOption On

    # Step 2: Drop Target Database (if exists)
    Write-Host "##[section]Dropping target database: $targetDB"
    $dropQuery = @"
    IF DB_ID('$targetDB') IS NOT NULL
    BEGIN
        ALTER DATABASE [$targetDB] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
        DROP DATABASE [$targetDB];
    END
"@

    Invoke-Sqlcmd `
        -ServerInstance $targetServer `
        -Query $dropQuery `
        -Username $sqlUser `
        -Password $sqlPass `
        -ErrorAction Stop

    # Step 3: Restore to Target Database with Renaming
    Write-Host "##[section]Restoring to target database: $targetDB"
    Restore-SqlDatabase `
        -ServerInstance $targetServer `
        -Database $targetDB `
        -BackupFile $backupPath `
        -ReplaceDatabase `
        -Credential (New-Object System.Management.Automation.PSCredential ($sqlUser, (ConvertTo-SecureString $sqlPass -AsPlainText -Force))) `
        -ErrorAction Stop

    Write-Host "##vso[task.complete result=Succeeded]"
}
catch {
    Write-Host "##vso[task.logissue type=error]$_"
    Write-Host "##vso[task.complete result=Failed]"
    exit 1
}
finally {
    # Cleanup backup file
    if (Test-Path $backupPath) {
        Remove-Item $backupPath -Force
    }
}
