# Stakeholder Cards y atributos de calidad

> Formato de las *Stakeholder Cards* de DecidArch: Project · Stakeholder · Goal · Quality
> Attributes con su QA-Priority.
>
> **Versión corregida.** La anterior usaba atributos amplios y no observables. Ver
> [`06-correcciones.md`](06-correcciones.md) para el detalle de qué cambió y por qué.

---

## Cómo se leen las QA-Priority

En el CardSet oficial de DecidArch **todos los atributos se imprimen con `QA-Priority: 0`**. Son
las Event Cards las que las modifican durante la partida, con instrucciones del tipo *"Change the
Owner's QA-Priority of Security to 2"*.

| Valor | Significado |
|---|---|
| **3** | Crítico — si no se alcanza, el stakeholder considera el sistema fallido |
| **2** | Alto |
| **1** | Medio |
| **0** | Sin priorizar — el valor con el que arranca toda la partida |

En el Scoring Sheet, la prioridad es un **umbral**: para cada atributo se calcula
`C = QA-Score − QA-Priority`, y **si algún C queda negativo, el equipo pierde**. Una prioridad 3
significa literalmente "este atributo debe terminar con al menos tres impactos positivos netos".

---

## Los 9 atributos de calidad

Cada uno es un sub-atributo observable, no un concepto amplio. Se puede comprobar si se cumple
o no; "usabilidad" no.

| Atributo | Qué se observa en Shinobi Arena |
|---|---|
| **Learnability** | Cuánto tarda un jugador nuevo en entender los controles y las mecánicas básicas |
| **Satisfaction** | Fluidez y respuesta del combate: que el personaje haga lo ordenado, cuando se ordena |
| **Accessibility** | Cuánto recuerda el jugador de las mecánicas al volver después de no jugar |
| **Performance** | Coste de cálculo por frame y estabilidad de la velocidad en pantalla |
| **Reliability** | Ausencia de estados rotos, personajes trabados y comportamiento impredecible |
| **Modifiability** | Esfuerzo para agregar un personaje, un ataque o una arena sin tocar lo existente |
| **Analysability** | Facilidad para leer el código y localizar la responsabilidad de cada clase |
| **Testability** | Poder comprobar una regla de combate sin jugar una partida completa |
| **Portability** | Esfuerzo para llevar el juego de Greenfoot a Unity y a otros sistemas operativos |

**Lo que no está aquí y antes sí:** el tiempo de construcción y la simplicidad. No son atributos
de calidad del software sino restricciones del proyecto, y viven en la Project Card. La
trazabilidad tampoco aparece: se absorbió en Analysability.

---

## Stakeholder Card 1

**Project:** Shinobi Arena
**Stakeholder:** **Jugador**

**Goal:**
El Jugador quiere sentarse frente al teclado y tener un combate que se sienta justo: que el
personaje responda a lo que ordenó, entender por qué perdió cuando pierde, y poder retomar el
juego semanas después sin reaprender los controles.

**Quality Attributes:**

- **Satisfaction** — Fluidez y respuesta del combate. *(QA-Priority: 0)*
- **Reliability** — Ausencia de estados rotos y comportamiento impredecible. *(QA-Priority: 0)*
- **Learnability** — Cuánto tarda en entender los controles y las mecánicas. *(QA-Priority: 0)*
- **Accessibility** — Cuánto recuerda al volver después de no jugar. *(QA-Priority: 0)*
- **Performance** — Coste de cálculo por frame y estabilidad de la velocidad. *(QA-Priority: 0)*

> El Jugador percibe la fluidez como **Satisfaction**, no como Performance. El rendimiento es un
> medio para conseguirla, no un fin en sí mismo.

---

## Stakeholder Card 2

**Project:** Shinobi Arena
**Stakeholder:** **Equipo de desarrollo**

**Goal:**
El Equipo construye el prototipo, lo mantiene durante el semestre y debe portarlo a Unity más
adelante. Necesita poder depurar rápido y agregar contenido sin reescribir lo que ya funciona.

**Quality Attributes:**

- **Portability** — Esfuerzo para llevar el juego a Unity y a otros sistemas operativos. *(QA-Priority: 0)*
- **Modifiability** — Esfuerzo para agregar un personaje, un ataque o una arena. *(QA-Priority: 0)*
- **Testability** — Poder comprobar una regla sin jugar una partida completa. *(QA-Priority: 0)*
- **Analysability** — Facilidad para leer el código y ubicar responsabilidades. *(QA-Priority: 0)*
- **Reliability** — Ausencia de estados rotos y comportamiento impredecible. *(QA-Priority: 0)*

---

## Stakeholder Card 3

**Project:** Shinobi Arena
**Stakeholder:** **Revisor técnico**

**Goal:**
El Revisor abre el proyecto sin conocimiento previo y debe poder explicar qué hace cada clase,
verificar que el comportamiento común no esté duplicado y comprobar las reglas del combate de
forma aislada.

**Quality Attributes:**

- **Analysability** — Facilidad para leer el código y ubicar responsabilidades. *(QA-Priority: 0)*
- **Modifiability** — Esfuerzo para agregar contenido sin tocar lo existente. *(QA-Priority: 0)*
- **Testability** — Poder comprobar una regla sin jugar una partida completa. *(QA-Priority: 0)*
- **Reliability** — Ausencia de estados rotos y comportamiento impredecible. *(QA-Priority: 0)*

> Antes este rol era "Docente / Evaluador". Se cambió porque el docente es interesado de la
> **entrega**, no del **sistema**; en DecidArch los stakeholders son del producto de software.
> El revisor técnico conserva las mismas preocupaciones y sí es un rol del producto.

---

## Trazabilidad: ningún atributo huérfano

Regla dada en clase: *"no pueden haber atributos de calidad puestos acá que no tengan
correspondencia con un stakeholder"*.

| Atributo | Le interesa a |
|---|---|
| Learnability | Jugador |
| Satisfaction | Jugador |
| Accessibility | Jugador |
| Performance | Jugador |
| Reliability | Jugador · Equipo de desarrollo · Revisor técnico |
| Modifiability | Equipo de desarrollo · Revisor técnico |
| Analysability | Equipo de desarrollo · Revisor técnico |
| Testability | Equipo de desarrollo · Revisor técnico |
| Portability | Equipo de desarrollo |

Los nueve están reclamados. Se revisó carta por carta: ninguna Concern Card usa un atributo que
no aparezca en alguna Stakeholder Card.

---

## La tensión del proyecto

Los tres stakeholders no quieren lo mismo, y ahí está el juego:

- El **Jugador** solo percibe Satisfaction, Learnability, Accessibility y Performance. No le
  importa cómo esté escrito el código.
- El **Revisor técnico** solo percibe Analysability, Modifiability y Testability. No juega.
- El **Equipo** está en medio: paga el costo de ambos lados y además carga con Portability.

Casi toda opción que sube Modifiability o Testability baja Analysability o Performance, y
viceversa. Ninguna decisión los deja a los tres contentos: eso es lo que la partida obliga a
negociar.
