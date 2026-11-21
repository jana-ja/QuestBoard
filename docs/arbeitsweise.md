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
- **Kapazität:** wird in jedem Sprint Planning neu erfragt: Wie viele Abende sind realistisch verfügbar?
  Abgeglichen mit der Velocity der letzten Sprints. Höchstens so viele Junior-Punkte wie Abende;
  alles darüber nur als markierter Stretch. Lieber zu wenig als zu viel einplanen.
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
   `feat(backend): add quest model`, `test(backend): cover rollover catch-up`, `fix(infra): correct caddy route`. Weitere Hinweise zu Git Naming Conventions in Punkt 8.
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
  - Status-Checks müssen grün sein (`check-changes` und `check-backend`), Regel gilt auch für Admins und darf nicht übergangen werden.
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

---

## 8. Git Naming Conventions

### Commits

`type(scope): describe the changes so others and future you understand what you did here`  
`type(scope)!: describe the breaking changes so others and future you understand what you did here`

Format:  
Imperativ, Englisch, klein, kein Punkt am Ende

#### Typen
| Type | Beispiel |
|---|---|
| feat | `feat(backend): add health endpoint`|
| fix | `fix(backend): handle missing timezone` |
| refactor | `refactor(backend): extract quest service` |
| test | `test(backend): cover day rollover` |
| docs | `docs: add ADR for database driver` |
| build | `build(backend): remove sqlalchemy and alembic` |
| ci | `ci: run pyright in backend workflow` |
| chore | `chore(backend): simplify ruff config` |
| style | `style(backend): apply ruff format` |
| perf | `perf(backend): index quest instances by day` |

Möglichst spezifisch wählen: Ist es ein Fehler (`fix`), nur Doku (`docs`), nur Tests (`test`), CI (`ci`) oder eine Abhängigkeit (`build`)? Erst wenn nichts davon passt, `chore`.

Merkt jemand, der das System betreibt oder benutzt, den Fehler? Dann fix. Merkt es nur, wer am Code arbeitet? Dann chore.

#### Scopes
backend, frontend, infra

Kein Scope, wenn die Änderung übergreifend ist oder bereits durch den Typ abgedeckt.

#### Breaking Changes
Werden durch `type(scope)!: ...` markiert und zusätzlich mit einem Footer versehen:
`BREAKING CHANGE: <was beachtet werden muss>`

Der Footer steht am Ende der Commit Message nach einer Leerzeile, beim PR (siehe unten) im PR-Text.

### Branches

`prefix/XX-short-name`  
`prefix/short-name` **nur** ohne zugehöriges Ticket

Format: Keine Klammern, keine Leerzeichen, kein Scope

#### Präfixe
Das Präfix beschreibt den Bereich der Änderungen
| Präfix | Beispiel | Typischer Commit-Typ |
|---|---|---|
| feat | `feat/19-board-endpoint` | feat |
| fix | `fix/compose-healthcheck` | fix |
| infra | `infra/20-caddy-reverse-proxy` | feat, build, ci |
| docs | `docs/7-adr-api-versioning`| docs |
| chore | `chore/5-break-ci-and-volumes` | chore, refactor, build, test |

Präfix Wahl:   
Fehler → `fix/`. Nur Doku → `docs/`. Sonst nach Bereich: `infra/` (infra/, .github/). Neue Funktion in Backend oder Frontend → `feat/`. Alles andere → `chore/`. Weitere Präfixe gibt es nicht.  

### PRs

`type(scope): describe the changes so others and future you understand what you did here`

Format: wie bei Commits

#### Inhalt des Titels
Beim Squash-Merge wird der PR Titel zur einzigen Commit Message.
- Bei PRs mit nur einem Commit sind diese identisch.
- Bei mehreren Commits beschreibt der PR Titel das Gesamtziel des PRs/Tickets. Der Typ ist der wichtigste Typ unter den Commits. feat und fix schlagen alles andere, docs, test, chore und build gelten nur, wenn sie allein stehen.

PR Nummer nicht in den Titel hinzufügen, wird beim mergen automatisch von GitHub angehängt.
Ticket Nummer nicht in den Titel hinzufügen, sondern per Closes (siehe unten), wird dann durch GitHub verknüpft.

#### Ticket
Closes #nr, wenn der PR das Ticket fertigstellt und schließen soll.
Refs #nr, wenn der PR zum Ticket beiträgt, es aber nicht fertigstellt.
