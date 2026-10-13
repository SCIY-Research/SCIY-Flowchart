# SCIY Flowchart 八种风格 AI 图片

> 历史风格示例（v0.3）：以下生成提示词及现有图片仅展示八类视觉结构，图片中的旧交互节点不代表现行流程。当前交互以 `SKILL.md` 和 `interaction-flow-v1.0.md` 为准：快速/自定义不默认；自定义先联合选择，再选候选图，最后选择全局/分区绘制。

按照附件 sciy-flowchart-v0.3/SKILL.md 的八种风格，使用内置 imagegen 每种各生成一张 PNG。根据用户请求交付 AI 图片。

## 共用提示词

Create ONE high-resolution landscape 16:9 Chinese workflow infographic for a scientific tool showcase page. Main title exactly “SCIY Flowchart 工作流程”. Add small Chinese style subtitle matching supplied family name. White or very light background, professional, clean, readable large Chinese sans-serif type, flat vector aesthetic. No external images, no watermark, no photos, no paper screenshots, no excessive decoration. All text Chinese except required title brand and output format acronyms.
The SAME exact directed workflow must be preserved in every style:
用户开始 → 输入来源 (two ALTERNATIVE options inside this node: 内容设计 / 图片重绘) → 生成方式.
生成方式 forks into two branches:
自定义生成: 语言与字体 → 选择风格 → 4个方案 → 选择方案 → 快速/高质量.
一键生成: 自动选风格 → 1个默认方案 → 自动快速绘制.
Both branch endpoints converge BEFORE the shared tail: 正式绘制 → 质量检查 → 导出结果 → SVG / PPTX / PNG / JSON.
All required labels above must be present legible and spelled exactly. Branch names clearly label their paths. Exactly one shared 正式绘制, 质量检查, 导出结果 each. Inputs are alternatives, not a sequence. No invented steps, feedback loops or dependencies. Visible arrowheads at all sequential links, no connectors through nodes, no text clipping, balanced margins. Use generous spacing and a composition suitable for all labels. Only one flowchart per image.

## 风格提示词

### 01-经典学术流程

Classic restrained journal flowchart, white background, black and navy thin rectangular boxes, orthogonal connectors, minimal decoration, dominant left-to-right flow with parallel branch rows.

### 02-模块分区学术

Academic modular layout: large phase panels 输入与配置, 方案生成, 绘制与导出; grouped submodules and generous gutters; muted blue lavender and teal panel headers, distinct phase hierarchy.

### 03-工程系统架构

Technical system architecture: input block at left, central generation subsystem container with two nested processing pipelines, renderer and quality control subsystem at right, output ports, precise square-corner blocks and orthogonal interface lines, restrained steel blue.

### 04-阶段时间线

Stage timeline: horizontal milestone backbone across canvas, phases 开始, 输入, 生成, 绘制, 检查, 导出; branches expand into two parallel tracks below generation milestone then converge. No invented dates or durations. Minimal muted ochre and blue.

### 05-泳道多主体流程

Formal swimlane chart: clearly labeled horizontal lanes 输入配置, 自定义生成, 一键生成, 绘制与导出; every node belongs to a lane; short cross-lane connectors, pale blue teal lanes, strong aligned column rhythm.

### 06-循环反馈优化

Cycle-inspired curvilinear workflow composition: arrange entry left, custom upper arc chain, automatic lower arc chain, both converge into right-hand shared final sequence. Open arcs with explicit directed arrows only. Do NOT close the cycle or add any feedback edges, retry steps, conditions or decisions not supplied. Circular composition only, same directed acyclic workflow.

### 07-网络概念关系

Layered directed concept-network composition: a central 生成方式 hub connects to two clearly separated clusters labeled 自定义生成 and 一键生成; within clusters preserve sequential arrows, both converge to shared drawing-output cluster. Small node cards, gentle rounded cluster boundaries, no unrelated crosslinks, no ambiguous bidirectional arrows.

### 08-图文融合流程

Illustrated scientific workflow with small original flat vector pictograms integrated into node cards: document/image input, typography letters, style swatches, four miniature proposals, selection cursor, speed/quality gauge, drawing pen, quality magnifier and exported files. Icons secondary to exact text and arrows, no people or photos, refined muted blue teal ochre.

## 检查与修正

经典版补齐生成方式节点；时间线版移除绕过分支的连线；泳道版修正自定义入口及两个分支的汇合位置；环形布局版将自定义分支连接至正式绘制。环形布局保持单向流程，未添加未提供的反馈步骤。
