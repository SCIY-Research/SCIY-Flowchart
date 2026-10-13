# SCIY Flowchart v0.5 — interaction state machine

```text
START
  |
  +-- input known? -- no --> ask: Content / Image
  |                     |
  |                     +--> INPUT_READY
  |
  +-- yes ------------------> INPUT_READY

INPUT_READY
  |
  +--> ask: One-click / Custom
        |
        +-- One-click
        |     -> auto language/font
        |     -> auto style
        |     -> 1 concept
        |     -> self-check
        |     -> Quick
        |     -> vector render
        |     -> QA/export
        |
        +-- Custom
              -> language/font
              -> show ONE local 8-style contact sheet
              -> choose 1 style
              -> 4 concepts A-D
              -> choose/regenerate/change/skip
              -> Quick or High-quality
              -> vector render
              -> QA/export
```

## Performance invariant

No web search and no external reference loading are required for any state above.
