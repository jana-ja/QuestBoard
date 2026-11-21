# ADR-0001: Monorepo für Backend, Frontend und Infrastruktur

Datum: 2026-11-21 · Status: angenommen

## Kontext

Quest Board besteht aus einem FastAPI-Backend, einem React-Frontend und der Infrastruktur
(Docker Compose, Caddy, später Deploy-Skripte). Es gibt eine Person im Team und einen
KI-Senior. Frontend und API laufen unter einer Domain; die OpenAPI-Beschreibung des
Backends ist der Vertrag, aus dem die Frontend-Typen generiert werden. Änderungen an der
API und am Frontend gehören deshalb oft zusammen.

## Entscheidung

Ein Repository mit getrennten Teilprojekten: `backend/`, `frontend/`, `infra/`, `docs/`.
Jedes Teilprojekt hat seine eigene Toolchain im eigenen Ordner (uv mit `pyproject.toml`,
npm mit `package.json`, Compose mit `compose.yaml`) und seine eigene README. Es gibt kein
gemeinsames Build-Werkzeug über alle Teile. Die CI hat einen Workflow pro Teilprojekt.

## Alternativen

- **Getrennte Repositories pro Teil:** Eine API-Änderung und die passende Frontend-Änderung
  bräuchten zwei PRs, die zusammen gemergt werden müssen; die generierten Typen müssten
  zwischen Repos übertragen werden. Für ein Ein-Personen-Projekt nur Mehraufwand.
- **Monorepo-Werkzeug (z. B. Nx, Turborepo) oder uv-Workspace:** Lohnt sich bei vielen
  Paketen einer Sprache mit gegenseitigen Abhängigkeiten. Wir haben je genau ein Python-
  und ein Node-Projekt – ein zusätzliches Werkzeug wäre mehr Komplexität als Nutzen.
- **Ein gemeinsames Projekt im Root** (eine `pyproject.toml` für alles): Vermischt
  Toolchains; Werkzeuge suchen ihre Konfiguration im falschen Ordner.

## Konsequenzen

- Einfacher: Eine Änderung über API und Frontend ist ein PR; Doku, Tickets und Code
  liegen an einem Ort; eine gemeinsame Historie.
- Schwieriger: Die CI muss wissen, was sich geändert hat. Jeder Workflow braucht einen
  Pfadfilter – und zwar auf Job-Ebene, weil Pflicht-Checks sonst bei PRs ohne passende
  Änderung nie ein Ergebnis melden (siehe Lessons Learned, 23.10.2026). Job-Namen
  müssen über alle Workflows eindeutig sein.
- Schwieriger: Befehle laufen im jeweiligen Ordner (`working-directory` in der CI,
  `cd backend` lokal); Werkzeuge im Editor müssen den richtigen Unterordner finden.
- Neu prüfen, wenn: ein zweites Python- oder Node-Paket dazukommt, das von einem
  bestehenden abhängt – dann ist ein Workspace eine Überlegung wert.
