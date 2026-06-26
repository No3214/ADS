#!/usr/bin/env python3
from __future__ import annotations
import os, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def status(ok: bool, text: str) -> None:
    print(f"[{'OK' if ok else 'WARN'}] {text}")

for cmd in ('python3', 'claude', 'pipx', 'gcloud'):
    status(bool(shutil.which(cmd)), f"{cmd}: {'bulundu' if shutil.which(cmd) else 'eksik'}")

status((ROOT / '.mcp.json').exists(), ".mcp.json mevcut" if (ROOT / '.mcp.json').exists() else ".mcp.json eksik; örnek dosyayı kopyala")

for name, secret in (
    ('GOOGLE_APPLICATION_CREDENTIALS', False),
    ('GOOGLE_PROJECT_ID', False),
    ('GOOGLE_ADS_DEVELOPER_TOKEN', True),
):
    value = os.getenv(name, '').strip()
    status(bool(value), f"{name}: {'tanımlı, değer gizlendi' if value and secret else value or 'eksik'}")

meta = os.getenv('META_AD_ACCOUNT_ID', '')
status(bool(re.fullmatch(r'act_\d+', meta)), "Meta ad account: doğru" if re.fullmatch(r'act_\d+', meta) else "Meta ad account eksik; act_... gerekli")

google = re.sub(r'\D', '', os.getenv('GOOGLE_ADS_CUSTOMER_ID', ''))
status(len(google) == 10, "Google customer ID: doğru" if len(google) == 10 else "Google customer ID eksik; 10 hane gerekli")

status(os.getenv('ADS_WRITES_ENABLED', 'false').lower() != 'true', "Gerçek yazma işlemleri bloke" if os.getenv('ADS_WRITES_ENABLED', 'false').lower() != 'true' else "Gerçek yazma etkin; guardrail kontrollerini doğrula")
print("Google limit: 15.000 TL/ay; Meta limit: 15.000 TL/ay")
