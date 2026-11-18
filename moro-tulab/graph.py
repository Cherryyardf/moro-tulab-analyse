import matplotlib.pyplot as plt
import networkx as nx
import math

def draw_conflict_graph():
    # 1. Definition der Themen (Knoten)
    themes = [
        "Wohnen\n(Bedürfnisse)", 
        "Infrastruktur\n(Attraktivität)", 
        "Soziales\n(Qualität)", 
        "Instrumente\n(Recht & Rahmen)", 
        "Kooperation\n(Interkommunal)"
    ]

    # 2. Definition der Konflikte (Verbindungen zwischen den Themen)
    # Format: (Start-Index, End-Index, Konflikt-Text)
    conflicts = [
        (0, 1, "Kosten vs.\nLeistbarkeit"),      # Wohnen <-> Infra
        (0, 3, "Innovation vs.\nVorschrift"),    # Wohnen <-> Instrumente
        (0, 2, "Privatheit vs.\nBegegnung"),     # Wohnen <-> Soziales
        (4, 0, "Kirchturmdenken vs.\nRegionalbedarf"), # Koop <-> Wohnen
        (4, 3, "Autonomie vs.\nVerbindlichkeit"), # Koop <-> Instrumente
        (1, 2, "Rentabilität vs.\nSozialer Nutzen"), # Infra <-> Soziales
    ]

    # Graph initialisieren
    G = nx.Graph()
    
    # 3. Positionierung im Fünfeck (Pentagon)
    pos = {}
    radius = 1.5
    center_x, center_y = 0, 0
    
    # Wir ordnen die 5 Themen im Kreis an (72 Grad Abstand)
    for i, theme in enumerate(themes):
        angle_deg = 90 + i * (360 / len(themes)) # Start bei 90 Grad (oben)
        angle_rad = math.radians(angle_deg)
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        pos[i] = (x, y)
        G.add_node(i, label=theme)

    # Plot erstellen
    plt.figure(figsize=(12, 10))
    ax = plt.gca()
    
    # Kanten (Linien) zeichnen
    for start, end, label in conflicts:
        G.add_edge(start, end)
        
        # Koordinaten für die Linie
        x_start, y_start = pos[start]
        x_end, y_end = pos[end]
        
        # Linie zeichnen (Grau, gestrichelt)
        plt.plot([x_start, x_end], [y_start, y_end], color='gray', linestyle='--', zorder=1, alpha=0.5)
        
        # Text (Konflikt) genau in die Mitte setzen
        mid_x = (x_start + x_end) / 2
        mid_y = (y_start + y_end) / 2
        
        # Textbox für den Konflikt
        plt.text(mid_x, mid_y, label, 
                 horizontalalignment='center', 
                 verticalalignment='center',
                 fontsize=9, 
                 color='red',
                 weight='bold',
                 bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.3', alpha=0.8),
                 zorder=3)

    # Knoten (Themen-Boxen) zeichnen
    for i, (x, y) in pos.items():
        plt.text(x, y, themes[i], 
                 horizontalalignment='center', 
                 verticalalignment='center',
                 fontsize=11, 
                 weight='bold',
                 bbox=dict(facecolor='#e6f2ff', edgecolor='#0052cc', boxstyle='round,pad=1', linewidth=2),
                 zorder=4)

    # Layout-Einstellungen
    plt.axis('off') # Achsen ausblenden
    plt.title("Spannungsfelder im Wohnbau", fontsize=16, pad=20)
    plt.tight_layout()
    
    # Anzeigen
    plt.show()

if __name__ == "__main__":
    draw_conflict_graph()