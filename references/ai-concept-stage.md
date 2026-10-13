# Concept stage v0.9

Four previews for Custom; one auto-approved blueprint for One-click. The approved design is a structural *blueprint*, not a publication-ready AI raster.

Four Custom candidates: same scientific nodes/relationships, same chosen structural family, same palette, distinct layouts. Must not merely repaint one arrangement.

1. Persist the user's semantic model in JSON with node IDs and exact graph edges before generating preview images.
2. If an image-generation tool is available in Codex, use it. Batch four when supported. Any generated text is provisional; reconstruct exact text in final vector output.
3. If image tool absent, unreachable or errors repeatedly, retry at most once for transient failure. Then produce local actual SVG concept files with `python scripts/concept-preview.py <input.json> <outputdir> --count 4` (or `--count 1` for One-click). Indicate "本地矢量预览" honestly.
4. User selects A/B/C/D and may modify palette **in the same message**; Quick is assumed unless High-quality requested.
5. Concept image generation is not a prerequisite for formal vector drawing. Retain source JSON and offline SVG if connectivity is unstable.

User actions: pick, another set, another family, skip. Rendering mode is an optional phrase in the same answer, not an extra round-trip.
