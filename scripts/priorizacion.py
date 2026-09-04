# -*- coding: utf-8 -*-
"""
Priorización de Concerns - Shinobi Arena
PR #1 - Unidad 1, Semana 1

Score = 0.4*Impacto + 0.3*Riesgo + 0.2*Dependencias + 0.1*Exigencia   (escala 1-5)

Ejecutar:  python3 scripts/priorizacion.py
Reproduce la tabla de docs/04-priorizacion.md
"""

PESOS = {"I": 0.4, "R": 0.3, "D": 0.2, "E": 0.1}

# (id, concern, Impacto, Riesgo, Dependencias, Exigencia)
CONCERNS = [
    ("C-01", "Representación del estado del luchador",                  5, 5, 4, 5),
    ("C-02", "Reparto de comportamiento entre Player y Enemy",          5, 5, 5, 5),
    ("C-03", "Toma de decisiones del enemigo (IA)",                     4, 3, 3, 5),
    ("C-04", "Detección de impactos (colisiones de golpes)",            5, 4, 4, 3),
    ("C-05", "Árbitro de las reglas del combate",                       4, 4, 5, 4),
    ("C-06", "Actualización del HUD (vida y chakra)",                   3, 2, 2, 4),
    ("C-07", "Creación de luchadores y sus variantes",                  3, 2, 3, 4),
    ("C-08", "Diferenciación entre personajes jugables",                4, 3, 3, 5),
    ("C-09", "Navegación entre pantallas del juego",                    3, 4, 4, 5),
    ("C-10", "Gestión de animaciones y sprites",                        3, 2, 2, 2),
    ("C-11", "Lectura del teclado",                                     3, 2, 2, 3),
    ("C-12", "Configuración de las arenas de combate",                  3, 3, 2, 4),
]

# Empates: menor valor de desempate = se muestra primero.
# C-08 antes que C-03 porque el polimorfismo pesa más en la rúbrica de U2.
DESEMPATE = {"C-08": 0, "C-03": 1}


def score(i, r, d, e):
    return round(PESOS["I"] * i + PESOS["R"] * r + PESOS["D"] * d + PESOS["E"] * e, 2)


def bloque(s):
    if s >= 4.0:
        return "A"   # decidir en Semana 1
    if s >= 3.0:
        return "B"   # decidir con el C4 Model, Semanas 2-5
    return "C"       # decidir al implementar, Unidad 2


def main():
    filas = [(score(i, r, d, e), cid, nom, i, r, d, e)
             for cid, nom, i, r, d, e in CONCERNS]
    filas.sort(key=lambda f: (-f[0], DESEMPATE.get(f[1], 99), f[1]))

    print("| # | ID | Concern | I | R | D | E | Score | Bloque |")
    print("|---|----|---------|---|---|---|---|-------|--------|")
    for n, (s, cid, nom, i, r, d, e) in enumerate(filas, 1):
        print(f"| {n} | {cid} | {nom} | {i} | {r} | {d} | {e} | **{s:.2f}** | {bloque(s)} |")

    print()
    for b, etiqueta in [("A", "decidir ahora (Semana 1)"),
                        ("B", "decidir con el C4 Model (Semanas 2-5)"),
                        ("C", "decidir al implementar (Unidad 2)")]:
        ids = [f[1] for f in filas if bloque(f[0]) == b]
        print(f"Bloque {b} - {etiqueta}: {len(ids)} concerns -> {', '.join(ids)}")

    assert round(sum(PESOS.values()), 6) == 1.0, "Los pesos deben sumar 1.0"
    assert len(CONCERNS) == 12, "Deben ser 12 concerns"
    assert len({c[0] for c in CONCERNS}) == 12, "Hay IDs duplicados"
    print("\nVerificaciones OK: pesos suman 1.0, 12 concerns, sin IDs duplicados.")


if __name__ == "__main__":
    main()
