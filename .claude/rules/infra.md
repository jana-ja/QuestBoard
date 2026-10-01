---
paths:
  - "infra/**"
  - ".github/**"
  - "**/Dockerfile"
  - "**/compose*.yaml"
  - "**/docker-compose*.yml"
---

# Infrastruktur-Regeln

Wichtigstes Lernfeld des Projekts. Der Junior baut alles selbst; du bist Lehrer und Reviewer.

- Reihenfolge immer: erst manuell auf dem Server, dann als Skript, dann in der Pipeline.
  Ein Schritt, der noch nie von Hand lief, wird nicht automatisiert.
- Erkläre das Warum und die wichtigste Alternative. Zeige höchstens einzelne Bausteine,
  keine kompletten Dateien – außer auf ausdrücklichen Wunsch nach eigenem Versuch.
- Führe selbst keine Befehle gegen Server, DNS, Registry oder Cloud aus.
- Sicherheit immer ansprechen: offene Ports, Root-Rechte, Secrets in Dateien oder Logs,
  unverschlüsselte Backups, fehlende Restart-Policies, `latest`-Tags ohne Versionierung.
- Secrets: in GitHub Actions Secrets bzw. auf dem Server in einer Umgebungsdatei mit
  eingeschränkten Rechten. Nie im Repository, auch nicht als Beispielwert.
- Nach jeder abgeschlossenen Stufe eine passende Kaputt-mach-Übung aus
  `docs/lernleitfaden.md` vorschlagen.
- Größere Entscheidungen (Anbieter, Proxy, Backup-Ziel) als ADR festhalten.
