# Quest Board – Infrastruktur

Lokale Entwicklungsumgebung mit Docker Compose. Aktuell läuft hier nur die Datenbank;
später kommen API und Reverse Proxy (Caddy) dazu. Überblick über das Gesamtprojekt:
[README im Root](../README.md).

## Voraussetzungen

- [Docker Desktop](https://docs.docker.com/desktop/) mit Docker Compose v2 (`docker compose`, nicht `docker-compose`)
- Optional für Verbindungen vom Host: der PostgreSQL-Client `psql`, z. B. per `brew install libpq`

Alle Befehle werden im Ordner `infra/` ausgeführt.

## Einrichten

Einmalig die Vorlage kopieren und Werte eintragen:

```bash
cp .env.example .env
```

| Variable | Bedeutung | Default |
|---|---|---|
| `POSTGRES_USER` | Benutzer der Datenbank | `postgres` |
| `POSTGRES_PASSWORD` | Passwort dieses Benutzers | - (Pflicht) |
| `POSTGRES_DB` | Name der Datenbank (Unterstrich statt Bindestrich) | `quest_board` |
| `POSTGRES_PORT` | Port auf dem Host | `5432` |

`.env` enthält Zugangsdaten und wird nicht eingecheckt. Benutzer, Passwort und Datenbankname
werden nur beim **ersten** Start mit leerem Volume ausgewertet – wer sie später ändert, muss
die Daten mit `docker compose down -v` löschen.

## Starten und Stoppen

| Befehl | Wirkung |
|---|---|
| `docker compose up -d` | Startet die Datenbank im Hintergrund |
| `docker compose ps` | Zeigt den Status; die Datenbank ist bereit, wenn dort `healthy` steht |
| `docker compose logs db` | Zeigt die Logs der Datenbank |
| `docker compose stop` | Hält den Container an; er bleibt bestehen |
| `docker compose down` | Entfernt den Container; die Daten im Volume bleiben erhalten |
| `docker compose down -v` | Entfernt Container **und Volume – alle Daten sind weg** |

Restart-Policy ist `unless-stopped`: Nach einem Absturz oder Neustart von Docker startet die
Datenbank von selbst wieder, außer sie wurde von Hand gestoppt.

## Verbinden

Im Container (kein lokaler Client nötig):

```bash
docker compose exec db psql -U <benutzer> -d <datenbank>
```

Vom Host aus (Passwort wird abgefragt):

```bash
psql -h 127.0.0.1 -p <port> -U <benutzer> -d <datenbank>
```

Der Port ist nur an `127.0.0.1` gebunden, die Datenbank ist also von anderen Rechnern im
Netzwerk aus nicht erreichbar.

## Daten

Die Daten liegen im benannten Volume `infra_db_data` (Compose setzt den Projektnamen `infra`
davor). Anzeigen mit:

```bash
docker volume ls --filter name=infra
docker volume inspect infra_db_data
```

Unter macOS liegt das Volume in der Linux-VM von Docker Desktop, nicht im Dateisystem des Macs.

## Struktur

```
compose.yaml   Dienste, Volumes, Ports, Healthcheck
.env.example   Namen der Umgebungsvariablen, ohne Werte – wird eingecheckt
.env           Eigene Werte – wird nicht eingecheckt
```
