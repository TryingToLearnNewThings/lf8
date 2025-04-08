# Quiz Game

## Beschreibung

Dieses Projekt ist ein einfaches **Quiz-Spiel**, das es den Benutzern ermöglicht, Fragen aus verschiedenen Kategorien zu beantworten. Die Fragen sind in einer **Datenbank** gespeichert, und das Spiel verwendet diese Datenbank, um zufällige Fragen anzuzeigen, die der Benutzer beantworten muss. Das Spiel verfolgt die richtigen Antworten und zeigt das Ergebnis am Ende an.

## Technologie-Stack

- **Python 3.x**: Hauptprogrammiersprache für das Spiel.
- **SQLite**: Eine leichtgewichtige relationale Datenbank, die lokal auf dem Rechner läuft und für das Speichern von Fragen und Kategorien verwendet wird.
- **SQLite3**: Wird verwendet, um mit der SQLite-Datenbank zu interagieren.
- **Random Modul**: Wird verwendet, um zufällige Fragen aus der Datenbank auszuwählen.

## Verwendete Datenbank

Das Quiz-Spiel verwendet eine **SQLite**-Datenbank namens `database.db`. In dieser Datenbank sind die Fragen und ihre zugehörigen Kategorien gespeichert.

### Tabellen in der Datenbank

1. **Question**: Speichert die Fragen, die richtigen Antworten und die Kategorie-ID.
    - `QuestionID` (Primärschlüssel)
    - `QuestionText` (Frage)
    - `CorrectAnswer` (Richtige Antwort)
    - `CategoryID` (Fremdschlüssel zur Tabelle `Category`)

2. **Category**: Speichert die verschiedenen Kategorien von Fragen.
    - `CategoryID` (Primärschlüssel)
    - `Name` (Kategorie-Name, z.B. "Politics", "Science")

## Funktionen

### 1. Fragen abfragen
Die `Question`-Klasse enthält eine Methode `get_questionID()`, die zufällige Fragen aus der Datenbank abruft, basierend auf einer bestimmten Kategorie. Diese Funktion stellt sicher, dass nur Fragen aus der gewünschten Kategorie (z.B. "Politics") angezeigt werden.

### 2. Benutzerantworten vergleichen
Die Benutzerantworten werden mit der richtigen Antwort in der Datenbank verglichen. Wenn der Benutzer die richtige Antwort auswählt, wird dies als "richtig" gezählt.

### 3. Zufällige Auswahl von Fragen
Durch die Nutzung der **`random`** Bibliothek wird jede Frage zufällig aus der Datenbank ausgewählt, um sicherzustellen, dass der Benutzer jedes Mal eine andere Erfahrung macht.

## Aufbau

### `main.py`

In der `main.py`-Datei wird das Quiz-Spiel gestartet. Hier wird eine **Frage** aus der Datenbank geladen und dem Benutzer präsentiert. Das Ergebnis wird am Ende angezeigt.

### `question.py`

Die `Question`-Klasse ist für das Abrufen der Fragen aus der SQLite-Datenbank verantwortlich. Die `get_questionID()`-Methode holt alle Fragen aus einer bestimmten Kategorie (z.B. "Politics") und gibt sie aus.

### `database.db`

Die SQLite-Datenbank `database.db` enthält alle Fragen und Kategorien, die für das Quiz benötigt werden. Es wird eine einfache Struktur verwendet, die zwei Tabellen enthält:
- **Question**: Speichert die Fragen.
- **Category**: Speichert die Kategorien von Fragen.

## Installation und Nutzung

1. **Voraussetzungen**

   - Python 3.x
   - SQLite3 (normalerweise bereits in Python installiert)
   
2. **Installation**

   - Klone dieses Repository:
     ```bash
     git clone https://github.com/dein-benutzername/Quiz-Game.git
     cd Quiz-Game
     ```

   - Die Datenbank wird automatisch erstellt, wenn du das Skript zum ersten Mal ausführst. Die Datei `database.db` enthält die Tabellen `Question` und `Category`, die mit den notwendigen Daten befüllt werden können.

3. **Starten des Spiels**

   Führe einfach das `main.py`-Skript aus:

   ```bash
   python main.py
