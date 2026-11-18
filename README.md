# MORO tu!Lab – Analyse zur Wohnraumaktivierung

Analysen, Visualisierungen und Hilfsskripte aus meinem Studium an der RWTH Aachen (2025–2026). Der Kontext ist ein tu!Lab-Projekt im Rahmen eines MORO-Vorhabens (Modellvorhaben der Raumordnung). Das Projekt untersucht, wie sich in Grenzgemeinden mehr Wohnraum aktivieren lässt. Im Mittelpunkt stehen Simmerath (DE) und Raeren (BE) mit ihren Planungsverfahren, Eigentümertypen, Beteiligungsformen und der Bevölkerungsentwicklung.

Aus dem Konzept entstand die Website **BAUKOMPASS**. Sie wird in eigenen Repositories gepflegt und ist deshalb hier nicht enthalten:

- Website: <https://cherryyardf.github.io/>
- Immobilien-Aktivierungs-Tool (Dashboard): <https://cherryyardf.github.io/tool/>

## Inhalt

| Datei | Art | Was sie tut |
|---|---|---|
| `moro-tulab/graph.py` | Python (networkx, matplotlib) | Konfliktgraph: Die fünf Themen Wohnen, Infrastruktur, Soziales, Instrumente und Kooperation stehen im Fünfeck. Die Kanten beschriften Zielkonflikte, z. B. „Kosten vs. Leistbarkeit“ oder „Kirchturmdenken vs. Regionalbedarf“. Er ist die Vorstufe zum Konzept. |
| `konzept-moro-tulab/analyse.html` | HTML (Tailwind, Chart.js) | **Vergleich der Planungsverfahren** im Wohnbau zwischen Simmerath und Raeren. Er zeigt die Planungspyramiden, die Gesamtdauer der Verfahren, System-Metriken sowie Flächennutzung und Zonierung. |
| `konzept-moro-tulab/analyse2.html` | HTML (Tailwind, Chart.js) | Überarbeitete Fassung des Verfahrensvergleichs, unter anderem mit geändertem Zeitdauer-Abschnitt. |
| `konzept-moro-tulab/eigentümertyp.html` | HTML | **Analyse-Raster „Der private Kleineigentümer“**: ein Baum der Eigentümertypen und ihrer Hemmnisse, gestützt auf eine BBSR-Studie zur Umwandlung von Nichtwohngebäuden. |
| `konzept-moro-tulab/Bürger.html` | HTML (Tailwind, Chart.js) | **Mock-up einer Beteiligungs-App „Unser Quartier“** mit Quartiersnachrichten, Leih-Angeboten, Stimmungsbarometer und Abstimmung über Schwerpunkte. |
| `konzept-moro-tulab/Bevölkerungsentwicklung.html` | HTML (Chart.js) | Diagramm der relativen Bevölkerungsentwicklung 2023–2040. |
| `konzept-moro-tulab/Flussdiagramm.html` | Mermaid-Quelltext | Gliederung der Präsentation als Flussdiagramm (Kontext → Analyse → …). Die Datei enthält nur Mermaid-Code und keine HTML-Seite; anzeigen lässt sie sich z. B. im [Mermaid Live Editor](https://mermaid.live). |
| `konzept-moro-tulab/sortier.py` | Python (pandas, openpyxl) | Ergänzt die Excel-Tabelle zum Rechtsvergleich (BauGB, BauNVO, BauO NRW, CoDT) um Zeilen zur Bundesförderung (KfW, BEG, AfA). Die Excel-Dateien selbst sind nicht im Repo. |
| `konzept-moro-tulab/SimmDaten/simmerath_extract.bat` | Batch (GDAL/ogr2ogr) | Schneidet aus einem OSM-Extrakt den Raum Aachen/Eifel/Simmerath aus und filtert die Daten in ein GeoPackage mit den Layern Verkehrsnetz, Versorgungs-POIs und Landnutzung. |

## Benutzung

**HTML-Seiten:** `index.html` (Übersicht) oder direkt die gewünschte Datei im Browser öffnen. Ein Build ist nicht nötig. Tailwind, Chart.js und Google Fonts kommen über ein CDN, deshalb brauchen die Seiten eine Internetverbindung.

**Skripte:**

```text
python moro-tulab/graph.py                          # benötigt networkx, matplotlib
python konzept-moro-tulab/sortier.py --help          # benötigt pandas, openpyxl
konzept-moro-tulab\SimmDaten\simmerath_extract.bat <OSM-Datei.osm.pbf> [Zielordner]
```

Das Batch-Skript braucht `ogr2ogr` im PATH, z. B. aus der OSGeo4W-Shell. Ohne Argumente gibt es seine Hilfe aus.

## Herkunft & Datierung

Die Dateien lagen ursprünglich nicht in Git. Die Historie wurde nachträglich aufgebaut, und jeder Commit gehört zu genau einer von drei Klassen. Welche das ist, steht im Commit selbst:

| Klasse | Commit-Datum | Kennzeichnung im Commit | In diesem Repo |
|---|---|---|---|
| **belegt** | historisch, aus einem unabhängigen Beleg | `Provenance: <Beleg>` | keine |
| **erschlossen** | historisch, aus der Datei-Änderungszeit | `Dating: inferred-from-file-mtime`, `Source:`, je Datei `Provenance: file-mtime …` | 6 Commits (18.11.2025 – 16.01.2026): `graph.py` und die sechs HTML-Dateien |
| **rekonstruiert** | Tag des Imports | `Reconstructed: true` | `sortier.py`, `simmerath_extract.bat` |

Die Ordner-Umbenennung, diese README, `index.html` und alle späteren Änderungen sind normale Commits mit ihrem tatsächlichen Datum.

Zur Einordnung:

- **Erschlossene Daten sind Näherungen.** Die Änderungszeit zeigt, wann eine Datei zuletzt gespeichert wurde, nicht wann die Arbeit begann. Die importierten Dateien wurden byte-genau übernommen.
- **Bereinigte Dateien werden nie rückdatiert.** `sortier.py` und `simmerath_extract.bat` stammen laut Dateizeit vom 17.12.2025. Sie enthielten absolute lokale Pfade und wurden deshalb parametrisiert. Ihre Commits tragen das Datum der Bereinigung.
- **Ordnernamen:** Beim Import hießen die Ordner noch wie im Original (`Konzpet MORO tu!Lab`, `MORO tu!Lab`). Sie wurden danach in URL-taugliche Namen umbenannt.
- Die Commits zeigen den Stand der Dateien, nicht den tatsächlichen Arbeitsverlauf. Zwischenstände, die nicht als Datei erhalten sind, wurden nicht erfunden.
- Die BAUKOMPASS-Website und das Dashboard haben ihre eigene Git-Historie in den oben verlinkten Repositories und sind hier bewusst nicht doppelt enthalten.

## Lizenz

© Lukas Willmy – alle Rechte vorbehalten. Ansicht ausdrücklich erwünscht.
