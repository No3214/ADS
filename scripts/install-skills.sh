#!/usr/bin/env bash
# Kozbeyli — Meta reklam Claude skill'lerini kur (analiz/read tarafı).
# Topluluk skill'leri: production'da kullanmadan önce fork + audit (docs/04, docs/10).
set -e
echo "Meta reklam skill'leri kuruluyor (npx skills add)..."
npx skills add https://github.com/AgriciDaniel/claude-ads
npx skills add https://github.com/ComposioHQ/awesome-claude-skills/tree/master/competitive-ads-extractor
echo ""
echo "Ön koşul: export META_ACCESS_TOKEN=...  (Meta Ad Library API; sohbete/URL'ye YAZMA)"
echo "Skill'ler: /spy /competitive-ads-extractor /bulk-creative '/ads meta' /ads-score (docs/11)"
