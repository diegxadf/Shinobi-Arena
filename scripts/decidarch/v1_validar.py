# -*- coding: utf-8 -*-
"""
Valida el mazo contra las reglas oficiales de DecidArch v1 y contra la
retroalimentacion del profesor (clase del 13 de agosto).

Scoring oficial (DecidArch-ScoreSheet.pdf):
  Paso 1  QA-Score = A - B,  A = numero de '+' (un '++' cuenta doble)
                             B = numero de '-' (un '--' cuenta doble)
  Paso 2  Por cada atributo de cada stakeholder: C = QA-Score - QA-Priority
          Si algun C < 0 -> se pierde la partida
          Stakeholders-Score = suma de los C
  Paso 3  Final Score = Stakeholders-Score - D,  D = concerns sin resolver
"""

import itertools
from v1_datos import QUALITY_ATTRIBUTES, QA, PROJECT, STAKEHOLDERS, CONCERNS, EVENTS

fallos, avisos = [], []
def check(c, m):  (None if c else fallos.append(m))
def warn(c, m):   (None if c else avisos.append(m))

VALOR = {"++": 2, "+": 1, "-": -1, "--": -2}

# ---- 1. tamano del mazo, igual al set oficial -----------------------------
check(len(CONCERNS) == 10, f"El set oficial trae 10 Concern Cards; hay {len(CONCERNS)}")
check(len(EVENTS) == 6,    f"El set oficial trae 6 Event Cards; hay {len(EVENTS)}")
check(len(STAKEHOLDERS) >= 2, "Debe haber al menos 2 Stakeholder Cards")
check(set(PROJECT) == {"project", "purpose"},
      "La Project Card oficial solo tiene los campos Project y Purpose")

# ---- 2. estructura de las cartas -----------------------------------------
for c in CONCERNS:
    check(len(c["options"]) == 3, f"Concern {c['id']}: el set oficial usa 3 opciones")
    for i, (desc, imp) in enumerate(c["options"], 1):
        check(all(v in VALOR for v in imp.values()),
              f"Concern {c['id']} opcion {i}: simbolo invalido (solo + ++ - --)")
        check(all(k in QA for k in imp),
              f"Concern {c['id']} opcion {i}: atributo desconocido")
        check(any(VALOR[v] > 0 for v in imp.values()),
              f"Concern {c['id']} opcion {i}: sin ningun impacto positivo")
        check(any(VALOR[v] < 0 for v in imp.values()),
              f"Concern {c['id']} opcion {i}: sin trade-offs, todos los impactos favorecen")

for e in EVENTS:
    check(set(e) == {"title", "description", "cambios"},
          f"Event '{e.get('title','?')}': campos inesperados")
    for st, at, pr in e["cambios"]:
        check(any(x["nombre"] == st for x in STAKEHOLDERS),
              f"Event '{e['title']}': stakeholder '{st}' no existe")
        check(at in QA, f"Event '{e['title']}': atributo '{at}' no existe")
        check(0 <= pr <= 3, f"Event '{e['title']}': prioridad {pr} fuera de 0-3")
        check(any(at in x["qa"] for x in STAKEHOLDERS if x["nombre"] == st),
              f"Event '{e['title']}': '{st}' no declara '{at}' en su carta")
check(all(x["qa"][k] == 0 for x in STAKEHOLDERS for k in x["qa"]),
      "En el CardSet oficial todas las QA-Priority se imprimen en 0")

# ---- 3. REGLA DEL PROFESOR ------------------------------------------------
# "No pueden haber atributos de calidad puestos aca que no tengan
#  correspondencia con un stakeholder."
reclamados = set()
for s in STAKEHOLDERS:
    reclamados |= set(s["qa"])
    check(all(k in QA for k in s["qa"]), f"{s['nombre']}: atributo desconocido")
    check(all(0 <= v <= 3 for v in s["qa"].values()),
          f"{s['nombre']}: QA-Priority fuera del rango 0-3")

usados = set()
for c in CONCERNS:
    for i, (_, imp) in enumerate(c["options"], 1):
        for k in imp:
            usados.add(k)
            check(k in reclamados,
                  f"Concern {c['id']} opcion {i}: '{k}' no le interesa a ningun stakeholder")

warn(reclamados <= usados,
     f"Atributos que ningun concern toca: {sorted(reclamados - usados)}")
check(usados <= set(QA) and reclamados <= set(QA), "Atributo fuera del catalogo declarado")

# ---- 4. ninguna opcion domina a otra --------------------------------------
def vec(imp):
    return {k: VALOR[imp[k]] if k in imp else 0 for k in QA}

for c in CONCERNS:
    for (a, (da, ia)), (b, (db, ib)) in itertools.permutations(
            list(enumerate(c["options"], 1)), 2):
        va, vb = vec(ia), vec(ib)
        if all(va[k] >= vb[k] for k in QA) and any(va[k] > vb[k] for k in QA):
            fallos.append(f"Concern {c['id']}: la opcion {a} domina a la {b}")

# ---- 5. scoring oficial ---------------------------------------------------
def qa_scores(eleccion):
    s = {k: 0 for k in QA}
    for c, idx in zip(CONCERNS, eleccion):
        for k, v in c["options"][idx][1].items():
            s[k] += VALOR[v]
    return s

def prioridades(eventos):
    """Prioridades tras aplicar los eventos indicados. Parten todas en 0."""
    pr = {st["nombre"]: dict(st["qa"]) for st in STAKEHOLDERS}
    for e in eventos:
        for stn, at, val in e["cambios"]:
            pr[stn][at] = val
    return pr

def evaluar(eleccion, sin_resolver=0, eventos=()):
    s = qa_scores(eleccion)
    pr = prioridades(eventos)
    cs, perdio = [], False
    for st in STAKEHOLDERS:
        for k, prio in pr[st["nombre"]].items():
            c = s[k] - prio
            cs.append(c)
            if c < 0:
                perdio = True
    return s, sum(cs) - sin_resolver, perdio

ESC = EVENTS  # escenario duro: se robaron los 6 eventos
total, ganadoras, mejor = 0, 0, None
for combo in itertools.product(range(3), repeat=len(CONCERNS)):
    total += 1
    s, final, perdio = evaluar(combo, eventos=ESC)
    if not perdio:
        ganadoras += 1
        if mejor is None or final > mejor[1]:
            mejor = (combo, final, s)

pct = 100 * ganadoras / total
check(ganadoras > 0, "Ningun conjunto de decisiones gana: el mazo es imposible")
check(ganadoras < total, "Todos los conjuntos ganan: el mazo no exige decidir")
warn(1 <= pct <= 45, f"Dificultad: gana el {pct:.1f}% de las combinaciones")

for idx, nom in enumerate(["todas 1 (lo mas barato)", "todas 2 (lo intermedio)",
                           "todas 3 (lo mas completo)"]):
    _, _, perdio = evaluar((idx,) * len(CONCERNS), eventos=ESC)
    check(perdio, f"La estrategia trivial '{nom}' gana; el mazo no obliga a decidir")

# ---- informe --------------------------------------------------------------
L = "=" * 70
print(L); print("VALIDACION DEL MAZO — DecidArch v1"); print(L)
print(f"Project Card: 1   Stakeholders: {len(STAKEHOLDERS)}   "
      f"Concerns: {len(CONCERNS)}   Events: {len(EVENTS)}")
print(f"Atributos de calidad declarados: {len(QA)}")
print()
print("Cobertura de atributos (regla del profesor)")
for k in QA:
    quien = [s["nombre"] for s in STAKEHOLDERS if k in s["qa"]]
    n = sum(1 for c in CONCERNS for _, i in c["options"] if k in i)
    print(f"  {k:16s} interesa a: {', '.join(quien):45s} aparece en {n:2d} opciones")
print()
print("Escenario evaluado: se robaron los 6 eventos (maxima exigencia)")
sin_ev = sum(1 for cb in itertools.product(range(3), repeat=len(CONCERNS))
             if not evaluar(cb)[2])
print(f"Combinaciones posibles: {total}")
print(f"  ganadoras sin eventos:  {sin_ev:6d} ({100*sin_ev/total:5.1f}%)")
print(f"  ganadoras con 6 eventos:{ganadoras:6d} ({pct:5.1f}%)")
print()
print("Estrategias triviales (segun el Scoring Sheet oficial):")
for idx, nom in enumerate(["todas 1", "todas 2", "todas 3"]):
    s, final, perdio = evaluar((idx,) * len(CONCERNS), eventos=ESC)
    print(f"  {nom:9s} -> {'PIERDE' if perdio else 'gana  '}   Final Score {final:+4d}")
print()
if mejor:
    combo, final, s = mejor
    print("Mejor partida posible:")
    print("   " + "  ".join(f"C{c['id']}:{i+1}" for c, i in zip(CONCERNS, combo)))
    print("   QA-Scores: " + "  ".join(f"{k[:4]}{s[k]:+d}" for k in QA))
    rango = ("Excelente" if final >= 30 else "Muy bueno" if final >= 20
             else "Bueno" if final >= 10 else "Suficiente" if final >= 0 else "Perdida")
    print(f"   Final Score {final}  ->  {rango}")
print()
for a in avisos:
    print("  ~ aviso: " + a)
if fallos:
    print("\nFALLOS:")
    for f in fallos:
        print("  x " + f)
    raise SystemExit(1)
print("\nTodas las validaciones OK")
