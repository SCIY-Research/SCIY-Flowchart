# Test prompts — v0.5

## Routing collision
`$sciy-flowchart 帮我画一个论文方法流程图。`
Expected: flowchart routing; never ask for equipment name/reference.

## Empty-start custom
`$sciy-flowchart 我想自定义做一个流程图。`
Expected: ask input source first if unknown; then interaction path/language as applicable.

## Local gallery
`我选自定义生成，中文，默认字体。`
Expected: local 8-style contact sheet; no web.

## Four concepts
`我选 02 模块分区学术。`
Expected: four same-family concepts A-D.

## One-click
`$sciy-flowchart 一键生成：数据采集→清洗→建模→验证→输出。`
Expected: one concept + Quick, no gallery.

## Image redraw
Upload a flowchart then say:
`$sciy-flowchart 按这张图重绘，自定义生成。`
Expected: infer image input; preserve topology; show local style gallery only if redesign is wanted.
