# Quest Board – Lernleitfaden

Stand: 01.10.2026

Dieses Dokument begleitet das Projekt über die gesamte Laufzeit. Es beschreibt, **wie** gelernt wird, Die Zusammenarbeit mit Claude Code im Team-Prozess ist in `docs/arbeitsweise.md` beschrieben, die technische Umsetzung in `CLAUDE.md`, `.claude/output-styles/senior-mentor.md` und `.claude/rules/`.

---

## 1. Ausgangslage und Ziel

- **Hintergrund:** App-Entwicklung, gute Kenntnisse in Kotlin, etwas Python-Erfahrung.
- **Lernziele:** Backend mit FastAPI und PostgreSQL; die komplette Betriebskette selbst beherrschen (Container, Server, Domain, HTTPS, CI/CD, Secrets, Backups); danach Infrastructure as Code, Monitoring und Cloud.
- **Bewusst kein Lernziel:** Frontend. Das schreibt Claude Code als Senior Developer.
- **Zusätzliches Lernziel:** Arbeiten wie in einem echten Team – Tickets, Branches, Pull Requests, Code Reviews, Sprints.
- **Zeitmodell:** Bis zur benutzbaren App (M3) gründlich und zügig lernen. Danach ohne Zeitdruck weiterbauen und vertiefen.

---

## 2. Lernprinzipien

### Erst manuell, dann automatisieren
Jeder Betriebsschritt wird zuerst von Hand ausgeführt, dann in ein Skript gegossen, erst dann in eine Pipeline übernommen. So ist klar, was die Automatisierung eigentlich tut – und man kann sie reparieren, wenn sie bricht.

### Immer nur ein neues Thema gleichzeitig
Wenn etwas nicht funktioniert, soll klar sein, wo man suchen muss. Deshalb gibt es den frühen Durchstich (M0.5): Die DevOps-Grundlagen werden mit einer leeren App gelernt, bevor Anmeldung, Datenbankmigrationen und Fachlogik dazukommen.

### Die App bleibt nach jeder Stufe funktionsfähig
Jede Stufe endet mit einem lauffähigen Zustand. Keine Baustellen, die über Wochen offen bleiben.

### Absichtlich kaputt machen
Nach jeder Stufe wird gezielt etwas zerstört und wieder repariert. Was man einmal geübt hat, versetzt einen im Ernstfall nicht in Panik. Konkrete Übungen stehen in Abschnitt 4.

### Entscheidungen kurz festhalten
Jede wichtige Entscheidung bekommt ein kurzes Entscheidungsprotokoll (Architecture Decision Record) in `docs/adr/`: Was wurde entschieden, warum, welche Alternativen gab es. Das zwingt dazu, die eigenen Gründe zu formulieren, und wird Teil der Projektdokumentation.

Vorlage:

```markdown
# ADR-0001: Titel

Datum: JJJJ-MM-TT · Status: angenommen

## Kontext
Welches Problem, welche Rahmenbedingungen?

## Entscheidung
Was wird gemacht?

## Alternativen
Was wurde verworfen und warum?

## Konsequenzen
Was wird dadurch einfacher, was schwieriger?
```

Erste Kandidaten: FastAPI als Backend, Monorepo, Sitzungen statt JWT, Tageswechsel "faul" statt als Job, VPS vor Cloud, Caddy als Reverse Proxy.

### Eigene Notizen zu Stolpersteinen
Wenn etwas mehr als eine halbe Stunde gekostet hat: Ursache und Lösung in zwei, drei Sätzen notieren (z. B. `docs/lessons-learned.md`). Das ist später Gold wert.

---

## 3. Arbeitsweise mit Claude

Claude Code arbeitet als **Senior Developer und Tech Lead**, der Mensch als **Junior Developer und Product Owner**. Der Prozess (Sprints, Tickets, Pull Requests, Reviews) ist in `docs/arbeitsweise.md` beschrieben.

### Frontend: der Senior liefert
Claude Code setzt das Frontend selbst um, auf eigenen Branches mit PR. Der Junior reviewt leichtgewichtig. Regeln: keine Fachlogik, alle Texte über Übersetzungsschlüssel, API-Typen nur generiert.

### Backend: der Junior baut, der Senior führt
- Der Senior schreibt Tickets mit Vorgaben und Akzeptanzkriterien und entscheidet technische Fragen mit kurzer Begründung.
- Der Junior implementiert die Kernlogik (Datenmodell, Tageswechsel, Lebenszyklus, Pool-Ziehung, Balance) selbst.
- Gerüste oder ein Beispiel als Muster darf der Senior als ausdrückliche "Vorgabe" liefern; Routine ohne Lerneffekt übernimmt er auf Nachfrage.
- Hilfe erfolgt gestuft: Rückfrage → Hinweis → Konzept → Fragment → Lösung (nur auf Wunsch).

### DevOps: der Senior ist Lehrer
- Erst manuell, dann Skript, dann Pipeline – der Junior führt alle Schritte selbst aus.
- Der Senior erklärt das Warum und Alternativen, zeigt höchstens einzelne Bausteine, reviewt und führt selbst keine Befehle gegen Server oder Cloud aus.
- Fehler werden gemeinsam über Hypothesen eingegrenzt; das ist selbst Lernziel.
- Sicherheitsrisiken werden immer angesprochen, auch ungefragt.
- Nach jeder Stufe schlägt der Senior eine Kaputt-mach-Übung vor; sie wird als `learning`-Ticket in den Sprint aufgenommen.

---

## 4. Lernpfad

### M0 – Fundament
**Lernen:** Projektstruktur in Python mit uv, Ruff und Pyright; Docker und Docker Compose lokal; erste GitHub-Actions-Pipeline.
**Kaputt machen:**
- Einen Typfehler einbauen und prüfen, dass die CI ihn findet.
- Den Datenbank-Container löschen und wieder hochfahren: Was ist mit den Daten passiert? (Stichwort Volumes.)

### M0.5 – Durchstich
Reihenfolge:
1. Minimale FastAPI mit `/api/health`, minimales Frontend, je ein Dockerfile, Docker Compose mit Caddy. Lokal alles unter einer Adresse.
2. VPS von Hand einrichten: SSH-Schlüssel, eigener Nutzer, kein Root-Login, Firewall, automatische Sicherheitsupdates, Docker.
3. Domain kaufen, DNS-Eintrag auf den Server setzen.
4. Manuell deployen, HTTPS über Caddy (optional vorher einmal Nginx mit manuell geholtem Zertifikat, um zu verstehen, was Caddy automatisiert).
5. Deploy-Skript schreiben.
6. CI: Linting, Typen, Tests.
7. CD: Images bauen, in die GitHub Container Registry schieben, per SSH deployen.

**Lernen:** Linux-Grundlagen, SSH, Firewall, DNS, TLS-Zertifikate, Reverse Proxy, Container-Registry, Secrets in GitHub.
**Kaputt machen:**
- Server neu starten: Kommt alles von selbst wieder hoch? (Restart-Policies.)
- API-Container stoppen: Was sieht man im Browser, was im Uptime-Check?
- Eine absichtlich fehlerhafte Version deployen und zurückrollen.
- Ein Secret absichtlich falsch setzen und die Fehlermeldung finden.

### M1 – Kern-Backend
**Lernen:** SQLAlchemy 2.0, Alembic-Migrationen, Pydantic Discriminated Unions, Tests mit Testcontainers, Transaktionen und Sperren in PostgreSQL.
**Kaputt machen:**
- Den Tageswechsel zweimal parallel auslösen (Test mit zwei gleichzeitigen Anfragen) und prüfen, dass die Sperre greift. Dann die Sperre entfernen und beobachten, was ohne sie passiert.
- Eine Migration schreiben, die fehlschlägt, und prüfen, was mit der Datenbank passiert (Transaktionen bei Migrationen).
- Tageswechsel über zwei Wochen Abwesenheit simulieren.

### M2 – Frontend
**Lernen:** Kaum eigenes Lernen, Fokus auf Zusammenspiel: OpenAPI als Vertrag, generierte Typen, PWA-Installation auf dem eigenen Handy.

### M3 – Benutzbar
**Lernen:** Sitzungen und Cookies (siehe Abschnitt 5.1), Passwort-Hashing, Backups mit `pg_dump`, Verschlüsselung, externer Speicher, Wiederherstellung.
**Kaputt machen:**
- **Pflicht:** Die Datenbank auf einer Testinstanz (oder lokal) komplett löschen und aus dem echten Backup wiederherstellen. Zeit messen und Schritte in einem Wiederherstellungs-Dokument festhalten.
- Das Sitzungs-Cookie im Browser manipulieren oder löschen und das Verhalten beobachten.
- Mit falschem Passwort mehrfach anmelden und die Begrenzung der Versuche prüfen.

### Ab M4 – ohne Zeitdruck
Mögliche Reihenfolge, jeweils mit eigenem Kaputt-mach-Teil:
1. **Infrastructure as Code** (Terraform oder OpenTofu): den bestehenden Server samt Firewall und DNS als Code beschreiben. Übung: Server per Code abreißen und neu aufbauen, dann Daten aus dem Backup zurückspielen.
2. **Monitoring:** Metriken (z. B. Prometheus und Grafana, oder ein schlanker Dienst), Alarme, zentrales Logging. Übung: Einen Alarm absichtlich auslösen.
3. **Staging-Umgebung** mit eigener Datenbank und automatischem Deployment vor Produktion.
4. **Cloud:** Infrastruktur bei einem großen Anbieter per Code nachbauen, mit Budget-Alarmen; nur zeitweise laufen lassen. Später eventuell Umzug ohne Ausfall (DNS, Datenbank).
5. **Optional:** Container-Orchestrierung (z. B. Kubernetes) als reines Lernexperiment.

---

## 5. Wissensbausteine

### 5.1 Wie Cookies und Sitzungen funktionieren

**Ein Cookie** ist ein kleiner Wert, den der Server dem Browser mit einer Antwort schickt und den der Browser danach **automatisch** bei jeder passenden Anfrage wieder mitsendet.

```
Antwort des Servers nach erfolgreichem Login:
  Set-Cookie: session=Xf3k…9a; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=2592000

Jede folgende Anfrage des Browsers an dieselbe Domain:
  Cookie: session=Xf3k…9a
```

**Der Ablauf bei serverseitigen Sitzungen:**
1. Login: Der Server prüft das Passwort gegen den Argon2-Hash.
2. Der Server erzeugt eine lange Zufalls-ID (z. B. mit `secrets.token_urlsafe(32)`) und speichert in der Tabelle `sessions` eine Zeile: Hash der ID, `user_id`, Ablaufzeit.
3. Der Server schickt die ID als Cookie zurück.
4. Bei jeder Anfrage liest das Backend das Cookie, sucht die Sitzung, prüft die Ablaufzeit und weiß damit, welcher Nutzer anfragt.
5. Abmelden = Zeile löschen. "Von allen Geräten abmelden" = alle Zeilen des Nutzers löschen.

Das Cookie selbst enthält also **keine Informationen**, nur einen zufälligen Schlüssel. Die Wahrheit liegt in der Datenbank. In der Datenbank wird nur ein Hash der ID gespeichert, damit ein Datenbank-Leak keine gültigen Sitzungen preisgibt.

**Die Attribute:**

| Attribut | Bedeutung | Schützt vor |
|---|---|---|
| `HttpOnly` | JavaScript kann das Cookie nicht lesen | Diebstahl der Sitzung über eingeschleustes Script (XSS) |
| `Secure` | Wird nur über HTTPS gesendet | Mitlesen im Netzwerk |
| `SameSite=Lax` | Wird bei Anfragen, die von fremden Seiten ausgelöst werden, nur bei einfacher Navigation mitgesendet, nicht bei z. B. Formular-POSTs | Cross-Site Request Forgery (CSRF) |
| `Path=/` | Gilt für die ganze Domain | – |
| `Max-Age` / `Expires` | Lebensdauer; ohne Angabe endet das Cookie mit dem Browser | – |
| `Domain` | Weglassen = nur exakt diese Domain | Versehentliches Teilen mit Subdomains |

**Warum eine Domain für Frontend und API so viel vereinfacht:** Der Browser sendet Cookies nur an die Domain, die sie gesetzt hat. Liegt die API auf einer anderen (Sub-)Domain, braucht man CORS mit `credentials`, passende `SameSite`-Einstellungen und muss jede Frontend-Anfrage explizit mit Cookies konfigurieren. Unter einer Domain funktioniert es einfach.

**Sitzung vs. JWT:** Ein JWT ist ein signiertes Token, das die Nutzerdaten selbst enthält. Der Server muss nichts nachschlagen – kann es aber auch nicht vor Ablauf widerrufen. Für eine App mit einem Backend und einer Datenbank sind Sitzungen einfacher und sicherer.

**Zum Selbstausprobieren:** In den Entwicklertools des Browsers unter "Anwendung/Speicher → Cookies" das Sitzungs-Cookie ansehen, `document.cookie` in der Konsole ausführen (es taucht wegen `HttpOnly` nicht auf), das Cookie löschen und die Seite neu laden.

### 5.2 Sperren in PostgreSQL für den Tageswechsel

**Das Problem:** Handy und Laptop schicken fast gleichzeitig die erste Anfrage des Tages. Beide sehen `last_rollover_day = gestern` und starten den Tageswechsel. Ergebnis: doppelte Instanzen, doppelte Pool-Ziehung.

Das ist eine klassische **Race Condition**: Zwischen "prüfen" und "handeln" kann ein anderer dazwischenkommen.

**Lösung 1: Zeilensperre mit `SELECT … FOR UPDATE`**

```sql
BEGIN;
SELECT last_rollover_day FROM users WHERE id = :user_id FOR UPDATE;
-- Die Zeile ist jetzt für andere FOR-UPDATE-Abfragen gesperrt.
-- Eine zweite Transaktion wartet an genau dieser Stelle.
-- Hier erneut prüfen: Ist last_rollover_day noch < heute?
--   ja   → Tageswechsel ausführen, last_rollover_day = heute setzen
--   nein → nichts tun (die andere Transaktion war schneller)
COMMIT;  -- gibt die Sperre frei
```

**Lösung 2: Advisory Lock**

Ein Advisory Lock ist eine Sperre auf eine frei gewählte Zahl, nicht auf eine Tabellenzeile. Die Anwendung entscheidet, was die Zahl bedeutet.

```sql
BEGIN;
SELECT pg_advisory_xact_lock(hashtextextended('rollover:' || :user_id, 0));
-- erneut prüfen, ggf. Tageswechsel ausführen
COMMIT;  -- "xact" = die Sperre endet automatisch mit der Transaktion
```

**In SQLAlchemy (Skizze):**

```python
async def ensure_rollover(session: AsyncSession, user: User, now: datetime) -> None:
    today = logical_day(user, now)              # aus Zeitzone und Tagesbeginn
    if user.last_rollover_day >= today:         # schneller Weg ohne Sperre
        return
    user_id = user.id
    async with session.begin():                 # Skizze: Transaktionsgrenze je nach App-Aufbau
        row = await session.execute(
            select(User.last_rollover_day)
            .where(User.id == user_id)
            .with_for_update()                  # erzeugt SELECT … FOR UPDATE
        )
        if row.scalar_one() >= today:           # erneut prüfen nach der Sperre
            return
        await rollover(session, user_id, now)   # idempotent und nachholfähig
        await session.execute(
            update(User).where(User.id == user_id).values(last_rollover_day=today)
        )
```

Das Muster heißt **"prüfen – sperren – erneut prüfen"** (Double-Checked Locking): Die erste Prüfung ohne Sperre macht den Normalfall schnell, die zweite nach der Sperre macht ihn korrekt.

**Wann welche Variante?**
- `FOR UPDATE` ist naheliegend, wenn es ohnehin eine passende Zeile gibt (hier die Nutzerzeile) – leicht verständlich, gut für den Einstieg.
- Advisory Locks eignen sich, wenn es keine natürliche Zeile gibt oder man keine Zeile blockieren möchte, die andere Anfragen gleichzeitig lesen oder ändern wollen.

**Zusätzliche Absicherung:** Der partielle Unique-Index "höchstens eine offene Instanz pro Quest" ist ein zweites Netz. Selbst wenn die Sperre einmal versagt, lehnt die Datenbank doppelte Instanzen ab.

**Zum Selbstausprobieren:** Zwei `psql`-Sitzungen öffnen, in beiden `BEGIN;` und dann nacheinander dieselbe `SELECT … FOR UPDATE`-Abfrage ausführen. Die zweite hängt, bis in der ersten `COMMIT;` ausgeführt wird. Danach als Test in pytest zwei gleichzeitige Anfragen mit `asyncio.gather` abschicken.

---

## 6. Checkliste "Bin ich bereit für den Alltag?" (vor M3)

- [ ] Ein Merge nach `main` bringt die neue Version ohne manuellen Schritt online.
- [ ] Nach einem Neustart des Servers läuft alles von selbst wieder.
- [ ] Ich weiß, wo ich die Logs der API finde und wie ich sie lese.
- [ ] Es gibt ein tägliches, verschlüsseltes Backup an einem externen Ort.
- [ ] Ich habe eine Wiederherstellung durchgeführt und die Schritte aufgeschrieben.
- [ ] Ein externer Check meldet mir, wenn die App nicht erreichbar ist.
- [ ] Keine Secrets im Repository, und ich weiß, wie ich ein Secret austausche.
- [ ] Die Firewall lässt nur 22, 80 und 443 durch; SSH geht nur mit Schlüssel.
