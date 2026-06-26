@echo off
REM Kozbeyli - Meta reklam Claude skill'lerini kur (Windows)
echo Meta reklam skill'leri kuruluyor...
call npx skills add https://github.com/AgriciDaniel/claude-ads
call npx skills add https://github.com/ComposioHQ/awesome-claude-skills/tree/master/competitive-ads-extractor
echo.
echo On kosul: set META_ACCESS_TOKEN=...  (sohbete/URL'ye YAZMA)
echo Skill'ler: /spy /competitive-ads-extractor /bulk-creative "/ads meta" /ads-score (docs/11)
pause
