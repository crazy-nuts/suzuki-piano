from pathlib import Path
from datetime import date
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
import os

BASE_URL = "https://crazy-nuts.github.io/suzuki-piano"
ROOT = Path(os.getcwd())

html_files = []

# ----------------------------
# 収集
# ----------------------------

# トップ
index_path = ROOT / "index.html"
if index_path.exists():
    html_files.append(index_path)

# blog配下
blog_dir = ROOT / "blog"
if blog_dir.exists():
    html_files.extend(blog_dir.glob("*.html"))

# ----------------------------
# XML生成
# ----------------------------

urlset = ET.Element(
    "urlset",
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
)

today = date.today().isoformat()

for path in html_files:
    rel = path.relative_to(ROOT).as_posix()

    # URL正規化（ここ重要）
    if rel == "index.html":
        url_path = ""
    elif rel.endswith("index.html"):
        url_path = rel.replace("index.html", "")
    else:
        url_path = rel

    url = ET.SubElement(urlset, "url")

    loc = ET.SubElement(url, "loc")
    loc.text = f"{BASE_URL}/{url_path}"

    lastmod = ET.SubElement(url, "lastmod")
    lastmod.text = today

    priority = ET.SubElement(url, "priority")

    if rel == "index.html":
        priority.text = "1.0"
    elif rel == "blog/index.html":
        priority.text = "0.9"
    else:
        priority.text = "0.8"

# ----------------------------
# 整形して書き出し（ここが今回の核心）
# ----------------------------

rough_string = ET.tostring(urlset, 'utf-8')
reparsed = md.parseString(rough_string)

with open(ROOT / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write(reparsed.toprettyxml(indent="  "))
