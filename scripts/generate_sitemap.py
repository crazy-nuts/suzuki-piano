from pathlib import Path
from datetime import date
import xml.etree.ElementTree as ET
import os

BASE_URL = "https://crazy-nuts.github.io/suzuki-piano"

ROOT = Path(os.getcwd())

html_files = []

# トップ
index_path = ROOT / "index.html"
if index_path.exists():
    html_files.append(index_path)

# blog配下
blog_dir = ROOT / "blog"
if blog_dir.exists():
    html_files.extend(blog_dir.glob("*.html"))

urlset = ET.Element(
    "urlset",
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
)

today = date.today().isoformat()

for path in html_files:
    rel = path.relative_to(ROOT).as_posix()

    url = ET.SubElement(urlset, "url")

    loc = ET.SubElement(url, "loc")
    loc.text = f"{BASE_URL}/{rel}"

    lastmod = ET.SubElement(url, "lastmod")
    lastmod.text = today

    priority = ET.SubElement(url, "priority")

    if rel == "index.html":
        priority.text = "1.0"
    elif rel == "blog/index.html":
        priority.text = "0.9"
    else:
        priority.text = "0.8"

tree = ET.ElementTree(urlset)
tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
