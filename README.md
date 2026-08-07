# Shinobi Arena

Videojuego de peleas 2D uno contra uno desarrollado en **Greenfoot + Java**, para el ramo de Programación de Videojuegos.

El jugador compite en el *Torneo de los Cinco Reinos* enfrentando rivales sucesivos —cada uno con un estilo de combate distinto— hasta el oponente final.

> Todos los personajes, nombres, clanes, técnicas, escenarios e historia son originales.

---

## Entregas

### Unidad 1 — Arquitectura (C1, 20%)

| Semana | Entregable | Estado | Documentación |
|---|---|---|---|
| 1 | Priorización de Concerns | ✅ | [`docs/u1-s1-priorizacion-concerns/`](docs/u1-s1-priorizacion-concerns/) |
| 2 | Priorización NFR → IaC | ⬜ | — |
| 3 | C4 Model Context | ⬜ | — |
| 4 | C4 Model Componente Dinámico | ⬜ | — |
| 5 | Story y Escenarios | ⬜ | — |

### Unidad 2 — Greenfoot (C2, 20%)

| Semana | Entregable | Estado |
|---|---|---|
| 6 | Diagramas de Clases | ⬜ |
| 7 | Refactoring C4 Model Dynamic View | ⬜ |
| 8 | Estrategia de Refactoring | ⬜ |
| 9 | Prototipo de Videojuego | ⬜ |
| 10 | Play Game | ⬜ |

### Unidad 3 — Unity (C3, 30%) · Unidad 4 — Porteo y despliegue (C4, 30%)

Pendientes.

---

## Decisiones arquitectónicas vigentes

Tomadas en la Semana 1 y justificadas en [`docs/u1-s1-priorizacion-concerns/05-decisiones-y-eventos.md`](docs/u1-s1-priorizacion-concerns/05-decisiones-y-eventos.md):

| ID | Decisión | Concern |
|---|---|---|
| D-01 | Clase abstracta `Fighter`; `Player` y `Enemy` la extienden | C-02 |
| D-02 | Patrón **State** para los estados del luchador | C-01 |
| D-03 | Actor `Hitbox` temporal para detectar impactos | C-04 |
| D-04 | `CombatManager` como colaborador de `FightWorld` (no Singleton) | C-05 |

## Estructura del repositorio

```
Shinobi-Arena/
├── docs/       Documentación de arquitectura, una carpeta por entrega
├── scripts/    Utilidades de apoyo (cálculos, validaciones)
└── README.md
```

## Utilidades

```bash
python3 scripts/priorizacion.py    # reproduce la tabla de priorización de concerns
```
