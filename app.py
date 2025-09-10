import csv
import os
from dataclasses import dataclass
from typing import List

from flask import Flask, render_template, url_for


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


@dataclass
class Tool:
    name: str
    link: str
    description: str
    usage: str


def generate_description(tool_name: str) -> str:
    """Return a short one-liner description inferred from the tool name."""
    name = tool_name.lower().strip()
    if "chat" in name:
        return "Conversational AI assistant for Q&A, brainstorming, and tutoring."
    if "image" in name or "photo" in name or "nano banana" in name:
        return "AI image generation and editing for visuals and mockups."
    if "code" in name or "copilot" in name:
        return "AI-assisted coding for faster development and learning."
    if "translate" in name or "translater" in name or "deepl" in name:
        return "High‑quality translation and multilingual writing assistance."
    if "data" in name or "vis" in name or "chart" in name:
        return "Data exploration and visualization to present insights clearly."
    if "prompt" in name or "optimizer" in name:
        return "Prompt crafting and refinement to improve AI outputs."
    if "test" in name:
        return "Online code execution and testing for quick validation."
    if "email" in name:
        return "Generates polished email drafts and replies quickly."
    return "AI tool to boost productivity and learning."


def generate_usage(tool_name: str) -> str:
    """Return a student/researcher‑oriented usage suggestion."""
    name = tool_name.lower().strip()
    if "chat" in name:
        return "Use for study guidance, concept explanations, and drafting research summaries."
    if "image" in name or "photo" in name or "nano banana" in name:
        return "Create figures for posters, slides, and illustrative examples in reports."
    if "code" in name or "copilot" in name:
        return "Generate boilerplate, learn patterns, and review snippets for assignments."
    if "translate" in name or "translater" in name or "deepl" in name:
        return "Translate papers and write bilingual abstracts with consistent terminology."
    if "data" in name or "vis" in name or "chart" in name:
        return "Quickly chart datasets, prototype dashboards, and communicate findings."
    if "prompt" in name or "optimizer" in name:
        return "Iterate on prompts to improve accuracy and reproducibility of AI runs."
    if "test" in name:
        return "Run snippets in a sandbox when you cannot install locally."
    if "email" in name:
        return "Draft professional outreach emails to labs, advisors, or collaborators."
    return "Incorporate into your workflow to automate routine academic tasks."


def load_tools(csv_path: str) -> List[Tool]:
    tools: List[Tool] = []
    if not os.path.exists(csv_path):
        return tools

    with open(csv_path, newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        # Try flexible header names
        # Normalize columns
        for row in reader:
            name = (
                row.get("Tool Name")
                or row.get("tool")
                or row.get("name")
                or "Untitled Tool"
            ).strip()
            link = (row.get("Link") or row.get("url") or row.get("href") or "").strip()
            description = generate_description(name)
            usage = generate_usage(name)
            tools.append(Tool(name=name, link=link, description=description, usage=usage))
    return tools


@app.route("/")
def index():
    csv_path = os.path.join(os.path.dirname(__file__), "table.csv")
    tools = load_tools(csv_path)
    return render_template("index.html", tools=tools)


if __name__ == "__main__":
    # Bind to all interfaces so others on the network can access
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


