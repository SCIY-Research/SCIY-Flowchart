# Color Palette Sources

The palette values in `COLOR-GALLERY.html` and `references/color-palettes.json` are adapted from the public `ggsci` palette database.

- Project: https://github.com/nanxstats/ggsci
- Palette database: https://github.com/nanxstats/ggsci/blob/master/R/palettes.R
- Documentation: https://nanx.me/ggsci/

Important naming rule:
- Use **NPG-inspired / NEJM-inspired / Lancet-inspired / JAMA-inspired / JCO-inspired** rather than “official journal palette”.
- ggsci itself describes these as palettes inspired by journal plots, except palettes that explicitly cite a design guide (for example BMJ / UChicago in its source comments).

SCIY adaptation rule:
- Source colors are not applied as full high-saturation node fills by default.
- Use source colors mainly for outlines, headers, key connectors, and accents.
- Generate light node fills by mixing the selected color with approximately 80–88% white.
- For simple diagrams, use 1–3 base colors; for complex diagrams, normally use no more than 4–5 base colors.
