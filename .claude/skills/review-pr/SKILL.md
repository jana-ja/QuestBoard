---
name: review-pr
description: Code Review eines Pull Requests wie ein Senior Developer – Ansatz, Akzeptanzkriterien, Tests, Sicherheit, Architekturregeln – mit gekennzeichneten Kommentaren und klarem Fazit.
argument-hint: "<PR-Nummer>"
disable-model-invocation: true
allowed-tools: Bash(gh pr view *) Bash(gh pr diff *) Bash(gh issue view *)
---

# Code Review für PR #$ARGUMENTS

## PR

!`gh pr view $ARGUMENTS --json number,title,body,headRefName,baseRefName,additions,deletions,files,statusCheckRollup`

## Diff

!`gh pr diff $ARGUMENTS`

## Ablauf

1. Verknüpftes Ticket lesen (`gh issue view <nr>`), Akzeptanzkriterien abgleichen.
2. Passende Abschnitte in Konzept/PRD lesen, wenn Fachlogik betroffen ist.
3. Bei Bedarf den Branch lokal ansehen und Tests ausführen
   (`gh pr checkout $ARGUMENTS`, dann die Testbefehle aus `CLAUDE.md`). Danach zurück zum
   vorherigen Branch wechseln.
4. Review schreiben:
   - **Gesamteindruck** (2–3 Sätze): Erfüllt der PR das Ticket? Stimmt der Ansatz?
   - **Kommentare** pro Datei/Zeile mit Kennzeichnung
     **[blocker]**, **[suggestion]**, **[nit]**, **[question]**, **[praise]**.
     Bei Blockern immer das Warum. Lösungen als Hinweis, nicht als fertigen Code –
     außer bei Einzeilern.
   - **Checkliste:** Tests für die Fachlogik · Fehlerfälle · Sicherheit (Secrets, Rechte,
     Validierung, `user_id`-Filter) · Architekturregeln aus `CLAUDE.md` · Migration dabei ·
     Doku/ADR aktualisiert · CI grün.
   - **Fazit:** Approve / Approve mit Kleinigkeiten / Changes requested.
5. Frage, ob du das Review als Kommentar am PR hinterlegen sollst. Falls ja:
   `gh pr review $ARGUMENTS --comment --body-file -`
   (GitHub erlaubt kein Approve des eigenen PRs; das Fazit steht im Kommentar.)
6. Wenn etwas besonders lehrreich war: Eintrag für `docs/lessons-learned.md` vorschlagen.
