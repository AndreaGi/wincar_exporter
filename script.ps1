#Ex: C:\Users\Andrea\PycharmProjects\wincar_exporter\script.ps1 -DbName 13_08 -DbPath C:\Users\Andrea\Desktop\dat_13_08\dat

param(
    [Parameter(Mandatory)]
    [string]$DbName,

    [Parameter(Mandatory)]
    [string]$DbPath

)

function Import-Tables {
    $tables = "clfo", "magaz", "stoaut", "com", "comrig", "magpro", "mov", "magdep"
    foreach ($table in $tables)
    {
        Write-Host "Importing $table"
        $make="ctutil -make $table $DbPath\xdd\$table.xdd"
        Write-Host $make
        Invoke-Expression $make

        $unload="vutil32.exe -unload $DbPath\d00\$table $DbPath\$table.dmp"
        Write-Host $unload
        Invoke-Expression $unload

        $load="ctutil -load $table $DbPath\$table.dmp A"
        Write-Host $load
        Invoke-Expression $load

        $sqlize="ctutil -sqlize $table $DbPath\xdd\$table.xdd ADMIN $DbName"
        Write-Host $sqlize
        Invoke-Expression $sqlize
        Write-Host "---- DONE $table ----"
    }
}

#if ($runCtadmn)
#{
#    Write Host "Set authentication with ctadmn: USER: ADMIN PASS:ADMIN 10 > 10 > COMPATIBILITY SQLIMPORT_ADMIN_PASSWORD"
#    Invoke-Expression "&  $toolPath\ctadmn.exe"
#}
#$DbName = Read-Host "Enter DB Name:"
Import-Tables

