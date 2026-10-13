# SCIY Flowchart v0.3 — Style Library

The library separates **structural family** from **visual theme**. In v0.3, the eight families below are the user-facing first-layer style choices. Visual tokens can be refined later without changing the underlying family.

| ID | Family | Primary information logic | Typical use |
|---|---|---|---|
| 01 | academic-classic | linear / branching / convergence | paper methods, screening, experiment steps |
| 02 | academic-modular | grouped phases / modules | complex methodology, modeling framework |
| 03 | technical-architecture | components / interfaces / systems | engineering, software, control, CFD/ML |
| 04 | timeline-stage | time / milestones / phases | schedules, staged experiments, project flow |
| 05 | swimlane | actors / modules / responsibilities | experiment-simulation-validation, teams |
| 06 | cycle-feedback | iteration / feedback / convergence | optimization, closed loop, model review |
| 07 | network-concept | multi-relation / concept / causal network | concept map, AHP/DEMATEL, risk network |
| 08 | illustrated-workflow | flow + semantic vector illustration | graphical abstract-like scientific workflow |

## Style selection principle

Choose the family from the **logic of the information**, not from color. A complex figure may combine several families internally in high-quality mode while retaining one shared typography and visual-token system.

## Preview assets

Each folder under `styles/` contains:

- `STYLE.md`
- `tokens.json`
- `preview.svg`
- `preview.png`

The previews are original SCIY assets and are intended for user selection.

## External references

See `references/external-examples/gallery.html` and `SOURCES.md`. These are web research examples used to understand the families; they are not the SCIY style assets.
