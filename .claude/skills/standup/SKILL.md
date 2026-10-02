---
name: standup
description: Kurzer Check-in zu Beginn einer Arbeitssession – was seit dem letzten Mal passiert ist, was heute dran ist, welche Blocker es gibt. Nutzen, wenn eine Session ohne konkreten Auftrag beginnt.
allowed-tools: Bash(git branch *) Bash(git log *) Bash(git status *) Bash(gh pr list *) Bash(gh issue list *)
---

# Standup

## Stand

Aktueller Branch:
!`git branch --show-current`

Letzte Commits:
!`git log --oneline -8`

Uncommittete Änderungen:
!`git status --short`

Offene Pull Requests:
!`gh pr list --json number,title,headRefName,reviewDecision`

Tickets im aktuellen Sprint:
!`gh issue list --state open --limit 30 --json number,title,labels,milestone`

## Ablauf

Höchstens fünf Sätze plus eine Frage:
1. Fasse zusammen, wo wir stehen (laufendes Ticket, offener PR, uncommittete Arbeit).
2. Weise auf Offenes hin, das zuerst erledigt werden sollte (z. B. Review-Kommentare
   beantworten, roter CI-Lauf, PR wartet auf Merge).
3. Schlage das Ziel für heute vor – realistisch für einen Abend.
4. Frage nach Blockern oder ob der Junior etwas anderes vorhat.
