Automatisches Bewässerungssystem

Projektübersicht

Das Ziel des Projekts ist es, ein autonomes Bewässerungssystem zu entwickeln, das:

    Die Bodenfeuchtigkeit regelmäßig misst.
    Automatisch die Wasserpumpe startet, wenn die Feuchtigkeit unter einen bestimmten Schwellenwert fällt.
    Die Pumpe für eine festgelegte Zeit (z.B. 20 Sekunden) laufen lässt und dann stoppt.
    Benutzerfreundliche Steuerung und Statusanzeige über eine Web-Oberfläche bietet.

Technische Details

Hardwarekomponenten

    Raspberry Pi 4 – als Steuerzentrale
    Relaismodul – zur Steuerung der Wasserpumpe
    Feuchtigkeitssensor – für die Bodenfeuchtigkeitsmessung
    ADC-Konverter – zur Wandlung der analogen Sensordaten für den Raspberry Pi
    Wasserpumpe – zur Bewässerung der Pflanzen
    Schläuche und Kabel – zur Verbindung der Komponenten

Software-Architektur

    Backend – Eine Python-API mit Flask auf dem Raspberry Pi zur Steuerung des Systems:
        /status: Liefert aktuelle Sensorwerte und den Zustand der Pumpe.
        /control: Startet oder stoppt die Pumpe über HTTP-Anfragen.
        /auto-control : überprüft die Feuchtigkeit alle 5 Stunden und aktiviert die Pumpe bei Bedarf automatisch.
    Frontend – Einfache Web-Oberfläche zur Anzeige des Pumpenstatus und manuellen Steuerung.

Installation & Setup

    Hardware anschließen – Sensoren und Pumpe mit dem Raspberry Pi verbinden.
    Python-Umgebung einrichten – Abhängigkeiten installieren und app.py ausführen.
    API starten – Das Backend kann im lokalen Netzwerk auf Port 5000 erreicht werden.
    Frontend testen – Über einen Browser oder ein REST-Tool wie Postman.

Nutzung

    Manuelle Steuerung – Über die Web-Oberfläche die Pumpe manuell starten/stoppen.
    Automatische Bewässerung – Die Pumpe wird automatisch bei niedrigem Feuchtigkeitswert gestartet.

Nächste Schritte(in der Zukunft)

    Verbesserung der Benutzeroberfläche
    Hinzufügen weiterer Sensoren zur Umgebungsüberwachung
    Optimierung der Feuchtigkeitsschwellen und der Bewässerungsdauer

