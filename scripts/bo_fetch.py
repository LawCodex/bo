#!/usr/bin/env python3
"""Bolivia: Constitución Política del Estado (Gaceta Oficial de Bolivia, free PDF) and a
metadata-only index of the laws listed by the Gaceta Oficial ("Normas publicadas > Leyes").

Full texts of laws are NOT reproduced: the Gaceta marks its texts "TEXTO DE CONSULTA —
Derechos Reservados © Gaceta Oficial de Bolivia" and, under art. 69 of the Ley de Imprenta
(19-01-1925) and R.M. 039/11 of the Ministerio de la Presidencia, editions of codes and
compilations of laws require prior government authorization. See README.
"""
import json
import os
import re
import sys
import time
from datetime import date

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bo_pdfmd as P  # noqa: E402

RAW = os.environ.get("RAW", "/Users/magicaltux/projects/lawcodex/_raw/bo")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
SITE = "http://www.gacetaoficialdebolivia.gob.bo"
CONST = SITE + "/app/webroot/archivos/CONSTITUCION.pdf"
TODAY = date.today().isoformat()
MESES = {m: i + 1 for i, m in enumerate("enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split())}
s = requests.Session()
s.headers["User-Agent"] = UA


def get(url, binary=False):
    for k in range(5):
        try:
            r = s.get(url, timeout=(30, 300))
            if r.status_code == 200:
                time.sleep(2)
                return r.content if binary else r.content.decode("utf-8", "replace")
        except requests.RequestException as e:
            print("ERR", url, e, file=sys.stderr)
        time.sleep(10 * (k + 1))
    raise RuntimeError(url)


def constitution():
    p = os.path.join(RAW, "const.pdf")
    if not P.pdf_ok(p):
        open(p, "wb").write(get(CONST, True))
    assert P.pdf_ok(p)
    pages = P.extract_pages(p)
    clean = P.clean_pages(pages[1:], head_n=4)
    clean = P.drop_lines(clean, [r"TEXTO DE CONSULTA", r"Derechos Reservados.*", r"\".*AÑO DE .*\""])
    md = P.lines_to_md(clean)
    front = {"title": "Constitución Política del Estado", "identifier": "CPE 2009", "type": "constitution",
             "jurisdiction": "bo", "language": "es", "date": "2009-02-07", "status": "in_force",
             "source": CONST, "retrieved": TODAY}
    out = os.path.join(REPO, "constitucion", "constitucion-politica-del-estado-2009.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(P.render(front, front["title"], md, None,
        "> Texto publicado por la Gaceta Oficial de Bolivia (promulgada el 7 de febrero de 2009)."))
    print("constitution", md.count("###### "), "articles")


def index():
    rows = []
    page = 1
    while True:
        cache = os.path.join(RAW, "list", f"leyes-{page:04d}.html")
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        if os.path.exists(cache):
            html = open(cache, encoding="utf-8").read()
        else:
            html = get(f"{SITE}/normas/listadonor/10/page:{page}")
            open(cache, "w", encoding="utf-8").write(html)
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text("\n")
        found = re.findall(r"(Ley N° ?\S+)\s+(\d{1,2} DE [A-ZÁÉÍÓÚ]+ DE \d{4})\s*\.-\s*(.*?)\s*Ver Norma.*?"
                           r"Publicado en edición:\s*(\S+)\s*\|\s*Fecha de Publicación:\s*([\d-]+)", text, re.S)
        if not found:
            break
        for num, fecha, title, ed, pub in found:
            rows.append({"numero": num.strip(), "fecha": fecha.strip(), "titulo": re.sub(r"\s+", " ", title).strip(),
                         "edicion": ed, "publicacion": pub})
        last = max([int(x) for x in re.findall(r"page:(\d+)", html)] + [page])
        if page >= last:
            break
        page += 1
    json.dump(rows, open(os.path.join(RAW, "leyes-index.json"), "w"), ensure_ascii=False, indent=0)
    by = {}
    for r in rows:
        y = r["fecha"][-4:]
        by.setdefault(y, []).append(r)
    d = os.path.join(REPO, "indice", "leyes")
    os.makedirs(d, exist_ok=True)
    for y, rs in sorted(by.items()):
        lines = ["| Número | Fecha | Título | Gaceta (edición) | Publicación |", "|---|---|---|---|---|"]
        for r in rs:
            lines.append("| " + " | ".join(x.replace("|", "\\|") for x in
                         (r["numero"], r["fecha"].title(), r["titulo"], r["edicion"], r["publicacion"])) + " |")
        front = {"title": f"Índice de leyes — {y}", "type": "index", "jurisdiction": "bo", "language": "es",
                 "source": SITE + "/normas/listadonor/10", "retrieved": TODAY}
        open(os.path.join(d, f"{y}.md"), "w", encoding="utf-8").write(
            P.render(front, front["title"], "Metadatos (sin texto) según el listado de la Gaceta Oficial de Bolivia.\n\n" + "\n".join(lines)))
    print("index", len(rows), "laws", len(by), "years")


if __name__ == "__main__":
    constitution()
    index()
