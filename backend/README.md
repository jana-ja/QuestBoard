# Quest Board – Backend

API für Quest Board, gebaut mit FastAPI. Überblick über das Gesamtprojekt: [README im Root](../README.md).

## Voraussetzungen

- [uv](https://docs.astral.sh/uv/) – verwaltet Python-Version, Abhängigkeiten und virtuelle Umgebung.
  Python 3.13 muss nicht separat installiert werden; uv lädt die Version aus `.python-version` bei Bedarf selbst.

Alle Befehle werden im Ordner `backend/` ausgeführt.

## Einrichten

```bash
uv sync
```

Legt `.venv/` an und installiert alle Abhängigkeiten exakt so, wie sie in `uv.lock` festgehalten sind
(inklusive der Entwicklungswerkzeuge).

## Starten

<!-- TODO: Startbefehl für Uvicorn und die lokale URL ergänzen -->

## Prüfen

| Befehl | Zweck |
|---|---|
| `uv run ruff check` | Linting: findet Fehlerquellen und Stilprobleme |
| `uv run ruff format --check` | Formatierung prüfen, ohne Dateien zu ändern |
| `uv run pyright` | Statische Typprüfung (strikter Modus) |
| `uv run pytest` | Tests ausführen |

Automatisch korrigieren:

```bash
uv run ruff check --fix
uv run ruff format
```

## Struktur

```
src/quest_board/   Anwendungscode
tests/             Tests (pytest)
pyproject.toml     Abhängigkeiten und Konfiguration von Ruff und Pyright
uv.lock            Exakt aufgelöste Versionen aller Abhängigkeiten – wird eingecheckt
```
