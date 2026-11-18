"""Ergänzt die Excel-Tabelle zum Rechtsvergleich um Zeilen zur Bundesförderung.

Beispiel:
    python sortier.py --ordner "D:\\Daten\\Rechtsvergleich"
    python sortier.py --ordner . --ausgabe Ergebnis.xlsx --pause
"""
import argparse
import openpyxl
from copy import copy
import os
import sys
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

# --- KONFIGURATION (über Kommandozeilen-Argumente, siehe parse_args) ---
base_path = input_filename = fallback_filename = output_filename = None
input_path = fallback_path = output_path = None


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Ergänzt die Rechtsvergleich-Tabelle (Excel) um Zeilen zur "
                    "Bundesförderung und speichert das Ergebnis als neue Datei.")
    parser.add_argument("--ordner", default=".",
                        help="Arbeitsordner mit den Excel-Dateien (Standard: aktueller Ordner). "
                             "Relative Dateinamen unten beziehen sich auf diesen Ordner.")
    parser.add_argument("--eingabe", default="Rechtsvergleich_KOMPLETT.xlsx",
                        help="Basis-Datei aus dem vorherigen Schritt (Standard: %(default)s)")
    parser.add_argument("--fallback", default="Rechtsvergleich_FINAL_MIT_QUELLEN.xlsx",
                        help="Wird verwendet, wenn die Basis-Datei fehlt (Standard: %(default)s)")
    parser.add_argument("--ausgabe", default="Rechtsvergleich_FINAL_ALL_LAYERS.xlsx",
                        help="Name der Ergebnisdatei (Standard: %(default)s)")
    parser.add_argument("--pause", action="store_true",
                        help="Am Ende auf Enter warten (praktisch beim Start per Doppelklick)")
    return parser.parse_args(argv)


def configure(args):
    global base_path, input_filename, fallback_filename, output_filename
    global input_path, fallback_path, output_path
    base_path = args.ordner
    input_filename = args.eingabe
    fallback_filename = args.fallback
    output_filename = args.ausgabe
    input_path = os.path.join(base_path, input_filename)
    fallback_path = os.path.join(base_path, fallback_filename)
    output_path = os.path.join(base_path, output_filename)

# --- DIE NEUEN DATEN (Bundesebene) ---
# Struktur: [Thema, BauGB (Bund), BauNVO, BauO NRW, CoDT, Kommentar, Quelle]

new_bund_data = [
    [
        "Neubau-Impuls (Bauüberhang)", 
        "Wiederaufnahme EH 55 (ab 12/2025)", 
        "", "", "", 
        "Aktivierung genehmigter, aber ruhender Projekte. Zinsverbilligung + 5% Direktzuschuss für Kommunen. Bedingung: Kein fossiles Heizen.", 
        "Förderungen über KfW hinaus.pdf (Abschnitt 1)"
    ],
    [
        "Kostengünstiges Bauen", 
        "KNN - Niedrigpreissegment (KfW 296)", 
        "", "", "", 
        "Fokus auf Flächeneffizienz (statt nur Dämmung). Baukostenobergrenze 2025 erhöht; Küchen zählen nun als Aufenthaltsraum (gut für kleine WE).", 
        "Förderungen über KfW hinaus.pdf (Abschnitt 1)"
    ],
    [
        "Familienförderung (Bund)", 
        "WEF - Wohneigentum für Familien (KfW 300)", 
        "", "", "", 
        "Einkommensgrenze: 90.000 EUR + 10k pro Kind. Zinsen ab 0,01% für klimafreundlichen Neubau.", 
        "Förderungen über KfW hinaus.pdf (Abschnitt 1)"
    ],
    [
        "Steuerliche Hebel (Investoren)", 
        "Degressive AfA & Sonder-AfA (§ 7b EStG)", 
        "", "", "", 
        "Massiver Anreiz: 5% Abschreibung über 6 Jahre (degressiv). Zusätzlich 5% Sonder-AfA für EH 40 möglich.", 
        "Förderungen über KfW hinaus.pdf (Abschnitt 1, AfA)"
    ],
    [
        "Bestandserwerb (Bundes-Pendant)", 
        "Jung kauft Alt (KfW 308)", 
        "", "", "", 
        "Erwerb von F/G/H-Klassen. Strenger als NRW: Sanierungspflicht auf EH 85 EE binnen 54 Monaten zwingend.", 
        "Förderungen über KfW hinaus.pdf (Abschnitt 2)"
    ],
    [
        "Genossenschaften", 
        "KfW 134 (Anteilsfinanzierung)", 
        "", "", "", 
        "Kredit für Genossenschaftsanteile inkl. 7,5% Tilgungszuschuss (geschenktes Geld). Alternative zum Eigentum.", 
        "Förderungen über KfW hinaus.pdf (Abschnitt 2)"
    ],
    [
        "Sanierung: Heizung & Hülle", 
        "BEG EM (KfW 458 / BAFA)", 
        "", "", "", 
        "Heizungstausch: Bis zu 70% Zuschuss (KfW). Gebäudehülle: 15-20% Zuschuss (BAFA). Kombinierbar.", 
        "Förderungen über KfW hinaus.pdf (Abschnitt 3)"
    ]
]

def run_bund_update():
    print(f"--- UPDATE BUNDESFÖRDERUNG ---")
    
    # Datei-Auswahl-Logik
    if os.path.exists(input_path):
        current_file = input_path
        print(f"Nutze Basis-Datei: {input_filename}")
    elif os.path.exists(fallback_path):
        current_file = fallback_path
        print(f"Nutze Fallback-Datei: {fallback_filename}")
    else:
        print("FEHLER: Keine Vorläufer-Datei gefunden. Bitte führen Sie den vorherigen Schritt aus.")
        return False

    try:
        # Laden der Excel
        try:
            wb = openpyxl.load_workbook(current_file)
            ws = wb.active
        except:
            # Fallback falls Pandas nötig ist
            df = pd.read_excel(current_file)
            wb = openpyxl.Workbook()
            ws = wb.active
            for r in dataframe_to_rows(df, index=False, header=True):
                ws.append(r)

        start_row = ws.max_row
        print(f"Füge {len(new_bund_data)} Zeilen Bundesförderung hinzu...")

        # Daten schreiben
        for i, row_data in enumerate(new_bund_data):
            current_row = start_row + 1 + i
            for col_idx, value in enumerate(row_data, start=1):
                cell = ws.cell(row=current_row, column=col_idx, value=value)
                
                # Style kopieren (von der letzten existierenden Zeile)
                if start_row > 1:
                    try:
                        source_cell = ws.cell(row=start_row, column=col_idx)
                        if source_cell.has_style:
                            cell.font = copy(source_cell.font)
                            cell.border = copy(source_cell.border)
                            cell.alignment = openpyxl.styles.Alignment(wrap_text=True, vertical='top')
                    except: pass

        # Speichern
        wb.save(output_path)
        print("-" * 40)
        print(f"ERFOLG! Datei gespeichert: {output_filename}")
        print("-" * 40)
        return True

    except PermissionError:
        print("\nFEHLER: Die Excel-Datei ist noch geöffnet. Bitte schließen!")
    except Exception as e:
        print(f"\nFEHLER: {e}")
    return False

if __name__ == "__main__":
    args = parse_args()
    configure(args)
    ok = run_bund_update()
    if args.pause:
        print("\n")
        input("Drücken Sie Enter zum Beenden...")
    sys.exit(0 if ok else 1)