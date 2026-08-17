# Generador del mazo DecidArch — Shinobi Arena

Produce [`ShinobiArena-DecidArch-Kit.pdf`](../../docs/u1-s1-priorizacion-concerns/ShinobiArena-DecidArch-Kit.pdf):
9 páginas A4 con las cartas recortables, las dos plantillas de registro y el Scoring Sheet,
siguiendo el formato de **DecidArch v1** (CardSet, GameRules, ScoreSheet y Templates oficiales).

## Archivos

| Archivo | Función |
|---|---|
| `v1_datos.py` | **Fuente única.** Project Card, 3 Stakeholder Cards, 10 Concern Cards y 6 Event Cards |
| `v1_validar.py` | Comprueba el mazo antes de imprimirlo. Si falla, no se genera nada |
| `v1_generar.py` | Construye el HTML con la maquetación oficial |

## Uso

```bash
pip install weasyprint
python3 v1_validar.py     # primero: si falla, no generes
python3 v1_generar.py
python3 -c "from weasyprint import HTML; HTML('v1_kit.html').write_pdf('ShinobiArena-DecidArch-Kit.pdf')"
```

## Qué comprueba el validador

1. **Tamaño del mazo** igual al set oficial: 10 Concern Cards, 6 Event Cards, 3 opciones por concern
2. **Notación válida**: solo los símbolos `+`, `++`, `-`, `--`
3. **Ninguna opción sin trade-offs** — toda opción debe tener al menos un impacto positivo y uno negativo
4. **Ninguna opción dominada** — si una fuera mejor o igual en los nueve atributos, elegir sería trivial
5. **Ningún atributo huérfano** — regla dada en clase: todo atributo usado en un concern debe estar declarado en alguna Stakeholder Card
6. **QA-Priority impresas en 0** — como en el CardSet oficial; son los eventos quienes las suben
7. **Eventos coherentes** — cada evento solo modifica atributos que ese stakeholder declara
8. **Mazo ganable y perdible** con el scoring oficial

## Scoring implementado

Tomado literalmente de `DecidArch-ScoreSheet.pdf`:

```
Paso 1   QA-Score = A − B      A = cantidad de "+"  ("++" cuenta dos veces)
                               B = cantidad de "−"  ("--" cuenta dos veces)
Paso 2   C = QA-Score − QA-Priority, por atributo y por stakeholder
         Si algún C < 0 → derrota
         Stakeholders-Score = Σ C
Paso 3   Final Score = Stakeholders-Score − D    (D = concerns sin resolver)
```

## Estado actual del mazo

```
Combinaciones posibles: 59.049
  ganadoras sin eventos:   5.200  ( 8,8 %)
  ganadoras con 6 eventos:   130  ( 0,2 %)

todas 1  -> pierde     elegir siempre lo simple deja el sistema sin arquitectura
todas 2  -> pierde
todas 3  -> pierde     elegir siempre lo elaborado hunde Performance y Analysability
```

Las Event Cards son la presión real: el mazo base es holgado y los eventos lo aprietan, que es
exactamente su función en DecidArch.

## Relación con la entrega

Los 10 concerns del mazo son los 10 mejor puntuados de los 12 de
[`04-priorizacion.md`](../../docs/u1-s1-priorizacion-concerns/04-priorizacion.md), en ese orden.
El detalle de las correcciones respecto de la primera versión está en
[`06-correcciones.md`](../../docs/u1-s1-priorizacion-concerns/06-correcciones.md).
