# Priorización de Concerns


> **Nota.** Este documento conserva el vocabulario de atributos de la primera versión.
> El análisis y el orden de los concerns siguen vigentes; los nombres de los atributos
> fueron corregidos en [`02-stakeholder-cards.md`](02-stakeholder-cards.md) y el motivo
> está en [`06-correcciones.md`](06-correcciones.md).

Este es el entregable central del PR. Priorizar no es ordenar por gusto: es responder **en qué orden hay que decidir**, con un criterio que otra persona pueda aplicar y obtener el mismo resultado.

---

## 1. Criterio de priorización

Cada concern se puntúa en cuatro dimensiones, escala 1 a 5:

### Impacto en atributos de calidad (I) — peso 0.4

Cuántos atributos de prioridad 1 quedan comprometidos por esta decisión y con qué fuerza.

| Puntaje | Significado |
|---|---|
| 5 | Afecta fuertemente a tres o más atributos de prioridad 1 |
| 4 | Afecta fuertemente a dos atributos de prioridad 1 |
| 3 | Afecta a un atributo de prioridad 1, o a varios de prioridad 2 |
| 2 | Afecta principalmente atributos de prioridad 2 |
| 1 | Afecta solo atributos de prioridad 3 |

### Riesgo de reversión (R) — peso 0.3

Cuánto cuesta cambiar de opción **después** de haber programado sobre ella. Es el criterio que distingue una decisión arquitectónica de una decisión de implementación.

| Puntaje | Significado |
|---|---|
| 5 | Cambiarla obliga a reescribir la mayor parte del código existente |
| 4 | Obliga a modificar varias clases y sus relaciones |
| 3 | Obliga a modificar una clase y quienes la usan |
| 2 | Se cambia dentro de una clase, sin afectar a nadie más |
| 1 | Es un ajuste local reversible en minutos |

### Dependencias (D) — peso 0.2

Cuántos otros concerns quedan bloqueados o condicionados mientras este no se resuelva.

| Puntaje | Significado |
|---|---|
| 5 | Bloquea cinco o más concerns |
| 4 | Bloquea tres o cuatro |
| 3 | Bloquea dos |
| 2 | Bloquea uno |
| 1 | No bloquea a ninguno |

### Exigencia de la rúbrica (E) — peso 0.1

Cuán explícitamente el ramo pide evidencia sobre este punto. Va con peso bajo a propósito: la arquitectura se decide por razones técnicas, y la rúbrica solo desempata.

| Puntaje | Significado |
|---|---|
| 5 | Es un contenido nombrado literalmente en la rúbrica |
| 3 | Está implícito en un contenido de la rúbrica |
| 1 | No aparece en la rúbrica |

### Fórmula

```
Score = 0.4·I + 0.3·R + 0.2·D + 0.1·E        (rango 1.0 – 5.0)
```

**Por qué el Riesgo pesa más que las Dependencias:** un concern muy dependido pero fácil de revertir se puede decidir provisionalmente y corregir después sin costo. Uno de riesgo alto, aunque nadie dependa de él, hay que acertarlo a la primera. En un proyecto de tres días, equivocarse en una decisión irreversible es el único error que no se puede absorber.

---

## 2. Tabla de puntajes

| # | ID | Concern | I | R | D | E | Score | Bloque |
|---|----|---------|---|---|---|---|-------|--------|
| 1 | C-02 | Reparto de comportamiento entre Player y Enemy | 5 | 5 | 5 | 5 | **5.00** | A |
| 2 | C-01 | Representación del estado del luchador | 5 | 5 | 4 | 5 | **4.80** | A |
| 3 | C-04 | Detección de impactos (colisiones de golpes) | 5 | 4 | 4 | 3 | **4.30** | A |
| 4 | C-05 | Árbitro de las reglas del combate | 4 | 4 | 5 | 4 | **4.20** | A |
| 5 | C-09 | Navegación entre pantallas del juego | 3 | 4 | 4 | 5 | **3.70** | B |
| 6 | C-08 | Diferenciación entre personajes jugables | 4 | 3 | 3 | 5 | **3.60** | B |
| 7 | C-03 | Toma de decisiones del enemigo (IA) | 4 | 3 | 3 | 5 | **3.60** | B |
| 8 | C-12 | Configuración de las arenas de combate | 3 | 3 | 2 | 4 | **2.90** | C |
| 9 | C-07 | Creación de luchadores y sus variantes | 3 | 2 | 3 | 4 | **2.80** | C |
| 10 | C-06 | Actualización del HUD (vida y chakra) | 3 | 2 | 2 | 4 | **2.60** | C |
| 11 | C-11 | Lectura del teclado | 3 | 2 | 2 | 3 | **2.50** | C |
| 12 | C-10 | Gestión de animaciones y sprites | 3 | 2 | 2 | 2 | **2.40** | C |

*Los puntajes fueron calculados con el script [`../scripts/priorizacion.py`](../../scripts/priorizacion.py), que reproduce esta tabla exacta.*

**Desempate C-08 / C-03:** ambos obtienen 3.60. Se coloca C-08 primero porque la diferenciación de personajes es la evidencia principal de **polimorfismo** del proyecto —el contenido con más peso en la rúbrica de la Unidad 2— mientras que la IA del enemigo puede empezar simple y refinarse.

---

## 3. Justificación de los cuatro primeros

### 1º — C-02 · Reparto de comportamiento entre Player y Enemy (5.00)

Único concern con 5 en las cuatro dimensiones. Define la jerarquía de clases completa: cada concern posterior asume implícitamente si existe o no un `Fighter` común. Decidirlo tarde significa que la lógica de vida, chakra, gravedad y daño ya está duplicada en dos clases, y que la duplicación es justamente lo que la rúbrica de refactoring penaliza. Es literalmente la primera línea de código del proyecto.

### 2º — C-01 · Representación del estado del luchador (4.80)

El estado atraviesa todo: qué se dibuja, qué input se acepta, si el golpe conecta, si el luchador puede moverse. Empezar con banderas booleanas y migrar a State después implica reescribir el `act()` de ambos luchadores y toda la lógica de animación. El riesgo es 5 porque no hay migración gradual posible: o se piensa en estados desde el inicio, o se reescribe. La rúbrica además nombra el patrón State explícitamente como opción sugerida.

### 3º — C-04 · Detección de impactos (4.30)

El impacto más alto posible en Jugabilidad —es lo que hace que un juego de peleas se sienta bien o se sienta roto— y define si existen o no clases como `Hitbox` y `Projectile`. Su Exigencia es baja (3) porque el ramo pide "sistema de colisiones" sin especificar cómo, pero su Impacto y Riesgo lo suben igual al Bloque A. Es el mejor ejemplo de por qué la rúbrica pesa 0.1: la decisión importa por razones técnicas, no porque la pidan.

### 4º — C-05 · Árbitro de las reglas del combate (4.20)

El de mayor Dependencias (5): daño, bloqueo, chakra, victoria y derrota pasan todos por aquí. Es la decisión que evita —o produce— la clase-Dios que el ramo prohíbe explícitamente en *Architectural Concerns*: "evitar que toda la lógica se encuentre dentro de una sola clase". Si `FightWorld` acumula las reglas, separarlas después obliga a desmontar la clase que ya coordina todo lo demás.

---

## 4. Por qué los del Bloque C pueden esperar

No es que sean poco importantes; es que **son locales y reversibles**.

- **C-06 (HUD)** — se puede empezar con polling y migrar a Observer cambiando solo dos clases, sin tocar el combate.
- **C-07 (creación)** — pasar de `new` directo a una `FighterFactory` es un refactor de una tarde, y es justamente el tipo de cambio que la Semana 8 (*Estrategia de Refactoring*) pide documentar.
- **C-10 (animaciones)** — encapsulado dentro del luchador; nada fuera de él depende de cómo se cargan las imágenes.
- **C-11 (teclado)** — afecta a una sola clase, `Player`.
- **C-12 (arenas)** — el prototipo necesita dos arenas y ambas opciones funcionan para dos; la diferencia recién aparece en la cuarta o quinta.

Dejarlos en Bloque C es una decisión deliberada: **son la reserva de refactoring de la Unidad 2**. Implementarlos primero en su versión simple y luego refactorizarlos produce la evidencia que piden las Semanas 7 y 8, en vez de tener que inventarla.

---

## 5. Mapa de dependencias

```
C-02  Fighter (Player/Enemy)
 ├──> C-01  Estado del luchador
 │     ├──> C-04  Detección de impactos
 │     └──> C-10  Animaciones
 ├──> C-03  IA del enemigo
 ├──> C-08  Diferenciación de personajes ──> C-07  Creación de luchadores
 ├──> C-06  Actualización del HUD
 └──> C-11  Lectura del teclado

C-05  Árbitro del combate
 ├──> C-04  Detección de impactos
 ├──> C-06  Actualización del HUD
 └──> C-09  Navegación entre pantallas ──> C-12  Arenas
```

Se lee de arriba hacia abajo: nada bajo `C-02` se puede decidir bien sin saber si existe una clase base común. Este grafo es el insumo directo del **C4 Model — Componente Dinámico** de la Semana 4.
