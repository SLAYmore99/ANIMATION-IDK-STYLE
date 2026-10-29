# Run in the folder with the .bin:  powershell -ExecutionPolicy Bypass -File unxor_v4.ps1
$in  = "Change03_small_steps_v4_1080p.mp4.xor5a.bin"
$out = "Change03_small_steps_v4_1080p.mp4"
$b = [System.IO.File]::ReadAllBytes((Join-Path $PWD $in))
for ($i = 0; $i -lt $b.Length; $i++) { $b[$i] = $b[$i] -bxor 0x5A }
[System.IO.File]::WriteAllBytes((Join-Path $PWD $out), $b)
certutil -hashfile $out MD5
Write-Host "Expected MD5: 194347ee93568de707f61e92a9a95251"
