# SCIY Flowchart v0.3 — Interaction state machine

## Core distinction

### A. Input source
- Content-to-diagram
- Image-to-diagram

### B. Interaction path
- Custom Design
- One-click

### C. Rendering mode
- Quick
- High-quality

These are separate dimensions.

## Custom path

```text
Input source
  -> Custom Design
  -> Language / Typography
  -> Show 8 style examples
  -> User chooses 1 family
  -> Generate 4 AI concepts in that family
  -> User chooses A/B/C/D OR regenerate OR change style OR skip
  -> Choose Quick / High-quality
  -> Formal vector drawing
  -> QA
  -> SVG / PPTX / PNG / JSON
```

## One-click path

```text
Input source
  -> One-click
  -> Auto language / default typography
  -> AI chooses 1 of 8 families
  -> Generate 1 AI concept
  -> Self-check
  -> Quick Mode
  -> Formal vector drawing
  -> QA
  -> SVG / PPTX / PNG / JSON
```

## Upgrade path after One-click

```text
One-click result
  -> regenerate
  -> switch style
  -> show 4 concepts for current family
  -> upgrade to High-quality while keeping blueprint
```

