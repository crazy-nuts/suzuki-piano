from pathlib import Path
from datetime import date
import xml.etree.ElementTree as ET

BASE_URL = "https://crazy-nuts.github.io/suzuki-piano"

# scripts/generate_sitemap.py を基準に、1つ上をサイトルートにする
ROOT = Path(__file__).resolve().parent.parent

html_files = []

# トップ
index_path = ROOT / "index.html"
if index_path.exists():
    html_files.append(index_path)

# blog配下
blog_dir = ROOT / "blog"
if blog_dir.exists():
    html_files.extend(sorted(blog_dir.glob("*.html")))

urlset = ET.Element(
    "urlset",
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
)

today = date.today().isoformat()


def to_public_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()

    # 正規URLに揃える
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel == "blog/index.html":
        return f"{BASE_URL}/blog/"

    return f"{BASE_URL}/{rel}"


for path in html_files:
    rel = path.relative_to(ROOT).as_posix()

    url = ET.SubElement(urlset, "url")

    loc = ET.SubElement(url, "loc")
    loc.text = to_public_url(path)

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
tree.write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
