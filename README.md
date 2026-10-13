# SCIY Flowchart v1.0

SCIY 科研流程图 Skill：支持文字设计、旧图重绘、快速与分区高质量绘制。

## 用户体验

- 第一层选择：**快速模式 / 自定义模式**，不预设选择。仅用户明确选择快速时执行快速路线。
- 快速模式：AI分析内容、选择合适结构，生成一个蓝图后直接绘制、检查并交付，不询问候选或重建方式。
- 自定义模式：结构＋配色＋语言（中文/英文/中英混排）＋字体＋字号同轮选择 → 4张AI候选（不可用时诚实提供SVG候选）→ 用户选图 → 再询问**全局绘制 / 高质量分区重建** → 按选择正式绘制。
- 全局绘制与分区重建是自定义模式中的第二层选择，不是快速模式的对立选项。只回复B选中了图片，不能直接开始正式绘制；若已明确“B＋全局绘制”则直接执行。
- 八类结构没有默认第一类。快速路线和自动结构选择均由AI分析科学依赖与构图适配性，比较候选结构并记录理由。
- 自定义模式在结构与配色同一轮明确询问输出语言（中文/英文/中英混排）、字体、字号，可选宋体＋Times New Roman、思源黑体＋Times New Roman、微软雅黑＋Arial或自定义；已有结构配色只补问未确认的语言与字体字号。默认字号15/13/12/10.5pt，字体以实际安装情况为准。快速模式不新增选择环节。

## 文件

- `SKILL.md`：唯一权威操作流程。
- `SELECTION-GALLERY.html`：结构参考 + 科研配色联合选择，推荐在 Codex 侧边面板直接打开。
- `SELECTION-GALLERY.md`：HTML 不能打开时的简化后备。
- `STYLE-GALLERY.html`、`COLOR-GALLERY.html`：原版独立图库，继续保留。
- `references/structure-reference-manifest.json`：32 项结构参考/来源。
- `references/color-palettes.json`：8 组色板。
- `scripts/concept-preview.py`：不依赖联网或图片 AI 的本地 A–D 矢量预览后备。
- `scripts/palette_utils.py`：SVG + PPTX 共用的配色解析。
- `scripts/layout_utils.py`：SVG/PPTX 共用精确布线与标题避障。
- `scripts/check-semantics.py`：可选约束声明（必需边/禁止边/并行方法）。
- `scripts/export-pptx.py`：原生 PPTX 对象、连接线箭头、显式字体与文字颜色。
- `scripts/export-png.py`：支持 CairoSVG 或外部本地转换器。
- `references/visual-prompting.md`：科学图示提示词、图形细节与可编辑分区重建规范。
- `scripts/self-check.py`、`scripts/release-check.py`：安装及端到端出图验证。

## 本地快速测试

```bash
python scripts/self-check.py
python scripts/concept-preview.py examples/sample-diagram.json output/concepts --count 4
python scripts/render-svg.py examples/sample-diagram.json output.svg
python scripts/release-check.py
```

正式 SCIY 图由源 JSON / 矢量编辑绘制，不应直接以 AI 位图代替论文图。

## 权利说明

图库的第三方论文图仅用于解释结构，不代表 SCIY 自有素材。保留来源和许可线索，但署名本身并不等于取得商业复制权。请检查每张原图的具体许可证和第三方 credit line；正式图必须根据用户内容独立设计。

## v1.0 发布验收边界

实测了论文案例的 SVG → PNG 与原生 PPTX → LibreOffice/PDF/PNG 渲染，解决了 v0.9 的白字、主题阴影、标题碰撞和箭头缺失问题。没有断言微软 PowerPoint 全版本无差异，或真实网路故障已端到端验证。发布前请在目标 Windows Codex 中确认一次。

论文样例 `examples/release-case-ml-gap.json` 根据 Agraz et al. (2024), Frontiers in Genetics, DOI 10.3389/fgene.2024.1442759 (CC BY 4.0) 方法内容独立整理，非原论文图片复制。图库第三方链接各自遵守来源许可。
