import json
from pathlib import Path
from collections import defaultdict
root = Path(__file__).resolve().parents[1]
tools = json.loads((root / "data/tools.json").read_text())
readme = root / "README.md"
text = readme.read_text()
prefix = text.split("## Tool directory")[0]
import re
prefix = re.sub(r'Catalog-\d+_tools', f'Catalog-{len(tools)}_tools', prefix)
prefix = re.sub(r'alt="\d+ tools"', f'alt="{len(tools)} tools"', prefix)
groups = defaultdict(list)
for tool in tools:
    groups[tool["category"]].append(tool)
lines = [prefix.rstrip(), "", "## Tool directory", "", f"**{len(tools):,} listings**", ""]
for category, entries in sorted(groups.items()):
    lines.extend([f"### {category} ({len(entries)})", ""])
    for tool in sorted(entries, key=lambda x: x["name"].lower()):
        name = tool["name"].replace("[", "\\[").replace("]", "\\]").replace("\n", " ")
        url = tool["url"].replace(" ", "%20").replace(")", "%29")
        if url.startswith("https://"):
            lines.append(f"- [{name}]({url})")
    lines.append("")
lines.extend(["## Contributing", "", "Suggest additions or corrections through GitHub Issues.", ""])
readme.write_text("\n".join(lines))
