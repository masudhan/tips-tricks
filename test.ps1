# Define variables
$serverInstance = "YourServerInstance"
$databaseName = "YourDatabaseName"
$backupPath = "C:\Backup\YourDatabaseName.bak"
$sqlUser = "YourSqlUser"
$sqlPassword = "YourSqlPassword"

# Backup command
sqlcmd -S $serverInstance -U $sqlUser -P $sqlPassword -Q "BACKUP DATABASE [$databaseName] TO DISK='$backupPath' WITH FORMAT, INIT"

# Restore command
sqlcmd -S $serverInstance -U $sqlUser -P $sqlPassword -Q "RESTORE DATABASE [$databaseName] FROM DISK='$backupPath' WITH REPLACE, RECOVERY"
