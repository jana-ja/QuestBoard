---
name: sprint-planning
description: Sprint Planning durchführen – Sprintziel vorschlagen, Tickets aus dem Backlog auswählen und schneiden, mit dem Product Owner abstimmen und in GitHub anlegen.
disable-model-invocation: true
allowed-tools: Bash(gh issue list *) Bash(git log *)
---

# Sprint Planning

Lies zuerst `docs/arbeitsweise.md` (Abschnitt Sprints) und den aktuellen Meilenstein in
`docs/quest-board-prd.md`.

## Aktueller Stand

Offene Issues:
!`gh issue list --state open --limit 50 --json number,title,labels,milestone`

Zuletzt geschlossen:
!`gh issue list --state closed --limit 15 --json number,title,closedAt`

Letzte Commits auf main:
!`git log --oneline -15 main`

## Ablauf

1. **Rückblick in einem Satz:** Was wurde im letzten Sprint fertig, was ist offen geblieben?
   Unfertiges wandert zurück ins Backlog oder in den neuen Sprint – nicht stillschweigend.
2. **Sprintziel vorschlagen:** ein Satz, der zum aktuellen Meilenstein passt
   (z. B. "Die leere App ist per HTTPS erreichbar").
3. **Tickets vorschlagen:** Aus dem Backlog und dem Meilenstein die nötigen Tickets ableiten.
   Fehlen Tickets, schreibe sie nach der Vorlage aus `/ticket`. Jedes Ticket bekommt
   Größe (1, 2, 3, 5 Punkte; 1 Punkt ≈ ein Abend), Bereich und Besitzer (junior/senior).
   Kapazität: rund 12–20 Stunden Junior-Zeit pro Sprint (2 Wochen); plane eher knapp.
4. **Mit dem Product Owner abstimmen:** Sprintziel und Ticketliste als Tabelle zeigen.
   Produktfragen mit **[PO]** markieren. Erst nach Zustimmung anlegen.
5. **Anlegen:** Issues mit `gh issue create` (Labels, Meilenstein `Sprint N`), falls es den
   Meilenstein noch nicht gibt, anlegen. Falls ein GitHub Project existiert, Issues dort
   eintragen.
6. **Erstes Ticket:** Empfiehl, womit der Junior anfängt, und warum.

Halte die Ausgabe kompakt: Tabelle plus wenige Sätze.
