"""Monkey/fuzz testi: kads CLI rastgele/bozuk girdide ASLA traceback ile cokmemeli;
her cagri int cikis kodu donmeli (kirilmaz CLI garantisi). doctor haric (ag yavas)."""
import random
import string
import pytest
from kads.cli import main

CMDS = ["config","plan","budget","kpi","keywords","creative","build","seo","presence","mcp",
        "skills","rules","audiences","report","golive","competitors","calendar","publish",
        "setup","status","apify","aeo","season","funnel","offers","web","b2b","selfcheck",
        "validate","guard","monitor","brief","pmax","demandgen","remarketing","utm",
        "attribution","allocate","conversions","version","help","bilinmeyen-xyz"]
FLAGS = ["--format","-f","--out","--metrics","--days","--revenue","--spend","--channel",
         "--url","--source","--medium","--campaign","--check","--approval","--n","-h","--help"]
VALS = ["table","json","yaml","md","csv","xml","","google","meta","all","offline","schema",
        "build","detail","packages","specs","rules","funnel","flow","ZZZ"]
JUNK = ["","--","-","---x","%s","../../etc/passwd","' OR 1=1 --",";ls","\t"," ","🔥","ç§ı",
        "999999999999","-1","0","{}","[]","NaN","None","--format","\x00bad"]

def _tok(rng):
    r = rng.random()
    if r < 0.45: return rng.choice(CMDS)
    if r < 0.70: return rng.choice(FLAGS)
    if r < 0.88: return rng.choice(VALS)
    if r < 0.95: return rng.choice(JUNK)
    return "".join(rng.choice(string.printable[:95]) for _ in range(rng.randint(0, 14)))

@pytest.mark.parametrize("seed", range(250))
def test_cli_never_crashes(seed, tmp_path, capsys):
    rng = random.Random(seed)
    argv = [_tok(rng) for _ in range(rng.randint(0, 5))]
    # --out gecerse gercek tmp dizinine yaz (repoyu kirletme)
    argv = [str(tmp_path) if (i and argv[i-1] == "--out") else a for i, a in enumerate(argv)]
    rc = main(argv)               # cokerse pytest hatasi = gercek bug
    assert isinstance(rc, int)
    capsys.readouterr()
