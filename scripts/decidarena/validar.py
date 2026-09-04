# -*- coding: utf-8 -*-
"""Valida que DecidArena sea un juego jugable: ganable, perdible y sin estrategia dominante."""

import itertools
from kit_datos import TRACKS, COD, STAKEHOLDERS, CONCERNS, EVENTOS, TIEMPO_INICIAL

fallos = []


def check(cond, msg):
    if not cond:
        fallos.append(msg)


# ---- 1. integridad estructural -------------------------------------------
check(len(CONCERNS) == 8, "Deben ser 8 concerns")
check(len(EVENTOS) == 8, "Deben ser 8 eventos")
check(len(TRACKS) == 5, "Deben ser 5 pistas de calidad")

for c in CONCERNS:
    check(len(c["opciones"]) == 3, f"{c['id']}: deben ser 3 opciones")
    for letra, nom, t, desc, imp in c["opciones"]:
        check(set(imp.keys()) == set(COD), f"{c['id']}{letra}: faltan pistas")
        check(1 <= t <= 4, f"{c['id']}{letra}: Tiempo fuera de 1-4")
        # regla del template: ninguna opcion sin trade-offs
        check(any(v < 0 for v in imp.values()),
              f"{c['id']}{letra} '{nom}': no tiene ningun impacto negativo (opcion sin trade-off)")
        check(any(v > 0 for v in imp.values()),
              f"{c['id']}{letra} '{nom}': no tiene ningun impacto positivo")

# ---- 2. ninguna opcion domina a otra dentro del mismo concern -------------
for c in CONCERNS:
    for (l1, n1, t1, _, i1), (l2, n2, t2, _, i2) in itertools.permutations(c["opciones"], 2):
        mejor_o_igual = all(i1[k] >= i2[k] for k in COD) and t1 <= t2
        estrictamente = any(i1[k] > i2[k] for k in COD) or t1 < t2
        check(not (mejor_o_igual and estrictamente),
              f"{c['id']}: la opcion {l1} domina a la {l2} (mejor o igual en todo y no mas cara)")

# ---- 3. los eventos apuntan a concerns existentes -------------------------
ids = {c["id"] for c in CONCERNS}
for e in EVENTOS:
    check(e["revisa"] in ids or e["revisa"] == "-",
          f"{e['id']}: revisa '{e['revisa']}', que no es un concern del mazo")

# ---- 4. simulacion: victoria posible, derrota posible ---------------------
PRIO3 = {s["sigla"]: [k for k, v in s["prioridades"].items() if v == 3] for s in STAKEHOLDERS}


def jugar(indices):
    tracks = {k: 0 for k in COD}
    tiempo = TIEMPO_INICIAL
    for c, idx in zip(CONCERNS, indices):
        _, _, t, _, imp = c["opciones"][idx]
        tiempo -= t
        for k in COD:
            tracks[k] += imp[k]
    return tracks, tiempo


def gana(tracks, tiempo):
    if tiempo < 0:
        return False
    if any(v < 0 for v in tracks.values()):
        return False
    for atrs in PRIO3.values():
        if any(tracks[a] <= 0 for a in atrs):
            return False
    return True


total = 0
victorias = []
for combo in itertools.product(range(3), repeat=8):
    tracks, tiempo = jugar(combo)
    total += 1
    if gana(tracks, tiempo):
        victorias.append(combo)

pct = 100 * len(victorias) / total
check(len(victorias) > 0, "El juego es imposible de ganar")
check(len(victorias) < total, "El juego es imposible de perder")
check(2 <= pct <= 40,
      f"Dificultad mal calibrada: gana el {pct:.1f}% de las combinaciones (se busca entre 2% y 40%)")

# ---- 5. ninguna estrategia trivial gana -----------------------------------
for idx, nombre in [(0, "todas A (siempre lo mas barato)"),
                    (1, "todas B (siempre lo intermedio)"),
                    (2, "todas C (siempre lo mas completo)")]:
    tr, ti = jugar((idx,) * 8)
    if False:
        pass
    check(not gana(tr, ti),
          f"Estrategia trivial '{nombre}' gana la partida; el juego no obliga a decidir")

# ---- informe --------------------------------------------------------------
print("=" * 66)
print("VALIDACION DE DECIDARENA")
print("=" * 66)
print(f"Concerns: {len(CONCERNS)}   Eventos: {len(EVENTOS)}   Pistas: {len(TRACKS)}")
print(f"Tiempo inicial: {TIEMPO_INICIAL}")
print(f"Combinaciones posibles: {total}")
print(f"Combinaciones ganadoras: {len(victorias)}  ({pct:.1f}%)")
print()
print("Estrategias triviales:")
for idx, nombre in [(0, "todas A"), (1, "todas B"), (2, "todas C")]:
    tr, ti = jugar((idx,) * 8)
    estado = "GANA" if gana(tr, ti) else "pierde"
    print(f"  {nombre:10s} -> {estado:6s}  "
          + "  ".join(f"{k}{tr[k]:+d}" for k in COD)
          + f"   Tiempo {ti:+d}")
print()
print("Atributos de prioridad 3 que deben terminar sobre 0:")
for s in STAKEHOLDERS:
    print(f"  {s['sigla']} {s['nombre']:22s} -> {', '.join(PRIO3[s['sigla']]) or '(ninguno)'}")
print()
if victorias:
    ej = victorias[len(victorias) // 2]
    tr, ti = jugar(ej)
    print("Ejemplo de partida ganadora:")
    print("  " + "  ".join(f"{c['id']}{'ABC'[i]}" for c, i in zip(CONCERNS, ej)))
    print("  " + "  ".join(f"{k}{tr[k]:+d}" for k in COD) + f"   Tiempo {ti:+d}")
print()
if fallos:
    print("FALLOS:")
    for f in fallos:
        print("  x " + f)
    raise SystemExit(1)
print("Todas las validaciones OK")
