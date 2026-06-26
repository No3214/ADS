#!/usr/bin/env python3
"""RSA basliklarini (<=30) ve aciklamalarini (<=90) dogrular. Turkce karakterler
tek karakter sayilir (Google da boyle sayar). Cikis: 0 uygun, 1 sorun."""
import re, sys, pathlib

lines = pathlib.Path("assets/google-rsa-tr.yaml").read_text(encoding="utf-8").splitlines()

def grab(name):
    items, inblk = [], False
    for ln in lines:
        if re.match(rf'^{re.escape(name)}:\s*(#.*)?$', ln):
            inblk = True; continue
        if inblk:
            if re.match(r'^[A-Za-z_]', ln):   # sonraki ust-seviye anahtar
                break
            m = re.match(r'^\s*-\s*"(.+?)"\s*$', ln)
            if m: items.append(m.group(1))
    return items

h, d = grab("headlines"), grab("descriptions")
ok = True
print(f"Basliklar: {len(h)} adet (hedef 15)")
for x in h:
    n = len(x); over = n > 30; ok &= not over
    print(f"  {n:2d}  {x}" + ("  <== ASIYOR" if over else ""))
print(f"Aciklamalar: {len(d)} adet (hedef 4)")
for x in d:
    n = len(x); over = n > 90; ok &= not over
    print(f"  {n:2d}  {x}" + ("  <== ASIYOR" if over else ""))
good = ok and len(h) == 15 and len(d) == 4
print("SONUC:", "UYGUN" if good else "SORUN VAR")
sys.exit(0 if good else 1)
