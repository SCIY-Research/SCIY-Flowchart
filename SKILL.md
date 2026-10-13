---
name: 流程图绘制1.0
description: Scientific flowcharts and research-method diagrams from text, papers or images. Offer Quick direct output or Custom design; neither route is assumed. Quick requires explicit user selection and AI content-based structure analysis. Custom provides structure/color selection and four AI concepts; only after the user picks a concept, ask Global drawing versus High-quality region reconstruction. Editable vector exports with honest offline fallback. Use for 流程图、方法框架、实验流程、技术路线、求解思路、工作流、论文流程图; not standalone equipment drawings.
---

# SCIY Flowchart v1.0

You are making a flowchart, not an equipment drawing. Equipment names alone do not trigger another drawing skill.

## Two levels of choice — do not confuse them

**Level 1 is the interaction route: 快速模式 versus 自定义模式.** Show these two routes when the user has not chosen. No default route. Only an explicit request for 快速模式 / 快速生成 / Quick mode or selection of its clearly labeled option enables Quick. Generic invocation, silence, “按默认” or a structure/color choice is not a Quick selection.

**Level 2 is the final drawing method inside Custom: 全局绘制 versus 高质量分区重建.** Ask this only after the user has selected an AI concept (or honestly labeled fallback concept). Do not offer these methods as the initial alternative to Quick. 全局绘制 inside Custom does not convert the task to the Quick interaction route.

Keep stored choices distinct: `interaction_route` is `quick` or `custom`; `drawing_method` is `global` or `region`. Candidate selection alone chooses neither a route nor a drawing method.

## Initial intake

Use already supplied papers, text and images without asking for them again. In Custom, explicitly ask the output language together with structure/color/typography; do not infer it from the source. In explicit Quick, honor a supplied language or infer it without adding questions. If the interaction route is missing, ask:

> 请选择：**① 快速模式**：AI根据内容选择合适结构，直接完成出图；**② 自定义模式**：先选结构和配色，再从4张AI候选图中选图，选定后再决定全局绘制或高质量分区重建。已有内容无需重复提供。

If content is also missing, request it in this same message. Wait for a missing route choice; source reading and semantic analysis may continue. Do not separately ask language, fonts or every optional preference. Preserve explicit choices already made for the current task.

## Shared AI structure analysis

Read `styles/index.json` and applicable local gallery references. Analyze scientific order, stages, parallel paths, actors, feedback, interfaces and information density. Consider all eight families, compare at least two plausible choices, and record the chosen family and rationale as `design_decision` plus explicit `meta.style` before rendering.

- 01 classic: primarily sequential steps, only if content supports it or the user selects it.
- 02 modular: grouped analyses or distinct research stages.
- 03 architecture: components and data/model interfaces.
- 04 timeline: chronological organization.
- 05 swimlane: actors or parallel responsibilities.
- 06 feedback: source-supported iteration.
- 07 network: relationships rather than one execution chain.
- 08 illustrated: useful equipment/data/model imagery.

**There is no default family 01.** List order, convenience and a renderer fallback must never choose the structure. The layout must actually reflect the chosen family; changing only a style token is insufficient. Automatic choice in either route uses this analysis. Preserve user-selected structures and scientific relations. Do not invent feedback or dependencies to fit a family.

## Route A — Quick direct output

Enter only when the user explicitly selects Quick. This is the original one-pass route, not a rendering-method question.

1. Parse the supplied content and save the semantic graph and source notes.
2. AI selects an appropriate structure using the shared analysis above. Apply SCIY colors `#3C5488`, `#4DBBD5`, `#00A087` unless the user already provided a palette.
3. Save `interaction_route: "quick"` and `drawing_method: "global"`. Create one AI design blueprint when the capability is available; on failure use one honestly labeled local vector concept. Do not ask the user to approve it.
4. Immediately draw the whole diagram as editable vector art, perform scientific/layout/visual checks and export supported SVG, PNG, source JSON and native PPTX.
5. Deliver the finished result in this run. **Do not ask for gallery selection, four candidates, candidate approval, or Global-versus-Region choice in Quick.**

Quick still requires content-aware structure choice; it does not mean default linear boxes. AI blueprints are not final publication graphics.

## Route B — Custom design

### Step 1: structure, color, output language, fonts and sizes together

Open `SELECTION-GALLERY.html`, or its Markdown fallback if HTML cannot be displayed. It contains 8 structural families × 4 references and 8 palettes. Ask:

> 请同轮选择**结构＋配色＋语言＋字体＋字号**，例如 `01-C + P07 + 中文 + 宋体/Times New Roman + 节点12pt`。语言请选择**中文 / 英文 / 中英混排**；字体可选“思源黑体＋Times New Roman”“宋体＋Times New Roman”“微软雅黑＋Arial”或自定义；字号可选默认（标题15pt、分组13pt、节点12pt、注释10.5pt）或自定。也可回复 `AI自动选择结构配色 + 英文 + 字体字号默认`。

Explicitly include output language (中文 / 英文 / 中英混排), Chinese/English fonts and size choices in the SAME question as structure/color, before generating candidates. Source language is not the output-language choice. Preserve an explicit language already chosen; otherwise wait for the missing language choice before generating concepts. An omitted answer does not authorize assuming Chinese or English. Save the choice in `meta.language` and use it in all candidate prompts and final vector labels. Offer defaults as a choice, not as a hidden assumption. If structure/color were already supplied but fonts were omitted, preserve them and ask only for missing language/font/size choices together once. Do not regenerate or re-ask confirmed settings. A combined answer giving no font/size after the options were shown may retain the displayed defaults; before vector export verify installed fonts and report a concrete substitution if needed. Save confirmed settings in `typography` and use them in both AI prompts and vector exporters. AI font appearance is approximate; final editable vector typography is authoritative.

Structure selection and palette are independent. A reference contributes hierarchy and layout inspiration, not copied colors, text, icons or composition. No web browsing for style selection, no initial preload of all remote references. Use local backups when references fail. Anchor all asset paths to this skill folder. “自动” authorizes AI analysis of structure/color, not an automatic choice of the later drawing method.

### Step 2: four concept images and user selection

Read `references/visual-prompting.md` when the source benefits from molecular, material, equipment, data or model illustrations. Use meaningful scientific graphics and preserve identification-critical geometry while keeping the blueprint feasible for editable PPT/vector reconstruction. Pure text boxes are not a universal default.

Persist one semantic graph before image generation. Generate four meaningfully different A/B/C/D layouts within the chosen family and palette, differing in orientation, grouping, emphasis or spacing while preserving scientific dependencies. Use the exposed AI image tool when available. If unavailable or failing, retry a transient failure at most once, then generate real programmatic SVG concepts and clearly label them as such. Do not falsely claim AI generation or endlessly retry services.

Fallback helper: `python scripts/concept-preview.py diagram.json output/concepts --count 4`. Inspect the output to ensure its actual composition matches the selected family; a helper's generic layout cannot silently replace it.

Show all four images and ask:

> 请选择 **A/B/C/D**（或换一批、换结构、跳过候选）。当前配色可一并调整。选定图片后，我再询问正式绘制方式。

Do not automatically render after a reply of `B`. It selects the blueprint only. If the user explicitly skips candidates, choose a source-supported blueprint and then proceed to Step 3; do not force four previews or switch to Quick.

### Step 3: only after image selection, ask drawing method

After the user selects the concept, show the selected image and ask:

> 已选 **B**。正式绘制请选择：**① 全局绘制**：按整张蓝图统一布局和矢量绘制；**② 高质量分区重建**：按语义区域逐区重建，再统一组装和连接。两者均可编辑。

No default drawing method. Wait for the user choice before final drawing. If the user has already explicitly selected the method (for example `B + 全局绘制`), honor that and do not ask again. A candidate letter, silence or automatic structure/color selection does not select the drawing method.

### Step 4: execute the selected drawing method

**Global drawing**: chosen blueprint → complete-diagram layout and native vector construction → scientific and visual QA → supported exports. This remains the Custom route because structure/color and concept selection have already occurred.

**High-quality region reconstruction**: chosen blueprint → semantic-region subdivision → substantive local geometry, typography and vector reconstruction → global assembly → cross-region connectors → scientific and visual QA → exports. Do not label a generic whole-diagram render, cropped SVGs or unchanged-template reassembly as High-quality. Do not arbitrarily quarter or raster-stitch the blueprint. Correct unsupported AI text/relations against the source before vector drawing.

Tool failure never authorizes switching the selected route or method. Preserve recoverable JSON and completed regions, explain a concrete limitation and avoid mislabeling an incomplete or Global result as Region reconstruction.

## Shared typography and resilience

In Custom, present and record font/size options at Step 1. In explicit Quick, use defaults without adding preference questions unless the user supplied fonts. Default choices: English Times New Roman; Chinese Source Han Sans SC or Noto Sans CJK SC, with installed-font fallback. Title 15 pt, groups 13 pt, nodes 12 pt and notes 10.5 pt by default; adapt to density without unreadable shrinking. Do not download or package fonts.

Final outputs are editable vector art. Preserve all successful outputs even if an optional converter fails. Distinguish AI concepts from programmatic previews and final vectors. Structure and palette decisions belong in the recoverable JSON, not just the chat.

## Actual export and palette application — important

Keep a JSON data model so users can edit/recolor without re-generating images. Use `scripts/validate-diagram.py`, `scripts/render-svg.py`, `scripts/export-png.py`, `scripts/export-pptx.py`, `scripts/assemble-svg.py` as needed.

Encode the palette in the **model JSON** before export (not just in the conversation):

```json
"color": { "palette_id": "P03" }
```

Or:

```json
"color": { "colors": ["#176B87", "#538C9A", "#B7A38C"] }
```

Both SVG renderer and PPTX exporter read this selection. Default is applied when missing; unsupported/invalid HEX colors fall back safely. Shapes get light-colored fills while line and selected key accents use original colors. Do not assign every available hue to every node; prioritize legibility.

Image-to-flowchart: do not silently change wording/topology. If a source label is unreadable, mark it for confirmation instead of inventing it.

## Scientific dependency validation (REQUIRED before final publication)

AI candidate images propose compositions; they are **not reliable scientific graphs**. Confirm causal/order relations from the original text, particularly training vs held-out test, alternative processing paths and feedback loops. When supported by the source, record assertions in the model JSON:

```json
"semantic_assertions": {
  "required_edges": [["raw", "preprocess"], ["train", "evaluate"]],
  "forbidden_edges": [["heldout", "train"]],
  "parallel_branches": [["baseline", "method_a", "method_b"]]
}
```

Run `python scripts/check-semantics.py diagram.json` before the final export. If assertions are absent, it emits a warning and manual verification remains mandatory. Never invent a scientific link to satisfy an assertion.

## Render and quality assurance — v1.0

Run `python scripts/validate-diagram.py diagram.json` before exporting. It checks canvas bounds, labels, node spacing, malformed waypoints, crossing of group titles, and route obstruction. Both `render-svg.py` and `export-pptx.py` now use `scripts/layout_utils.py` for common orthogonal waypoints and automatic detours around title bands / unrelated nodes. Preserve exact author line breaks. Review long feedback paths manually when required.

`export-pptx.py` draws native PowerPoint line segments with arrowheads at path ends, editable node text/shapes, visible main and group titles. **Text color and font are explicit**, not dependent on theme; default shadow effects are disabled. Visual check of the actual PPTX in PowerPoint/LibreOffice is still advisable; check font fallback on the recipient's system.

`export-png.py` uses Python CairoSVG when available, or local Inkscape, rsvg-convert, ImageMagick as fallback. Missing optional tools do not justify inventing outputs: return successfully generated SVG/JSON and explain which optional export was skipped.

If image generation fails due to network error, follow the pre-existing **single retry → clearly labeled programmatic SVG preview** rule. A skill cannot force an absent model-side image-generation capability.

Package check: `python scripts/self-check.py`; deterministic end-to-end export check: `python scripts/release-check.py`; test cases: `references/test-prompts-v1.0.md`. Do not claim real network-drop recovery or native Microsoft PowerPoint fidelity was fully exercised if not tested.

**Historical files**: earlier v0.3–v0.9 notes are archived only. This file and `references/interaction-flow-v1.0.md` take precedence.

## Quality and rights

Check scientific relation accuracy, text readability, all original nodes, no unintentional crossings, page balance, corresponding SVG/PPTX appearance. Preserve source JSON and output from successful converters even if one export fails. Do not advertise `.drawio` export as built-in unless separately implemented. Scientific references are for structure inspiration only. Attribution does not cure incompatible permissions; see `NOTICE-ASSETS.md`.


