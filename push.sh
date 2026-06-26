#!/usr/bin/env bash
# Kozbeyli Konagi - GitHub'a yukle (mac/linux)
set -e
cd "$(dirname "$0")"
[ -d .git ] && rm -rf .git
git init -b main
git config user.name "Yunuscan Oruk"
git config user.email "yunuscanoruk@gmail.com"
git add -A
git commit -m "feat: kads v1.0 - Kozbeyli Konagi reklam & dijital operasyon sistemi"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/No3214/ADS.git
git push -u origin main
echo "Bitti. Repo yoksa once github.com/No3214/ADS olustur."
