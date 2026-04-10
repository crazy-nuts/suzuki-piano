from pathlib import Path
from datetime import date
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
import os

BASE_URL = "https://crazy-nuts.github.io/suzuki-piano"
ROOT = Path(os.getcwd())

html_files = []

# ----------------------------
# ファイル収集
# ----------------------------

for path in ROOT.rglob("*.html"):
    # sitemap自身は除外
    if "google" in path.name:
        continue
    html_files.append(path)

# ----------------------------
# XML構築
# ----------------------------

urlset = ET.Element("urlset")
urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

today = date.today().isoformat()

for path in html_files:
    rel = path.relative_to(ROOT).as_posix()

    # URL正規化
    if rel == "index.html":
        url_path = ""
    elif rel.endswith("index.html"):
        url_path = rel.replace("index.html", "")
    else:
        url_path = rel

    url = ET.SubElement(urlset, "url")

    ET.SubElement(url, "loc").text = f"{BASE_URL}/{url_path}"
    ET.SubElement(url, "lastmod").text = today
    ET.SubElement(url, "priority").text = "0.8"

# ----------------------------
# XML整形（ここが重要）
# ----------------------------

rough_string = ET.tostring(urlset, 'utf-8')
reparsed = md.parseString(rough_string)

pretty_xml = reparsed.toprettyxml(indent="  ")

# ----------------------------
# 上書き保存（絶対これ）
# ----------------------------

with open(ROOT / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml)
    
