# Quest Board

Installierbare Web-App (PWA), die Todos im Stil eines Mittelalter-RPGs als Quests darstellt.
Neben Pflichten schlägt sie gezielt Quests für Erholung, Hobbys und neue Erfahrungen vor und
misst die Balance zwischen Work und Fun.

Quest Board ist zugleich ein Lernprojekt für Backend-Entwicklung mit Python sowie DevOps,
Deployment und Cloud.

## Aufbau des Repositorys

| Ordner | Inhalt |
|---|---|
| [`backend/`](backend/README.md) | API mit FastAPI, später SQLAlchemy und PostgreSQL |
| `frontend/` | React + TypeScript als PWA *(folgt)* |
| `infra/` | Docker Compose, Caddy, Deploy- und Backup-Skripte *(folgt)* |
| `.github/` | CI-Workflows, Issue- und PR-Vorlagen |
| [`docs/`](docs/) | Anforderungen, Fachkonzept, Arbeitsweise, Architekturentscheidungen |

Frontend und API laufen unter einer Domain: das Frontend unter `/`, die API unter `/api`.

Jedes Teilprojekt hat eine eigene README mit Einrichtung, Start und Prüfbefehlen.

## Dokumentation

- [Anforderungen (PRD)](docs/quest-board-prd.md) – Ziele, Tech Stack, Architektur, Meilensteine
- [Fachkonzept](docs/quest-board-konzept.md) – Quest-Modell, Lebenszyklus, Balance, Belohnungen
- [Arbeitsweise](docs/arbeitsweise.md) – Sprints, Tickets, Reviews, Definition of Done
- [Lernleitfaden](docs/lernleitfaden.md) – Lernpfad pro Meilenstein
- [Architekturentscheidungen](docs/adr/)
- [Lessons Learned](docs/lessons-learned.md)

## Mitarbeit

Änderungen laufen über Branch → Pull Request → grüne CI → Merge; `main` ist geschützt.
Commits folgen [Conventional Commits](https://www.conventionalcommits.org/) auf Englisch.
Details in der [Arbeitsweise](docs/arbeitsweise.md).
