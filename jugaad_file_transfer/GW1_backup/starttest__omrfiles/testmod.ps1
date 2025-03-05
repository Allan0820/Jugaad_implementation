# Original string
$hash = "hashfile.dat"

# Remove the file extension
$hash = [System.IO.Path]::GetFileNameWithoutExtension($hash)

# Verify the modification
Write-Host "Modified hash:" $hash
