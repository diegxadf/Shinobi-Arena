# Project Card

> Formato tomado de la *Project Card* de DecidArch.

---

**Project:** Shinobi Arena

**Purpose:**

Shinobi Arena es un videojuego de peleas 2D de uno contra uno, con vista lateral y control por teclado, desarrollado en Greenfoot con Java. El jugador encarna a un guerrero que compite en el *Torneo de los Cinco Reinos* y debe vencer a rivales sucesivos —cada uno con un estilo de combate distinto— para convertirse en Guardián Supremo.

El sistema debe cumplir dos propósitos simultáneos que no siempre apuntan en la misma dirección: **ser un juego que se pueda jugar de principio a fin**, y **ser una pieza de código que demuestre explícitamente contenidos de Programación Orientada a Objetos**. Esta doble finalidad es el origen de casi todas las tensiones arquitectónicas de este documento.

---

## Alcance del prototipo mínimo

| Incluido en el prototipo | Fuera del alcance inicial |
|---|---|
| 1 personaje jugable | Modo dos jugadores |
| 2 enemigos con comportamiento diferenciado | Combos y cancelaciones |
| 2 escenarios de combate | Guardado de progreso |
| Movimiento, salto, ataque, patada, bloqueo, proyectil | Sonido y música |
| 1 habilidad especial con consumo de chakra | Selector de personaje |
| Barra de vida y barra de energía | Ranking o puntajes persistentes |
| IA básica del enemigo | Red / multijugador online |
| Condición de victoria y de derrota | Animaciones cuadro a cuadro completas |
| Menú principal y reinicio de partida | Cronómetro de combate (opcional) |

---

## Restricciones (constraints)

Las restricciones no se negocian y acotan el espacio de opciones de cada Concern Card.

| # | Restricción | Origen | Consecuencia arquitectónica |
|---|---|---|---|
| R1 | El motor es **Greenfoot + Java** | Unidad 2 del ramo | Todo actor visible hereda de `Actor`; el bucle de juego es `act()`, no se puede reemplazar |
| R2 | El prototipo se construye en **3 días de trabajo efectivo** | Plan de trabajo propio | Se prefiere la opción simple y correcta sobre la opción general y elegante |
| R3 | El código debe **evidenciar** herencia, polimorfismo, encapsulamiento y composición | Rúbrica U2 | Una solución que funcione pero concentre todo en una clase es una solución reprobada |
| R4 | **Cero contenido con derechos de terceros**: nombres, personajes, aldeas, símbolos, música o técnicas de obras existentes | Enunciado del proyecto | Todos los assets y nombres son originales |
| R5 | El juego se **porta a Unity/C# en la Unidad 3** | Calendario del ramo | Conviene que las reglas de combate no queden pegadas a la API de Greenfoot |
| R6 | Debe ser **ejecutable y demostrable en vivo** ante el profesor | Entregable "Play Game", U2 S10 | Ningún estado del juego puede quedar sin salida (no hay pantallas muertas) |

---

## Contexto del sistema

```
        ┌──────────────┐
        │   Jugador    │  usa teclado, observa pantalla
        └──────┬───────┘
               │
        ┌──────▼────────────────────────┐
        │      SHINOBI ARENA            │
        │  (escenario Greenfoot + Java) │
        └──────┬────────────────────────┘
               │ se ejecuta sobre
        ┌──────▼───────┐
        │   Greenfoot  │  World, Actor, GreenfootImage, teclado
        │   + JVM      │
        └──────────────┘
```

El detalle de este contexto se formaliza en el **C4 Model — Context** de la Semana 3. Aquí se incluye solo para dejar claro qué está dentro del sistema y qué no.
