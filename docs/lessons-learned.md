# Lessons Learned

Wenn etwas mehr als eine halbe Stunde gekostet hat: Ursache und Lösung in zwei, drei Sätzen.

| Datum | Thema | Was war das Problem? | Ursache und Lösung |
|---|---|---|---|
|6.10.26|venv|Virtuelle Umgebungen kann man nicht verschieben. Eine venv enthält absolute Pfade, zum Beispiel in den Shebangs und in der .pth-Datei des editable installierten Pakets.|.venv löschen und uv sync neu ausführen. Und in VS Code den Interpreter neu wählen und das Fenster neu laden.|
|23.10.26|Git|Ein Branch, der von origin/main aus angelegt wird, trackt main. Dann landet git push auf main. Abhilfe: von einem lokalen Branch aus anlegen oder mit git push -u origin <branch> pushen.|
|23.10.26|Force-Push zur Korrektur|Bei einem Force-Push zur Korrektur muss man vorher den richtigen Zielstand prüfen.|Mit dem Activity-Log auf GitHub oder git reflog nachsehen, welcher Commit vorher oben lag. Wird der falsche Stand gepusht, verschwinden gemergte PRs.|
| 23.10.26 | GitHub Actions Jobs | Check-Backend Job soll effizient nur bei Änderungen am backend laufen, aber andere PRs nicht blocken. | Ein übersprungener Job gilt für einen Pflichtcheck als erfolgreich, ein nicht gestarteter Workflow liefert gar kein Ergebnis. Deshalb gehört der Pfadfilter auf die Job-Ebene, und der Job, der die Änderungen prüft, ist selbst ein Pflichtcheck. |
| 23.10.26 | GitHub Actions Jobs | Pflichtchecks erst einstellen, wenn der Workflow auf main liegt. Sonst blockiert jeder andere PR, weil sein Workflow nirgends existiert. |
| 24.10.26 | PostgreSQL | Bezeichner mit '-' müssen in Anfürhungszeichen gesetzt werden ("example-name"). | In Bezeichnern bevorzugt "_" statt "-" verwenden. |

