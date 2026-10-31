"""Build the hosted copy of the BlackSeed landing page and (optionally) deploy it.

landing/index.html is written for claude.ai Artifacts (no <html>/<head>/<body>),
so this wraps it in a full document with Open Graph tags for Facebook sharing.

  python build.py           # rebuild site/ from ../landing
  python build.py --deploy  # rebuild, commit and push to GitHub Pages
"""
import shutil
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
LANDING = SITE.parent / "landing"
BASE_URL = "https://targoostore-web.github.io/blackseed/"

HEAD = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}">
<meta property="og:title" content="BlackSeed — توب لاين">
<meta property="og:description" content="مجموعة BlackSeed الاحترافية للعناية بالشعر: شامبو، ماسك، سيروم وعطر شعر في علبة هدية. اطلبوها الآن من توب لاين، الخليل.">
<meta property="og:image" content="{BASE_URL}assets/collection.jpg">
<meta property="og:locale" content="ar_AR">
<meta name="twitter:card" content="summary_large_image">
<style>body{{margin:0}}</style>
</head>
<body>
"""
TAIL = "\n</body>\n</html>\n"


def build():
    src = (LANDING / "index.html").read_text(encoding="utf-8")
    (SITE / "index.html").write_text(HEAD + src + TAIL, encoding="utf-8", newline="\n")
    shutil.rmtree(SITE / "assets", ignore_errors=True)
    shutil.copytree(LANDING / "assets", SITE / "assets", ignore=shutil.ignore_patterns(".*"))
    (SITE / ".nojekyll").touch()
    print("built", SITE / "index.html")


def deploy():
    git = ["git", "-C", str(SITE)]
    subprocess.run(git + ["add", "-A"], check=True)
    if subprocess.run(git + ["diff", "--cached", "--quiet"]).returncode == 0:
        print("nothing changed")
        return
    subprocess.run(git + ["commit", "-m", "Update landing page"], check=True)
    subprocess.run(git + ["push"], check=True)
    print("pushed; live at", BASE_URL, "in about a minute")


if __name__ == "__main__":
    build()
    if "--deploy" in sys.argv:
        deploy()
