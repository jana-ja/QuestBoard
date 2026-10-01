---
paths:
  - "backend/**"
---

# Backend-Regeln

Hier implementiert der Junior. Du gibst Vorgaben, beantwortest Fragen und reviewst
(siehe Output Style "Senior Mentor", gestufte Hilfe).

## Stack
Python, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), Alembic, asyncpg/psycopg 3,
uv, Ruff, Pyright (strict), structlog, pytest + pytest-asyncio + Testcontainers.

## Konventionen
- Typen überall; Pyright im strikten Modus muss grün sein.
- Varianten (Seite, Wiederholung, Verbindlichkeit) als Pydantic Discriminated Unions;
  Fallunterscheidung mit `match` und `assert_never`.
- Fachlogik als reine Funktionen, die "jetzt" als Parameter bekommen – nie `datetime.now()`
  tief in der Logik. So lassen sich Tage in Tests simulieren.
- Schichten: Router (HTTP) → Services (Fachlogik) → Repositories/Queries (Datenbank).
  Router enthalten keine Fachlogik.
- Auswertungen (Balance, Zähler) gern als SQL über SQLAlchemy Core.
- Fehler an die API als Codes (`quest.cannot_return_main`), nicht als Sätze.
- Konfiguration über pydantic-settings und Umgebungsvariablen; Balance- und Pool-Konstanten
  gesammelt in einer Settings-Gruppe.
- Jede Schemaänderung als Alembic-Migration; Migrationen sind Teil des PRs.

## Tests
- Jede Fachregel aus `docs/quest-board-konzept.md`, die umgesetzt wird, bekommt mindestens
  einen Test. Besonders: Lebenszyklus, Tageswechsel (inkl. Nachholen und Parallelität),
  Bearbeitungsregeln, Pool-Ziehung.
- Datenbanktests gegen echtes PostgreSQL (Testcontainers), keine SQLite-Abkürzung.
