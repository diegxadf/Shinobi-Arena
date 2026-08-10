# Concern Cards — Shinobi Arena

> Formato tomado de las *Concern Cards* de DecidArch: cada carta plantea una pregunta abierta del sistema, lista opciones numeradas y anota el impacto de cada opción sobre los atributos de calidad con `(+)`, `(++)`, `(-)`, `(--)`.

**Abreviaturas de atributos** (ver [`02-stakeholder-cards.md`](02-stakeholder-cards.md)):
MOD modificabilidad · JUG jugabilidad · COM comprensibilidad · SIM simplicidad · REN rendimiento · FIA fiabilidad · TRA trazabilidad · TES testeabilidad · POR portabilidad

Un concern es **arquitectónico** cuando su respuesta condiciona la forma del resto del sistema. Preguntas como "¿cuánto daño hace la patada?" no aparecen aquí: son parámetros de balance, no arquitectura.

---

## Concern Card C-01

**Concern-ID:** 1
**Concern:** Un luchador puede estar quieto, caminando, saltando, atacando, bloqueando, golpeado o derrotado, y durante algunos de esos estados no debe poder hacer otras cosas (quien está siendo golpeado no puede atacar). ¿Cómo se representa el estado de un luchador y sus transiciones?

**Options:**

1. **Banderas booleanas dentro de `Fighter`** (`atacando`, `saltando`, `bloqueando`) consultadas con `if` anidados.
   SIM (++), COM (--), MOD (--), FIA (--)

2. **Un `enum FighterState` con un `switch` en `act()`** que decide qué se puede hacer en cada estado.
   SIM (+), COM (+), MOD (-), FIA (+), TRA (+)

3. **Patrón State: una clase por estado** (`IdleState`, `WalkingState`, `AttackingState`…) que implementan una interfaz común y deciden su propia transición.
   MOD (++), COM (++), TRA (++), POR (+), SIM (--), REN (-)

---

## Concern Card C-02

**Concern-ID:** 2
**Concern:** El jugador y el enemigo comparten casi todo (vida, chakra, posición, gravedad, recibir daño, morir) y se diferencian solo en quién decide sus acciones. ¿Cómo se reparte ese comportamiento entre clases?

**Options:**

1. **Dos clases independientes**, `Player` y `Enemy`, ambas heredando directamente de `Actor`, cada una con su propia copia de la lógica.
   SIM (+), MOD (--), COM (--), TRA (--)

2. **Clase abstracta `Fighter`** que hereda de `Actor` y concentra vida, chakra, física y daño; `Player` y `Enemy` la extienden y solo redefinen cómo se deciden las acciones.
   MOD (++), COM (++), TRA (++), SIM (+)

3. **Composición por componentes**: `Fighter` contiene objetos `Movimiento`, `Combate`, `Salud` intercambiables.
   MOD (++), TES (++), POR (++), SIM (--), COM (-)

---

## Concern Card C-03

**Concern-ID:** 3
**Concern:** El enemigo debe acercarse, retroceder, atacar a distancia adecuada, bloquear ocasionalmente y usar su especial, sin caer en una secuencia fija y sin atacar en todos los frames. ¿Dónde vive esa lógica de decisión y cómo se estructura?

**Options:**

1. **Dentro de `Enemy.act()`**, como una cadena de `if` sobre la distancia al jugador.
   SIM (++), MOD (--), COM (-), TES (--)

2. **Clase `EnemyAI` separada** a la que `Enemy` delega la decisión; devuelve una acción y `Enemy` la ejecuta.
   MOD (++), COM (++), TES (++), TRA (+), SIM (-)

3. **Autómata de estados de IA** (`Perseguir`, `Atacar`, `Retroceder`, `Esperar`) con cooldowns y transiciones probabilísticas.
   MOD (++), JUG (++), COM (+), SIM (--)

---

## Concern Card C-04

**Concern-ID:** 4
**Concern:** Un golpe conecta durante unos pocos frames y solo en una zona por delante del personaje; un proyectil impacta en otro momento y con otra forma. ¿Cómo se detecta que un ataque impactó a un luchador?

**Options:**

1. **`getIntersectingObjects()` de Greenfoot entre los sprites completos** de los dos luchadores mientras dura el ataque.
   SIM (++), JUG (--), REN (+), POR (--)

2. **Un actor `Hitbox` temporal** que el ataque crea durante sus frames activos y que se destruye al terminar; el impacto se detecta contra ese actor.
   JUG (++), MOD (++), TRA (++), COM (+), SIM (-)

3. **Cálculo geométrico de rectángulos** en una clase de combate, sin crear actores.
   REN (++), TES (++), POR (++), SIM (--), COM (-)

---

## Concern Card C-05

**Concern-ID:** 5
**Concern:** Alguien tiene que aplicar el daño, restar chakra, decidir si el bloqueo lo reduce, detectar que la vida llegó a cero y declarar victoria o derrota. ¿Qué componente arbitra las reglas del combate?

**Options:**

1. **`FightWorld` hace todo**: crea los actores, aplica el daño y decide el final.
   SIM (++), COM (--), MOD (--), TES (--)

2. **`CombatManager` como colaborador**: `FightWorld` lo crea y le delega las reglas; el manager no sabe dibujar ni leer teclado.
   COM (++), MOD (++), TES (++), POR (++), SIM (-)

3. **`CombatManager` como Singleton global** accesible desde cualquier clase.
   SIM (+), TES (--), MOD (-), COM (-)

---

## Concern Card C-06

**Concern-ID:** 6
**Concern:** La barra de vida y la de chakra deben reflejar el estado del luchador en todo momento. ¿Cómo se mantienen sincronizadas con el luchador?

**Options:**

1. **Polling**: `FightWorld` pregunta `getVida()` a cada luchador en cada `act()` y redibuja las barras.
   SIM (++), COM (+), REN (-), MOD (-)

2. **Observer**: el `Fighter` notifica a sus observadores cuando su vida o chakra cambia, y las barras se actualizan solas.
   MOD (++), COM (++), TRA (++), REN (+), SIM (--)

3. **Referencia directa**: cada `Fighter` guarda un puntero a su `HealthBar` y la actualiza al recibir daño.
   SIM (+), MOD (--), COM (-)

---

## Concern Card C-07

**Concern-ID:** 7
**Concern:** El prototipo necesita un jugador y dos enemigos distintos, y más adelante posiblemente más personajes. ¿Cómo se crean los luchadores y sus variantes?

**Options:**

1. **`new` directo en `FightWorld`** con los parámetros de cada personaje escritos ahí mismo.
   SIM (++), MOD (--), COM (-)

2. **`FighterFactory`** con un método que recibe el tipo de personaje y devuelve el `Fighter` ya configurado.
   MOD (++), COM (++), TRA (+), SIM (-)

3. **Datos externos + fábrica**: las estadísticas viven en un archivo de configuración que la fábrica lee.
   MOD (++), TES (+), SIM (--), FIA (-)

---

## Concern Card C-08

**Concern-ID:** 8
**Concern:** Kaien usa fuego, Raiko es rápido y eléctrico, Sora ataca a distancia con viento. ¿Cómo se representa la diferencia de estilo y habilidades entre personajes?

**Options:**

1. **Un `if` por personaje dentro de `Fighter.usarEspecial()`** consultando el nombre del personaje.
   SIM (+), MOD (--), COM (--), TRA (--)

2. **Una subclase por personaje** que redefine `usarEspecial()` y sus estadísticas base.
   MOD (++), COM (++), TRA (++), SIM (+)

3. **Objeto `Tecnica` intercambiable** que el luchador contiene por composición y puede cambiarse en caliente.
   MOD (++), TES (++), POR (+), SIM (-), COM (-)

---

## Concern Card C-09

**Concern-ID:** 9
**Concern:** El juego tiene pantalla de inicio, combate, victoria, derrota y reinicio. ¿Cómo se organiza la navegación entre esas pantallas?

**Options:**

1. **Un solo `World`** que cambia su fondo y dibuja el menú o el combate según una variable de estado.
   SIM (+), COM (--), MOD (--), FIA (-)

2. **Tres `World`: `MenuWorld`, `FightWorld`, `EndWorld`**, con `Greenfoot.setWorld()` para transitar entre ellos.
   COM (++), MOD (++), TRA (++), SIM (+), FIA (+)

3. **Un `World` con un `GameState`** que delega el dibujado y el input al estado activo.
   MOD (+), POR (++), SIM (--), COM (-)

---

## Concern Card C-10

**Concern-ID:** 10
**Concern:** Cada estado del luchador necesita su imagen, y los ataques idealmente se animan en varios cuadros. ¿Cómo se gestionan las imágenes y animaciones?

**Options:**

1. **`setImage("archivo.png")` con rutas literales** repartidas por el código donde se necesiten.
   SIM (++), MOD (--), COM (--), FIA (-)

2. **Clase `Animacion`** (lista de `GreenfootImage` + temporizador) que el luchador usa por composición, una por estado.
   MOD (++), COM (++), JUG (+), SIM (-)

3. **Cargador genérico de spritesheets** que recorta los cuadros en tiempo de ejecución.
   MOD (+), REN (-), SIM (--)

---

## Concern Card C-11

**Concern-ID:** 11
**Concern:** El jugador controla su personaje con el teclado, y el enemigo con la misma clase base no tiene teclado. ¿Cómo se lee y se traduce la entrada del usuario?

**Options:**

1. **`Greenfoot.isKeyDown()` directamente en `Player.act()`**.
   SIM (++), POR (--), TES (--), MOD (-)

2. **`InputHandler`** que traduce teclas a acciones del dominio (`MOVER_IZQUIERDA`, `ATACAR`) y se las entrega al `Player`.
   POR (++), TES (++), MOD (+), COM (+), SIM (-)

3. **Mapa de teclas configurable** por el usuario, cargado al iniciar.
   JUG (+), SIM (--), MOD (+)

---

## Concern Card C-12

**Concern-ID:** 12
**Concern:** El prototipo necesita dos arenas (bosque de bambú y templo abandonado) que se diferencian en fondo, altura del suelo, límites laterales y posiciones iniciales. ¿Cómo se configura un escenario de combate?

**Options:**

1. **Una subclase de `FightWorld` por arena** (`BosqueWorld`, `TemploWorld`).
   SIM (+), MOD (-), COM (-), TRA (-)

2. **`FightWorld` parametrizado con un objeto `Arena`** que aporta fondo, suelo, límites y puntos de aparición.
   MOD (++), COM (++), TRA (+), TES (+), SIM (-)

3. **Arenas definidas en un archivo de datos** leído al iniciar el combate.
   MOD (++), SIM (--), FIA (-)

---

## Tabla resumen

| ID | Concern | Decisión que condiciona |
|---|---|---|
| C-01 | Estado del luchador | Toda la lógica de `act()` de ambos luchadores |
| C-02 | Reparto Player / Enemy | La jerarquía de clases completa |
| C-03 | Decisiones del enemigo | La clase `Enemy` y su testeabilidad |
| C-04 | Detección de impactos | Cómo se siente el combate y qué clases existen para golpear |
| C-05 | Árbitro del combate | Dónde viven las reglas y si `FightWorld` se vuelve una clase-Dios |
| C-06 | Actualización del HUD | El acoplamiento entre luchadores e interfaz |
| C-07 | Creación de luchadores | Cuánto cuesta agregar el tercer personaje |
| C-08 | Diferenciación de personajes | La evidencia de polimorfismo del proyecto |
| C-09 | Navegación entre pantallas | La organización inicio → combate → cierre |
| C-10 | Animaciones y sprites | El trabajo repetitivo de la Unidad 2 |
| C-11 | Lectura del teclado | La portabilidad a Unity y la testeabilidad |
| C-12 | Configuración de arenas | Cuánto cuesta la tercera arena |
