# Quest Board – Product Requirements Document (v1)

Stand: 01.10.2026 · Status: Entwurf

Verwandte Dokumente:
- `quest-board-konzept.md` – Fachkonzept (Quest-Modell, Regeln, Board, Balance, Belohnungen)
- `lernleitfaden.md` – Lernprinzipien und Lernpfad
- `arbeitsweise.md` – Rollen, Sprints, Tickets, Reviews, Definition of Done

---

## 1. Überblick

Quest Board ist eine installierbare Web-App (PWA), die Todos im Stil eines Mittelalter-RPGs als Quests darstellt. Anders als klassische Todo-Apps schlägt sie neben Pflichten gezielt Quests für Erholung, Hobbys und neue Erfahrungen vor und misst die Balance zwischen Work und Fun. Ziel ist eine angenehme Abwechslung statt Abarbeiten unter Druck.

Das Projekt dient gleichzeitig als Lernprojekt für Backend-Entwicklung mit Python sowie DevOps, Deployment und Cloud. Alle Betriebsschritte werden selbst ausgeführt.

## 2. Problem und Ziele

**Problem:** Todo-Apps und Gamification-Apps belohnen fast ausschließlich Produktivität. Erholung und Hobbys tauchen dort nicht auf oder werden als "Belohnung" für erledigte Arbeit behandelt. Das verstärkt das Gefühl, Freizeit erst verdienen zu müssen.

**Produktziele:**
1. Pflichten und Erledigungen im Blick behalten und ohne Druck abarbeiten.
2. Fun-Quests (Rast und Erkundung) als gleichwertigen Teil des Alltags etablieren.
3. Die Balance zwischen Work und Fun sichtbar machen und das Angebot automatisch danach ausrichten.
4. Eine Atmosphäre schaffen, die Spaß macht und zum Öffnen der App einlädt.

**Lernziele:**
1. Ein Backend mit FastAPI, SQLAlchemy und PostgreSQL professionell aufbauen und testen.
2. Die komplette Betriebskette selbst beherrschen: Container, Server, Domain, HTTPS, CI/CD, Secrets, Backups.
3. Nach der Nutzbarkeit: Infrastructure as Code, Monitoring und Cloud.

## 3. Nutzer

- **v1:** eine Person (der Entwickler bzw. die Entwicklerin selbst). Nutzung täglich auf Handy und Desktop.
- **Später:** möglicherweise ein kleiner Kreis von Freunden. Das Datenmodell ist dafür vorbereitet (jede Tabelle hat einen Besitzer), soziale Funktionen sind nicht geplant.

## 4. Nicht-Ziele für v1

- Soziale Funktionen, Freundeslisten, Ranglisten
- Offene Registrierung, Einladungen, E-Mail-Versand
- Offline-Nutzung und Push-Benachrichtigungen (Architektur hält beides offen)
- Native Mobile-Apps, Homescreen-Widgets
- Pfade, Fraktionen, Events, Questreihen, Tages-Mana, Zähl-Quests
- Ingame-Währung, Shop, reale Belohnungen
- Englische Oberfläche (Struktur ist vorbereitet)
- Kalender-Anbindung

---

## 5. Funktionale Anforderungen

Die fachlichen Regeln sind im Fachkonzept ausführlich beschrieben; hier stehen die Anforderungen in prüfbarer Form. Priorität: **Muss** = Voraussetzung für "benutzbar" (M3), **Soll** = Teil von v1, **Kann** = wenn Zeit bleibt.

### 5.1 Quests verwalten

| ID | Anforderung | Prio |
|---|---|---|
| Q-1 | Quests können über einen Dialog angelegt werden (Pflicht/Spaß → Wie oft → Main/Side), danach Formular mit Details. | Muss |
| Q-2 | Schnellanlage nur mit Name; Default Side, Work, einmalig, nicht verbindlich, Größe M. | Muss |
| Q-3 | Alle Kombinationen aus Seite (Work/Fun mit optionaler Fun-Art), Wiederholung (Einmalig/Cooldown/Turnus), Verbindlichkeit (Keine/Immer/Ab Datum), Größe, `visible_from` und Fristen werden unterstützt, inklusive der Validierungsregeln. | Muss |
| Q-4 | Quests können bearbeitet werden; Änderungen wirken sofort auf Offenes und Zukünftiges, Vergangenes bleibt unverändert (Regeln siehe Konzept, Abschnitt 6). | Muss |
| Q-5 | Quests können gelöscht werden; bereits erledigte werden archiviert statt gelöscht. | Muss |
| Q-6 | Es gibt eine Übersicht aller eigenen Quests (Pool), aus der man direkt Quests annehmen kann. | Soll |

### 5.2 Board und Logbuch

| ID | Anforderung | Prio |
|---|---|---|
| B-1 | Das Board zeigt links alle fälligen Side Quests mit festem Turnus, rechts 6–8 Pool-Quests. | Muss |
| B-2 | Die Pool-Ziehung erfolgt einmal pro logischem Tag, gewichtet und nach Balance aufgeteilt (mind. 2 pro Seite, Auffüllen bei leerer Seite). | Muss (Balance-Aufteilung: Soll) |
| B-3 | Side Quests können vom Board angenommen werden und wandern ins Logbuch. | Muss |
| B-4 | Main Quests erscheinen automatisch im Logbuch und können nicht zurückgelegt werden. | Muss |
| B-5 | Side Quests können aus dem Logbuch zurückgelegt werden. | Muss |
| B-6 | Quests im Logbuch können abgehakt werden; direkt danach ist "Rückgängig" möglich, bis zum Tageswechsel können sie wieder geöffnet werden. | Muss |
| B-7 | Spontan erledigte Dinge können nachgetragen werden (aus dem Pool oder als freie Quest). | Muss |
| B-8 | Work-Side-Quests zeigen Skip- bzw. Angebots-Badges; Fun-Quests nie. | Soll |
| B-9 | Überfällige Main Quests werden markiert, das Alter von Quests im Logbuch wird dezent angezeigt. | Soll |
| B-10 | Eskalierende Quests werden an ihrem Datum zur Main Quest (Siegel-Moment). | Muss (Inszenierung: Soll) |

### 5.3 Tageswechsel

| ID | Anforderung | Prio |
|---|---|---|
| T-1 | Der Tageswechsel folgt dem logischen Tag des Nutzers (Zeitzone, Tagesbeginn Default 4:00 Uhr). | Muss |
| T-2 | Er wird bei der ersten Anfrage eines neuen logischen Tages ausgeführt und holt verpasste Tage nach. | Muss |
| T-3 | Er ist idempotent und läuft bei gleichzeitigen Anfragen nur einmal (Sperre pro Nutzer). | Muss |

### 5.4 Balance

| ID | Anforderung | Prio |
|---|---|---|
| BA-1 | Die Balance wird als Fun-Anteil der erledigten Punkte mit Abklingen (Halbwertszeit 3 Tage) und neutralem Grundwert berechnet. | Soll |
| BA-2 | Sie wird als Waage mit erklärendem Text dargestellt, nicht als Prozentwert. | Soll |
| BA-3 | Sie steuert die Aufteilung der Pool-Slots. | Soll |
| BA-4 | Alle Stellschrauben sind zentral konfigurierbar, ohne Codeänderung. | Soll |

### 5.5 Belohnungen

| ID | Anforderung | Prio |
|---|---|---|
| R-1 | Abhak-Moment mit Animation und Geräusch. | Soll (einfache Variante: Muss) |
| R-2 | Heldenlevel aus allen Punkten, mit Harmonie-Bonus in der ausgeglichenen Zone. | Soll |
| R-3 | Heldenchronik: Liste pro Tag mit erledigten Quests und Waage des Tages. | Soll |
| R-4 | Titel und Erfolge, aus der Historie abgeleitet. | Kann |

### 5.6 Onboarding und Konto

| ID | Anforderung | Prio |
|---|---|---|
| O-1 | Anmeldung mit Benutzername und Passwort; Abmelden, auch "von allen Geräten". | Muss |
| O-2 | Konten werden per Kommandozeilenbefehl auf dem Server angelegt; Passwort-Reset ebenfalls per Kommandozeile. | Muss |
| O-3 | Profil mit Zeitzone, Tagesbeginn und Wochenbeginn. | Soll (Zeitzone: Muss) |
| O-4 | Onboarding als kleine Quests, mit Auswahl aus einem Startpaket. | Soll |
| O-5 | Export aller eigenen Daten als JSON. | Kann |

---

## 6. Nicht-funktionale Anforderungen

| Bereich | Anforderung |
|---|---|
| Plattform | PWA, installierbar auf iOS, Android und Desktop; responsive ab 360 px Breite. |
| Synchronisierung | Mehrere Geräte zeigen denselben Stand; nach einer Aktion auf einem Gerät zeigt das andere beim nächsten Laden den neuen Stand. |
| Performance | Board und Logbuch laden in unter 1 s (bei einem Nutzer ohne Weiteres erreichbar). |
| Sprache | Oberfläche Deutsch. Alle Texte über Übersetzungsschlüssel; das Backend liefert Codes statt Sätzen; Datums- und Zahlenformate über `Intl`. |
| Sicherheit | Nur HTTPS; Passwörter mit Argon2; Sitzungs-Cookies `HttpOnly`, `Secure`, `SameSite=Lax`; Begrenzung der Login-Versuche; keine Secrets im Repository. |
| Datenhaltung | Tägliches, verschlüsseltes Backup an einem externen Ort; Wiederherstellung mindestens einmal getestet. |
| Verfügbarkeit | Kein formales Ziel. Ausfälle werden über einen externen Uptime-Check bemerkt. |
| Wartbarkeit | Linting, strikte Typprüfung und Tests laufen bei jedem Push; Fachlogik im Backend ist durch Tests abgedeckt, insbesondere Tageswechsel, Lebenszyklus und Pool-Ziehung. |
| Portabilität | Nur Standard-Bausteine (Container, PostgreSQL, S3-kompatibler Speicher); kein anbieterspezifischer Dienst in v1. |
| Kosten | Laufender Betrieb unter 10 € pro Monat. |
| Datenschutz | Solange nur eine Person die App nutzt, keine besonderen Anforderungen. Vor dem Einladen weiterer Personen: Impressum, Datenschutzerklärung, Konto- und Datenlöschung. |

---

## 7. Tech Stack

### Backend

| Baustein | Wahl | Anmerkung |
|---|---|---|
| Sprache | Python 3.13 (oder aktuelle stabile Version) | |
| Framework | FastAPI | OpenAPI-Beschreibung wird automatisch erzeugt |
| Server | Uvicorn | |
| Modelle, Validierung | Pydantic v2 | Discriminated Unions für Seite, Wiederholung, Verbindlichkeit |
| Datenbankzugriff | SQLAlchemy 2.0 (async) | Core für SQL-nahe Auswertungen, ORM wo praktisch |
| Treiber | asyncpg oder psycopg 3 | async-fähig |
| Migrationen | Alembic | |
| Paketverwaltung | uv | |
| Codequalität | Ruff (Linting, Formatierung), Pyright im strikten Modus | |
| Logging | structlog, JSON-Ausgabe | |
| Passwörter | argon2-cffi | |
| Tests | pytest, pytest-asyncio, Testcontainers (PostgreSQL) | |
| Geplante Jobs | – in v1 | später Procrastinate (Job-Queue in PostgreSQL) |

### Frontend (umgesetzt durch Claude Code)

| Baustein | Wahl |
|---|---|
| Sprache | TypeScript |
| Framework | React als Single-Page-App |
| Build | Vite |
| PWA | vite-plugin-pwa (Manifest, Service Worker) |
| Datenabruf | TanStack Query |
| API-Typen | openapi-typescript (generiert aus der OpenAPI-Beschreibung), dazu openapi-fetch |
| Übersetzung | react-i18next |
| Styling, Animationen | nach Wahl von Claude Code, passend zur RPG-Atmosphäre |

### Datenbank

PostgreSQL (aktuelle stabile Hauptversion).

### Infrastruktur und Betrieb

| Baustein | Wahl |
|---|---|
| Hosting (Phase 1) | Virtueller Server (VPS) bei einem günstigen Anbieter mit Rechenzentrum in Deutschland, z. B. Hetzner |
| Betriebssystem | Ubuntu LTS oder Debian |
| Container | Docker, Docker Compose |
| Reverse Proxy, HTTPS | Caddy (automatische Zertifikate); optional vorher einmal Nginx mit manuellem Zertifikat zum Lernen |
| Code und CI/CD | GitHub, GitHub Actions |
| Container-Registry | GitHub Container Registry |
| Backups | Verschlüsselte `pg_dump`-Sicherungen auf S3-kompatiblen Speicher bei einem anderen Anbieter oder in einer anderen Region |
| Überwachung | Externer Uptime-Check; Logs über Docker |
| Später | Terraform (oder OpenTofu), Monitoring mit Metriken und zentralem Logging, Staging, Cloud-Anbieter |

---

## 8. Architektur

### 8.1 Überblick

```
Browser (PWA)
   │  HTTPS, eine Domain
   ▼
Caddy ── /        → statische Frontend-Dateien
      └─ /api/*   → FastAPI-Container ── PostgreSQL-Container (Volume)
                                    └── Backups → externer S3-Speicher
```

Frontend und API laufen unter **derselben Domain** (Frontend unter `/`, API unter `/api`). Dadurch entfällt CORS, und Sitzungs-Cookies funktionieren ohne Sonderkonfiguration.

### 8.2 Verteilung der Logik

- **Backend:** gesamte Fachlogik – Tageswechsel, Pool-Ziehung, Lebenszyklus, Eskalation, Balance, Punkte, Level, Erfolge, Validierung, Berechtigungen. Das Backend ist die einzige Quelle der Wahrheit.
- **Frontend:** Darstellung, Anlege-Dialog, Animationen, Oberflächenzustand, Übersetzung. Keine Fachregeln. Später bei Offline-Unterstützung höchstens vorläufige Anzeigen, die der Server bestätigt oder korrigiert.

### 8.3 API-Design

- **Anzeigefertige Lese-Endpunkte**, z. B.:
  - `GET /api/board` – feste Seite, Pool-Seite, Balance-Zone
  - `GET /api/logbook` – offene und heute erledigte Quests
  - `GET /api/quests` – Pool bzw. alle eigenen Quests
  - `GET /api/hero` – Level, Titel, Balance
  - `GET /api/chronicle?from=…&to=…`
- **Aktions-Endpunkte statt freiem Datenbearbeiten**, z. B.:
  - `POST /api/quests`, `PATCH /api/quests/{id}`, `DELETE /api/quests/{id}`
  - `POST /api/instances/{id}/accept | complete | return | reopen`
  - `POST /api/quests/{id}/accept` (direkt aus dem Pool)
  - `POST /api/log-afterwards` (nachtragen)
- Das Backend prüft bei jeder Aktion die Regeln. Fehler werden als Codes zurückgegeben (z. B. `quest.cannot_return_main`), das Frontend übersetzt.
- Der Aufbau nach Aktionen erleichtert später Offline-Unterstützung: Aktionen können gesammelt und nachgeschickt werden.
- Die OpenAPI-Beschreibung ist der Vertrag zwischen Backend und Frontend. Die Frontend-Typen werden daraus generiert, nie von Hand geschrieben. Die CI prüft, dass die generierten Typen aktuell sind.

### 8.4 Anmeldung

- Selbst gebaut: Benutzername und Passwort, Hash mit Argon2.
- **Serverseitige Sitzungen** in einer Tabelle `sessions` (zufällige ID, `user_id`, Ablaufzeit, zuletzt benutzt, Gerätebeschreibung). Der Browser erhält nur die zufällige Sitzungs-ID als Cookie.
- Cookie-Attribute: `HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`, begrenzte Lebensdauer mit Verlängerung bei Nutzung.
- Sitzungen sind jederzeit widerrufbar (Abmelden, von allen Geräten abmelden).
- Schutz vor Cross-Site-Anfragen: `SameSite=Lax` plus Prüfung des `Origin`-Headers bei ändernden Anfragen.
- Begrenzung der Login-Versuche pro Benutzername und IP.
- Registrierung geschlossen; Konten und Passwort-Reset per CLI-Befehl.

### 8.5 Tageswechsel

- Alle Zeitpunkte in UTC; logischer Tag aus Zeitzone und Tagesbeginn des Nutzers.
- Eine idempotente, nachholfähige Funktion `rollover(user_id, now)`, aufgerufen von einer Abhängigkeit (Dependency) vor jeder API-Anfrage, wenn `last_rollover_day < logischer_tag`.
- Absicherung gegen parallele Ausführung durch eine Sperre pro Nutzer in PostgreSQL (`pg_advisory_xact_lock` oder `SELECT … FOR UPDATE`), danach erneute Prüfung.
- Später ruft zusätzlich ein geplanter Job dieselbe Funktion auf.

### 8.6 Konfiguration

- Alle Einstellungen über Umgebungsvariablen, eingelesen mit pydantic-settings.
- Balance- und Pool-Konstanten in einer eigenen Konfigurationsgruppe mit Defaults im Code, überschreibbar per Umgebungsvariable. So können sie in der Testphase ohne Codeänderung angepasst werden.

### 8.7 Übersetzung

- Frontend: alle Texte über react-i18next-Schlüssel, Deutsch als einzige Sprache in v1.
- Backend: liefert nur Codes mit Parametern, keine Sätze.
- Inhalte (Startpaket, Onboarding) liegen pro Sprache in eigenen Dateien.

---

## 9. Repository-Struktur

Monorepo auf GitHub:

```
quest-board/
├── backend/              FastAPI-App, Tests, Alembic-Migrationen, CLI
├── frontend/             React-App (Claude Code)
├── infra/                Docker Compose, Caddy-Konfiguration, Deploy- und Backup-Skripte,
│                         später Terraform
├── docs/
│   ├── quest-board-prd.md
│   ├── quest-board-konzept.md
│   ├── lernleitfaden.md
│   ├── arbeitsweise.md
│   ├── lessons-learned.md
│   └── adr/              Entscheidungsprotokolle (Architecture Decision Records)
├── .github/workflows/    CI/CD, nach Pfaden getrennt
└── CLAUDE.md             Arbeitsanweisungen für Claude Code
```

Die `CLAUDE.md` enthält mindestens:
- Verweise auf PRD, Konzept und Lernleitfaden.
- Frontend: keine Fachlogik; alle Texte über Übersetzungsschlüssel; API-Typen nur generiert.
- Rollen: Claude als Senior Developer, der Mensch als Junior Developer und Product Owner (Details in `docs/arbeitsweise.md` und im Lernleitfaden).

---

## 10. Betrieb und Deployment

### Phase 1: VPS (bis zur Nutzbarkeit und darüber hinaus)

- Docker Compose mit den Diensten `caddy`, `api`, `db`.
- Restart-Policies, damit alle Dienste nach einem Neustart des Servers von selbst starten.
- **CI** (bei jedem Push und Pull Request): Ruff, Pyright, pytest mit Testcontainers; Frontend-Linting, Typprüfung und Build; Prüfung, dass die generierten API-Typen aktuell sind.
- **CD** (bei Push auf `main`): Images bauen und in die GitHub Container Registry schieben, per SSH auf dem Server die neuen Images ziehen, Alembic-Migrationen ausführen, Dienste neu starten.
- **Secrets:** in GitHub als verschlüsselte Secrets; auf dem Server in einer Umgebungsdatei mit eingeschränkten Rechten.
- **Server-Absicherung:** nur SSH-Schlüssel, kein Root-Login, Firewall (nur 22, 80, 443), automatische Sicherheitsupdates.
- **Backups:** täglicher verschlüsselter `pg_dump` an einen externen Ort mit Aufbewahrungsregel; dokumentierte und getestete Wiederherstellung.
- **Überwachung:** externer Uptime-Check auf einen Health-Endpunkt (`GET /api/health`), der auch die Datenbankverbindung prüft.
- **Umgebungen:** lokal und Produktion.

### Phase 2: nach der Nutzbarkeit, ohne Zeitdruck

- Infrastructure as Code für Server, Firewall und DNS.
- Metriken, Dashboards, Alarme, zentrales Logging.
- Staging-Umgebung.
- Nachbau der Infrastruktur bei einem großen Cloud-Anbieter per Infrastructure as Code, zunächst zeitweise (hochfahren, üben, abreißen), mit Budget-Alarmen. Eventueller Umzug inklusive Datenbank-Wiederherstellung und DNS-Umstellung.

---

## 11. Meilensteine

| Meilenstein | Inhalt | Ergebnis |
|---|---|---|
| **M0 Fundament** | Repository, Projektstruktur, lokale Entwicklung mit Docker Compose (PostgreSQL), CI mit Linting, Typprüfung und Tests | Leeres Projekt, das automatisch geprüft wird |
| **M0.5 Durchstich** | Minimale API (`/api/health`) und minimales Frontend einmal komplett online: Server, Domain, HTTPS, manuelles Deployment, dann Skript, dann CD | Jede Änderung geht automatisch online |
| **M1 Kern-Backend** | Datenmodell, Migrationen, Quests anlegen, bearbeiten, löschen; Aktionen; Tageswechsel mit Sperre; Pool-Ziehung; Tests | Fachlogik funktioniert und ist getestet |
| **M2 Frontend** | Board, Logbuch, Dialog und Schnellanlage, Übersetzungsstruktur, PWA-Grundlagen | App ist bedienbar |
| **M3 Benutzbar** | Anmeldung, Profil mit Zeitzone, Backups mit getesteter Wiederherstellung, Uptime-Check | Tägliche Nutzung im Alltag |
| *ab hier ohne Zeitdruck* | | |
| **M4 Balance und Belohnungen** | Balance und Waage, Pool-Aufteilung nach Balance, Level mit Harmonie-Bonus, Chronik, Abhak-Moment, ggf. Titel | Das Spielgefühl ist da |
| **M5 Onboarding** | Startpaket, Onboarding-Quests | Einstieg ohne Erklärung möglich |
| **M6 Stabilisierung** | Konstanten einstellen, DevOps Phase 2 beginnen | Erfolgskriterien erreicht |

**Zeitliche Einschätzung** bei etwa 6–10 Stunden pro Woche: M3 nach etwa 3–4 Monaten, v1 komplett nach etwa 5–7 Monaten. M0.5 und M3 enthalten die größte Unsicherheit, weil viele DevOps-Themen zum ersten Mal auftreten.

---

## 12. Erfolgskriterien

**Produkt:**
1. Die App wird vier Wochen lang an mindestens fünf von sieben Tagen genutzt.
2. Sie ersetzt die bisherige Todo-Lösung; es gibt keine parallele Liste mehr.
3. Fun-Quests werden tatsächlich gemacht, im Schnitt mindestens drei pro Woche.
4. Die Pool-Vorschläge fühlen sich meistens passend an (wöchentliche kurze Selbsteinschätzung).
5. Die Balance-Konstanten bleiben nach der Testphase zwei Wochen lang unverändert, weil sie stimmig sind.

**Technik:**
6. Jedes Deployment läuft automatisiert.
7. Eine Wiederherstellung aus dem Backup wurde mindestens einmal erfolgreich durchgeführt.
8. Keine Datenverluste im gesamten Testzeitraum.

---

## 13. Risiken

| Risiko | Gegenmaßnahme |
|---|---|
| DevOps-Probleme überlagern sich und kosten viel Zeit | Durchstich (M0.5) früh und isoliert; immer nur ein neues Thema gleichzeitig |
| Motivation sinkt vor der Nutzbarkeit | M3 bewusst schlank; Belohnungen erst danach |
| Datenverlust bei echter Nutzung | Backups und Wiederherstellungstest sind Teil von M3 |
| Fachlogik wird komplex und fehleranfällig (Tageswechsel, Bearbeitungsregeln) | Reine Funktionen mit "jetzt" als Parameter, umfangreiche Tests mit simulierten Tagen |
| Balance fühlt sich falsch an | Alle Konstanten konfigurierbar; bewusste Testphase |
| Frontend enthält unbemerkt Fachlogik | Regel in `CLAUDE.md`, anzeigefertige API-Endpunkte |
| Laufende Kosten steigen, besonders in der Cloud-Phase | VPS für Produktion, Cloud nur zeitweise per Infrastructure as Code, Budget-Alarme |

---

## 14. Offene Punkte

- Konkreter VPS-Anbieter, Domain und Backup-Ziel (Entscheidung bei M0.5)
- Anzahl der Pool-Slots und Konstanten (Testphase)
- Levelkurve und Höhe des Harmonie-Bonus
- Visuelle Sprache und Herkunft von Illustrationen, Icons und Geräuschen (Lizenzen beachten)
- Inhalt des Startpakets
