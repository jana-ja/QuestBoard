---
name: sprint-review
description: Sprint Review und Retrospektive am Ende eines Sprints – Ergebnis gegen Sprintziel prüfen, Demo, Lernfortschritt, Retro-Fragen und konkrete Verbesserungen für Prozess und CLAUDE.md.
disable-model-invocation: true
allowed-tools: Bash(gh issue list *) Bash(gh pr list *)
---

# Sprint Review und Retrospektive

## Stand

Zuletzt geschlossene Issues (nach `closedAt` auf den Sprintzeitraum eingrenzen):
!`gh issue list --state closed --limit 30 --json number,title,labels,milestone,closedAt`

Noch offene Issues:
!`gh issue list --state open --limit 50 --json number,title,labels,milestone`

Gemergte PRs:
!`gh pr list --state merged --limit 15 --json number,title,mergedAt`

## Teil 1: Review (Produkt)

1. Sprintziel nennen und ehrlich bewerten: erreicht / teilweise / nicht erreicht.
2. Was ist fertig im Sinne der Definition of Done (`docs/arbeitsweise.md`)?
   Was ist "fast fertig" – das zählt nicht als fertig.
3. **Demo:** Schlage vor, was der Junior zeigen bzw. ausprobieren soll
   (Endpunkt aufrufen, App auf dem Handy öffnen, Deployment auslösen).
4. **[PO]**-Fragen: Passt das Ergebnis? Ändert sich etwas an Prioritäten im Backlog?
5. Punkte: geplant vs. erledigt (Velocity) – als Information, nicht als Bewertung.

## Teil 2: Retrospektive (Team)

Stelle diese Fragen und warte auf Antworten, bevor du deine eigene Sicht ergänzt:
- Was lief gut?
- Was lief nicht gut oder hat unnötig Zeit gekostet?
- Was habe ich gelernt? Was ist noch unklar?
- Wie war die Zusammenarbeit mit dem Senior (zu viel / zu wenig Hilfe, Tickets klar genug)?

Ergänze danach deine Sicht als Senior: ein Lob, eine Beobachtung, eine Empfehlung.

## Teil 3: Maßnahmen

- Höchstens zwei konkrete Verbesserungen für den nächsten Sprint.
- Vorschläge für `docs/lessons-learned.md`.
- Vorschläge für `CLAUDE.md`, Rules oder Skills, falls du wiederholt etwas falsch gemacht
  hast oder der Junior etwas wiederholt erklären musste. Erst zeigen, dann nach Freigabe ändern.
- Prüfen, ob ein Meilenstein erreicht ist und eine Kaputt-mach-Übung aus dem
  Lernleitfaden ansteht.

Zum Schluss: Hinweis auf `/sprint-planning` für den nächsten Sprint.
