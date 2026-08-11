# PR #1 — Priorización de Concerns · Shinobi Arena

**Unidad 1 (C1) · Semana 1 · 3–10 de agosto**
**Tema de la rúbrica:** Architectural Concerns
**Método aplicado:** DecidArch (card set del ramo), adaptado al proyecto propio

---

## Qué entrega este PR

La Semana 1 no pide código ni diagramas todavía: pide **identificar y priorizar los concerns arquitectónicos** del proyecto. Este PR hace exactamente eso, reutilizando el formato de cartas de DecidArch (Project / Stakeholder / Concern / Event) sobre *Shinobi Arena* en lugar del caso de ejemplo "Social News Platform" que trae el set.

| Documento | Contenido |
|---|---|
| [`docs/01-project-card.md`](01-project-card.md) | Project Card: propósito, alcance y restricciones del sistema |
| [`docs/02-stakeholder-cards.md`](02-stakeholder-cards.md) | 3 Stakeholder Cards con atributos de calidad y su QA-Priority |
| [`docs/03-concern-cards.md`](03-concern-cards.md) | 12 Concern Cards con opciones y su impacto en atributos de calidad |
| [`docs/04-priorizacion.md`](04-priorizacion.md) | Criterio de priorización, tabla de puntajes y ranking en 3 bloques |
| [`docs/05-decisiones-y-eventos.md`](05-decisiones-y-eventos.md) | Decisión tomada en los 4 concerns del Bloque A + Event Cards del ramo |
| [`PULL_REQUEST.md`](PULL_REQUEST.md) | Texto publicado en la descripción del PR |
| [`DecidArena-Kit-Imprimible.pdf`](DecidArena-Kit-Imprimible.pdf) | **Versión jugable e imprimible** de esta entrega: 12 páginas A4 con cartas recortables, tablero y hojas de registro |

## Versión imprimible

La misma priorización, convertida en un juego de mesa jugable siguiendo el formato del kit
DecidArch: 3 Stakeholder Cards, 8 Concern Cards, 8 Event Cards, tablero de pistas de calidad
y hojas de preparación, registro y puntuación.

Los 8 concerns del mazo son los 8 mejor puntuados de los 12 de
[`04-priorizacion.md`](04-priorizacion.md), en ese mismo orden. Los 9 atributos de calidad se
condensan en 5 pistas jugables (JUG, FIA, REN, EXT, ALC); cada carta indica qué condensa.

El generador está en [`scripts/decidarena/`](../../scripts/decidarena/) e incluye un
validador que comprueba que el juego sea ganable, perdible y sin estrategia dominante antes
de producir el PDF.

## Resultado en una tabla

Los 12 concerns quedaron ordenados por el puntaje `0.4·Impacto + 0.3·Riesgo + 0.2·Dependencias + 0.1·Exigencia`:

| Bloque | Cuándo se decide | Concerns |
|---|---|---|
| **A — decidir ahora** | Semana 1, antes de escribir la primera clase | C-02 Reparto Player/Enemy · C-01 Estado del luchador · C-04 Detección de impactos · C-05 Árbitro del combate |
| **B — decidir con el C4 Model** | Semanas 2–5 | C-09 Navegación entre pantallas · C-08 Diferenciación de personajes · C-03 IA del enemigo |
| **C — decidir al implementar** | Unidad 2 (Greenfoot) | C-12 Arenas · C-07 Creación de luchadores · C-06 HUD · C-11 Teclado · C-10 Animaciones |

El criterio de corte no es "qué me interesa más", sino **cuánto cuesta cambiar la decisión después**. Los cuatro del Bloque A son los que, si se deciden mal, obligan a reescribir el resto del proyecto; los del Bloque C son locales y se pueden cambiar en una tarde.

## Por qué se separó "priorizar concerns" de "tomar decisiones"

DecidArch mezcla ambas cosas en una partida. Para esta entrega se separaron a propósito:

- **Priorizar** un concern responde *¿cuándo tengo que decidir esto?*
- **Decidir** un concern responde *¿qué opción elijo?*

La Semana 1 evalúa lo primero. Lo segundo se documenta solo para el Bloque A (en [`05-decisiones-y-eventos.md`](05-decisiones-y-eventos.md)), porque son decisiones que ya bloquean el trabajo de la Semana 2.

Corresponde a la Unidad 1, Semana 1 (3–10 de agosto).
