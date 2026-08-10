# Stakeholder Cards

> Formato tomado de las *Stakeholder Cards* de DecidArch (Project / Stakeholder / Goal / Quality Attributes con QA-Priority).

## Cómo se lee la QA-Priority

En el card set original todos los atributos empiezan en **QA-Priority: 0** y las Event Cards los mueven a 1, 2 o 3 (la carta *"New project manager"* baja Security a 1 y Availability a 3, es decir: **número más bajo = más prioritario**). Se conserva esa convención:

| Valor | Significado |
|---|---|
| **1** | Crítico — si se sacrifica, el stakeholder considera el sistema fallido |
| **2** | Alto — se protege salvo que choque con un atributo de prioridad 1 |
| **3** | Medio — deseable, es el primero que se cede en un trade-off |
| **0** | Sin priorizar (estado inicial, no debería quedar ninguno así al cerrar la Semana 1) |

---

## Stakeholder Card 1

**Project:** Shinobi Arena
**Stakeholder:** **Jugador**

**Goal:**
El Jugador quiere sentarse frente al teclado y tener un combate que se sienta justo y responsivo: que el personaje haga lo que él ordenó, en el momento en que lo ordenó, y que entienda por qué perdió cuando pierde.

**Quality Attributes:**

- **Jugabilidad / Usabilidad** — Los controles deben ser aprendibles en menos de un minuto y el personaje debe responder al input sin retardo perceptible. El estado del combate (vida, chakra) debe ser legible de un vistazo. *(QA-Priority: 1)*
- **Rendimiento** — El combate debe correr fluido y sin tirones durante el intercambio de golpes, incluso con proyectiles en pantalla. *(QA-Priority: 2)*
- **Fiabilidad** — El juego no debe caerse ni quedarse trabado en un estado sin salida (por ejemplo, un personaje congelado en medio de un ataque). *(QA-Priority: 2)*

---

## Stakeholder Card 2

**Project:** Shinobi Arena
**Stakeholder:** **Docente / Evaluador**

**Goal:**
El Docente necesita abrir el proyecto y verificar, leyendo el código y los diagramas, que se aplicaron los contenidos del ramo. Le importa menos que el juego sea divertido y más que la arquitectura sea correcta, explicable y trazable hasta los diagramas entregados.

**Quality Attributes:**

- **Modificabilidad** — El proyecto debe permitir agregar un personaje o un ataque nuevo sin tocar clases existentes ni duplicar código. Es la evidencia directa de herencia y polimorfismo. *(QA-Priority: 1)*
- **Comprensibilidad / Analizabilidad** — Cada clase debe tener una responsabilidad que se pueda enunciar en una frase. No debe existir una clase que concentre la lógica del juego. *(QA-Priority: 1)*
- **Trazabilidad** — Los nombres de clases, atributos y métodos del código deben coincidir con los del diagrama de clases y el C4 Model. *(QA-Priority: 2)*
- **Fiabilidad** — La demostración en vivo del entregable *Play Game* no puede fallar. *(QA-Priority: 2)*

---

## Stakeholder Card 3

**Project:** Shinobi Arena
**Stakeholder:** **Desarrollador / Mantenedor**

**Goal:**
El Desarrollador es una sola persona con tres días para el prototipo, un semestre por delante con entregas semanales, y la obligación de rehacer el juego en Unity en la Unidad 3. Necesita llegar a un juego terminado sin quedar atrapado en su propia arquitectura.

**Quality Attributes:**

- **Simplicidad / Tiempo de construcción** — Cada decisión debe poder implementarse y depurarse dentro del plazo. Una solución que no alcanza a terminarse vale cero. *(QA-Priority: 1)*
- **Modificabilidad** — Las entregas semanales agregan funcionalidad sobre lo ya entregado; el código debe soportar ese crecimiento incremental. *(QA-Priority: 1)*
- **Testeabilidad** — Debe poder probarse una regla de combate (por ejemplo, "el bloqueo reduce el daño a la mitad") sin tener que jugar una partida completa. *(QA-Priority: 3)*
- **Portabilidad** — Las reglas del combate deberían sobrevivir al cambio de Greenfoot a Unity. *(QA-Priority: 3 → ver Event Card E-02)*

---

## Atributos de calidad consolidados

Cuando dos stakeholders priorizan distinto el mismo atributo, gana la prioridad más alta (número más bajo). Este es el vector contra el que se puntúa el impacto de cada concern:

| Atributo | Abrev. | Prioridad final | Peso | Quién lo exige |
|---|---|---|---|---|
| Modificabilidad | **MOD** | 1 | 3 | Docente, Desarrollador |
| Jugabilidad / Usabilidad | **JUG** | 1 | 3 | Jugador |
| Comprensibilidad | **COM** | 1 | 3 | Docente |
| Simplicidad / Tiempo | **SIM** | 1 | 3 | Desarrollador |
| Rendimiento | **REN** | 2 | 2 | Jugador |
| Fiabilidad | **FIA** | 2 | 2 | Jugador, Docente |
| Trazabilidad | **TRA** | 2 | 2 | Docente |
| Testeabilidad | **TES** | 3 | 1 | Desarrollador |
| Portabilidad | **POR** | 3 | 1 | Desarrollador |

### La tensión central del proyecto

Cuatro atributos empatados en prioridad 1 no es un error de análisis: es el conflicto real del proyecto. **Modificabilidad y Comprensibilidad empujan hacia más clases y más abstracción; Simplicidad y Tiempo empujan hacia menos.**

Regla de desempate adoptada, y que se aplicará en todas las decisiones de este PR:

> Se acepta abstracción **solo donde el proyecto ya tiene variación conocida** (varios personajes, varios estados, varios enemigos, varias arenas). Donde hay un solo caso y no se prevé un segundo, se implementa directo. Un patrón de diseño sin variación que lo justifique es complejidad que no se puede defender ante el profesor.
