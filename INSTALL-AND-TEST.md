# SCIY Flowchart v1.0 — 安装 / 发布前验证

1. 解压后把唯一的 `流程图绘制1.0/` 文件夹放进你的 `$CODEX_HOME/skills/`（Windows 通常是 `%USERPROFILE%\.codex\skills\`），确认其中根目录存在 `SKILL.md`。旧版同名目录先备份到 skills 目录之外，再安装新版；随后刷新技能或重启 Codex。
2. `python scripts/self-check.py` — 静态/离线交互/样例验收。
3. `python scripts/release-check.py` — 必要科学依赖规则、自动避标题、SVG、可选 PNG、可选原生 PPTX 的积分测试；如果依赖缺失，结果明确写 SKIP。
4. 如需导出 PNG，可用 `pip install cairosvg`（可选）；可编辑 PPTX 使用 `pip install python-pptx`。CLI fallback：Inkscape 或 rsvg-convert 或 ImageMagick。没有外部软件也可以生成 SVG。
5. 按 `references/test-prompts-v1.0.md` 核对两层交互：先快速/自定义；快速一次完成；自定义先同轮结构配色语言字体字号、4张候选、选图后再全局/分区选择。自动结构不得默认01。
6. 用浏览器打开 `SELECTION-GALLERY.html` 并切断网络，确认第三方图不可达时正常展示清晰标记的本地备用图。首次调用 Skill 不应自动搜索网页。
7. 如果可用，请在真实 Windows PowerPoint 中打开 PPTX，逐一检查字体替换、箭头方向、换行和跨平台效果；Linux LibreOffice 的校验只是一个独立渲染器验证，不是所有 MS Office 版本的保证。

### 示例：ML-GAP 学术论文图

```
python scripts/check-semantics.py examples/release-case-ml-gap.json
python scripts/validate-diagram.py examples/release-case-ml-gap.json
python scripts/render-svg.py examples/release-case-ml-gap.json ml-gap.svg
python scripts/export-png.py ml-gap.svg ml-gap.png
python scripts/export-pptx.py examples/release-case-ml-gap.json ml-gap.pptx
```

引用：Agraz et al., 2024, *Frontiers in Genetics*, https://doi.org/10.3389/fgene.2024.1442759 （CC BY 4.0）。示例是依据方法逻辑独立重构，非原论文原图。
