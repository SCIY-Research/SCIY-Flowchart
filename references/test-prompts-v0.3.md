# SCIY Flowchart v0.3 — Test prompts

Use these in a fresh Codex session after installing the skill.

## Test 1 — Custom / content input

> 帮我画一个科研流程图：输入实验数据，进行预处理，建立模型，参数优化，验证，最后输出结果。我想自己选风格。

Expected behavior:
- recognizes content input
- enters Custom Design
- asks language/typography only if needed
- shows 8 style families
- after one family is selected, creates 4 concepts
- does not formally render before concept approval unless user skips

## Test 2 — One-click / content input

> 一键生成：把“实验准备→数据采集→数据清洗→建模→验证→结果输出”做成论文流程图。

Expected behavior:
- asks no unnecessary questions
- auto-selects one style
- creates one concept
- automatically uses Quick Mode
- produces final vector outputs

## Test 3 — Custom / image redraw

> 我上传一张流程图。我要重绘，但换成更高级的科研风格，我想自己选。

Expected behavior:
- recognizes image input
- offers Custom Design
- shows 8 families plus Preserve original style where appropriate
- generates four redesign concepts after style selection

## Test 4 — High-quality after concept approval

> 选方案 C。这个图比较复杂，用高质量模式。

Expected behavior:
- locks concept C as visual blueprint
- builds global region map
- redraws semantic regions separately
- assembles vector regions into one master

## Test 5 — One-click upgrade

> 这个一键生成的构图不错，但帮我升级成高质量版本。

Expected behavior:
- keeps current style and visual blueprint
- does not re-run style selection
- switches from Quick to High-quality
- regenerates only formal vector construction

