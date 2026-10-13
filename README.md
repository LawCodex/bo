# LawCodex — Bolivia (bo)

Bolivian legislation as Markdown: the **Constitución Política del Estado (2009)** and a
metadata-only **index of 5,164 laws** (number, date, title, Gaceta edition, publication date)
as listed by the **Gaceta Oficial del Estado Plurinacional de Bolivia**.

Part of [LawCodex](https://github.com/LawCodex): one public repository per jurisdiction.

Retrieved: **2026-10-13**. Language: Spanish (`es`).

Status: **minimal** — the full texts of laws are deliberately not reproduced (see below).

## What is covered

| Category | Directory | Files |
|---|---|---|
| Constitución Política del Estado, promulgated 7 Feb 2009 (411 articles + transitional provisions; not amended since) | `constitucion/` | 1 |
| Index of laws (metadata only, 5,164 entries, 1960–2026), one file per year of the law | `indice/leyes/<year>.md` | 57 |

## What is NOT covered, and why

- **Full texts of laws, decrees and codes.** The Gaceta Oficial de Bolivia
  (http://www.gacetaoficialdebolivia.gob.bo/) is the only official online source. Every text
  it serves (HTML "Ver Norma", Word and PDF) is stamped *"TEXTO DE CONSULTA — Derechos
  Reservados © Gaceta Oficial de Bolivia"*, the Gaceta sells subscriptions, and its own
  "Autorización de Publicación de Textos Oficiales" page (R.M. 039/11 of the Ministerio de la
  Presidencia) recalls that under art. 69 of the Ley de Imprenta of 19 January 1925 editions of
  the Constitution, the codes and compilations of laws require prior government authorization.
  Bolivia's copyright law (Ley 1322 of 1992) has no explicit exclusion for official texts.
  We therefore publish only the Constitution and a factual index, pending authorization from
  the Gaceta Oficial / Ministerio de la Presidencia (contact: info_gob@gacetaoficialdebolivia.gob.bo)
  to republish the law texts.
- Decretos supremos, resoluciones, departmental/municipal norms (also listed by the Gaceta).

## Sources

- Constitution: http://www.gacetaoficialdebolivia.gob.bo/app/webroot/archivos/CONSTITUCION.pdf
  (free PDF published by the Gaceta; the running header "TEXTO DE CONSULTA / Derechos
  Reservados" and the year motto have been removed).
- Index: http://www.gacetaoficialdebolivia.gob.bo/normas/listadonor/10 ("Normas publicadas —
  Leyes", all result pages). Laws before the 2009 Constitution keep their old numbering, so
  numbers repeat across eras; the "Fecha" column disambiguates.

## Structure

```
constitucion/constitucion-politica-del-estado-2009.md
indice/leyes/<year>.md     table: number | date | title | Gaceta edition | publication date
```

## Regenerate

```
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
RAW=/path/to/scratch .venv/bin/python scripts/bo_fetch.py
```

`scripts/bo_pdfmd.py` converts PDF text to structured Markdown (heading and article detection).
