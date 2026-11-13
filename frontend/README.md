# Quest Board – Frontend

Single Page App mit React, TypeScript und Vite. Überblick über das Gesamtprojekt:
[README im Root](../README.md).

## Voraussetzungen

- Node.js in der Hauptversion aus `.nvmrc` (aktuell 24) mit npm

Alle Befehle werden im Ordner `frontend/` ausgeführt.

## Einrichten

```bash
npm ci
```

Installiert die Abhängigkeiten exakt so, wie sie in `package-lock.json` festgehalten sind.

## Starten

```bash
npm run dev
```

Startet den Vite-Dev-Server mit Hot Reload unter `http://localhost:5173`.

## Prüfen

| Befehl | Zweck |
|---|---|
| `npm run lint` | Linting mit oxlint, inklusive Regeln mit Typinformation; Warnungen zählen als Fehler |
| `npm run typecheck` | Typprüfung mit TypeScript (strikter Modus) |
| `npm run build` | Typprüfung und Produktions-Build nach `dist/` |
| `npm run preview` | Den Build aus `dist/` lokal ansehen |

## Struktur

```
src/                 Anwendungscode
index.html           Einstiegsseite
vite.config.ts       Vite-Konfiguration
tsconfig*.json       TypeScript: App-Code und Konfigurationsdateien getrennt
.oxlintrc.json       Lint-Regeln
.nvmrc               Node-Hauptversion (lokal und in der CI)
package-lock.json    Exakt aufgelöste Versionen – wird eingecheckt
```
