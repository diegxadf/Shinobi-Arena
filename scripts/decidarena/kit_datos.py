# -*- coding: utf-8 -*-
"""
DECIDARENA — datos del juego de mesa para Shinobi Arena.
Adaptacion del kit DecidAbyss al proyecto propio.

Este archivo es la fuente unica: de aqui salen el PDF y las validaciones.
"""

TIEMPO_INICIAL = 18

# ---------------------------------------------------------------- pistas
# Los 9 atributos de la documentación se condensan en 5 pistas jugables.
TRACKS = [
    ("JUG", "Jugabilidad",       "Sensación del combate, legibilidad y justicia percibida.",
     "Jugabilidad"),
    ("FIA", "Fiabilidad",        "Ausencia de estados rotos, bugs y comportamiento impredecible.",
     "Fiabilidad + Testeabilidad"),
    ("REN", "Rendimiento",       "Fluidez en pantalla, coste de cálculo por frame.",
     "Rendimiento"),
    ("EXT", "Extensibilidad",    "Facilidad para agregar personajes, ataques y arenas sin romper nada.",
     "Modificabilidad + Comprensibilidad + Trazabilidad + Portabilidad"),
    ("ALC", "Alcance",           "Tiempo del semestre y probabilidad real de terminar el prototipo.",
     "Simplicidad / Tiempo de construcción"),
]
COD = [t[0] for t in TRACKS]

# ---------------------------------------------------------------- stakeholders
STAKEHOLDERS = [
    {
        "sigla": "SJ", "nombre": "JUGADOR",
        "objetivo": "Que el combate se sienta justo y responsivo: que el personaje haga lo que "
                    "ordeno, cuando lo ordeno, y entender por qué perdio cuando pierde.",
        "prioridades": {"JUG": 3, "FIA": 3, "REN": 2, "EXT": 0, "ALC": 0},
        "tension": "Lo que hace que el combate se sienta bien casi siempre cuesta más tiempo de implementación.",
    },
    {
        "sigla": "SD", "nombre": "DOCENTE / EVALUADOR",
        "objetivo": "Abrir el proyecto y verificar, leyendo el código, que se aplicaron herencia, "
                    "polimorfismo y separacion de responsabilidades.",
        "prioridades": {"JUG": 0, "FIA": 2, "REN": 1, "EXT": 3, "ALC": 1},
        "tension": "Exigir más estructura puede impedir que el prototipo llegue a estar jugable.",
    },
    {
        "sigla": "SL", "nombre": "DESARROLLADOR",
        "objetivo": "Una sola persona, tres días para el prototipo y entregas cada semana. "
                    "Llegar a un juego terminado sin quedar atrapado en su propia arquitectura.",
        "prioridades": {"JUG": 1, "FIA": 2, "REN": 1, "EXT": 2, "ALC": 3},
        "tension": "Lo que se construye rápido hoy suele ser lo que hay que reescribir en la semana 9.",
    },
]

# ---------------------------------------------------------------- concerns
# orden = ranking de la priorización (documento 04). Se juegan los 8 primeros.
CONCERNS = [
    {
        "id": "C1", "ref": "C-02", "puntaje": "5,00",
        "titulo": "REPARTO PLAYER / ENEMY",
        "pregunta": "El jugador y el enemigo comparten vida, chakra, gravedad y daño, y solo se "
                    "diferencian en quien decide sus acciones. Cómo se reparte ese comportamiento entre clases?",
        "opciones": [
            ("A", "Dos clases independientes", 1,
             "Player y Enemy heredan de Actor por separado, cada una con su copia de la lógica.",
             {"JUG": 0, "FIA": -1, "REN": 0, "EXT": -2, "ALC": +2}),
            ("B", "Clase abstracta Fighter", 2,
             "Fighter concentra vida, chakra y física; Player y Enemy solo redefinen como se decide la acción.",
             {"JUG": 0, "FIA": +1, "REN": 0, "EXT": +2, "ALC": -1}),
            ("C", "Composición por componentes", 3,
             "Fighter contiene objetos Movimiento, Combate y Salud intercambiables.",
             {"JUG": 0, "FIA": +2, "REN": -1, "EXT": +2, "ALC": -2}),
        ],
    },
    {
        "id": "C2", "ref": "C-01", "puntaje": "4,80",
        "titulo": "ESTADO DEL LUCHADOR",
        "pregunta": "Un luchador puede estar quieto, caminando, saltando, atacando, bloqueando, "
                    "golpeado o derrotado, y hay combinaciones prohibidas. Cómo se representa su estado?",
        "opciones": [
            ("A", "Banderas booleanas", 1,
             "Variables atacando / saltando / bloqueando consultadas con if anidados.",
             {"JUG": -1, "FIA": -2, "REN": +1, "EXT": -2, "ALC": +2}),
            ("B", "enum FighterState + switch", 2,
             "Un enumerado y un switch en act() deciden que se puede hacer en cada estado.",
             {"JUG": +1, "FIA": +1, "REN": +1, "EXT": 0, "ALC": -1}),
            ("C", "Patron State: una clase por estado", 3,
             "IdleState, AttackingState, HurtState... cada una decide sus propias transiciones.",
             {"JUG": +2, "FIA": +2, "REN": -1, "EXT": +2, "ALC": -2}),
        ],
    },
    {
        "id": "C3", "ref": "C-04", "puntaje": "4,30",
        "titulo": "DETECCIÓN DE IMPACTOS",
        "pregunta": "Un golpe conecta durante pocos cuadros y solo en una zona por delante del "
                    "personaje. Cómo se detecta que un ataque impacto?",
        "opciones": [
            ("A", "Intersección de sprites completos", 1,
             "getIntersectingObjects entre los dos personajes mientras dura el ataque.",
             {"JUG": -2, "FIA": 0, "REN": +1, "EXT": 0, "ALC": +2}),
            ("B", "Actor Hitbox temporal", 2,
             "El ataque crea una zona activa frente al personaje y la destruye al terminar.",
             {"JUG": +2, "FIA": +1, "REN": 0, "EXT": +2, "ALC": -1}),
            ("C", "Cálculo geométrico en el manager", 3,
             "Rectangulos calculados sin crear actores; más barato y testeable, más código propio.",
             {"JUG": +1, "FIA": +1, "REN": +2, "EXT": +1, "ALC": -2}),
        ],
    },
    {
        "id": "C4", "ref": "C-05", "puntaje": "4,20",
        "titulo": "ÁRBITRO DEL COMBATE",
        "pregunta": "Alguien debe aplicar daño, restar chakra, considerar el bloqueo y declarar "
                    "la victoria. Qué componente arbitra las reglas?",
        "opciones": [
            ("A", "Todo dentro de FightWorld", 1,
             "El World crea los actores, aplica el daño y decide el final del combate.",
             {"JUG": 0, "FIA": -1, "REN": +1, "EXT": -2, "ALC": +2}),
            ("B", "CombatManager colaborador", 2,
             "Clase dedicada a las reglas; no sabe dibujar ni leer teclado. Sobrevive al porteo a Unity.",
             {"JUG": +1, "FIA": +2, "REN": 0, "EXT": +2, "ALC": -1}),
            ("C", "CombatManager Singleton global", 1,
             "Cómodo de invocar desde cualquier clase, pero el estado sobrevive al reinicio de partida.",
             {"JUG": -1, "FIA": -2, "REN": +1, "EXT": -1, "ALC": +1}),
        ],
    },
    {
        "id": "C5", "ref": "C-09", "puntaje": "3,70",
        "titulo": "NAVEGACION ENTRE PANTALLAS",
        "pregunta": "El juego tiene inicio, combate, victoria, derrota y reinicio. Cómo se "
                    "organiza el paso entre esas pantallas?",
        "opciones": [
            ("A", "Un solo World con variable de estado", 1,
             "El mismo World cambia su fondo y dibuja menu o combate segun una variable.",
             {"JUG": -1, "FIA": -1, "REN": +1, "EXT": -2, "ALC": +2}),
            ("B", "Tres Worlds con setWorld()", 2,
             "MenuWorld, FightWorld y EndWorld como escenarios separados.",
             {"JUG": +1, "FIA": +2, "REN": +1, "EXT": +1, "ALC": -1}),
            ("C", "Un World con GameState", 3,
             "El World delega dibujado e input al estado activo; portable, pero más indirecto.",
             {"JUG": 0, "FIA": +1, "REN": 0, "EXT": +2, "ALC": -2}),
        ],
    },
    {
        "id": "C6", "ref": "C-08", "puntaje": "3,60",
        "titulo": "DIFERENCIACION DE PERSONAJES",
        "pregunta": "Kaien usa fuego, Raiko es eléctrico y veloz, Sora ataca a distancia. Cómo se "
                    "representa la diferencia de estilo entre personajes?",
        "opciones": [
            ("A", "Un if por personaje", 1,
             "usarEspecial() consulta el nombre del personaje y ramifica.",
             {"JUG": 0, "FIA": -1, "REN": 0, "EXT": -2, "ALC": +2}),
            ("B", "Una subclase por personaje", 2,
             "Cada personaje redefine usarEspecial() y sus estadisticas base. Evidencia de polimorfismo.",
             {"JUG": +1, "FIA": +1, "REN": 0, "EXT": +2, "ALC": -1}),
            ("C", "Objeto Tecnica intercambiable", 3,
             "La habilidad es un objeto que el luchador contiene y puede cambiarse en caliente.",
             {"JUG": +2, "FIA": +1, "REN": -1, "EXT": +2, "ALC": -2}),
        ],
    },
    {
        "id": "C7", "ref": "C-03", "puntaje": "3,60",
        "titulo": "INTELIGENCIA DEL ENEMIGO",
        "pregunta": "El enemigo debe acercarse, retroceder, atacar a distancia adecuada y bloquear "
                    "de vez en cuando, sin caer en una secuencia fija. Dónde vive esa lógica?",
        "opciones": [
            ("A", "Cadena de if en Enemy.act()", 1,
             "Decisiones segun la distancia al jugador, escritas dentro del propio enemigo.",
             {"JUG": -1, "FIA": 0, "REN": +1, "EXT": -2, "ALC": +2}),
            ("B", "Clase EnemyAI separada", 2,
             "Enemy delega la decisión; la IA devuelve una acción y el enemigo la ejecuta.",
             {"JUG": +1, "FIA": +1, "REN": 0, "EXT": +2, "ALC": -1}),
            ("C", "Autómata de estados con cooldowns", 3,
             "Perseguir, Atacar, Retroceder y Esperar con transiciones probabilísticas.",
             {"JUG": +2, "FIA": +1, "REN": -1, "EXT": +2, "ALC": -2}),
        ],
    },
    {
        "id": "C8", "ref": "C-12", "puntaje": "2,90",
        "titulo": "ARENAS DE COMBATE",
        "pregunta": "El prototipo necesita dos arenas que difieren en fondo, altura del suelo, "
                    "límites y posiciones iniciales. Cómo se configura un escenario?",
        "opciones": [
            ("A", "Una subclase de World por arena", 1,
             "BosqueWorld y TemploWorld; predecible de probar, pero duplica estructura.",
             {"JUG": 0, "FIA": +1, "REN": +1, "EXT": -1, "ALC": +2}),
            ("B", "FightWorld + objeto Arena", 2,
             "Un objeto aporta fondo, suelo, límites y puntos de aparicion.",
             {"JUG": +1, "FIA": +1, "REN": 0, "EXT": +2, "ALC": -1}),
            ("C", "Arenas definidas en un archivo", 3,
             "Se cargan al iniciar el combate; maxima flexibilidad, más superficie de fallo.",
             {"JUG": +2, "FIA": -1, "REN": 0, "EXT": +2, "ALC": -2}),
        ],
    },
]

# ---------------------------------------------------------------- eventos
EVENTOS = [
    {
        "id": "E1", "titulo": "PLAYTEST: LOS GOLPES NO SE SIENTEN",
        "contexto": "Quienes prueban el juego dicen que reciben daño sin que el golpe se vea conectar.",
        "consecuencia": "Revisa C3. Si elegiste A: JUG -2 y FIA -1. Si B: sin penalización. "
                        "Si C: JUG -1. Puedes reconsiderar C3.",
        "revisa": "C3",
    },
    {
        "id": "E2", "titulo": "SE PIDE UN TERCER PERSONAJE",
        "contexto": "El profesor quiere ver un personaje más para comprobar que el diseño escala.",
        "consecuencia": "Revisa C6. A: EXT -2 y gasta 2 Tiempo. B: gasta 1 Tiempo. C: EXT +1.",
        "revisa": "C6",
    },
    {
        "id": "E3", "titulo": "EL ENEMIGO ES PREDECIBLE",
        "contexto": "Tras dos combates cualquiera descubre el patron del rival y gana sin esfuerzo.",
        "consecuencia": "Revisa C7. A: JUG -2 y gasta 1 Tiempo. B: JUG -1. C: JUG +1.",
        "revisa": "C7",
    },
    {
        "id": "E4", "titulo": "BUG: PERSONAJE CONGELADO",
        "contexto": "Si te golpean a mitad de un ataque, el luchador queda trabado y no responde más.",
        "consecuencia": "Revisa C2. A: FIA -3 y gasta 2 Tiempo. B: FIA -1. C: sin penalización. "
                        "Puedes reconsiderar C2.",
        "revisa": "C2",
    },
    {
        "id": "E5", "titulo": "RECESO DE FIESTAS PATRIAS",
        "contexto": "La semana del 18 de septiembre no tiene clases ni entrega y el calendario se corre.",
        "consecuencia": "Pierde 3 fichas de Tiempo. No se recuperan aunque mantengas todas las decisiones. "
                        "A partir de ahora, ante empate el equipo elige la opción más barata.",
        "revisa": "-",
    },
    {
        "id": "E6", "titulo": "EL JUEGO SE PORTA A UNITY",
        "contexto": "La Unidad 3 exige rehacer el juego en Unity. Lo pegado a la API de Greenfoot se reescribe.",
        "consecuencia": "Revisa C4. A: EXT -2 y gasta 2 Tiempo. B: EXT +2. C: EXT -1 y FIA -1.",
        "revisa": "C4",
    },
    {
        "id": "E7", "titulo": "UNA TERCERA ARENA",
        "contexto": "Se agrega la azotea nocturna, con otra altura de suelo y otros límites laterales.",
        "consecuencia": "Revisa C8. A: gasta 2 Tiempo y EXT -1. B: gasta 1 Tiempo. C: sin costo.",
        "revisa": "C8",
    },
    {
        "id": "E8", "titulo": "REVISION DE ORIGINALIDAD",
        "contexto": "Se revisa que ningun nombre, técnica ni asset provenga de una obra con derechos.",
        "consecuencia": "Revisa C6. A: gasta 2 Tiempo, porque los datos del personaje están repartidos "
                        "por el código. B o C: gasta 1 Tiempo. Todos: registra el origen de cada asset.",
        "revisa": "C6",
    },
]
