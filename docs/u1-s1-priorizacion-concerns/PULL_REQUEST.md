# Texto para la descripción del Pull Request

> Copiar desde aquí hacia abajo en el campo de descripción del PR en GitHub.

---

**Título del PR:** `PR#1 · U1-S1 · Priorización de Concerns — Shinobi Arena`

**Rama sugerida:** `docs/pr01-priorizacion-concerns`

---

## Descripción

Primera entrega de la Unidad 1 (Semana 1, 3–10 de agosto). Identifica y prioriza los **concerns arquitectónicos** de *Shinobi Arena*, aplicando el método DecidArch del ramo sobre el proyecto propio en lugar del caso de ejemplo del card set.

## Qué se agrega

- **Project Card** con propósito, alcance del prototipo y 6 restricciones que acotan el espacio de decisión.
- **3 Stakeholder Cards** (Jugador, Docente/Evaluador, Desarrollador) con 9 atributos de calidad y su QA-Priority, siguiendo la convención del card set donde 1 es la prioridad más alta.
- **12 Concern Cards** con opciones numeradas e impacto sobre atributos de calidad.
- **Criterio de priorización explícito y reproducible**: `Score = 0.4·Impacto + 0.3·Riesgo de reversión + 0.2·Dependencias + 0.1·Exigencia de rúbrica`.
- **Ranking en 3 bloques** según cuándo debe tomarse cada decisión.
- **4 decisiones tomadas** (Bloque A) con su trade-off y su condición de revisión.
- **3 Event Cards** derivadas de restricciones reales del ramo.
- Script `scripts/priorizacion.py` que reproduce la tabla de puntajes.

## Resultado

| Bloque | Cuándo | Concerns |
|---|---|---|
| **A** | Semana 1 | C-02 Reparto Player/Enemy · C-01 Estado del luchador · C-04 Detección de impactos · C-05 Árbitro del combate |
| **B** | Semanas 2–5 | C-09 Navegación · C-08 Diferenciación de personajes · C-03 IA del enemigo |
| **C** | Unidad 2 | C-12 Arenas · C-07 Creación de luchadores · C-06 HUD · C-11 Teclado · C-10 Animaciones |

Decisiones del Bloque A: `Fighter` abstracta con `Player`/`Enemy` · patrón **State** para los estados del luchador · `Hitbox` temporal para los impactos · `CombatManager` como colaborador de `FightWorld` (no Singleton).

## Cobertura de la rúbrica — Unidad 1, Semana 1

| Contenido | Dónde |
|---|---|
| Architectural Concerns | `docs/u1-s1-priorizacion-concerns/03-concern-cards.md` — 12 concerns con opciones e impacto |
| Priorización | `docs/u1-s1-priorizacion-concerns/04-priorizacion.md` — criterio, puntajes y bloques |
| Architectural Concerns / clase-Dios | Decisión D-04: `CombatManager` separado de `FightWorld` |
| Architectural Design Patterns | Decisión D-02: patrón State, con justificación técnica y plan de contingencia |
| Trazabilidad hacia el C4 Model | Grafo de dependencias en `docs/u1-s1-priorizacion-concerns/04-priorizacion.md` §5, insumo de la Semana 4 |
