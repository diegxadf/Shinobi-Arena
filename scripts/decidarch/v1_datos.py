# -*- coding: utf-8 -*-
"""
Shinobi Arena — mazo DecidArch v1.

Formato tomado de los PDF oficiales del repositorio DecidArch (2017-2018):
CardSet, GameRules, ScoreSheet y Templates.

Estructura del mazo oficial replicada:
  1 Project Card · 2-3 Stakeholder Cards · 10 Concern Cards · 6 Event Cards

Notacion de impactos: (+) (++) (-) (--). La lista de cada opción termina en "..."
porque en DecidArch es abierta: los jugadores pueden agregar impactos durante la
partida y anotarlos en la columna Rationale.
"""

# ---------------------------------------------------------------- atributos
# Sub-atributos observables, no conceptos amplios.
# El profesor: "usability no es observable, es un concepto muy amplio;
# tienen que particularizar el atributo de calidad que pueda ser observable".
QUALITY_ATTRIBUTES = [
    ("Learnability",
     "Cuánto tarda un jugador nuevo en entender los controles y las mecánicas basicas."),
    ("Satisfaction",
     "Fluidez y respuesta del combate: que el personaje haga lo ordenado, cuando se ordena."),
    ("Accessibility",
     "Cuánto recuerda el jugador de las mecánicas al volver despues de no jugar."),
    ("Performance",
     "Coste de cálculo por frame y estabilidad de la velocidad en pantalla."),
    ("Reliability",
     "Ausencia de estados rotos, personajes trabados y comportamiento impredecible."),
    ("Modifiability",
     "Esfuerzo para agregar un personaje, un ataque o una arena sin tocar lo existente."),
    ("Analysability",
     "Facilidad para leer el código y localizar la responsabilidad de cada clase."),
    ("Testability",
     "Poder comprobar una regla de combate sin tener que jugar una partida completa."),
    ("Portability",
     "Esfuerzo para llevar el juego de Greenfoot a Unity y a otros sistemas operativos."),
]
QA = [q[0] for q in QUALITY_ATTRIBUTES]

# ---------------------------------------------------------------- project
PROJECT = {
    "project": "Shinobi Arena",
    "purpose": "Shinobi Arena es un videojuego de peleas 2D de uno contra uno, con vista "
               "lateral y control por teclado, que se instala y se ejecuta localmente. "
               "El jugador compite en el Torneo de los Cinco Reinos enfrentando rivales "
               "sucesivos, cada uno con un estilo de combate distinto, hasta el oponente "
               "final. Se construye en Greenfoot con Java y debe portarse a Unity más adelante.",
}

# ---------------------------------------------------------------- stakeholders
# Todas las QA-Priority parten en 0, como en el CardSet oficial de DecidArch.
# Son las Event Cards las que las suben durante la partida.
# Regla del profesor: todo atributo usado en un concern debe pertenecer al menos
# a un stakeholder. "Si no hay interesado en lo que están haciendo, están
# haciendo algo que no deben hacer."
STAKEHOLDERS = [
    {
        "nombre": "Jugador",
        "goal": "El Jugador quiere sentarse frente al teclado y tener un combate que se "
                "sienta justo: que el personaje responda a lo que ordeno, entender por qué "
                "perdio cuando pierde, y poder retomar el juego semanas despues sin "
                "reaprender los controles.",
        "qa": {
            "Satisfaction": 0,
            "Reliability": 0,
            "Learnability": 0,
            "Accessibility": 0,
            "Performance": 0,
        },
    },
    {
        "nombre": "Equipo de desarrollo",
        "goal": "El Equipo construye el prototipo, lo mantiene durante el semestre y debe "
                "portarlo a Unity más adelante. Necesita poder depurar rápido y agregar "
                "contenido sin reescribir lo que ya funciona.",
        "qa": {
            "Portability": 0,
            "Modifiability": 0,
            "Testability": 0,
            "Analysability": 0,
            "Reliability": 0,
        },
    },
    {
        "nombre": "Revisor técnico",
        "goal": "El Revisor abre el proyecto sin conocimiento previo y debe poder explicar "
                "qué hace cada clase, verificar que el comportamiento comun no este "
                "duplicado y comprobar las reglas del combate de forma aislada.",
        "qa": {
            "Analysability": 0,
            "Modifiability": 0,
            "Testability": 0,
            "Reliability": 0,
        },
    },
]

# ---------------------------------------------------------------- concerns
# Los 10 mejor puntuados de los 12 identificados en la priorización.
# "ref" y "puntaje" remiten al documento 04-priorización.md.
CONCERNS = [
    {
        "id": 1, "ref": "C-02", "puntaje": "5,00",
        "concern": "El jugador y el enemigo comparten vida, chakra, gravedad y daño, y solo "
                   "se diferencian en quien decide sus acciones. Cómo debe repartirse ese "
                   "comportamiento entre clases?",
        "options": [
            ("Dos clases independientes: Player y Enemy heredan de Actor por separado, cada "
             "una con su propia copia de la lógica de vida, chakra y física.",
             {"Performance": "+", "Modifiability": "--", "Analysability": "-", "Testability": "-"}),
            ("Clase abstracta Fighter: concentra vida, chakra, física y daño; Player y Enemy "
             "la extienden y solo redefinen como se decide la acción.",
             {"Modifiability": "++", "Analysability": "++", "Reliability": "+", "Testability": "-"}),
            ("Composición por componentes: Fighter contiene objetos Movimiento, Combate y "
             "Salud intercambiables entre si.",
             {"Modifiability": "++", "Testability": "++", "Portability": "+", "Analysability": "--", "Performance": "-"}),
        ],
    },
    {
        "id": 2, "ref": "C-01", "puntaje": "4,80",
        "concern": "Un luchador puede estar quieto, caminando, saltando, atacando, "
                   "bloqueando, golpeado o derrotado, y hay combinaciones prohibidas: quien "
                   "esta siendo golpeado no puede atacar. Cómo se representa su estado?",
        "options": [
            ("Banderas booleanas dentro de Fighter: atacando, saltando y bloqueando "
             "consultadas con if anidados.",
             {"Performance": "++", "Reliability": "--", "Modifiability": "--", "Analysability": "-", "Satisfaction": "-"}),
            ("Un enum FighterState con un switch en act() que decide que acciones se "
             "permiten en cada estado.",
             {"Reliability": "+", "Satisfaction": "+", "Analysability": "+", "Performance": "+", "Modifiability": "-"}),
            ("Patron State: una clase por estado (IdleState, AttackingState, HurtState...), "
             "cada una decide sus propias transiciones.",
             {"Reliability": "++", "Modifiability": "++", "Analysability": "++", "Satisfaction": "+", "Testability": "+", "Performance": "-"}),
        ],
    },
    {
        "id": 3, "ref": "C-04", "puntaje": "4,30",
        "concern": "Un golpe conecta durante pocos cuadros y solo en una zona por delante "
                   "del personaje; un proyectil impacta en otro momento y con otra forma. "
                   "Cómo se detecta que un ataque impacto?",
        "options": [
            ("Intersección de los sprites completos con getIntersectingObjects mientras "
             "dura el ataque.",
             {"Performance": "++", "Reliability": "+", "Satisfaction": "--", "Modifiability": "-"}),
            ("Un actor Hitbox temporal que el ataque crea durante sus cuadros activos y "
             "destruye al terminar; Projectile reutiliza el mismo mecanismo.",
             {"Satisfaction": "++", "Modifiability": "++", "Learnability": "+", "Analysability": "+", "Performance": "-"}),
            ("Cálculo geométrico de rectangulos dentro del árbitro del combate, sin crear "
             "actores adicionales.",
             {"Performance": "++", "Testability": "++", "Portability": "+", "Satisfaction": "+", "Analysability": "--"}),
        ],
    },
    {
        "id": 4, "ref": "C-05", "puntaje": "4,20",
        "concern": "Alguien debe aplicar el daño, restar chakra, decidir si el bloqueo lo "
                   "reduce, detectar que la vida llego a cero y declarar el resultado. Que "
                   "componente arbitra las reglas del combate?",
        "options": [
            ("FightWorld hace todo: crea los actores, aplica el daño y decide el final.",
             {"Performance": "+", "Analysability": "--", "Modifiability": "--", "Testability": "--", "Portability": "-"}),
            ("Un CombatManager colaborador: FightWorld le delega las reglas; el manager no "
             "sabe dibujar ni leer teclado, y no depende de la API de Greenfoot.",
             {"Analysability": "++", "Modifiability": "++", "Testability": "++", "Portability": "++", "Reliability": "+", "Performance": "-"}),
            ("Un CombatManager Singleton accesible desde cualquier clase.",
             {"Performance": "+", "Testability": "--", "Reliability": "--", "Modifiability": "-", "Portability": "-"}),
        ],
    },
    {
        "id": 5, "ref": "C-09", "puntaje": "3,70",
        "concern": "El juego tiene pantalla de inicio, combate, victoria, derrota y "
                   "reinicio. Cómo se organiza el paso entre esas pantallas?",
        "options": [
            ("Un solo World que cambia su fondo y dibuja el menu o el combate segun una "
             "variable de estado interna.",
             {"Performance": "+", "Analysability": "--", "Modifiability": "--", "Reliability": "-", "Learnability": "-"}),
            ("Tres World separados (MenuWorld, FightWorld, EndWorld) enlazados con "
             "Greenfoot.setWorld().",
             {"Analysability": "++", "Modifiability": "++", "Reliability": "++", "Learnability": "++", "Portability": "-"}),
            ("Un World con un objeto GameState que delega el dibujado y el input al estado "
             "activo.",
             {"Portability": "++", "Modifiability": "+", "Testability": "+", "Reliability": "+", "Analysability": "-", "Learnability": "-"}),
        ],
    },
    {
        "id": 6, "ref": "C-08", "puntaje": "3,60",
        "concern": "Kaien usa técnicas de fuego, Raiko es eléctrico y veloz, Sora ataca a "
                   "distancia con viento. Cómo se representa la diferencia de estilo y "
                   "habilidades entre personajes?",
        "options": [
            ("Un if por personaje dentro de Fighter.usarEspecial(), consultando el nombre "
             "del personaje.",
             {"Performance": "+", "Modifiability": "--", "Analysability": "--", "Accessibility": "-"}),
            ("Una subclase por personaje que redefine usarEspecial() y sus estadísticas base.",
             {"Modifiability": "++", "Analysability": "++", "Accessibility": "+", "Reliability": "+", "Testability": "-"}),
            ("Un objeto Tecnica intercambiable que el luchador contiene por composición y "
             "puede cambiarse en caliente.",
             {"Modifiability": "++", "Testability": "++", "Accessibility": "++", "Analysability": "-", "Performance": "-"}),
        ],
    },
    {
        "id": 7, "ref": "C-03", "puntaje": "3,60",
        "concern": "El enemigo debe acercarse, retroceder, atacar a distancia adecuada, "
                   "bloquear de manera ocasional y usar su especial, sin caer en una "
                   "secuencia fija. Dónde vive esa lógica de decisión?",
        "options": [
            ("Una cadena de if sobre la distancia al jugador, escrita dentro de Enemy.act().",
             {"Performance": "+", "Modifiability": "--", "Testability": "--", "Satisfaction": "-", "Accessibility": "-"}),
            ("Una clase EnemyAI separada a la que Enemy delega: la IA devuelve una acción y "
             "el enemigo la ejecuta.",
             {"Modifiability": "++", "Testability": "++", "Analysability": "+", "Portability": "+", "Performance": "-"}),
            ("Un autómata de estados de IA (Perseguir, Atacar, Retroceder, Esperar) con "
             "cooldowns y transiciones probabilísticas.",
             {"Satisfaction": "++", "Accessibility": "++", "Modifiability": "+", "Reliability": "+", "Performance": "-", "Analysability": "-"}),
        ],
    },
    {
        "id": 8, "ref": "C-12", "puntaje": "2,90",
        "concern": "El prototipo necesita dos arenas que se diferencian en fondo, altura "
                   "del suelo, límites laterales y posiciones iniciales. Cómo se configura "
                   "un escenario de combate?",
        "options": [
            ("Una subclase de World por arena: BosqueWorld y TemploWorld.",
             {"Reliability": "+", "Performance": "+", "Modifiability": "-", "Analysability": "-"}),
            ("FightWorld parametrizado con un objeto Arena que aporta fondo, suelo, límites "
             "y puntos de aparición.",
             {"Modifiability": "+", "Analysability": "+", "Testability": "+", "Portability": "+", "Reliability": "-"}),
            ("Arenas definidas en un archivo de datos que se lee al iniciar el combate.",
             {"Modifiability": "++", "Portability": "+", "Testability": "+", "Reliability": "--", "Analysability": "-"}),
        ],
    },
    {
        "id": 9, "ref": "C-07", "puntaje": "2,80",
        "concern": "El prototipo necesita un jugador y dos enemigos distintos, y más "
                   "adelante posiblemente más personajes. Cómo se crean los luchadores y "
                   "sus variantes?",
        "options": [
            ("Con new directo en FightWorld, escribiendo ahi los parámetros de cada "
             "personaje.",
             {"Performance": "+", "Modifiability": "--", "Analysability": "-", "Testability": "-"}),
            ("Una FighterFactory con un método que recibe el tipo de personaje y devuelve "
             "el Fighter ya configurado.",
             {"Modifiability": "++", "Analysability": "++", "Testability": "+", "Performance": "-"}),
            ("Estadísticas en un archivo de configuración externo que la fabrica lee al "
             "crear cada luchador.",
             {"Modifiability": "++", "Testability": "++", "Portability": "+", "Reliability": "-", "Analysability": "-"}),
        ],
    },
    {
        "id": 10, "ref": "C-06", "puntaje": "2,60",
        "concern": "La barra de vida y la de chakra deben reflejar el estado del luchador "
                   "en todo momento. Cómo se mantienen sincronizadas con el?",
        "options": [
            ("Polling: FightWorld pregunta getVida() a cada luchador en cada act() y "
             "redibuja las barras.",
             {"Analysability": "+", "Modifiability": "-", "Performance": "-", "Satisfaction": "-"}),
            ("Observer: el Fighter notifica a sus observadores cuando su vida o chakra "
             "cambia, y las barras se actualizan solas.",
             {"Modifiability": "++", "Performance": "+", "Satisfaction": "+", "Learnability": "+", "Analysability": "-"}),
            ("Referencia directa: cada Fighter guarda un puntero a su HealthBar y la "
             "actualiza al recibir daño.",
             {"Performance": "++", "Satisfaction": "+", "Modifiability": "--", "Analysability": "-"}),
        ],
    },
]

# ---------------------------------------------------------------- eventos
# Formato oficial: solo Title y Description. Todo el efecto va en la descripción.
# El profesor: "los eventos pueden afectar positivamente... y pueden cambiar las
# prioridades de algun stakeholder".
EVENTS = [
    {
        "title": "Playtest: los golpes no se sienten",
        "cambios": [("Jugador", "Satisfaction", 3), ("Jugador", "Reliability", 2)],
        "description": "Quienes prueban el prototipo reportan que reciben daño sin ver el "
                       "golpe conectar, y que a veces el personaje queda trabado a mitad "
                       "de un ataque.\n\n"
                       "La Satisfaction del Jugador sube a QA-Priority 3 si no lo estaba. "
                       "Reconsideren los concerns 2 y 3.",
    },
    {
        "title": "El porteo a Unity se adelanta",
        "cambios": [("Equipo de desarrollo", "Portability", 3)],
        "description": "La siguiente unidad del proyecto exige rehacer el juego en Unity. "
                       "Todo lo que dependa de la API de Greenfoot habra que reescribirlo "
                       "desde cero.\n\n"
                       "La Portability del Equipo de desarrollo sube a QA-Priority 3. "
                       "Reconsideren los concerns 4 y 5.",
    },
    {
        "title": "Se incorpora un desarrollador nuevo",
        "cambios": [("Equipo de desarrollo", "Analysability", 2), ("Revisor técnico", "Analysability", 3)],
        "description": "Una persona sin contexto se suma al equipo y debe poder trabajar "
                       "sobre el código existente sin que se lo expliquen entero.\n\n"
                       "La Analysability del Equipo de desarrollo sube a QA-Priority 3. "
                       "El Revisor técnico mantiene la suya. Reconsideren el concern 1.",
    },
    {
        "title": "Torneo de exhibición en la universidad",
        "cambios": [("Jugador", "Learnability", 3), ("Jugador", "Accessibility", 1)],
        "description": "El juego se mostrara en una feria abierta donde la gente juega una "
                       "sola partida, de pie y sin explicacion previa.\n\n"
                       "La Learnability del Jugador sube a QA-Priority 3 y la Accessibility "
                       "baja a 1: importa que lo entiendan ahora, no que lo recuerden en un "
                       "mes. Reconsideren los concerns 5 y 10.",
    },
    {
        "title": "Se agregan dos personajes jugables",
        "cambios": [("Revisor técnico", "Modifiability", 3), ("Equipo de desarrollo", "Modifiability", 2)],
        "description": "El alcance del proyecto crece: hay que sumar dos luchadores más con "
                       "técnicas propias, reutilizando los sistemas existentes.\n\n"
                       "Si en el concern 6 eligieron la opción 1, la deuda se paga ahora: "
                       "cuenten Modifiability (- -) una segunda vez. Si eligieron 2 o 3, "
                       "sumen Modifiability (+). Reconsideren los concerns 6 y 9.",
    },
    {
        "title": "Auditoría de originalidad del contenido",
        "cambios": [("Equipo de desarrollo", "Testability", 2)],
        "description": "Se revisa que ningun nombre, técnica ni recurso grafico provenga de "
                       "una obra con derechos de autor. Todo lo que no tenga origen "
                       "documentado debe reemplazarse.\n\n"
                       "Los datos de cada personaje deben poder sustituirse sin tocar el "
                       "resto del sistema. Reconsideren el concern 9 y registren en la "
                       "columna Rationale que atributo los protegio.",
    },
]
