import json
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote

root = Path(__file__).resolve().parents[1]
tools = json.loads((root / "data/tools.json").read_text(encoding="utf-8"))
groups = defaultdict(list)
for tool in tools:
    groups[tool["category"]].append(tool)
lines = ["<p align=\"center\"><img src=\"assets/banner.svg\" alt=\"Best Free AI Tools Directory\" width=\"100%\"></p>\n\n# Best Free AI Tools Directory\n\nDiscover AI image generators, video tools, coding assistants, AI agents, automation software, local AI models and open-source alternatives. Compare projects and check free access and licensing.\n\n**[Explore the interactive directory](https://vaibcc.github.io/free-ai-tools-directory/)** · [Download full JSON catalog](data/tools.json) · [Suggest a project](https://github.com/vaibcc/free-ai-tools-directory/issues)\n\nCatalog inclusion does not guarantee that a project is free, actively maintained or independently verified. Check licenses, free-plan limits and hosting requirements.\n\n", "## Catalog overview", "", f"**{len(tools):,} listings · {len(groups)} populated categories**", "", "| Category | Listings | Browse |", "| --- | ---: | --- |"]
badges = "<p align=\"center\">\n  <img src=\"https://img.shields.io/badge/Catalog-CATALOGCOUNT-007ec6\" alt=\"Catalog listings\">\n  <img src=\"https://img.shields.io/badge/Categories-CATEGORYCOUNT-16877c\" alt=\"Populated categories\">\n  <img src=\"https://img.shields.io/badge/Updates-Automated-8957e5\" alt=\"Automated updates\">\n  <img src=\"https://img.shields.io/badge/Access-Free-238636\" alt=\"Free directory access\">\n  <img src=\"https://img.shields.io/github/license/vaibcc/free-ai-tools-directory\" alt=\"Repository license\">\n  <img src=\"https://img.shields.io/badge/Hosting-GitHub%20Pages-555555\" alt=\"GitHub Pages\">\n  <img src=\"https://img.shields.io/github/stars/vaibcc/free-ai-tools-directory\" alt=\"GitHub stars\">\n  <img src=\"https://img.shields.io/github/forks/vaibcc/free-ai-tools-directory\" alt=\"GitHub forks\">\n  <img src=\"https://img.shields.io/github/last-commit/vaibcc/free-ai-tools-directory\" alt=\"Last commit\">\n</p>\n\n".replace("CATALOGCOUNT", quote(f"{len(tools):,}", safe="")).replace("CATEGORYCOUNT", str(len(groups)))
lines[0] = lines[0].replace("# Best Free AI Tools Directory\n\n", "# Best Free AI Tools Directory\n\n" + badges)
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
