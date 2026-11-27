"""Discover AI repository candidates without claiming verified free access."""
import argparse
import json
import os
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "tools.json"
TOPICS = {
    "Local AI": ["local-llm", "llm-inference", "ollama"],
    "AI agents": ["ai-agents", "autonomous-agents", "agentic-ai"],
    "Coding": ["ai-coding", "code-generation", "coding-assistant"],
    "Image": ["image-generation", "stable-diffusion", "image-enhancement"],
    "Audio": ["text-to-speech", "speech-recognition", "audio-generation"],
    "Video": ["video-generation", "text-to-video"],
    "RAG and infrastructure": ["retrieval-augmented-generation", "vector-database", "llmops"],
    "AI security": ["llm-security", "ai-security", "prompt-injection"],
    "Documents": ["document-ai", "ocr", "document-understanding"],
    "Data science": ["machine-learning", "deep-learning", "automl"],
    "Automation": ["ai-automation", "workflow-automation"],
    "Education": ["ai-education", "ai-tutor"],
    "Research": ["scientific-machine-learning", "ai-research"],
    "Multimodal": ["multimodal", "vision-language-model"],
    "Chat assistants": ["chatbot", "llm-chatbot"],
    "Robotics": ["robot-learning", "embodied-ai"],
    "Translation": ["machine-translation", "neural-machine-translation"],
    "Search": ["semantic-search", "neural-search"],
}

def request(query, page):
    params = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": 100, "page": page})
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "VAIB-AI-Atlas"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request("https://api.github.com/search/repositories?" + params, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=40) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (403, 429, 502, 503):
                raise
            delay = int(exc.headers.get("Retry-After", "60"))
            time.sleep(min(max(delay, 10), 300))
    raise RuntimeError("GitHub API unavailable after retries")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=3, choices=range(1, 11))
    parser.add_argument("--min-stars", type=int, default=10)
    args = parser.parse_args()
    records = json.loads(CATALOG.read_text(encoding="utf-8")) if CATALOG.exists() else []
    known = {r["url"].rstrip("/").lower(): r for r in records}
    for category, topics in TOPICS.items():
        for topic in topics:
            for page in range(1, args.pages + 1):
                result = request(f"topic:{topic} stars:>={args.min_stars} archived:false fork:false", page)
                items = result.get("items", [])
                for item in items:
                    url = item["html_url"]
                    key = url.rstrip("/").lower()
                    if key in known:
                        continue
                    known[key] = {
                        "name": item["name"],
                        "url": url,
                        "category": category,
                        "description": item.get("description") or "AI repository candidate.",
                        "status": "Unverified candidate",
                        "source": "GitHub API",
                        "stars": item["stargazers_count"],
                        "license": (item.get("license") or {}).get("spdx_id"),
                        "repository_id": item["id"],
                        "updated_at": item["updated_at"],
                    }
                print(f"{topic}: page {page}, catalog {len(known)}", flush=True)
                if len(items) < 100:
                    break
                time.sleep(7)
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    temporary = CATALOG.with_suffix(".tmp")
    temporary.write_text(json.dumps(list(known.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(CATALOG)

if __name__ == "__main__":
    main()
