import json
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote

root = Path(__file__).resolve().parents[1]
tools = json.loads((root / "data/tools.json").read_text(encoding="utf-8"))
groups = defaultdict(list)
for tool in tools:
    groups[tool["category"]].append(tool)
lines = ["<p align=\"center\"><img src=\"assets/banner.svg\" alt=\"Free AI Tools Directory\" width=\"100%\"></p>\n\n# Free AI Tools Directory\n\nBrowse AI software, open-source projects and development resources across the categories actually present in the catalog.\n\n**[Explore the interactive directory](https://vaibcc.github.io/free-ai-tools-directory/)** · [Download full JSON catalog](data/tools.json) · [Suggest a project](https://github.com/vaibcc/free-ai-tools-directory/issues)\n\nCatalog inclusion does not guarantee that a project is free, actively maintained or independently verified. Check licenses, free-plan limits and hosting requirements.\n\n", "## Catalog overview", "", f"**{len(tools):,} listings · {len(groups)} populated categories**", "", "| Category | Listings | Browse |", "| --- | ---: | --- |"]
for category, entries in sorted(groups.items()):
    anchor = category.lower().replace(" ", "-")
    lines.append(f"| {category} | {len(entries):,} | [View examples](#{anchor}) |")
lines.extend(["", "## Category highlights", ""])
for category, entries in sorted(groups.items()):
    lines.extend([f"### {category}", ""])
    valid = [t for t in entries if t.get("url", "").startswith("https://")]
    for tool in sorted(valid, key=lambda x: x["name"].lower())[:8]:
        name = tool["name"].replace("[", "\\[").replace("]", "\\]").replace("\n", " ")
        url = quote(tool["url"], safe=":/?&=#%+@")
        lines.append(f"- [{name}]({url})")
    lines.extend(["", "[Browse all listings on the website](https://vaibcc.github.io/free-ai-tools-directory/)", ""])
lines.extend(["## Contributing", "", "Suggest additions or corrections through GitHub Issues. The catalog and this overview are refreshed automatically.", ""])
(root / "README.md").write_text("\n".join(lines), encoding="utf-8")
