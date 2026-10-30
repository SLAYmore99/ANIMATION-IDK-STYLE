@echo off
rem Un-XORs (0x5A) and joins the parts into LIFE_ON_CLAUDE_NINE_article_v5_ALPHA.mov, then prints its MD5.
rem Put this file in the same folder as all ALPHA_v5.partNN.xor files and double-click it.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$out=[IO.File]::Create('LIFE_ON_CLAUDE_NINE_article_v5_ALPHA.mov');" ^
 "Get-ChildItem 'ALPHA_v5.part*.xor' | Sort-Object Name | ForEach-Object {" ^
 "  $b=[IO.File]::ReadAllBytes($_.FullName); for($i=0;$i -lt $b.Length;$i++){ $b[$i]=$b[$i] -bxor 0x5A };" ^
 "  $out.Write($b,0,$b.Length); Write-Host 'joined' $_.Name };" ^
 "$out.Close()"
certutil -hashfile LIFE_ON_CLAUDE_NINE_article_v5_ALPHA.mov MD5
echo Expected MD5: 9d4f6c67fdfd68547de04670d6f66e94
pause
