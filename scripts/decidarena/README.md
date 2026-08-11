# DecidArena — generador del kit imprimible

Adaptación del juego de mesa **DecidArch** al proyecto Shinobi Arena. Produce
[`DecidArena-Kit-Imprimible.pdf`](../../docs/u1-s1-priorizacion-concerns/DecidArena-Kit-Imprimible.pdf):
12 páginas A4 con reglas, cartas recortables, tablero y hojas de registro.

## Archivos

| Archivo | Función |
|---|---|
| `kit_datos.py` | **Fuente única.** Pistas de calidad, stakeholders, 8 concerns con sus opciones e impactos, y 8 eventos |
| `validar.py` | Comprueba que el juego sea jugable antes de imprimirlo |
| `generar_kit.py` | Construye el HTML a partir de los datos |
| `kit_estilos.css` | Maquetación A4 |

## Uso

```bash
pip install weasyprint
python3 validar.py        # primero: si falla, no generes nada
python3 generar_kit.py
python3 -c "from weasyprint import HTML; HTML('kit.html').write_pdf('DecidArena-Kit-Imprimible.pdf')"
```

## Qué comprueba `validar.py`

El kit no se imprime hasta que estas cinco condiciones se cumplen:

1. **Estructura** — 8 concerns con 3 opciones cada uno, 8 eventos, 5 pistas, costos de Tiempo entre 1 y 4.
2. **Ninguna opción sin trade-offs** — regla explícita de DecidArch: toda opción debe tener al menos un impacto negativo y uno positivo.
3. **Ninguna opción dominada** — si una opción fuera mejor o igual en las cinco pistas y no más cara que otra, elegir sería trivial.
4. **Dificultad calibrada** — se simulan las 6.561 combinaciones posibles; deben ganar entre el 2 % y el 40 %.
5. **Sin estrategia trivial** — elegir siempre A, siempre B o siempre C debe perder.

La primera versión de los datos falló la condición 2: todas las opciones B eran gratis, así que
"elegir siempre lo intermedio" ganaba y el juego no obligaba a decidir nada. Se les asignó
un costo en Alcance, que es lo que ocurre en la realidad: construirlo bien consume semestre.

## Estado actual

```
Combinaciones posibles:  6.561
Combinaciones ganadoras:   338  (5,2 %)

todas A  -> pierde   EXT -13   (sin arquitectura)
todas B  -> pierde   ALC  -8   (no alcanza el semestre)
todas C  -> pierde   ALC -13, Tiempo -4
```

## Relación con la entrega

Los 8 concerns del mazo son los 8 mejor puntuados de los 12 de
[`04-priorizacion.md`](../../docs/u1-s1-priorizacion-concerns/04-priorizacion.md), en ese
mismo orden. Los 9 atributos de calidad de
[`02-stakeholder-cards.md`](../../docs/u1-s1-priorizacion-concerns/02-stakeholder-cards.md)
se condensan en 5 pistas jugables; cada carta indica qué atributos condensa.
