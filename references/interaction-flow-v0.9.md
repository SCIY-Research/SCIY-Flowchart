# SCIY Flowchart v0.9 — compact interaction contract

## Missing content: one consolidated intake

“请发内容或图片；① 一键生成（推荐/默认）或② 自定义。语言、字体字号可一起补充，不填自动判断。”

## One-click (no other questions)

Input → infer language & structure → optional 1 concept image or local SVG fallback → default palette → Quick vector draw → QA/export. Never ask for palette/mode/candidate confirmation.

## Custom

Input → **one combined style + palette question** with `SELECTION-GALLERY.html` / `.md` → 4 layouts as actual images (AI when available, local vector previews if tool fails) → **one combined A–D + color adjustment + optional HQ question** → default Quick draw → QA/export.

If the user already gave custom style and palette, skip their chooser. If they say “用B”，skip any confirmation and render Quick.

Question count target: at most 3 interactions from blank request (intake, joint style/color, candidate choice), at most 2 when supplied input. Essential clarifications about unreadable source semantics can be asked, but not aesthetic preferences by separate turns.

## Network failure

Persist semantic JSON before image calls; no web search or endless retries; one transient retry maximum; local SVG fallback using `scripts/concept-preview.py`; preserve user choices; never claim a fallback SVG was AI-generated.
