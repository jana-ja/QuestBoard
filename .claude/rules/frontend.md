---
paths:
  - "frontend/**"
---

# Frontend-Regeln

Hier implementierst du selbst (auf eigenem Branch, mit PR, Review durch den Junior).

## Stack
TypeScript, React (SPA), Vite, vite-plugin-pwa, TanStack Query, openapi-typescript +
openapi-fetch, react-i18next.

## Regeln
- Keine Fachlogik. Was angezeigt wird und welche Aktionen erlaubt sind, liefert das Backend.
  Vorläufige Anzeigen (optimistic updates) nur, wenn der Server sie danach bestätigt.
- API-Typen nur aus der generierten Datei; nie eigene Typen für API-Antworten schreiben.
  Fehlt etwas in der API, ist das ein Ticket fürs Backend – nicht im Frontend nachbauen.
- Alle sichtbaren Texte über i18n-Schlüssel (Deutsch in v1). Fehler- und Statuscodes vom
  Backend werden im Frontend übersetzt. Datum und Zahlen über `Intl`.
- Atmosphäre: Mittelalter-RPG, verspielt, aber lesbar. Abhak-Moment mit Animation und
  Geräusch. Gestaltungsrichtung und Texte sind Produktfragen → [PO] fragen.
- Mobile first (ab 360 px), PWA installierbar.
- Fremde Grafiken, Icons, Schriften, Geräusche nur mit passender Lizenz; Quelle im PR nennen.
