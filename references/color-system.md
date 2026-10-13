# SCIY Color System v0.9

Structure references NEVER specify final colors. User may choose a journal/scientific-inspired preset `P01–P08`, default, a description/HEX, or color reference image. Color and structure selection are combined into one step at `SELECTION-GALLERY.html`.

Model format:
```json
"color": { "palette_id": "P03" }
```
or
```json
"color": { "colors": ["#176B87", "#6A9AA6", "#C7A77A"] }
```

Script `scripts/palette_utils.py` is shared by `render-svg.py` and `export-pptx.py`. Empty/invalid user tokens fall back to default palette; user-provided language-only color descriptions must be mapped by the model into actual HEX values before invoking exporters.

SCIY defaults: deep blue #3C5488, cyan #4DBBD5, teal #00A087, white background, dark text, light fills 82–90% white. Keep contrast strong and avoid using every available palette hue indiscriminately.

Palette names ending in inspired are NOT official journal color mandates.
