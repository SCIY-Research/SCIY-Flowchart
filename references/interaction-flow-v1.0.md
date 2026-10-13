# SCIY two-level interaction contract

## First level: Quick or Custom
If not already selected, offer **快速模式** (AI chooses a content-appropriate structure and completes output directly) and **自定义模式** (structure/color → four concepts → selected image → drawing-method choice). Neither route is default. Quick requires an explicit user selection. Do not present High-quality region reconstruction as the initial counterpart of Quick.

Quick: content → semantic graph → AI structure comparison → one blueprint or honest fallback → complete-diagram vector drawing → QA → exports. No gallery questions, four-concept approval, or Global/Region question.

Custom: combined structure/color/output-language/Chinese-English fonts/font-size choice → four AI concepts or honest SVG fallbacks → user selects A/B/C/D → **then** ask Global drawing versus High-quality region reconstruction → selected method → QA and exports.

## Second level: inside Custom, after image selection
“B” selects the image only. Ask **① 全局绘制** (whole-blueprint vector construction) or **② 高质量分区重建** (substantive semantic-region reconstruction and assembly), with neither method preselected. If the user already says “B + 全局绘制”, proceed without repeating the question. Global inside Custom remains Custom; it is not the Quick route.

Skipping candidates permits choosing one blueprint, then asking the drawing-method question. Automatic structure/color choice does not select a drawing method. Missing replies never select a route or method.

## Shared scientific and design constraints
Use source-supported dependencies. Explicit `interaction_route` and `drawing_method` are separate model fields. AI analyzes all eight families and compares plausible choices, recording chosen family and rationale. No default 01; only a user selection or a content-based sequential-flow reason permits classic linear structure. Do not let renderer defaults choose composition.

Save semantics before image generation. Retry transient image failure at most once, then use honest vector previews without switching route or method. Verify training versus held-out evaluation, alternative branches and feedback against the source. Run semantic and layout validators; inspect actual exported visuals.

High-quality requires substantive reconstruction from the selected blueprint. Cropping and reassembling an unchanged generic SVG does not qualify. Keep optional-export limitations honest and preserve successful vector/model files.

## Font intake location
In Custom, Step 1 must explicitly show font and size options together with structure and palette, before AI candidate generation. Offer Source Han Sans SC + Times New Roman, SimSun + Times New Roman, Microsoft YaHei + Arial, or custom fonts; offer default title/group/node/note sizes 15/13/12/10.5pt or custom sizes. Preserve supplied structure/palette and ask only missing typography if it was previously omitted. Save typography in JSON and carry it into prompts and native vector exports. AI concepts do not guarantee precise font metrics. Quick remains one-pass and uses supplied settings or displayed defaults without extra intake.

In Custom, explicitly ask 中文 / 英文 / 中英混排 in that same intake question. Do not infer output language from the paper or from the chosen font. Preserve already selected settings and ask only missing language/typography together. Record meta.language and carry it through concepts and final vector text; wait for a missing language answer. Quick honors supplied language or infers it without additional questions.

