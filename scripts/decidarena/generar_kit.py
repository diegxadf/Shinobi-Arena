# -*- coding: utf-8 -*-
"""Genera el kit imprimible DecidArena en HTML, listo para convertir a PDF."""

from kit_datos import TRACKS, COD, STAKEHOLDERS, CONCERNS, EVENTOS, TIEMPO_INICIAL

PIE = "DecidArena · Shinobi Arena | Adaptación educativa de DecidArch"


def imp(d):
    """Formatea los impactos de una opcion."""
    partes = []
    for k in COD:
        v = d[k]
        s = f"{v:+d}" if v else "0"
        cls = "pos" if v > 0 else ("neg" if v < 0 else "cero")
        partes.append(f'<span class="{cls}">{k} {s}</span>')
    return " <i>|</i> ".join(partes)


def cabecera(num, titulo, nota):
    return f'''<div class="banda">
  <div class="banda-t">{num}. {titulo}</div>
  <div class="banda-n">{nota}</div>
</div>'''


# ------------------------------------------------------------------ paginas
P = []

# --- portada
P.append(f'''<section class="pagina portada">
  <div class="p-marca">DECIDARENA</div>
  <div class="p-sub">Architecture Decisions for Shinobi Arena</div>
  <div class="p-linea"></div>
  <div class="p-tag">Juego de mesa listo para imprimir</div>
  <div class="p-caja">
    <div class="p-caja-t">BASADO EN</div>
    <p>DecidArch (de Boer, 2026) y la priorización de architectural concerns
    orientada a stakeholders (Pareto et al., 2011).</p>
  </div>
  <div class="p-caja">
    <div class="p-caja-t">CONTENIDO DE ESTE KIT</div>
    <p>3 Stakeholder Cards · 8 Concern Cards · 8 Event Cards · 1 tablero ·
    3 hojas de registro. Los 8 concerns son los 8 mejor puntuados de los 12
    identificados en la priorización de la Semana 1.</p>
  </div>
  <div class="p-pie">Proyecto: Shinobi Arena | Programación de Videojuegos | 2026</div>
</section>''')

# --- reglas
P.append(f'''<section class="pagina">
{cabecera(1, "Reglas rápidas", "2-4 jugadores | 35-50 min")}
<div class="regla"><div class="r-t">OBJETIVO</div>
<p>Resolver los 8 architectural concerns de Shinobi Arena, mantener las cinco cualidades
del sistema en un estado aceptable, satisfacer los atributos prioritarios de los tres
stakeholders y terminar sin agotar el Tiempo.</p></div>

<div class="regla"><div class="r-t">PREPARACIÓN</div>
<p>Coloca el tablero. Todas las pistas de calidad comienzan en 0 y el Tiempo en
{TIEMPO_INICIAL}. Deja visibles la Project Card y las 3 Stakeholder Cards. Baraja las
Concern Cards y las Event Cards por separado. Cada jugador recibe una Decision
Preparation Sheet.</p></div>

<div class="regla"><div class="r-t">TURNO</div>
<p>1) Roba una Concern Card. 2) Cada jugador elige o propone una opción de forma
independiente y escribe un rationale breve. 3) Comparen propuestas. 4) El equipo elige
una opción. 5) Paga su costo de Tiempo, aplica los impactos y registra la decisión en la
Decision Taking Sheet.</p></div>

<div class="regla"><div class="r-t">EVENTOS</div>
<p>Después de cada 2 concerns resueltos, roba 1 Event Card. El evento cambia el contexto.
Aplica su efecto y decide si mantienes o reconsideras la decisión afectada.</p></div>

<div class="regla"><div class="r-t">RECONSIDERAR</div>
<p>Para cambiar una decisión ya tomada: revierte sus impactos, paga 1 ficha de Tiempo por
el cambio más max(0, costo nuevo − costo anterior), aplica la nueva opción y registra el
nuevo rationale.</p></div>

<div class="regla"><div class="r-t">NUEVAS OPCIONES</div>
<p>Como en DecidArch, el equipo puede proponer una <b>Opción D</b>. Debe escribir:
descripción, costo de Tiempo (1-4), impactos en JUG/FIA/REN/EXT/ALC y rationale.
No se permite una opción sin trade-offs.</p></div>

<div class="regla vic"><div class="r-t">VICTORIA</div>
<p>Ganan como equipo si: <b>(a)</b> resolvieron los 8 concerns; <b>(b)</b> ninguna pista
de calidad termina bajo 0; <b>(c)</b> para cada stakeholder, todos sus atributos de
prioridad 3 terminan sobre 0; y <b>(d)</b> el Tiempo final es 0 o mayor.</p></div>

<div class="aviso"><b>Está calibrado:</b> de las 6.561 combinaciones posibles de decisiones,
solo el 5,2 % gana. Elegir siempre la opción más barata pierde por falta de arquitectura;
elegir siempre la más completa pierde por falta de tiempo. No existe una línea segura.</div>
<div class="pie">{PIE}</div>
</section>''')

# --- proyecto y atributos
filas = "".join(f'''<div class="qa">
  <div class="qa-cod">{c}</div>
  <div class="qa-txt"><b>{n}</b><br><span class="qa-d">{d}</span>
  <br><span class="qa-map">Condensa: {m}</span></div>
</div>''' for c, n, d, m in TRACKS)

P.append(f'''<section class="pagina">
{cabecera(2, "Proyecto y atributos", "Base de la partida")}
<div class="proj">
  <div class="proj-t">PROJECT CARD · SHINOBI ARENA</div>
  <p><b>Premisa:</b> juego de peleas 2D uno contra uno, vista lateral, control por teclado,
  desarrollado en Greenfoot con Java. El jugador compite en el Torneo de los Cinco Reinos
  enfrentando rivales sucesivos hasta el oponente final.</p>
  <p><b>Core loop:</b> menú → selección de arena → combate → victoria o derrota → reinicio
  o siguiente rival.</p>
  <p><b>Restricciones:</b> prototipo universitario de 3 días efectivos; el motor es Greenfoot
  y no se puede reemplazar; el código debe evidenciar herencia, polimorfismo, encapsulamiento
  y composición; todo el contenido debe ser original; el juego se porta a Unity en la Unidad 3.</p>
  <p><b>La tensión de fondo:</b> el proyecto debe ser un juego que se pueda jugar de principio
  a fin <i>y</i> una pieza de código que demuestre contenidos de POO. Esos dos objetivos no
  siempre apuntan en la misma dirección.</p>
</div>
<div class="sub-t">Pistas de calidad</div>
{filas}
<div class="escala"><b>Escala de impacto por opción:</b> −2 perjudica bastante · −1 perjudica ·
0 neutro · +1 favorece · +2 favorece fuertemente. El <b>costo de Tiempo</b> representa el
esfuerzo relativo para este prototipo; es una adaptación propuesta, no una regla literal
del PDF DecidArch.</div>
<div class="pie">{PIE}</div>
</section>''')

# --- stakeholders
sk = ""
for s in STAKEHOLDERS:
    prio = " ".join(f'<b>{k}:{s["prioridades"][k]}</b>' for k in COD)
    sk += f'''<div class="carta sk">
  <div class="c-top"><span>STAKEHOLDER CARD</span><span class="c-id">{s["sigla"]}</span></div>
  <div class="c-tit">{s["nombre"]}</div>
  <div class="c-body">
    <div class="c-lab">OBJETIVO</div><p>{s["objetivo"]}</p>
    <div class="c-lab">PRIORIDADES</div><p class="prio">{prio}</p>
    <div class="c-lab">TENSIÓN</div><p>{s["tension"]}</p>
    <div class="c-lab">SATISFACCIÓN</div>
    <p>Al final, todo atributo con prioridad 3 en esta carta debe estar sobre 0.</p>
  </div><div class="c-dot"></div>
</div>'''

ref = "".join(f'<tr><td class="rc">{c}</td><td>{n}</td></tr>' for c, n, _, _ in TRACKS)
sk += f'''<div class="carta ref">
  <div class="c-top"><span>CARTA DE REFERENCIA</span><span class="c-id">REF</span></div>
  <div class="c-tit">PISTAS Y ESCALA</div>
  <div class="c-body">
    <div class="c-lab">LAS CINCO PISTAS</div>
    <table class="reftab">{ref}</table>
    <div class="c-lab">ESCALA</div>
    <p>−2 perjudica bastante · −1 perjudica · 0 neutro · +1 favorece · +2 favorece
    fuertemente.</p>
    <div class="c-lab">PRIORIDAD DEL STAKEHOLDER</div>
    <p>3 crítica · 2 alta · 1 media · 0 indiferente. Solo los atributos en 3 condicionan
    la victoria.</p>
    <div class="c-lab">RECUERDA</div>
    <p>Ninguna opción es la respuesta correcta. Lo que se evalúa es el rationale.</p>
  </div><div class="c-dot"></div>
</div>'''

P.append(f'''<section class="pagina">
{cabecera(3, "Stakeholder Cards", "Recortar por los bordes")}
<div class="grid">{sk}</div>
<div class="pie">{PIE}</div>
</section>''')

# --- concerns
def carta_concern(c):
    ops = ""
    for letra, nom, t, desc, im in c["opciones"]:
        ops += f'''<div class="c-lab">OPCIÓN {letra}</div>
<p class="op-n">{letra}. {nom} <span class="t">[Tiempo {t}]</span></p>
<p class="op-d">{desc}</p>
<p class="op-i">{imp(im)}</p>'''
    return f'''<div class="carta cn">
  <div class="c-top"><span>CONCERN CARD</span><span class="c-id">{c["ref"]} · {c["puntaje"]}</span></div>
  <div class="c-tit">{c["id"]} — {c["titulo"]}</div>
  <div class="c-body">
    <div class="c-lab">CONCERN</div><p>{c["pregunta"]}</p>
    {ops}
    <div class="c-lab">REGLA</div>
    <p class="mini">También puedes proponer una Opción D con rationale y trade-offs.</p>
  </div><div class="c-dot"></div>
</div>'''


for i, (ini, fin) in enumerate([(0, 4), (4, 8)], start=1):
    cs = "".join(carta_concern(c) for c in CONCERNS[ini:fin])
    P.append(f'''<section class="pagina">
{cabecera(f"4.{i}", "Concern Cards", "No marcan una respuesta correcta")}
<div class="grid">{cs}</div>
<div class="pie">{PIE}</div>
</section>''')

# --- eventos
def carta_evento(e):
    return f'''<div class="carta ev">
  <div class="c-top"><span>EVENT CARD</span><span class="c-id">{e["id"]}</span></div>
  <div class="c-tit">{e["titulo"]}</div>
  <div class="c-body">
    <div class="c-lab">CAMBIO DE CONTEXTO</div><p>{e["contexto"]}</p>
    <div class="c-lab">CONSECUENCIA</div><p>{e["consecuencia"]}</p>
    <div class="c-lab">DECISIÓN</div>
    <p>El equipo debe registrar si mantiene o cambia la decisión afectada, y por qué.</p>
  </div><div class="c-dot"></div>
</div>'''


for i, (ini, fin) in enumerate([(0, 4), (4, 8)], start=1):
    es = "".join(carta_evento(e) for e in EVENTOS[ini:fin])
    P.append(f'''<section class="pagina">
{cabecera(f"5.{i}", "Event Cards", "Robar después de cada 2 concerns")}
<div class="grid">{es}</div>
<div class="pie">{PIE}</div>
</section>''')

# --- tablero
celdas = "".join(f'<td class="{"cero" if v==0 else ""}">{v}</td>' for v in range(-5, 16))
pistas = "".join(f'''<tr class="tr-pista">
  <td class="tp-cod">{c}</td>{celdas}<td class="tp-nom">{n}</td></tr>''' for c, n, _, _ in TRACKS)
tiempo = "".join(f'<td class="{"cero" if v==0 else ""}">{v}</td>'
                 for v in range(TIEMPO_INICIAL, -1, -1))

P.append(f'''<section class="pagina tablero">
<div class="tb-t">DECIDARENA — TABLERO DE PARTIDA</div>
<div class="slots">
  <div class="slot"><span>PROJECT CARD</span></div>
  <div class="slot"><span>STAKEHOLDER EN FOCO</span></div>
  <div class="slot"><span>CONCERN ACTUAL</span></div>
  <div class="slot"><span>EVENTO / RECONSIDERACIÓN</span></div>
</div>
<div class="tb-s">PISTAS DE CALIDAD</div>
<table class="track">{pistas}</table>
<div class="tb-s">TIEMPO (comienza en {TIEMPO_INICIAL})</div>
<table class="track tiempo"><tr>{tiempo}</tr></table>
<div class="tb-n">Coloca un marcador sobre el 0 de cada pista de calidad y sobre
{TIEMPO_INICIAL} en la pista de Tiempo.</div>
</section>''')

# --- hoja de preparacion
bloques = "".join(f'''<div class="prep">
  <div class="prep-h">Concern {i}: <span class="ln s"></span>
  &nbsp;&nbsp;Opción sugerida: <span class="ln s"></span></div>
  <div class="prep-l">Rationale / trade-off principal:</div>
  <div class="prep-box"></div>
</div>''' for i in range(1, 9))

P.append(f'''<section class="pagina">
{cabecera(6, "Decision Preparation Sheet", "Imprimir una por jugador")}
<div class="campos">Jugador: <span class="ln xl"></span>
&nbsp;&nbsp;Partida: <span class="ln l"></span></div>
{bloques}
<div class="pie">{PIE}</div>
</section>''')

# --- hoja de registro
filas_reg = "".join(f'''<tr><td class="id">{c["id"]}</td><td></td><td></td>
<td></td><td></td><td></td><td></td></tr>''' for c in CONCERNS)

P.append(f'''<section class="pagina">
{cabecera(7, "Decision Taking Sheet", "Registro grupal")}
<div class="campos">Equipo: <span class="ln xl"></span>
&nbsp;&nbsp;Fecha: <span class="ln l"></span>
&nbsp;&nbsp;Tiempo inicial: <b>{TIEMPO_INICIAL}</b></div>
<table class="reg">
<tr><th>ID</th><th>Opción</th><th>Rationale breve</th>
<th>JUG/FIA/REN/EXT/ALC</th><th>Costo</th><th>Evento / Recons.</th><th>Decisión final</th></tr>
{filas_reg}
</table>
<div class="escala">Si se cambia una decisión: revertir los impactos anteriores, aplicar
los nuevos y anotar el motivo del cambio.</div>
<div class="pie">{PIE}</div>
</section>''')

# --- scoring
chk = "".join(f'''<tr><td class="rc">{c}</td><td>{n}</td>
<td class="cast">≥ 0</td><td class="cast"><span class="cuad"></span></td></tr>'''
              for c, n, _, _ in TRACKS)
sat = "".join(f'''<tr><td class="rc">{s["sigla"]}</td><td>{s["nombre"].title()}</td>
<td class="cast">{", ".join(k for k in COD if s["prioridades"][k] == 3)} &gt; 0</td>
<td class="cast"><span class="cuad"></span></td></tr>''' for s in STAKEHOLDERS)

P.append(f'''<section class="pagina">
{cabecera(8, "Scoring Sheet", "Comprobar victoria")}
<div class="sub-t">A. Calidad final</div>
<table class="score">{chk}</table>
<div class="sub-t">B. Satisfacción de stakeholders</div>
<table class="score">{sat}</table>
<div class="sub-t">C. Tiempo y cierre</div>
<div class="cierre">
  <p>Tiempo final: <span class="ln m"></span> (debe ser ≥ 0)</p>
  <p>Concerns resueltos: <span class="ln s"></span> / 8</p>
  <p>Pistas bajo 0: <span class="ln s"></span> (debe ser 0)</p>
</div>
<div class="regla vic"><div class="r-t">RESULTADO</div>
<p>Si las tres secciones se cumplen, el equipo gana. Si alguna falla, anoten cuál y qué
decisión la provocó: esa conversación es el objetivo real del juego.</p></div>
<div class="sub-t">D. Cierre de la partida</div>
<div class="cierre">
  <p>¿Qué decisión resultó más cara de lo esperado?<span class="ln xl"></span></p>
  <p>¿Qué evento los obligó a reconsiderar?<span class="ln xl"></span></p>
  <p>¿Qué harían distinto en una segunda partida?<span class="ln xl"></span></p>
</div>
<div class="pie">{PIE}</div>
</section>''')

# ------------------------------------------------------------------ salida
CSS = open("kit_estilos.css", encoding="utf-8").read()
html = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>{"".join(P)}</body></html>'''

with open("kit.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"kit.html generado — {len(P)} páginas")
