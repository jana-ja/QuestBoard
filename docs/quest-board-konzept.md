# Quest Board – Fachkonzept

Stand: 29.09.2026

Quest Board ist eine Todo-App mit Gamification im Mittelalter-RPG-Stil. Neben verpflichtenden Aufgaben schlägt sie gezielt Quests für Hobbys, Erholung und neue Erfahrungen vor, um eine Balance zwischen Work und Fun herzustellen.

Dieses Dokument beschreibt die **Fachlogik**: Quest-Modell, Regeln, Board, Balance und Belohnungen. Produktumfang, Technik, Betrieb und Meilensteine stehen im PRD (`quest-board-prd.md`).

---

## 1. Getroffene Entscheidungen

| Thema | Entscheidung |
|---|---|
| Benennung | Es gibt nur **Main Quests** (verbindlich) und **Side Quests** (freiwillig). Alle weiteren Eigenschaften sind frei kombinierbar und werden über Symbole dargestellt, nicht über eigene Namen. |
| Main ist abgeleitet | Main ist kein gespeichertes Feld, sondern ergibt sich aus der Verbindlichkeit am aktuellen Datum. |
| Work/Fun | Jede Quest bringt entweder Work- oder Fun-Punkte. Work/Fun ist unabhängig von Main/Side, damit Work nicht als "wichtiger" dargestellt wird. |
| Punktarten | In v1 nur Work und Fun. Keine dritte Punktart für Growth; Wachstum wird später über Pfade abgebildet. |
| Fun-Art | Fun-Quests haben optional eine Art: **Rast** oder **Erkundung**. Beide bringen Fun-Punkte; die Art dient der Reflexion und der Mischung im Pool. |
| Life/Character | Keine eigenen Typen. Eine Quest kann optional auf einen Pfad einzahlen, unabhängig von Work/Fun. |
| Wiederholung | Drei Arten: **Einmalig**, **Cooldown** (ab Erledigung), **Fester Turnus** (kalendergebunden). |
| Lebensspanne | Gibt es nur bei festem Turnus. Default = Turnus, kürzer erlaubt, länger nicht. |
| Turnus-Anker | Statt eines Offsets gibt es ein Anker-Datum (erstes Auftreten). Rotationen entstehen durch versetzte Anker. |
| Zeiteinheiten | Tage, Wochen, Monate, Jahre. |
| Verbindlichkeit | **Keine**, **Immer** oder **Ab Datum** (Eskalation). "Ab Datum" nur bei Work. Fun wird nur als fester Termin oder Ritual verbindlich. |
| Eskalation | Eine Side Quest mit "Ab Datum" wird an diesem Datum zur Main Quest und automatisch ins Logbuch gesetzt (Siegel-Moment). |
| Zurücklegen | Side Quests können aus dem Logbuch zurückgelegt werden, Main Quests nicht. Die Regel wird aus der aktuellen Verbindlichkeit abgeleitet. |
| Verfallen | Nur Quests mit festem Turnus verfallen (am Ende ihrer Lebensspanne). Alles andere bleibt, bis es erledigt oder zurückgelegt wird. |
| Überfällig | Nur Quests mit Frist können überfällig werden (absolutes Fälligkeitsdatum oder relative Frist bei Cooldown). Ohne Frist wird nur das Alter angezeigt. |
| Übersprungen | Eine nicht erledigte Turnus-Quest zählt als übersprungen, egal ob sie angenommen wurde oder nicht. Der Zähler gilt seit der letzten Erledigung. |
| Badges | Work-Side-Quests zeigen `times_skipped` bzw. `times_offered` an. Fun-Quests zeigen nie Badges, auch wenn intern gezählt wird. |
| Angebots-Sperre | Gibt es nicht. Zufall plus Cooldown sorgt für genug Abwechslung. |
| Angefangen-Status | Gibt es nicht. Eine angenommene Quest im Logbuch *ist* angefangen. |
| Lange liegende Quests | Das Alter einer Quest im Logbuch wird dezent angezeigt; optional kommt ein freundlicher Hinweis nach längerer Zeit. |
| Nachtragen | Spontan erledigte Dinge können nachgetragen werden (aus dem Pool oder als freie Quest, direkt erledigt). |
| Bearbeiten | Änderungen gelten sofort für alles Offene und Zukünftige, Vergangenes bleibt über die Snapshots unverändert. Details in Abschnitt 6. |
| Rückgängig | Abhaken ohne Sicherheitsdialog, dafür mit "Rückgängig" direkt danach und Wiederöffnen bis zum Tageswechsel. |
| Löschen | Nie erledigte Quests werden gelöscht, sonst archiviert (`is_active = false`). Für den Nutzer sieht beides gleich aus. |
| Überbuchung | Man darf mehr annehmen als geplant, mit Hinweis (relevant ab Einführung des Tages-Manas). |
| Tages- und Wochenbeginn | Default 4:00 Uhr und Montag, im Profil einstellbar. |
| Tageswechsel | Eine idempotente, nachholfähige Funktion, in v1 "faul" bei der ersten Anfrage des Tages aufgerufen, abgesichert durch eine Sperre pro Nutzer. Details in Abschnitt 8. |
| Vorlage und Instanz | Quests sind Vorlagen, das konkrete Auftreten ist eine Instanz mit Snapshot bei Erledigung. Zähler, Balance und Punkte werden aus den Instanzen abgeleitet. |
| Balance | Fun-Anteil der erledigten Punkte mit exponentiellem Abklingen und neutralem Grundwert, bezogen auf einen Zielwert. Keine Minuspunkte. Details in Abschnitt 9. |
| Belohnungen v1 | Abhak-Moment, Heldenlevel mit Harmonie-Bonus, schlichte Heldenchronik, Titel und Erfolge. Keine Ingame-Währung, keine Verlust-Mechaniken. Details in Abschnitt 10. |
| Level fixieren | In der Testphase werden Level aus der Historie abgeleitet. Später werden erreichte Level fixiert, damit Formeländerungen niemanden zurückstufen. |
| Startpaket und Onboarding | Ein Startpaket mit Beispiel-Quests wird beim Onboarding in den eigenen Pool **kopiert**. Das Onboarding selbst besteht aus kleinen Quests. Details in Abschnitt 11. |
| Mehrere Nutzer | Jede Tabelle hat einen Besitzer (`user_id`), IDs sind UUIDs. Soziale Funktionen sind nicht geplant; falls doch, dann höchstens "sehen, was andere machen". |
| Pfade und Fraktionen | Beide sind zusätzliche Punktetöpfe mit Rängen und werden später gemeinsam konzipiert, eventuell mit gemeinsamem Grundmodell. |
| Event-Quests (später) | Einmalige Event-Quests, die zum Eventende offen sind, verschwinden. |
| Questreihen (später) | Werden als Folge von Etappen modelliert; eine Etappe kann mehrere Quests enthalten. |

---

## 2. Datenmodell

Notation in Python mit Pydantic, passend zum Backend (FastAPI). Die Varianten sind **Discriminated Unions** – das Python-Gegenstück zu sealed classes. Mit `match` und `assert_never` prüft der Type Checker, dass alle Fälle behandelt werden.

```python
from datetime import date, datetime
from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID
from pydantic import BaseModel, Field, model_validator


# --- Zeitspannen ---------------------------------------------------------

class TimeUnit(StrEnum):
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"

class Timespan(BaseModel):
    amount: int = Field(gt=0)
    unit: TimeUnit
    # fits_into(other): konservativer Vergleich in Tagen (Monat = 28, Jahr = 365)


# --- Seite (Work / Fun) --------------------------------------------------

class FunKind(StrEnum):
    REST = "rest"
    EXPLORATION = "exploration"

class Work(BaseModel):
    type: Literal["work"] = "work"

class Fun(BaseModel):
    type: Literal["fun"] = "fun"
    kind: FunKind | None = None

Side = Annotated[Work | Fun, Field(discriminator="type")]


# --- Wiederholung --------------------------------------------------------

class Once(BaseModel):
    type: Literal["once"] = "once"

class Cooldown(BaseModel):
    type: Literal["cooldown"] = "cooldown"
    after: Timespan
    due_within: Timespan | None = None   # relative Frist ab Erscheinen, nur mit Always

class Fixed(BaseModel):
    type: Literal["fixed"] = "fixed"
    every: Timespan
    anchor: date                          # erstes Auftreten
    lifespan: Timespan | None = None      # None = gesamter Turnus; sonst ≤ every

Recurrence = Annotated[Once | Cooldown | Fixed, Field(discriminator="type")]


# --- Verbindlichkeit -----------------------------------------------------

class NotBinding(BaseModel):
    type: Literal["none"] = "none"         # freiwillig

class Always(BaseModel):
    type: Literal["always"] = "always"     # immer verbindlich

class From(BaseModel):
    type: Literal["from"] = "from"         # ab Datum verbindlich (nur Work)
    date: date

Binding = Annotated[NotBinding | Always | From, Field(discriminator="type")]


# --- Vorlage ------------------------------------------------------------

class Size(StrEnum):
    S = "s"
    M = "m"
    L = "l"

class Quest(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    side: Side
    recurrence: Recurrence
    binding: Binding
    visible_from: date | None = None      # erscheint ab
    due_date: date | None = None          # absolute Frist, nur mit Always oder From
    size: Size                            # Gewicht für Punkte und Balance
    path_id: UUID | None = None           # später: Pfade
    faction_id: UUID | None = None        # später: Fraktionen
    event_id: UUID | None = None          # später: Events
    chain_stage_id: UUID | None = None    # später: Questreihen
    is_active: bool = True

    @model_validator(mode="after")
    def check_rules(self) -> "Quest": ...  # Regeln siehe "Validierungsregeln"


# --- Auftreten ----------------------------------------------------------

class Status(StrEnum):
    OFFERED = "offered"
    ACCEPTED = "accepted"
    DONE = "done"
    EXPIRED = "expired"
    RETURNED = "returned"

class Origin(StrEnum):
    BOARD = "board"                        # vom Board angenommen
    AUTO_LOGBOOK = "auto_logbook"          # automatisch ins Logbuch (Main)
    LOGGED_AFTERWARDS = "logged_afterwards"  # nachgetragen

class QuestInstance(BaseModel):
    id: UUID
    user_id: UUID
    quest_id: UUID
    logical_day: date                     # Tag, an dem die Instanz erschienen ist
    shown_from: datetime                  # erschienen auf Board bzw. im Logbuch
    expires_at: datetime | None           # nur bei Fixed (Ende der Lebensspanne)
    due_at: datetime | None               # konkrete Frist (aus due_date oder due_within)
    accepted_at: datetime | None
    completed_at: datetime | None
    status: Status
    snapshot: "QuestSnapshot | None"      # wird bei Erledigung geschrieben


# Enthält alles, was Balance, Chronik, Erfolge und spätere Pfade/Fraktionen brauchen,
# damit spätere Änderungen an der Vorlage die Historie nicht verändern.
class QuestSnapshot(BaseModel):
    name: str
    side: Side                            # inkl. Fun-Art
    size: Size
    points: int
    completed_at: datetime
    was_main: bool
    was_escalated: bool
    origin: Origin
    path_id: UUID | None                  # in v1 noch nicht ausgewertet
    faction_id: UUID | None               # in v1 noch nicht ausgewertet
    balance_at_completion: float
```

In der Datenbank werden die Varianten als flache Spalten gespeichert (z. B. `side`, `fun_kind`, `recurrence_type`, `every_amount`, …) und über CHECK-Constraints abgesichert. Das Mapping zwischen Tabellen und Pydantic-Modellen ist die einzige Stelle, an der beide Welten aufeinandertreffen.

### Abgeleitete Werte

```python
def is_binding_at(quest: Quest, day: date) -> bool:
    match quest.binding:
        case NotBinding():
            return False
        case Always():
            return True
        case From(date=d):
            return day >= d
        case _ as unreachable:
            assert_never(unreachable)

is_main          = is_binding_at(quest, heute)
can_return       = not is_binding_at(quest, heute)
is_fixed_on_board = isinstance(quest.recurrence, Fixed)
times_skipped    = Anzahl EXPIRED-Instanzen seit der letzten DONE-Instanz
times_offered    = Anzahl angebotener Instanzen seit der letzten Annahme
```

### Validierungsregeln

- `From` nur bei `Work`.
- Bei `Fun` ist Verbindlichkeit nur als Termin (`Once` + `Always`) oder Ritual (`Fixed` + `Always`) erlaubt; `Cooldown` + `Always` nicht.
- `due_date` nur mit `Always` oder `From`.
- `due_within` nur bei `Cooldown` mit `Always`.
- `lifespan ≤ every` bei `Fixed`.
- Pro Quest gibt es höchstens eine offene Instanz (Status `OFFERED` oder `ACCEPTED`). In der Datenbank als partieller Unique-Index abgesichert.

---

## 3. Quest-Arten

Die Arbeitstitel beschreiben nur Kombinationen, sie sind keine eigenen Namen in der App. Sichtbar ist nur **Main** oder **Side**.

| In der App | Seite | Wiederholung | Verbindlichkeit | visible_from | Frist | Beispiele | Verhalten |
|---|---|---|---|---|---|---|---|
| **Side** · Turnus | Work | Fixed | None | – | – | Kühlschrank checken (täglich), Bad putzen (wöchentlich), Keller fegen (6-Wochen-Rotation) | Liegt für die Lebensspanne auf der festen Board-Seite, muss angenommen werden. Verfällt am Ende, nicht erledigt = übersprungen, Badge sichtbar. |
| **Main** · Turnus | Work | Fixed | Always | – | – | Miete prüfen, Mülltonne rausstellen | Jede Instanz landet automatisch im Logbuch. Verfällt am Ende und wird als verpasst markiert. |
| **Side** · einmalig ("Iwann") | Work | Once | None | optional | – | Kram aussortieren, Glas wegbringen | Wird aus dem Pool gezogen, `times_offered`-Badge. Zurücklegbar, verschwindet nach Erledigung. |
| **Side** · wiederkehrend | Work | Cooldown | None | – | – | Haare schneiden, Auto waschen | Wie einmalig, kehrt nach Erledigung mit Cooldown in den Pool zurück. |
| **Main** · wiederkehrend | Work | Cooldown | Always | optional (erste Instanz) | optional `due_within` | Zahnarztkontrolle, Reifendruck prüfen | Nach Ablauf des Cooldowns automatisch im Logbuch. Überfällig nur mit Frist. |
| **Side → Main** · eskalierend | Work | Once | From(Datum) | optional | optional `due_date` | Steuererklärung, Kleiderschrank aussortieren | Bis zum Datum normale Side Quest im Pool, danach Main (Siegel). Wird häufiger gezogen, je näher das Datum rückt, kurz vorher garantiert. |
| **Main** · einmalig | Work | Once | Always | – | optional `due_date` | Auto in die Werkstatt, Geschenk besorgen | Sofort im Logbuch, nicht zurücklegbar. Nach Frist überfällig markiert, bleibt stehen. |
| **Main** · Termin | Work oder Fun | Once | Always | gesetzt | `due_date` | Arzttermin, Konzert, Geburtstagsfeier | Erscheint ab `visible_from` direkt im Logbuch. |
| **Side** · wiederkehrend | Fun | Cooldown | None | – | – | Serie schauen, Puzzle, Freundin schreiben, Linolschnitt | Wird aus dem Pool gezogen, keine Badges. Bleibt im Logbuch, bis abgehakt oder zurückgelegt; kehrt danach in den Pool zurück (nach Abhaken mit Cooldown). |
| **Side** · einmalig | Fun | Once | None | optional | – | Neues Restaurant testen, Kletterhalle ausprobieren | Wie wiederkehrend, verschwindet nach Erledigung. Typischerweise Erkundung. |
| **Side** · Ritual | Fun | Fixed | None | – | – | Sonntagsspaziergang | Erscheint regelmäßig auf der festen Board-Seite, nie ein Skip-Badge. |
| **Main** · Ritual | Fun | Fixed | Always | – | – | Spieleabend freitags | Fester wiederkehrender Termin im Logbuch. |

Für alle Arten gilt: `size` ist immer gesetzt, Fun-Quests haben optional eine Fun-Art.

---

## 4. Lebenszyklus

| | Abhaken | Zurücklegen | Ende der Lebensspanne |
|---|---|---|---|
| **Side, Fixed** | erledigt bis zum nächsten Turnus | zurück aufs Board | verfällt, übersprungen +1 |
| **Main, Fixed** | erledigt bis zum nächsten Turnus | nicht möglich | verfällt, als verpasst markiert |
| **Side, Once** | verschwindet komplett | zurück in den Pool | – |
| **Side, Cooldown** | zurück in den Pool mit Cooldown | zurück in den Pool | – |
| **Main, Once** | erledigt | nicht möglich | – (bleibt, ggf. überfällig) |
| **Main, Cooldown** | neue Instanz nach Cooldown | nicht möglich | – (bleibt, ggf. überfällig) |

### Rückgängig machen

- Direkt nach dem Abhaken erscheint kurz ein Hinweis mit **"Rückgängig"**.
- Zusätzlich kann eine erledigte Quest **bis zum Tageswechsel** im Bereich "Heute erledigt" des Logbuchs wieder geöffnet werden. Danach ist sie festgeschrieben.
- Da Punkte, Balance, Level und Erfolge aus den Instanzen abgeleitet werden, korrigiert sich beim Rückgängigmachen alles automatisch. Eine einmalige Quest, die verschwunden war, ist wieder da; ein begonnener Cooldown wird aufgehoben.
- Kein Sicherheitsdialog beim Abhaken: Er würde den Abhak-Moment stören und wird erfahrungsgemäß reflexartig weggeklickt.

---

## 5. Quests anlegen

### Dialog

Die Fragen werden in dieser Reihenfolge gestellt, weil die Optionen voneinander abhängen:

1. **Pflicht oder Spaß?** → Work / Fun
2. **Wie oft?** → einmalig / zu festen Zeiten / wieder nach einer Pause
3. **Main Quest oder Side Quest?** Die Optionen hängen von 1 und 2 ab:
   - Work, einmalig: Side / Main sofort / Main ab Datum
   - Work, wiederholend: Side / Main
   - Fun: Side / Main (fester Termin bzw. Ritual)

Danach folgt ein Formular mit den vorausgefüllten Antworten und den restlichen Details (Name, Größe, Zeitangaben, Fun-Art usw.).

### Schnellanlage (Brain-Dump)

Nur der Name wird eingegeben. Default: **Side Quest, Work, einmalig, nicht verbindlich, Größe M**. Details können später ergänzt werden.

Welche Wege tatsächlich genutzt werden, wird getestet und danach verfeinert.

---

## 6. Quests bearbeiten und löschen

**Grundregel:** Änderungen gelten sofort für alles Offene und Zukünftige. Vergangenes bleibt unverändert (über die Snapshots geschützt).

| Änderung | Wirkung |
|---|---|
| Name, Größe, Seite, Fun-Art | Offene Instanzen zeigen sofort den neuen Stand. Punkte und Seite werden erst beim Abhaken im Snapshot festgehalten. |
| Cooldown | Wirkt sofort, weil der nächste mögliche Zeitpunkt aus letzter Erledigung + Cooldown berechnet wird. |
| Lebensspanne | Die offene Instanz wird angepasst: `expires_at = shown_from + neue Lebensspanne`. Verkürzen und Verlängern funktionieren gleich. |
| Turnus | Der Anker wird auf das Erscheinungsdatum der offenen Instanz gesetzt (bzw. der letzten, falls keine offen ist). Die nächste Instanz erscheint bei `Anker + neuer Turnus`. Beispiel: Die Quest erschien Montag mit 2-Wochen-Turnus, Umstellung auf wöchentlich → nächste Instanz kommenden Montag. |
| Verbindlichkeit | Ergibt sich aus der abgeleiteten Regel: Wird eine Quest verbindlich, wandert sie ins Logbuch; wird sie freiwillig, darf sie zurückgelegt werden. |
| Wiederholungsart | Die offene Instanz bleibt bestehen; die neue Art gilt ab der nächsten Instanz. |

**Randfälle:**
- Liegt die neu berechnete Lebensspanne bereits in der Vergangenheit, endet die Instanz beim nächsten Tageswechsel statt sofort, damit sie heute noch erledigt werden kann.
- Es gibt nie zwei offene Instanzen derselben Quest. Eine neue Instanz entsteht erst, wenn die vorherige beendet ist.

**Löschen:**
- Wurde die Quest nie erledigt, wird sie mitsamt offenen Instanzen gelöscht.
- Andernfalls wird sie archiviert (`is_active = false`), damit Snapshots und Verweise erhalten bleiben. Offene Instanzen werden entfernt.
- Für den Nutzer sieht beides gleich aus.

---

## 7. Board und Logbuch

### Zwei Hauptansichten

- **Quest Board:** das Angebot. Hier nimmt man Side Quests bewusst an.
- **Logbuch:** alles, wozu man sich verpflichtet hat: automatisch gesetzte Main Quests und angenommene Side Quests. Zeigt offene und heute erledigte Quests. Wenn das Logbuch abgehakt ist, ist der Tag geschafft, auch wenn das Board nicht leer ist.

### Aufbau des Boards

**Linke Seite: feste Quests.** Alle Side Quests mit festem Turnus, die gerade fällig sind, werden vollständig angezeigt (Work und Fun, also auch Rituale).

**Rechte Seite: Pool-Quests.** 6–8 Slots (abhängig vom Design), einmal beim Tageswechsel gezogen und für den Tag stabil.

- Die Aufteilung auf Work und Fun richtet sich nach der Balance der letzten Tage und berücksichtigt, was auf der festen Seite schon an Work liegt.
- Mindestens 2 Slots pro Seite sind garantiert; die übrigen werden nach Balance verteilt (z. B. bei 7 Slots: ausgeglichen 3 Work / 4 Fun, Work-lastig 2 / 5, Fun-lastig 4 / 3).
- Innerhalb einer Seite wird gewichtet zufällig aus allen passenden Quests gezogen; Once und Cooldown landen im selben Topf.
- Ist eine Seite leer, wird mit der anderen aufgefüllt.
- Angenommene Slots werden nicht neu gefüllt.
- Nicht angenommene Angebote gehen am Tagesende still zurück in den Pool.

**Gewichtung Work:**
- Alter bzw. `times_offered` erhöht das Gewicht.
- Eskalierende Quests werden umso häufiger gezogen, je näher das Datum rückt, und in den letzten Tagen davor garantiert angezeigt.

**Gewichtung Fun:**
- Die Fun-Arten werden gemischt (nach viel Rast eher Erkundung).
- `times_offered` wird gezählt, aber nicht angezeigt. Ob es das Gewicht beeinflusst, ist offen.

---

## 8. Tageswechsel

### Logischer Tag

- Alle Zeitpunkte werden in **UTC** gespeichert.
- Jeder Nutzer hat eine Zeitzone und einen Tagesbeginn (Default 4:00 Uhr).
- `logischer_tag = (jetzt in Nutzer-Zeitzone − Tagesbeginn).date()` – um 2 Uhr nachts ist also noch "gestern".

### Ablauf

Der Tageswechsel ist **eine Funktion**, die:
- **idempotent** ist (mehrfaches Ausführen richtet keinen Schaden an),
- **nachholen** kann (auch wenn mehrere Tage vergangen sind),
- "jetzt" als **Parameter** bekommt (dadurch in Tests beliebig simulierbar).

Schritte je Nutzer, für jeden verpassten logischen Tag in Reihenfolge:

1. Instanzen mit abgelaufener Lebensspanne → `EXPIRED`.
2. Fällige Turnus-Quests erzeugen neue Instanzen (Main → Logbuch, Side → feste Board-Seite).
3. Cooldown-Main-Quests mit abgelaufenem Cooldown → neue Instanz im Logbuch.
4. Side Quests, deren Eskalationsdatum erreicht ist → Main, Instanz im Logbuch (falls nicht schon angenommen).
5. Quests mit erreichtem `visible_from` werden aktiv.
6. Nicht angenommene Pool-Angebote des Vortags gehen zurück in den Pool.
7. Erledigte Instanzen des Vortags werden festgeschrieben (kein Wiederöffnen mehr).

Danach einmalig, **nur für heute**: Ziehung der Pool-Slots. Zuletzt wird `last_rollover_day` des Nutzers auf heute gesetzt.

### Auslöser

- **v1:** "faul" – jede API-Anfrage prüft, ob `last_rollover_day < logischer_tag`, und ruft den Tageswechsel vorher auf.
- **Später** (mit Benachrichtigungen): zusätzlich ein geplanter Job, der dieselbe Funktion aufruft.

### Gleichzeitige Anfragen

Schicken zwei Geräte gleichzeitig die erste Anfrage des Tages, darf der Tageswechsel nicht doppelt laufen. Lösung: eine **Sperre pro Nutzer in PostgreSQL** (transaktionsgebundener Advisory Lock oder `SELECT … FOR UPDATE` auf der Nutzerzeile), danach erneute Prüfung von `last_rollover_day`. Erklärung im Lernleitfaden.

### Offener Punkt für später

Bei langer Abwesenheit sammeln Turnus-Quests viele Skips (z. B. 14 nach zwei Wochen Urlaub). Das beeinflusst nur die Gewichtung, ein **Urlaubsmodus** wäre aber eine sinnvolle Ergänzung.

---

## 9. Balance

### Was zählt

- Alle **erledigten Instanzen** (Main und Side, angenommen, automatisch oder nachgetragen), berechnet aus den Snapshots.
- **Punkte nach Größe:** S = 1, M = 2, L = 3 (bei Bedarf später 1 / 2 / 4).
- **Keine Minuspunkte:** Verfallene und zurückgelegte Quests zählen nicht. Die Balance misst, was getan wurde, nicht was liegen blieb.

### Berechnung

Exponentielles Abklingen statt festem Fenster, damit die Balance sich fließend bewegt und nicht springt, wenn ein Tag aus dem Fenster fällt.

```python
def weight(days_ago: float) -> float:
    return 0.5 ** (days_ago / HALF_LIFE_DAYS)

work = sum(i.points * weight(i.days_ago) for i in done if isinstance(i.side, Work))
fun  = sum(i.points * weight(i.days_ago) for i in done if isinstance(i.side, Fun))

# neutraler Grundwert, damit wenig Daten nicht zu Extremwerten führen
balance = (fun + PRIOR) / (work + fun + 2 * PRIOR)   # Fun-Anteil, 0..1
```

Die Berechnung lässt sich auch direkt als eine SQL-Abfrage über die Snapshots formulieren.

| Stellschraube | Wert v1 | Einstellbar |
|---|---|---|
| Punkte pro Größe | S = 1, M = 2, L = 3 | intern |
| Halbwertszeit | 3 Tage | intern |
| Neutraler Grundwert (`PRIOR`) | 2 Punkte pro Seite | intern |
| Zielwert | 50 % Fun | zunächst intern, später im Profil (sobald es Profileinstellungen gibt, direkt mit aufnehmen) |
| Ausgeglichene Zone | Ziel ± 10 Prozentpunkte | intern |

Zonen: **ausgeglichen**, **Work-lastig**, **Fun-lastig**. Alle Bewertungen beziehen sich auf die Abweichung vom Zielwert, nicht von der Mitte.

### Wirkung auf das Board

```python
deficit   = target - balance                         # positiv = zu wenig Fun
fun_share = clamp(0.5 + deficit * K + fixed_work_load * F, 0.0, 1.0)

free_slots = total_slots - 2 * MIN_PER_SIDE
fun_slots  = MIN_PER_SIDE + round(free_slots * fun_share)
work_slots = total_slots - fun_slots
```

- `K`: wie stark die Balance durchschlägt.
- `fixed_work_load`: Anteil offener Work-Quests auf der festen Board-Seite; verschiebt Slots zugunsten von Fun, wenn dort viel Arbeit liegt.
- Konstanten werden in der Testphase angepasst.

### Darstellung

- **Waage:** Neigung = Balance, Füllung der Schalen = Gesamtaktivität (ruhige vs. volle Woche). Atmosphärisch z. B. Schwert und Laute.
- **Texte statt Prozentwerte**, z. B. "Deine Waage neigt sich zur Arbeit, die Taverne hat heute ein paar Angebote mehr". Das erklärt gleichzeitig, warum das Board so aussieht. Das Backend liefert dafür nur einen Code (z. B. `balance.work_heavy`), das Frontend übersetzt.

### Später

- Buffs und Debuffs abhängig von der Zone (z. B. "Erschöpft", "Ausgeruht").

---

## 10. Belohnungen

### v1

1. **Abhak-Moment:** Animation, Geräusch, Pergament, Siegel, sichtbare Bewegung der Waage. Hier bewusst viel Designzeit investieren – das trägt die App.
2. **Heldenlevel:** aus der Summe aller Punkte, Work und Fun zählen gleich.
   - **Harmonie-Bonus:** Solange die Waage in der ausgeglichenen Zone ist, bringen Quests mehr Erfahrung (z. B. +20 %). Belohnt wird die Balance selbst, nicht nur die Menge. Nur Bonus, nie Abzug.
   - **Level fixieren:** In der Testphase werden Level aus der Historie abgeleitet, damit die Formel angepasst werden kann. **Später werden erreichte Level festgehalten**, damit Formeländerungen niemanden zurückstufen.
3. **Heldenchronik (schlicht):** Liste pro Tag mit der Waage des Tages, später Wochenrückblick. Belohnt durch Erinnerung statt durch Gegenwert.
4. **Titel und Erfolge:** vollständig aus erledigten Instanzen ableitbar. Beispiele:
   - "Erste Erkundung", "10 Rasten", "Hundert Quests"
   - "Waage der Weisen": 7 Tage in Folge ausgeglichen
   - "Bezwinger der Bürokratie": eine eskalierte Main Quest erledigt
   - "Aufgeräumter Geist": 5 Iwann-Quests in einer Woche

### Bewusst nicht

- **Ingame-Währung und Shop:** bringt Konsum-Logik und Entscheidungsaufwand. Falls überhaupt, später; Freischaltungen dann eher über Level und Erfolge statt über Kauf.
- **Verlust-Mechaniken:** kein Levelverlust, kein Abzug, keine zerbrechenden Streaks.
- **Reale Belohnungen:** höchstens später als optionale "Schatzkammer".

### Hinweis

Quest-Inflation (Aufgaben künstlich zerlegen für mehr Punkte) wird durch Gewichtung nach Größe und den Harmonie-Bonus gedämpft.

---

## 11. Startpaket und Onboarding

### Startpaket

- Eine Datei mit Quest-Vorlagen im Repository (z. B. `backend/app/seed/starter_pack.de.yaml`), pro Sprache eine Datei.
- Beim Onboarding wählt man Vorlagen aus, die als **eigene Quests kopiert** werden. Es gibt keine Verknüpfung zur Vorlage, jede Kopie ist frei anpassbar.
- Inhalt: eine Mischung aus Work-Turnus-Quests (z. B. Bad putzen), Iwann-Quests und Fun-Quests beider Arten (Rast und Erkundung), damit Board und Balance vom ersten Tag an funktionieren.

### Onboarding

Das Onboarding besteht selbst aus kleinen Quests, die die App durch Benutzung erklären:

1. Wähle Quests aus dem Startpaket.
2. Lege deine erste eigene Side Quest an (Dialog).
3. Notiere schnell eine Idee (Schnellanlage).
4. Nimm eine Quest vom Board an.
5. Hake sie im Logbuch ab.

Später, wenn es Questreihen gibt, wird daraus eine Tutorial-Questreihe.

---

## 12. Später

- **Pfade und Fraktionen:** gemeinsam konzipieren, beide als zusätzliche Punktetöpfe mit Rängen. Die Snapshots speichern Pfad und Fraktion bereits, sodass rückwirkende Auswertung möglich ist.
- **Level fixieren**
- **Zielwert der Balance im Profil**
- **Buffs und Debuffs** abhängig von der Balance
- **Tages-Mana:** Energie-Check am Morgen, Kapazität für das Logbuch, Hinweis bei Überbuchung
- **Fraktionen:** Ränge, Fraktionen als Questgeber, Briefe vernachlässigter Fraktionen
- **Events:** Zeitraum mit eigenem Theme und eigenen Quests; einmalige Event-Quests verschwinden am Eventende
- **Questreihen:** Etappen mit Freischaltung, später auch als Weg zu Pfad-Rangaufstiegen
- **Zähl-Quests:** "3× diese Woche" als Quest mit Zielanzahl und Zeitfenster
- **Stimmungs-Check** nach Quests für die Reflexion (Rast vs. Erkundung)
- **"Neu würfeln"** der Pool-Slots einmal pro Tag
- **Urlaubsmodus** gegen Skip-Anhäufung bei Abwesenheit
- **Kalender-Anbindung** (nur lesend), um freie Zeiten zu erkennen
- **Soziale Funktionen:** höchstens "sehen, was andere machen" (Level, Titel, Chronik)

## 13. Offene Fachfragen

- Genaue Anzahl der Pool-Slots und Konstanten der Pool-Formel (Testphase)
- Höhe des Harmonie-Bonus und Levelkurve
- Ab wann der Hinweis bei lange liegenden Quests erscheint
- Visuelle Sprache für Work/Fun, Turnus, Cooldown, Fun-Arten und das Siegel
- Inhalt des Startpakets
