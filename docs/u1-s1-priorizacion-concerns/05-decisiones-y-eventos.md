# Decisiones del Bloque A y Event Cards

## Parte 1 — Decisiones tomadas

Solo se deciden aquí los cuatro concerns del Bloque A, porque bloquean el trabajo de la Semana 2. Los Bloques B y C quedan abiertos a propósito: decidirlos ahora sería adivinar sin información.

Cada decisión sigue el formato de una partida de DecidArch: opción elegida, atributos favorecidos, **atributo sacrificado** (una decisión que no sacrifica nada es señal de que el concern estaba mal planteado) y condición de revisión.

---

### D-01 · Concern C-02 — Reparto de comportamiento entre Player y Enemy

**Opción elegida: 2 — Clase abstracta `Fighter`, con `Player` y `Enemy` como subclases.**

`Fighter` concentra vida, chakra, posición, gravedad, recibir daño y morir. Declara un método abstracto `decidirAccion()` que cada subclase implementa: `Player` lo resuelve leyendo el teclado, `Enemy` consultando su IA. `Fighter.act()` queda como método plantilla: decide, aplica física, resuelve colisiones, actualiza estado.

| | |
|---|---|
| **Favorece** | MOD (++), COM (++), TRA (++), SIM (+) |
| **Sacrifica** | Nada relevante en esta escala. La opción 3 (componentes) daría más MOD y POR, pero a un costo de SIM que el plazo no admite |
| **Por qué no la 1** | Duplicar la lógica en dos clases es exactamente el antipatrón que la Unidad 2 pide eliminar |
| **Por qué no la 3** | Composición por componentes se justifica cuando los componentes se recombinan de verdad. Con un jugador y dos enemigos no hay variación que la sostenga, y sería un patrón puesto para aparentar complejidad |
| **Se revisa si** | Aparece un enemigo que necesita un esquema de movimiento radicalmente distinto (por ejemplo, volar) |

> Este es el punto donde el proyecto demuestra **herencia** y **método plantilla**. `Fighter` es abstracta y no se instancia nunca.

---

### D-02 · Concern C-01 — Representación del estado del luchador

**Opción elegida: 3 — Patrón State, con una clase por estado.**

Interfaz `FighterState` con `entrar(Fighter)`, `actualizar(Fighter)` y `salir(Fighter)`. Implementaciones: `IdleState`, `WalkingState`, `JumpingState`, `AttackingState`, `BlockingState`, `HurtState`, `DefeatedState`. `Fighter` contiene su estado actual y delega en él; los estados deciden a cuál transitar.

| | |
|---|---|
| **Favorece** | MOD (++), COM (++), TRA (++), FIA (++) |
| **Sacrifica** | **SIM (--)**: siete clases pequeñas en vez de un `enum` y un `switch`. Es el costo aceptado más caro del proyecto |
| **Por qué se acepta** | Resuelve por construcción el problema de "durante ATTACKING no se puede bloquear": si el estado no implementa la transición, la acción es imposible. Con banderas booleanas ese problema reaparece como bug en cada estado nuevo |
| **Alternativa de contingencia** | Si al final del Día 1 los estados no están funcionando, se retrocede a la opción 2 (`enum` + `switch`) que preserva la misma separación conceptual con menos clases. Se documenta el retroceso como decisión, no como fracaso |
| **Se revisa si** | El Día 1 termina sin movimiento funcional en pantalla |

> Aquí vive el **patrón de diseño** exigido por la rúbrica, y se puede defender oralmente sin recurrir a "lo puse porque lo pedían": el patrón elimina una clase entera de bugs.

---

### D-03 · Concern C-04 — Detección de impactos

**Opción elegida: 2 — Actor `Hitbox` temporal.**

Cuando `AttackingState` alcanza sus frames activos, crea un `Hitbox` frente al luchador con daño, duración y dueño. El `Hitbox` detecta intersección con `Fighter` distinto de su dueño, reporta el impacto al `CombatManager` y se autodestruye. `Projectile` reutiliza el mismo mecanismo, pero se desplaza en vez de acompañar al atacante.

| | |
|---|---|
| **Favorece** | JUG (++), MOD (++), TRA (++), COM (+) |
| **Sacrifica** | **SIM (-)**: dos clases más (`Hitbox`, `Projectile`) y actores que aparecen y desaparecen durante el combate |
| **Por qué no la 1** | Intersectar los sprites completos hace que el jugador reciba daño por estar cerca en vez de por ser golpeado. Es el defecto que arruina la sensación de un juego de peleas |
| **Por qué no la 3** | El cálculo geométrico puro es más eficiente y testeable, pero renuncia al soporte de colisiones de Greenfoot que la Unidad 2 pide usar |
| **Se revisa si** | La cantidad de actores temporales degrada el rendimiento con varios proyectiles simultáneos |

> `Hitbox` y `Projectile` heredando de `Actor` con comportamiento compartido son un segundo lugar donde se evidencia **herencia**, independiente de la jerarquía de `Fighter`.

---

### D-04 · Concern C-05 — Árbitro de las reglas del combate

**Opción elegida: 2 — `CombatManager` como colaborador de `FightWorld`.**

`FightWorld` construye el escenario, crea los actores y el `CombatManager`, y le delega las reglas. El `CombatManager` aplica daño, considera el bloqueo, administra el chakra, detecta la derrota y avisa el fin del combate. No sabe dibujar ni leer teclado: recibe eventos y responde con decisiones.

| | |
|---|---|
| **Favorece** | COM (++), MOD (++), TES (++), POR (++) |
| **Sacrifica** | **SIM (-)**: una clase más y una indirección entre `FightWorld` y las reglas |
| **Por qué no la 1** | Produce la clase-Dios que *Architectural Concerns* prohíbe explícitamente |
| **Por qué no la 3** | Un Singleton hace el acceso más cómodo y las pruebas imposibles: el estado del combate anterior sobrevive al reinicio de partida, que es justamente una funcionalidad requerida. La rúbrica advierte usar Singleton "solamente si realmente es necesario"; aquí no lo es |
| **Se revisa si** | El `CombatManager` empieza a necesitar acceso a la representación visual |

> Esta decisión es la que hace que las reglas del combate sobrevivan al **porteo a Unity** de la Unidad 3: `CombatManager` no depende de la API de Greenfoot y se traduce casi literalmente a C#.

---

### Resumen de sacrificios

| Decisión | Atributo sacrificado | Magnitud |
|---|---|---|
| D-01 Fighter abstracta | Portabilidad respecto de la opción por componentes | Baja |
| D-02 Patrón State | **Simplicidad** | **Alta** |
| D-03 Hitbox temporal | Simplicidad y rendimiento | Media |
| D-04 CombatManager | Simplicidad | Baja |

Las cuatro decisiones sacrifican **Simplicidad**, que es un atributo de prioridad 1. Esto es coherente, no contradictorio: el ramo evalúa arquitectura, y la Simplicidad se protege recortando **alcance** —menos personajes, menos animaciones, sin sonido— y no recortando estructura. El presupuesto de complejidad se gasta entero en el Bloque A y no queda nada para los Bloques B y C, que por eso arrancan en su opción más simple.

---

## Parte 2 — Event Cards

Las Event Cards de DecidArch introducen cambios de contexto a mitad de partida y obligan a repriorizar. Estas tres son eventos reales del ramo, no hipotéticos.

---

### Event Card E-01

**Title:** Receso de Fiestas Patrias

**Description:**
La semana del 18 de septiembre no tiene clases ni entrega, de modo que el calendario del semestre se corre y el tiempo disponible para el prototipo se acorta.

Cambia la QA-Priority del **Desarrollador**:
- Simplicidad / Tiempo → se mantiene en **1**, pero se vuelve vinculante: cualquier decisión de Bloque B o C que compita con el plazo se resuelve por la opción más simple.

**Consecuencia sobre la priorización:** ninguna reordenación. El Bloque C se congela en su opción 1 hasta que el prototipo esté jugable de principio a fin.

---

### Event Card E-02

**Title:** El juego se porta a Unity

**Description:**
La Unidad 3 exige rehacer el juego en Unity con C#, y la Unidad 4 exige portarlo y desplegarlo. Lo que esté acoplado a la API de Greenfoot habrá que reescribirlo desde cero.

Cambia la QA-Priority del **Desarrollador**:
- Portabilidad: **3 → 2**

**Consecuencia sobre la priorización:**

- **C-05** (árbitro del combate) sube su Impacto de 4 a 5: la opción `CombatManager` desacoplado es ahora la única que preserva trabajo entre unidades. Refuerza D-04, que ya estaba tomada.
- **C-11** (lectura del teclado) gana relevancia: `InputHandler` traduce teclas a acciones del dominio y sobrevive al cambio de motor. Sube de Bloque C a **frontera C/B** — se reevalúa en la Semana 7 (*Refactoring C4 Model Dynamic View*), no antes.

---

### Event Card E-03

**Title:** Revisión de originalidad del contenido

**Description:**
El proyecto se inspira en combates de anime ninja pero no puede reutilizar personajes, nombres, aldeas, símbolos, música, escenarios ni habilidades protegidas por derechos de autor.

Todo asset o nombre de origen dudoso impacta la viabilidad de la entrega con **(- -)**.

**Consecuencia sobre la priorización:**

Ninguna reordenación de concerns arquitectónicos, pero se agrega una restricción transversal: **todo asset entra al repositorio con su origen documentado**. Nombres de personajes (Kaien, Raiko, Sora, Kuro, Nami), técnicas y arenas son originales del proyecto.

Refuerza la decisión D-01: con los datos de cada personaje encapsulados en su propia subclase, reemplazar un personaje entero —si hiciera falta— no toca el resto del sistema.

---

## Estado de los atributos al cerrar la Semana 1

| Atributo | Prioridad inicial | Prioridad tras eventos | Movida por |
|---|---|---|---|
| Modificabilidad | 1 | 1 | — |
| Jugabilidad | 1 | 1 | — |
| Comprensibilidad | 1 | 1 | — |
| Simplicidad / Tiempo | 1 | 1 (vinculante) | E-01 |
| Rendimiento | 2 | 2 | — |
| Fiabilidad | 2 | 2 | — |
| Trazabilidad | 2 | 2 | — |
| Portabilidad | 3 | **2** | E-02 |
| Testeabilidad | 3 | 3 | — |

Ningún atributo queda en QA-Priority 0. La priorización de la Semana 1 está cerrada.
