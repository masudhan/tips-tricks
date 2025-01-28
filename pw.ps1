<#
.SYNOPSIS
Export/Import MSSQL tables between databases using BCP with Azure DevOps Release Pipeline variables.
#>

param(
    [string]$SourceServer,
    [string]$SourceDatabase,
    [string]$SourceUser,
    [string]$SourcePassword,
    [string]$DestinationServer,
    [string]$DestinationDatabase,
    [string]$DestinationUser,
    [string]$DestinationPassword,
    [string]$Tables,  # Comma-separated table names from Azure variables
    [string]$BCPFormatFile = ""  # Optional format file
)

$ErrorActionPreference = "Stop"

# Convert comma-separated tables to array
$tableArray = $Tables -split ',' | ForEach-Object { $_.Trim() }

function Invoke-BcpExport {
    param($Table, $OutputFile)
    try {
        Write-Host "##[command]Exporting table: $Table"
        $bcpCommand = "bcp `"$SourceDatabase.dbo.$Table`" out `"$OutputFile`" -S $SourceServer -U $SourceUser -P $SourcePassword -c -C 65001 -N -k"
        Invoke-Expression $bcpCommand
        if ($LASTEXITCODE -ne 0) { throw "BCP export failed" }
    }
    catch {
        Write-Host "##vso[task.logissue type=error]Error exporting $Table : $_"
        exit 1
    }
}

function Invoke-BcpImport {
    param($Table, $InputFile)
    try {
        Write-Host "##[command]Importing table: $Table"
        
        # Truncate target table
        $truncateCommand = "sqlcmd -S $DestinationServer -U $DestinationUser -P $DestinationPassword -d $DestinationDatabase -Q `"TRUNCATE TABLE dbo.$Table`""
        Invoke-Expression $truncateCommand
        if ($LASTEXITCODE -ne 0) { throw "Truncate failed" }

        # Import data
        $bcpParams = if ($BCPFormatFile) { "-f `"$BCPFormatFile`"" } else { "-c -C 65001 -N -k" }
        $importCommand = "bcp `"$DestinationDatabase.dbo.$Table`" in `"$InputFile`" -S $DestinationServer -U $DestinationUser -P $DestinationPassword $bcpParams"
        Invoke-Expression $importCommand
        if ($LASTEXITCODE -ne 0) { throw "BCP import failed" }
    }
    catch {
        Write-Host "##vso[task.logissue type=error]Error importing $Table : $_"
        exit 1
    }
}

# Main execution
try {
    $tempDir = New-Item -ItemType Directory -Path "$env:AGENT_TEMPDIRECTORY\BCP_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Force

    foreach ($table in $tableArray) {
        $exportFile = Join-Path -Path $tempDir -ChildPath "$table.dat"
        Invoke-BcpExport -Table $table -OutputFile $exportFile
        Invoke-BcpImport -Table $table -InputFile $exportFile
    }

    Write-Host "##[section]All tables migrated successfully!"
    exit 0
}
catch {
    Write-Host "##vso[task.logissue type=error]Fatal error: $_"
    exit 1
}
finally {
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}