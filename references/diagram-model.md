# SCIY Diagram Model v0.2

The model is a JSON object. Keep stable IDs so later edits can target only changed regions.

## Minimal structure

```json
{
  "meta": {
    "id": "example",
    "title": "Example Flow",
    "language": "en",
    "style": "academic-classic"
  },
  "canvas": {
    "width": 1600,
    "height": 900,
    "background": "#ffffff"
  },
  "typography": {
    "english_font": "Times New Roman",
    "chinese_font": "Source Han Sans SC",
    "node_pt": 12,
    "group_pt": 13,
    "title_pt": 15,
    "note_pt": 10.5
  },
  "groups": [],
  "nodes": [],
  "edges": []
}
```

## Node

```json
{
  "id": "n1",
  "type": "process",
  "text": "Build model",
  "x": 100,
  "y": 100,
  "w": 260,
  "h": 90,
  "group": "g1",
  "emphasis": "normal"
}
```

Supported v0.2 node types:
- `process`
- `rounded`
- `decision`
- `start`
- `end`
- `note`

## Group

```json
{
  "id": "g1",
  "label": "Model construction",
  "x": 60,
  "y": 60,
  "w": 520,
  "h": 360
}
```

Groups are optional. Use them for semantic regions or modules.

## Edge

Simple edge:

```json
{
  "id": "e1",
  "from": "n1",
  "to": "n2",
  "label": "",
  "kind": "main"
}
```

Explicit orthogonal path:

```json
{
  "id": "e2",
  "from": "n2",
  "to": "n3",
  "kind": "feedback",
  "points": [[620, 300], [760, 300], [760, 120], [620, 120]]
}
```

When `points` exists, the renderer uses it. Otherwise the renderer computes a simple center-to-center orthogonal route.

## Recommended semantics

`kind` values:
- `main`
- `secondary`
- `feedback`
- `constraint`

`emphasis` values:
- `normal`
- `strong`
- `muted`

## High-quality region manifest

The final assembly manifest is separate from the diagram JSON:

```json
{
  "canvas": {"width": 1600, "height": 900, "background": "#ffffff"},
  "parts": [
    {"file": "part-a.svg", "x": 60, "y": 80, "width": 650, "height": 320},
    {"file": "part-b.svg", "x": 820, "y": 80, "width": 650, "height": 320}
  ],
  "cross_edges": [
    {"points": [[710, 240], [820, 240]], "label": ""}
  ]
}
```
