# -*- coding: utf-8 -*-
"""Genera el kit imprimible siguiendo la maquetación de los PDF oficiales de DecidArch."""

from v1_datos import QUALITY_ATTRIBUTES, QA, PROJECT, STAKEHOLDERS, CONCERNS, EVENTS

CSS = """
@page { size: A4; margin: 14mm 12mm; }
* { box-sizing: border-box; }
body { margin:0; font-family:"DejaVu Sans", Arial, sans-serif; color:#000; font-size:9pt; }
.pagina { page-break-after: always; }
.pagina:last-child { page-break-after: auto; }

h1.hoja { font-size:15pt; margin:0 0 2mm; font-weight:700; }
p.sub { font-size:8.5pt; color:#444; margin:0 0 5mm; }

/* --- cartas: 2x2 por hoja, borde de corte --- */
.grid { display:grid; grid-template-columns:1fr 1fr; gap:5mm; }
.card { border:1.6px solid #000; padding:4mm 4.5mm; height:126mm; overflow:hidden;
        display:flex; flex-direction:column; }
.card .tipo { font-size:11pt; font-weight:700; margin-bottom:3mm; }
.card .fila { display:flex; justify-content:space-between; align-items:baseline; }
.lab { font-size:7.2pt; color:#555; margin-top:2.5mm; }
.val { font-size:9.6pt; font-weight:700; }
.txt { font-size:8.1pt; line-height:1.36; margin:1mm 0 0; text-align:justify; }
.centro { text-align:center; }

.qa-item { margin-top:2mm; font-size:8.1pt; line-height:1.34; }
.qa-item b { font-size:8.4pt; }
.prio { font-weight:700; }

.opt { margin-top:2.4mm; display:flex; gap:2.5mm; }
.opt .n { font-size:9.5pt; font-weight:700; min-width:4mm; }
.opt .cuerpo { flex:1; }
.opt .d { font-size:8pt; line-height:1.34; text-align:justify; }
.opt .imp { font-size:7.5pt; margin-top:0.8mm; }
.rule { border:0; border-top:1px solid #000; margin:2.2mm 0 0; }
.puntos { font-size:9pt; margin-top:1.5mm; }
.pieid { margin-top:auto; font-size:7pt; color:#666; text-align:right; }

/* --- plantillas --- */
table.pl { width:100%; border-collapse:collapse; margin-top:4mm; }
table.pl th { border:1px solid #000; background:#eee; font-size:8.2pt; padding:2mm;
              text-align:left; font-weight:700; }
table.pl td { border:1px solid #000; height:17mm; }
.gid { font-size:9pt; margin-top:3mm; }
.gid span { display:inline-block; border-bottom:1px solid #000; width:55mm; }

/* --- scoring --- */
table.sc { width:100%; border-collapse:collapse; font-size:7.2pt; margin-bottom:2.5mm; }
table.sc th, table.sc td { border:1px solid #000; padding:1.1mm 1mm; text-align:center; }
table.sc th { background:#eee; font-weight:700; font-size:7pt; }
table.sc td.izq, table.sc th.izq { text-align:left; }
.paso { font-size:10pt; font-weight:700; margin:3mm 0 1.2mm; }
.alto td { height:8mm; }
.nota { font-size:7.6pt; color:#333; margin-top:1.5mm; line-height:1.4; }
ul.reglas { font-size:8.6pt; line-height:1.5; padding-left:5mm; margin:1mm 0 3mm; }
ul.reglas li { margin:1.2mm 0; }
.dest { border:1.4px solid #000; padding:3mm 4mm; margin-top:3mm; font-size:8.6pt; line-height:1.45; }
"""


def impactos(d):
    partes = [f"{k} ({v.replace('++','+ +').replace('--','- -')})" for k, v in d.items()]
    return ", ".join(partes) + ", ..."


def carta_project():
    return f"""<div class="card">
  <div class="tipo">Project Card</div>
  <div class="lab">Project:</div><div class="val">{PROJECT['project']}</div>
  <div class="lab">Purpose:</div><p class="txt">{PROJECT['purpose']}</p>
</div>"""


def carta_stakeholder(s):
    qas = "".join(
        f'<div class="qa-item"><b>{k}</b> — {dict(QUALITY_ATTRIBUTES)[k]} '
        f'<span class="prio">(QA-Priority: {v})</span></div>'
        for k, v in s["qa"].items())
    return f"""<div class="card">
  <div class="tipo">Stakeholder Card</div>
  <div class="lab">Project:</div><div class="val" style="font-size:8.6pt">{PROJECT['project']}</div>
  <div class="lab">Stakeholder:</div><div class="val">{s['nombre']}</div>
  <div class="lab">Goal:</div><p class="txt">{s['goal']}</p>
  <div class="lab">Quality Attributes:</div>{qas}
</div>"""


def carta_concern(c):
    ops = ""
    for i, (desc, imp) in enumerate(c["options"], 1):
        ops += f"""<div class="opt"><div class="n">{i}</div><div class="cuerpo">
        <div class="d">{desc}</div><div class="imp">{impactos(imp)}</div></div></div>
        <hr class="rule">"""
    return f"""<div class="card">
  <div class="tipo">Concern Card</div>
  <div class="fila"><div><span class="lab">Concern-ID:</span> <span class="val">{c['id']}</span></div>
    <div class="lab">prioridad {c['puntaje']} · {c['ref']}</div></div>
  <div class="lab">Concern:</div><p class="txt">{c['concern']}</p>
  <div class="lab">Options:</div>{ops}
  <div class="puntos">...</div>
</div>"""


def carta_event(e):
    cuerpo = "".join(f'<p class="txt">{p}</p>' for p in e["description"].split("\n\n"))
    return f"""<div class="card">
  <div class="tipo">Event Card</div>
  <div class="lab">Title:</div><div class="val">{e['title']}</div>
  <div class="lab">Description:</div>{cuerpo}
</div>"""


# ------------------------------------------------------------------ paginas
P = []

# --- reglas resumidas
P.append(f"""<section class="pagina">
<h1 class="hoja">DecidArch — Shinobi Arena</h1>
<p class="sub">Resumen de reglas. El reglamento completo está en DecidArch-GameRules.pdf</p>

<div class="paso">Contenido del mazo</div>
<ul class="reglas">
  <li>1 Project Card · {len(STAKEHOLDERS)} Stakeholder Cards · {len(CONCERNS)} Concern Cards · {len(EVENTS)} Event Cards</li>
  <li>1 Decision Preparation Template por jugador · 1 Decision Taking Template por grupo · 1 Scoring Sheet</li>
  <li>Equipo de 2 a 4 jugadores. Duración: 30 minutos. Hace falta un lápiz y un reloj.</li>
</ul>

<div class="paso">Preparación</div>
<ul class="reglas">
  <li>Dejar a la vista la Project Card y las Stakeholder Cards.</li>
  <li>Formar dos mazos boca abajo y barajados: uno de Concern Cards y otro de Event Cards.</li>
  <li>Entregar una Decision Preparation Template a cada jugador y una Decision Taking Template al grupo.</li>
  <li>Todas las QA-Priority arrancan en 0. Son las Event Cards las que las modifican.</li>
</ul>

<div class="paso">Turno</div>
<ul class="reglas">
  <li>El jugador de turno roba una Concern Card.</li>
  <li>Cada jugador, de forma independiente, elige una opción y la anota con su rationale en su plantilla individual.</li>
  <li>El grupo discute y decide una sola opción, y la registra en la Decision Taking Template.</li>
  <li>Pasa el turno al siguiente jugador.</li>
</ul>

<div class="paso">Event Cards</div>
<ul class="reglas">
  <li>Al terminar la ronda, cuando todos han jugado su turno, se roba una Event Card.</li>
  <li>El evento cambia el contexto del proyecto. Sus efectos duran el resto de la partida.</li>
  <li>Hay que reconsiderar las decisiones ya tomadas a la luz del cambio.</li>
  <li>Si no quedan Event Cards, se sigue jugando sin robar.</li>
</ul>

<div class="paso">Opciones propias y símbolo &lt;?&gt;</div>
<ul class="reglas">
  <li>Los jugadores pueden proponer opciones nuevas en cualquier momento, anotándolas en la columna de opción.</li>
  <li>También pueden corregir los impactos de una opción existente, justificándolo en la columna Rationale.</li>
  <li>La lista de impactos de cada opcion termina en "..." porque no es cerrada.</li>
</ul>

<div class="dest"><b>Fin de la partida.</b> Se juega hasta agotar los 30 minutos o resolver todas las
Concern Cards. Después se calcula el resultado con el Scoring Sheet: si algún valor de C queda
bajo cero, el equipo pierde, sin importar el puntaje acumulado.</div>
</section>""")

# --- cartas
grupos = [
    [carta_project()] + [carta_stakeholder(s) for s in STAKEHOLDERS],
    [carta_concern(c) for c in CONCERNS[0:4]],
    [carta_concern(c) for c in CONCERNS[4:8]],
    [carta_concern(c) for c in CONCERNS[8:10]] + [carta_event(e) for e in EVENTS[0:2]],
    [carta_event(e) for e in EVENTS[2:6]],
]
for g in grupos:
    P.append(f'<section class="pagina"><div class="grid">{"".join(g)}</div></section>')

# --- plantillas
for titulo, quien, col in [
        ("Decision Preparation Template (Individual)",
         "Cada jugador recibe una plantilla individual.", "Suggested Option"),
        ("Decision Taking Template (Group)",
         "Registra las decisiones del grupo.", "Chosen Option")]:
    razon = "why the option is suggested" if "Suggested" in col else "why the option is chosen"
    filas = "".join("<tr><td></td><td></td><td></td></tr>" for _ in range(10))
    P.append(f"""<section class="pagina">
<h1 class="hoja">{titulo}</h1>
<p class="sub">{quien}</p>
<div class="gid">Group-ID: <span></span></div>
<table class="pl">
<tr><th style="width:22mm">Concern-ID</th><th style="width:40mm">{col}</th>
    <th>Rationale ({razon})</th></tr>{filas}</table>
</section>""")

# --- scoring sheet
th = "".join(f'<th>{k}</th>' for k in QA)
vac = "".join("<td></td>" for _ in QA)
paso2 = ""
for s in STAKEHOLDERS:
    for j, k in enumerate(s["qa"]):
        nombre = f'<td class="izq" rowspan="{len(s["qa"])}"><b>{s["nombre"]}</b></td>' if j == 0 else ""
        paso2 += f'<tr>{nombre}<td class="izq">{k}</td><td></td><td></td><td></td></tr>'

P.append(f"""<section class="pagina">
<h1 class="hoja">Scoring Sheet</h1>
<p class="sub">Se completa al terminar la partida. Fórmulas tomadas de DecidArch-ScoreSheet.pdf</p>

<div class="paso">Paso 1 · QA-Scores</div>
<table class="sc">
<tr><th class="izq" style="width:52mm">Quality Attribute</th>{th}</tr>
<tr class="alto"><td class="izq">A = cantidad de "+"  ("+ +" cuenta dos veces)</td>{vac}</tr>
<tr class="alto"><td class="izq">B = cantidad de "-"  ("- -" cuenta dos veces)</td>{vac}</tr>
<tr class="alto"><td class="izq"><b>QA-Score = A - B</b></td>{vac}</tr>
</table>
<div class="nota">Se cuentan solo los impactos de las opciones efectivamente elegidas, incluyendo
los que el equipo haya agregado durante la partida.</div>

<div class="paso">Paso 2 · Stakeholders-Score</div>
<table class="sc">
<tr><th class="izq" style="width:38mm">Stakeholder</th><th class="izq" style="width:38mm">Quality Attribute</th>
    <th style="width:26mm">QA-Score</th><th style="width:26mm">QA-Priority</th>
    <th>C = QA-Score - QA-Priority</th></tr>
{paso2}
<tr><td class="izq" colspan="4"><b>¿Hay algún valor de C menor que 0?</b>
    Si lo hay, perdieron la partida.</td><td>Si / No</td></tr>
<tr><td class="izq" colspan="4"><b>Stakeholders-Score = suma de los valores de C</b></td><td></td></tr>
</table>
<div class="nota">Usar la QA-Priority vigente al terminar la partida, ya modificada por las Event Cards.</div>

<div class="paso">Paso 3 · Final Score</div>
<table class="sc">
<tr><td class="izq" style="width:70%">D = Concern Cards que quedaron sin resolver</td><td></td></tr>
<tr><td class="izq"><b>Final Score = Stakeholders-Score - D</b></td><td></td></tr>
</table>

<table class="sc" style="width:62%">
<tr><th class="izq">Final Score</th><th class="izq">Resultado</th></tr>
<tr><td class="izq">Menor que 0</td><td class="izq">Perdieron la partida</td></tr>
<tr><td class="izq">0 a 9</td><td class="izq">Suficiente</td></tr>
<tr><td class="izq">10 a 19</td><td class="izq">Bueno</td></tr>
<tr><td class="izq">20 a 29</td><td class="izq">Muy bueno</td></tr>
<tr><td class="izq">30 o más</td><td class="izq">Excelente</td></tr>
</table>
</section>""")

html = f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
open("v1_kit.html", "w", encoding="utf-8").write(html)
print(f"v1_kit.html generado — {len(P)} paginas")
