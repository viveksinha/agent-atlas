#!/usr/bin/env python3
"""Convert learning-mode-on Markdown primer parts to AgentAtlas HTML pages."""

import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD_SRC = Path(
    "/Users/viveksinha/Library/CloudStorage/GoogleDrive-wiki.victorcreed@gmail.com/"
    "My Drive/random-personal/bobs-bar/learning-mode-on"
)
OUT_DIR = ROOT / "learn"

PARTS = [
    {
        "file": "AI_Agents_Primer_Part1.md",
        "out": "part1.html",
        "title": "Part 1 — Foundations",
        "subtitle": "Sections A–I · LLMs, agents, prompts, skills, modes, and context",
        "part_num": 1,
        "part_label": "Foundations",
        "prev": None,
        "next": ("part2.html", "Part 2 — Practice →"),
        "sections": [
            ("a-what-is-an-llm", "A. LLM"),
            ("b-what-is-github-copilot", "B. Copilot"),
            ("c-what-is-agentic-ai-what-is-an-agent", "C. Agents"),
            ("d-how-to-write-a-good-prompt", "D. Prompts"),
            ("e-skills-rules-and-instructions", "E. Skills"),
            ("f-modes-plan-ask-agent", "F. Modes"),
            ("g-what-is-context", "G. Context"),
            ("h-how-agents-use-skills-rules-and-instructions", "H. Skills in use"),
            ("i-prompt-vs-agent-which-one-to-use", "I. Prompt vs agent"),
        ],
    },
    {
        "file": "AI_Agents_Primer_Part2.md",
        "out": "part2.html",
        "title": "Part 2 — Practice",
        "subtitle": "Sections J–S · Tools, MCP, models, skills, security, and workflows",
        "part_num": 2,
        "part_label": "Practice",
        "prev": ("part1.html", "← Part 1 — Foundations"),
        "next": ("part3.html", "Part 3 — Scale →"),
        "sections": [
            ("j-tools-how-agents-take-action-in-the-real-world", "J. Tools"),
            ("k-mcp-connecting-agents-to-your-apps", "K. MCP"),
            ("l-models-picking-the-right-brain-for-the-job", "L. Models"),
            ("m-human-in-the-loop-when-to-approve-when-to-auto-run", "M. HITL"),
            ("n-building-your-first-skill", "N. First skill"),
            ("o-when-things-go-wrong-common-agent-failures", "O. Failures"),
            ("p-memory-across-sessions-what-persists-vs-what-doesnt", "P. Memory"),
            ("q-security-privacy-basics", "Q. Security"),
            ("r-evaluating-an-agent-is-it-actually-working", "R. Evaluation"),
            ("s-from-one-agent-to-a-workflow-chaining-steps-together", "S. Workflows"),
        ],
    },
    {
        "file": "AI_Agents_Primer_Part3.md",
        "out": "part3.html",
        "title": "Part 3 — Scale",
        "subtitle": "Sections T–Y · Subagents, automations, RAG, cost, team rollout, production",
        "part_num": 3,
        "part_label": "Scale",
        "prev": ("part2.html", "← Part 2 — Practice"),
        "next": None,
        "sections": [
            ("t-subagents-delegating-work-to-specialized-agents", "T. Subagents"),
            ("u-hooks-automations-running-agents-without-asking", "U. Hooks"),
            ("v-rag-giving-agents-a-searchable-knowledge-base", "V. RAG"),
            ("w-cost-tokens-keeping-agent-runs-affordable", "W. Cost"),
            ("x-team-rollout-sharing-skills-rules-and-agents", "X. Team rollout"),
            ("y-the-production-agent-checklist-from-experiment-to-trusted-system", "Y. Production"),
        ],
    },
]

NAV_SVG = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

THEME_BTN = """<button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" title="Toggle dark mode">
      <svg class="icon-moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      <svg class="icon-sun"  width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
    </button>"""

FOOTER = """<footer>
  <div class="footer-left">
    <p>AgentAtlas &nbsp;&middot;&nbsp; Navigate the world of AI agents &nbsp;&middot;&nbsp; Built with <span class="heart">&#10084;&#65039;</span> for the world</p>
  </div>
  <div class="footer-right">
    <a href="https://www.linkedin.com/in/sinha-vivek/" target="_blank" title="LinkedIn" aria-label="LinkedIn">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.855v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
    </a>
    <a href="https://github.com/viveksinha" target="_blank" title="GitHub" aria-label="GitHub">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
    </a>
    <a href="https://x.com/geekwhotravels" target="_blank" title="X / Twitter" aria-label="X / Twitter">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>
    </a>
  </div>
</footer>"""


def slugify_heading(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"^##?\s*", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s


def rewrite_links(text: str) -> str:
    def repl(m):
        label, url = m.group(1), m.group(2)
        if url.startswith("./AI_Agents_Primer_Part1.md"):
            url = "part1.html" + url.split(".md", 1)[-1]
        elif url.startswith("./AI_Agents_Primer_Part2.md"):
            url = "part2.html" + url.split(".md", 1)[-1]
        elif url.startswith("./AI_Agents_Primer_Part3.md"):
            url = "part3.html" + url.split(".md", 1)[-1]
        elif url in ("./README.md", "./AI_Agents_Primer_INDEX.md"):
            url = "../learn.html"
        return f'<a href="{html.escape(url)}">{inline_format(label)}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def inline_format(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def parse_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header, sep, body = rows[0], rows[1], rows[2:]
    out = ['<div class="table-wrap"><table class="learn-table"><thead><tr>']
    for c in header:
        out.append(f"<th>{inline_format(c)}</th>")
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        for c in row:
            out.append(f"<td>{inline_format(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def convert_markdown(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    skip_until = 0

    while i < len(lines):
        line = lines[i]

        if i < skip_until:
            i += 1
            continue

        if line.startswith("# ") and not line.startswith("## "):
            i += 1
            continue

        if line.strip() == "---":
            i += 1
            continue

        if line.startswith("```"):
            lang = line[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            content = "\n".join(block)
            if lang == "mermaid":
                out.append(f'<div class="mermaid-wrap"><pre class="mermaid">{html.escape(content)}</pre></div>')
            else:
                out.append(f'<pre class="learn-code">{html.escape(content)}</pre>')
            continue

        if line.startswith("## "):
            if out and out[-1] != "</section>":
                if any(s.startswith("<section") for s in out):
                    out.append("</section>")
            title = line[3:].strip()
            sid = slugify_heading(title)
            out.append(f'<section class="learn-section section-anchor" id="{sid}">')
            out.append(f'<h2 class="learn-section-title">{inline_format(title)}</h2>')
            i += 1
            continue

        if line.startswith("### "):
            out.append(f"<h3>{inline_format(line[4:].strip())}</h3>")
            i += 1
            continue

        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:-]+\|", lines[i + 1]):
            table_lines = [line]
            i += 1
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1
            out.append(parse_table(table_lines))
            continue

        if re.match(r"^[-*] ", line):
            out.append("<ul>")
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                item = re.sub(r"^[-*] ", "", lines[i])
                out.append(f"<li>{rewrite_links(inline_format(item))}</li>")
                i += 1
            out.append("</ul>")
            continue

        if re.match(r"^\d+\. ", line):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                item = re.sub(r"^\d+\. ", "", lines[i])
                out.append(f"<li>{rewrite_links(inline_format(item))}</li>")
                i += 1
            out.append("</ol>")
            continue

        if line.strip() == "":
            i += 1
            continue

        if line.startswith("> "):
            out.append('<blockquote class="callout callout-tip"><p>')
            while i < len(lines) and (lines[i].startswith("> ") or lines[i].strip() == ""):
                if lines[i].startswith("> "):
                    out.append(rewrite_links(inline_format(lines[i][2:].strip())) + " ")
                i += 1
            out.append("</p></blockquote>")
            continue

        if line.startswith("*") and not line.startswith("**") and line.endswith("*") and line.count("*") == 2:
            out.append(f'<p class="learn-intro"><em>{inline_format(line.strip()[1:-1])}</em></p>')
            i += 1
            continue

        if line.startswith("**") and line.endswith("**") and line.count("**") == 2:
            out.append(f'<p><strong>{inline_format(line.strip()[2:-2])}</strong></p>')
            i += 1
            continue

        para = rewrite_links(inline_format(line.strip()))
        if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("#", "-", "*", "|", "```")) and not re.match(r"^\d+\. ", lines[i + 1]):
            parts = [para]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "-", "*", "|", "```")) and not re.match(r"^\d+\. ", lines[i]):
                parts.append(rewrite_links(inline_format(lines[i].strip())))
                i += 1
            out.append(f"<p>{' '.join(parts)}</p>")
            continue

        out.append(f"<p>{para}</p>")
        i += 1

    html_out = "\n".join(out)
    html_out = re.sub(r"(</section>\s*)+<section", "</section>\n<section", html_out)
    if "<section" in html_out and not html_out.rstrip().endswith("</section>"):
        html_out += "\n</section>"
    return html_out


def build_page(part: dict, body_html: str) -> str:
    quick_nav = "\n".join(
        f'      <a href="#{sid}">{label}</a>' for sid, label in part["sections"]
    )
    prev_link = ""
    if part["prev"]:
        prev_link = f'<a href="{part["prev"][0]}">{part["prev"][1]}</a>'
    else:
        prev_link = '<span></span>'
    next_link = ""
    if part["next"]:
        next_link = f'<a href="{part["next"][0]}">{part["next"][1]}</a>'
    else:
        next_link = '<a href="../learn.html">Course complete ✓</a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{part["title"]} — Learn — AgentAtlas</title>
  <link rel="stylesheet" href="../css/style.css" />
  <link rel="stylesheet" href="../css/learn.css" />
</head>
<body>

<nav>
  <div class="nav-inner">
    <a class="nav-logo" href="../index.html">
      <span class="logo-icon">{NAV_SVG}</span>
      AgentAtlas
    </a>
    <ul class="nav-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../learn.html">Learn</a></li>
      <li><a href="../resources.html">Resources</a></li>
      <li><a href="../tools.html">Tools</a></li>
      <li><a href="../examples.html">Examples</a></li>
      <li><a href="../deep-tech.html">Deep Tech</a></li>
    </ul>
    {THEME_BTN}
  </div>
</nav>

<div class="learn-hero">
  <div class="breadcrumb" style="margin-bottom:14px; font-size:0.8rem;"><a href="../index.html">Home</a> › <a href="../learn.html">Learn</a> › {part["title"]}</div>
  <h1>{part["title"]}</h1>
  <p>{part["subtitle"]}</p>
  <div class="hero-tags">
    <span class="hero-tag">Beginner</span>
    <span class="hero-tag">Cursor &amp; VS Code</span>
    <span class="hero-tag">25 Sections</span>
  </div>
</div>

<div class="learn-progress">Part {part["part_num"]} of 3 · {part["part_label"]}</div>

<nav class="learn-quick-nav" aria-label="Section navigation">
  <div class="learn-quick-nav-inner">
{quick_nav}
  </div>
</nav>

<div class="container learn-container">
  <article class="learn-prose">
{body_html}
  </article>

  <nav class="learn-part-nav" aria-label="Part navigation">
    {prev_link}
    <a href="../learn.html" class="learn-index-link">Course index</a>
    {next_link}
  </nav>
</div>

{FOOTER}
<script src="../js/main.js"></script>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

  function mermaidTheme() {{
    const t = document.documentElement.getAttribute('data-theme');
    if (t === 'dark') return 'dark';
    if (t === 'light') return 'neutral';
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'neutral';
  }}

  async function renderMermaid() {{
    mermaid.initialize({{ startOnLoad: false, theme: mermaidTheme(), securityLevel: 'loose' }});
    await mermaid.run({{ querySelector: '.mermaid' }});
  }}

  renderMermaid();
  document.getElementById('themeToggle')?.addEventListener('click', () => setTimeout(renderMermaid, 350));
</script>
</body>
</html>
"""


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for part in PARTS:
        md_path = MD_SRC / part["file"]
        md_text = md_path.read_text(encoding="utf-8")
        md_text = re.sub(
            r"^\*\*Course index:\*\*[^\n]*\n\n\*\*Example personas\*\*[^\n]*\n\n---\n\n",
            "",
            md_text,
            count=1,
        )
        md_text = re.sub(
            r"^\*\*Course index:\*\*[^\n]*\n\n---\n\n",
            "",
            md_text,
            count=1,
        )
        md_text = re.sub(
            r"^\*Continues from[^\n]*\n\n---\n\n",
            "",
            md_text,
            count=1,
        )
        body = convert_markdown(md_text)
        page = build_page(part, body)
        out_path = OUT_DIR / part["out"]
        out_path.write_text(page, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(ROOT)} ({len(page):,} bytes)")


if __name__ == "__main__":
    main()
