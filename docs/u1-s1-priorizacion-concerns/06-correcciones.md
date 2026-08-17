# Correcciones a la entrega de la Semana 1

Este documento registra qué se corrigió respecto del Pull Request #1 y por qué. Recoge dos
fuentes: la retroalimentación en clase del 13 de agosto y los PDF oficiales del repositorio
DecidArch (CardSet, GameRules, ScoreSheet y Templates).

---

## 1. Corrección de formato

La primera versión se construyó sobre un kit de otro equipo, no sobre DecidArch v1. Eso
introdujo mecánicas que **no existen en el juego oficial**.

| Primera versión | DecidArch v1 |
|---|---|
| Opciones A / B / C | Opciones **1 / 2 / 3** |
| Impactos numéricos `JUG +2, FIA −1` | Símbolos `Modifiability (+ +), Reliability (-)` |
| Costo de Tiempo 1-4 por opción | No existe |
| Tablero con pistas de −5 a 15 y contador de Tiempo | No existe |
| Victoria por umbrales inventados | Fórmula del Scoring Sheet oficial |
| Event Card con tres campos | Solo `Title` y `Description` |
| Evento cada 2 concerns | Al final de cada ronda |
| Project Card con premisa, core loop y restricciones | Solo `Project` y `Purpose` |
| 5 atributos de calidad condensados | 9 atributos, sin condensar |

### El scoring correcto

1. **QA-Score** por atributo: `A` = cantidad de `+` (un `+ +` cuenta dos veces),
   `B` = cantidad de `-` (un `- -` cuenta dos veces). `QA-Score = A − B`
2. **Stakeholders-Score**: para cada atributo de cada stakeholder, `C = QA-Score − QA-Priority`.
   **Si algún C queda bajo cero, el equipo pierde**, sin importar el puntaje acumulado.
   El score es la suma de los C.
3. **Final Score = Stakeholders-Score − D**, donde D son los concerns sin resolver.

Escala: menos de 0 perdieron · 0-9 suficiente · 10-19 bueno · 20-29 muy bueno · 30 o más excelente.

### Las QA-Priority parten en 0

En el CardSet oficial **todos los atributos se imprimen con `QA-Priority: 0`**. Son las Event
Cards las que las suben durante la partida ("Change the Owner's QA-Priority of Security to 2").
La primera versión las fijaba altas desde el inicio, lo que además volvía el mazo imposible de
ganar.

---

## 2. Corrección de los atributos de calidad

En clase se señaló que los atributos amplios no sirven:

> "Usability sigue siendo un atributo muy vago, tienen que usar algo más preciso."
> "Usability no es observable, es un concepto muy amplio."
> "Cada vez que encuentren un elemento tienen que particularizar el atributo de calidad
> que pueda ser observable."

### Qué se eliminó y por qué

| Atributo anterior | Problema | Reemplazo |
|---|---|---|
| **Jugabilidad / Usabilidad** | El atributo vago señalado en clase | Se parte en **Learnability**, **Satisfaction** y **Accessibility** |
| **Simplicidad / Tiempo de construcción** | No es un atributo de calidad del software, es una restricción del proyecto | Pasa a la Project Card como restricción |
| **Trazabilidad** | No es un atributo de calidad estándar | Se absorbe en **Analysability** |
| **Comprensibilidad** | Nombre informal | Se renombra **Analysability** |

Se conservan Modificabilidad (**Modifiability**), Rendimiento (**Performance**),
Fiabilidad (**Reliability**), Testeabilidad (**Testability**) y Portabilidad (**Portability**).

### Los 9 atributos vigentes

| Atributo | Qué se observa |
|---|---|
| **Learnability** | Cuánto tarda un jugador nuevo en entender los controles y las mecánicas |
| **Satisfaction** | Fluidez y respuesta del combate |
| **Accessibility** | Cuánto recuerda el jugador al volver tras un tiempo sin jugar |
| **Performance** | Coste de cálculo por frame y estabilidad de la velocidad |
| **Reliability** | Ausencia de estados rotos y comportamiento impredecible |
| **Modifiability** | Esfuerzo para agregar un personaje, ataque o arena |
| **Analysability** | Facilidad para leer el código y ubicar responsabilidades |
| **Testability** | Comprobar una regla sin jugar una partida completa |
| **Portability** | Esfuerzo para llevar el juego a Unity y a otros sistemas operativos |

En clase también se corrigió que **la fluidez percibida es Satisfaction, no Performance**. Por
eso el Jugador prioriza Satisfaction por sobre Performance: el rendimiento es un medio, no un fin.

---

## 3. Trazabilidad entre concerns y stakeholders

Regla dada en clase:

> "No pueden haber atributos de calidad puestos acá que no tengan correspondencia con un
> stakeholder. Tiene que haber al menos uno que esté interesado, porque si no hay interesado
> en lo que están haciendo, están haciendo algo que no deben hacer."

Se comprueba automáticamente en [`scripts/decidarch/v1_validar.py`](../../scripts/decidarch/v1_validar.py):
cada atributo que aparece en una opción debe estar declarado en al menos una Stakeholder Card.

| Atributo | Le interesa a |
|---|---|
| Learnability, Satisfaction, Accessibility, Performance | Jugador |
| Portability | Equipo de desarrollo |
| Reliability | Jugador, Equipo de desarrollo, Revisor técnico |
| Modifiability, Analysability, Testability | Equipo de desarrollo, Revisor técnico |

También se cambió el stakeholder **"Docente / Evaluador"** por **"Revisor técnico"**. El docente
es interesado de la entrega, no del sistema; el revisor técnico sí es un rol del producto, y
mantiene las mismas preocupaciones de mantenibilidad.

---

## 4. Corrección de las Event Cards

En clase se observó que los eventos del equipo revisado solo restaban:

> "Aquí hay algo que no están haciendo en ninguno de esos eventos: los eventos pueden afectar
> positivamente, y pueden cambiar las prioridades de algún stakeholder."

Las 6 Event Cards de este mazo **modifican QA-Priority de stakeholders concretos**, y varias lo
hacen al alza en atributos que las decisiones ya tomadas favorecen:

| Evento | Qué mueve |
|---|---|
| Playtest: los golpes no se sienten | Satisfaction del Jugador a 3, Reliability a 2 |
| El porteo a Unity se adelanta | Portability del Equipo a 3 |
| Se incorpora un desarrollador nuevo | Analysability del Equipo a 2 y del Revisor a 3 |
| Torneo de exhibición en la universidad | Learnability del Jugador a 3, Accessibility baja a 1 |
| Se agregan dos personajes jugables | Modifiability del Revisor a 3 y del Equipo a 2 |
| Auditoría de originalidad del contenido | Testability del Equipo a 2 |

---

## 5. Tamaño del mazo

El set oficial trae **1 Project Card, 2 Stakeholder Cards, 10 Concern Cards y 6 Event Cards**.
Este mazo replica ese tamaño con 3 Stakeholder Cards. Los 10 concerns son los 10 mejor puntuados
de los 12 de [`04-priorizacion.md`](04-priorizacion.md); quedan fuera C-11 (lectura del teclado)
y C-10 (animaciones), los dos últimos del ranking.

---

## 6. Verificación

`v1_validar.py` no deja generar el PDF si algo falla. Comprueba:

1. El mazo tiene el tamaño del set oficial
2. Cada Concern Card tiene 3 opciones con símbolos válidos
3. Ninguna opción carece de trade-offs, y ninguna domina a otra
4. **Ningún atributo queda huérfano** (regla de clase)
5. Todas las QA-Priority se imprimen en 0
6. Cada Event Card solo modifica atributos que el stakeholder declara
7. El mazo es ganable y perdible, con el scoring oficial

Resultado con el mazo actual, simulando las 59.049 combinaciones posibles:

```
ganadoras sin eventos:    5200  ( 8,8 %)
ganadoras con 6 eventos:   130  ( 0,2 %)

todas 1  -> pierde   (sin arquitectura)
todas 2  -> pierde
todas 3  -> pierde   (sin rendimiento ni analizabilidad)
```

---

## Qué documentos quedaron superados

`02-stakeholder-cards.md` se reescribió con los atributos corregidos. `03-concern-cards.md` y
`04-priorizacion.md` conservan el análisis original, que sigue siendo válido como razonamiento:
lo que cambió es el vocabulario de los atributos y el formato de las cartas, no la identificación
ni el orden de los concerns.
