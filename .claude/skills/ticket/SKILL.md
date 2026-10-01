---
name: ticket
description: Ein Ticket (GitHub Issue) nach der Team-Vorlage schreiben – Story, Task, Spike oder Bug – mit Akzeptanzkriterien, Vorgaben und Lernziel, aber ohne die Lösung vorwegzunehmen.
argument-hint: "[Thema des Tickets]"
---

# Ticket schreiben

Thema: $ARGUMENTS

Lies die relevanten Abschnitte in `docs/quest-board-prd.md` und `docs/quest-board-konzept.md`.
Wähle den Typ: **story** (Nutzerwert), **task** (technisch), **spike** (zeitbegrenzt
recherchieren, Ergebnis ist eine Entscheidung oder ein ADR), **bug**, **learning**
(reine Übung, z. B. Kaputt-mach-Übung).

## Vorlage

```markdown
## Ziel
Ein bis zwei Sätze: Was soll danach möglich sein und warum?
(Story: "Als Nutzer möchte ich …, damit …")

## Kontext
- Anforderungen: PRD Q-1, B-3 …
- Fachlogik: Konzept Abschnitt …
- Abhängigkeiten: #12

## Akzeptanzkriterien
- [ ] prüfbares Kriterium
- [ ] Tests für …
- [ ] Doku/ADR aktualisiert (falls nötig)

## Technische Vorgaben
- Gesetzt: … (z. B. Ort im Code, Bibliothek, Muster)
- Frei wählbar: …

## Lernziel
Was soll der Junior danach verstanden haben?

## Einstieg
Zwei bis drei Hinweise, wo man anfängt – keine Lösung.

Größe: 1 | 2 | 3 | 5 · Bereich: backend | frontend | infra | docs · Besitzer: junior | senior
```

## Regeln
- Tickets über 5 Punkte aufteilen.
- Akzeptanzkriterien müssen prüfbar sein ("Endpunkt liefert 409, wenn …", nicht "funktioniert gut").
- Bei Produktunklarheiten: **[PO]**-Frage stellen, bevor das Ticket angelegt wird.
- Zeige das Ticket erst zur Freigabe, dann anlegen mit
  `gh issue create --title "<typ>: <titel>" --label "<typ>,<bereich>,<besitzer>" --body-file -`.
