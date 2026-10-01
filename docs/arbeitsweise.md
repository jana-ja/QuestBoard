# Quest Board – Arbeitsweise im Team

Stand: 01.10.2026

Dieses Projekt simuliert den Alltag in einem kleinen Entwicklungsteam. Claude Code übernimmt die Rolle des Senior Developers, der Mensch die Rolle des Junior Developers und Product Owners. Der Prozess ist bewusst an Scrum angelehnt, aber auf ein Zwei-Personen-Team mit Feierabend-Kapazität zugeschnitten.

---

## 1. Rollen

| Rolle | Wer | Verantwortung |
|---|---|---|
| **Product Owner** | Mensch | Entscheidet über Produktverhalten, Umfang und Prioritäten. Nimmt Sprintergebnisse ab. |
| **Junior Developer** | Mensch | Implementiert Backend und Infrastruktur nach Tickets. Stellt PRs, beantwortet Reviews, merged nach Freigabe. |
| **Senior Developer / Tech Lead** | Claude Code | Trifft technische Entscheidungen, schreibt Tickets, gibt Vorgaben, reviewt, setzt das Frontend um, achtet auf den Prozess. |
| **Scrum Master** | geteilt | Claude erinnert an Zeremonien und Prozessschritte; der Mensch entscheidet, wann sie stattfinden. |

**Entscheidungsregel:** Technische Fragen entscheidet der Senior (mit Begründung, der Junior darf widersprechen). Produktfragen entscheidet der Product Owner; der Senior markiert sie mit **[PO]** und macht einen Vorschlag.

---

## 2. Sprints

- **Länge:** 2 Wochen.
- **Kapazität:** rund 12–20 Stunden Junior-Zeit pro Sprint. Lieber zu wenig als zu viel einplanen.
- **Schätzung:** Punkte 1, 2, 3, 5 (1 Punkt ≈ ein Abend). Größere Tickets werden geteilt.
- **Sprintziel:** Ein Satz, der zum aktuellen Meilenstein passt. Er ist wichtiger als jedes einzelne Ticket.
- **Sprint 0** entspricht Meilenstein M0 (Fundament), danach folgen die Meilensteine aus dem PRD. Ein Meilenstein kann mehrere Sprints umfassen.

### Zeremonien

| Zeremonie | Wann | Skill | Dauer |
|---|---|---|---|
| Sprint Planning | Sprintbeginn | `/sprint-planning` | 30–45 min |
| Standup / Check-in | Beginn jeder Arbeitssession | `/standup` | 2–5 min |
| Ticket schreiben | bei Bedarf | `/ticket` | – |
| Code Review | pro PR | `/review-pr <nr>` | – |
| Sprint Review + Retro | Sprintende | `/sprint-review` | 30–45 min |

Ein ausgefallener Abend ist kein Problem; der Sprint wird nicht verlängert, sondern im Review ehrlich bewertet.

---

## 3. Backlog und Tickets

- **Werkzeug:** GitHub Issues, Meilensteine pro Sprint (`Sprint 0`, `Sprint 1`, …). Optional ein GitHub Project als Board mit den Spalten *Backlog → Sprint → In Arbeit → Review → Fertig*.
- **Labels:**
  - Typ: `story`, `task`, `spike`, `bug`, `learning`
  - Bereich: `backend`, `frontend`, `infra`, `docs`
  - Besitzer: `junior`, `senior`
- **Ticket-Vorlage:** `.github/ISSUE_TEMPLATE/ticket.md` bzw. Skill `/ticket`. Jedes Ticket hat Ziel, Kontext mit Verweisen auf PRD und Konzept, prüfbare Akzeptanzkriterien, technische Vorgaben, Lernziel und Einstiegshinweise – aber nicht die Lösung.
- **Spikes** sind zeitlich begrenzt (z. B. 2 Stunden) und enden mit einer Entscheidung oder einem ADR.
- **Learning-Tickets** sind Übungen ohne Produktwert, z. B. die Kaputt-mach-Übungen aus dem Lernleitfaden. Sie gehören fest in die Sprints.

---

## 4. Entwicklungsablauf pro Ticket

1. Ticket in "In Arbeit" schieben, Branch anlegen: `feat/<nr>-kurzbeschreibung` (auch `fix/`, `chore/`, `docs/`, `infra/`).
2. Implementieren, kleine Commits nach Conventional Commits auf Englisch:
   `feat(backend): add quest model`, `test(backend): cover rollover catch-up`, `fix(infra): correct caddy route`.
3. Lokal prüfen: Linting, Typen, Tests (Befehle in `CLAUDE.md`).
4. Push, Pull Request mit der PR-Vorlage, `Closes #<nr>`.
5. CI muss grün sein.
6. Review durch den Senior (`/review-pr <nr>`). Kommentare beantworten oder umsetzen; Diskussion ist ausdrücklich erwünscht.
7. Bei "Approve": **Squash Merge** durch den Junior, Branch löschen.
8. Erkenntnisse, die mehr als eine halbe Stunde gekostet haben, in `docs/lessons-learned.md`.

Für Frontend-Tickets des Seniors gilt derselbe Ablauf mit vertauschten Rollen: Claude stellt den PR, der Junior reviewt und merged.

### Review-Kennzeichnungen

| Kennzeichnung | Bedeutung |
|---|---|
| **[blocker]** | Muss vor dem Merge geändert werden |
| **[suggestion]** | Sollte geändert werden, Begründung folgt |
| **[nit]** | Kleinigkeit, optional |
| **[question]** | Verständnisfrage, keine Änderung nötig |
| **[praise]** | Was gut gelöst ist |

### Gestufte Hilfe

Wenn der Junior feststeckt, hilft der Senior in Stufen: Rückfrage → Hinweis → Konzept erklären → kleines Fragment → vollständige Lösung (nur auf ausdrücklichen Wunsch). Bei Fehlersuche werden Hypothesen gemeinsam aufgestellt und geprüft.

---

## 5. Definition of Done

Ein Ticket ist fertig, wenn:

- [ ] alle Akzeptanzkriterien erfüllt sind,
- [ ] neue oder geänderte Fachlogik durch Tests abgedeckt ist,
- [ ] die CI grün ist (Linting, strikte Typprüfung, Tests),
- [ ] der PR reviewt und gemergt ist,
- [ ] Migrationen enthalten sind, falls sich das Schema geändert hat,
- [ ] betroffene Doku aktualisiert ist (PRD, Konzept, ADR, `CLAUDE.md`, Lessons Learned),
- [ ] ab M0.5: die Änderung automatisch deployt wurde und online funktioniert.

"Fast fertig" zählt im Sprint Review als nicht fertig.

---

## 6. Repository-Regeln

- `main` ist geschützt (Branch Protection auf GitHub):
  - Änderungen nur per Pull Request,
  - Status-Checks müssen grün sein (sobald die CI existiert),
  - **keine** erforderlichen Approvals – GitHub erlaubt nicht, den eigenen PR freizugeben; das Fazit des Reviews steht als Kommentar im PR,
  - Force-Push und Löschen von `main` verboten.
- Merge-Strategie: Squash Merge, damit `main` eine lesbare Historie mit einem Commit pro Ticket hat.
- Claude Code darf nicht auf `main` pushen und nicht mergen (zusätzlich in `.claude/settings.json` gesperrt).

---

## 7. Wie die Konfiguration von Claude Code aufgebaut ist

| Datei | Zweck | Wann geladen |
|---|---|---|
| `CLAUDE.md` | Rollen, Dokumentenkarte, Architekturregeln, Git-Regeln, Befehle | jede Session |
| `.claude/output-styles/senior-mentor.md` | Rolle und Verhalten als Senior: Entscheidungen, gestufte Hilfe, Reviews | jede Antwort (über `outputStyle` in `.claude/settings.json`) |
| `.claude/rules/backend.md`, `frontend.md`, `infra.md` | Bereichsregeln | nur bei Arbeit an passenden Dateien |
| `.claude/skills/*` | Abläufe für Zeremonien | nur beim Aufruf |
| `.claude/settings.json` | Output Style, erlaubte Lesebefehle, gesperrte Aktionen (Push auf `main`, Merge) | immer, technisch erzwungen |
| `docs/*` | Inhaltliche Grundlage | bei Bedarf gelesen |

**Pflege:** Wenn Claude denselben Fehler zweimal macht oder etwas wiederholt erklärt werden muss, gehört es in `CLAUDE.md` oder eine Rule. Das wird in jeder Retro geprüft.
