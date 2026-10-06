# Lessons Learned

Wenn etwas mehr als eine halbe Stunde gekostet hat: Ursache und Lösung in zwei, drei Sätzen.

| Datum | Thema | Was war das Problem? | Ursache und Lösung |
|---|---|---|---|
|6.10.26|venv|Virtuelle Umgebungen kann man nicht verschieben. Eine venv enthält absolute Pfade, zum Beispiel in den Shebangs und in der .pth-Datei des editable installierten Pakets.|.venv löschen und uv sync neu ausführen. Und in VS Code den Interpreter neu wählen und das Fenster neu laden.|