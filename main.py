import json
import random
import os
import time
import sys
from typing import Optional, Any

import pygame
from gtts import gTTS
from rich.console import Console
from rich.table import Table
from rich import box
import rich

# --- GLOBALE CONFIGURATIE ---
console = Console()

# --- HULPFUNCTIES ---

def clear_screen() -> None:
    """Wist de console output op basis van het besturingssysteem."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_json(bestand: str) -> dict[str, Any]:
    """
    Laadt data uit een JSON-bestand met foutafhandeling.
    
    Args:
        bestand: Pad naar het JSON-bestand.
        
    Returns:
        De ingeladen dictionary.
    """
    try:
        with open(bestand, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"[bold red]Fout:[/bold red] Bestand '{bestand}' niet gevonden.")
        return {}
    except json.JSONDecodeError:
        console.print(f"[bold red]Fout:[/bold red] Bestand '{bestand}' bevat ongeldige JSON.")
        return {}

def speak_polish(text: str, language: str = 'pl') -> None:
    """
    Zet tekst om naar spraak en speelt deze af via Pygame.
    
    Args:
        text: De tekst die uitgesproken moet worden.
        language: De taalcode (standaard 'pl' voor Pools).
    """
    if not text:
        return
        
    try:
        tts = gTTS(text=text, lang=language)
        filename = "temp_audio.mp3"
        tts.save(filename)
        
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
    except Exception as e:
        console.print(f"[dim red]Audio fout: {e}[/dim red]")

def word_translate(word_input: str, word_category: dict[str, str]) -> str:
    """
    Vertaalt een woord op basis van een specifieke categorie-lijst.
    
    Returns:
        De vertaling of "Unknown" als het woord niet bestaat.
    """
    return word_category.get(word_input, "Unknown")

# --- RICH TABEL FUNCTIES ---

def display_categories_tableR(data: dict[str, dict[str, str]]) -> None:
    """Toont categorieën in compacte kolommen zonder onnodige witruimte."""
    if not data:
        return

    # 1. Bepaal de breedte op basis van de langste naam
    max_label_len = max(len(cat) for cat in data.keys())
    # We geven de kolom precies genoeg ruimte, maar niet meer dan dat
    label_width = max(10, max_label_len + 2) 
    
    # Bereken hoeveel sets er op het scherm passen
    # (Nr: 4, Categorie: label_width, Items: 6) + marges
    full_col_set_width = 4 + label_width + 6 + 4
    
    term_width = console.width
    num_columns = max(1, term_width // full_col_set_width)
    
    # Beperk het aantal kolommen tot het aantal items (voor als je er maar 2 hebt)
    num_columns = min(num_columns, len(data))

    # CRUCIAL: expand=False zorgt dat de tabel niet breder wordt dan de kolommen
    table = Table(
        title="[bold green]Beschikbare Categorieën[/bold green]", 
        box=box.ROUNDED, 
        expand=False, 
        padding=(0, 1)
    )
    
    # 2. Kolommen toevoegen
    for _ in range(num_columns):
        table.add_column("Nr.", justify="right", style="dim", width=4)
        table.add_column("Categorie", style="yellow", width=label_width)
        table.add_column("Items", justify="center", style="cyan", width=6)

    items = list(data.items())
    
    # 3. Rijen vullen
    for i in range(0, len(items), num_columns):
        row_data = []
        chunk = items[i : i + num_columns]
        for idx, (cat, woorden) in enumerate(chunk, i + 1):
            row_data.extend([str(idx), cat.capitalize(), str(len(woorden))])
        
        # Alleen rijen toevoegen die echt data bevatten
        if row_data:
            while len(row_data) < num_columns * 3:
                row_data.extend(["", "", ""])
            table.add_row(*row_data)

    console.print(table)

def category_listR(
    cat_input: str, 
    data: dict[str, dict[str, str]], 
    base_lang: str = "Nederlands", 
    trans_lang: str = "Pools"
) -> None:
    """Toont genummerde woorden/zinnen in een tabel, links uitgelijnd."""
    if cat_input not in data:
        console.print(f"[bold yellow]Waarschuwing:[/bold yellow] Categorie '{cat_input}' niet gevonden.")
        return

    items = list(data[cat_input].items())
    
    # Bereken breedtes (rekening houdend met het nummer "99. ")
    max_nl = max((len(nl) for nl, _ in items), default=10) + 4
    max_pl = max((len(pl) for _, pl in items), default=10)
    
    pair_width = max_nl + max_pl + 6
    num_pairs = max(1, console.width // pair_width)

    table = Table(title=f"\n[bold blue]{cat_input.upper()}[/bold blue]", box=box.ROUNDED, expand=False)

    for _ in range(num_pairs):
        table.add_column("Nr.", style="dim", justify="right", width=3)
        table.add_column(base_lang, style="cyan", justify="left", min_width=max_nl - 4)
        table.add_column(trans_lang, style="magenta", justify="left", min_width=max_pl)

    # Vul de rijen
    for i in range(0, len(items), num_pairs):
        row_data = []
        chunk = items[i : i + num_pairs]
        for idx, (nl, pl) in enumerate(chunk, i + 1):
            row_data.extend([str(idx), nl, pl])
        
        while len(row_data) < num_pairs * 3:
            row_data.extend(["", "", ""])
        table.add_row(*row_data)

    console.print(table)

# --- PROGRAMMA ONDERDELEN ---

def toon_woorden_help() -> None:
    """Toont de help-instructies voor de woorden-module."""
    rich.print("\n[bold]Opties voor woorden leren:[/bold]")
    options = {
        "woorden": "Vertaal een woord en hoor de uitspraak.",
        "categorieën": "Bekijk alle beschikbare thema's.",
        "categorie": "Leer woorden binnen een specifiek thema.",
        "willekeurig": "Krijg een willekeurig Pools woord.",
        "stop": "Terug naar het hoofdmenu."
    }
    for cmd, desc in options.items():
        rich.print(f"  [yellow]{cmd:12}[/yellow] : {desc}")

def woorden_programma() -> None:
    """Hoofd-onderdeel voor het leren van losse woorden."""
    data = load_json('woorden.json')
    if not data: return

    # Maak een lijst van categorienamen voor nummer-selectie
    categorielijst = list(data.keys())

    alle_woorden: dict[str, str] = {}
    for cat_data in data.values():
        alle_woorden.update(cat_data)

    while True:
        clear_screen()
        console.print("[bold cyan]--- Woorden Leren ---[/bold cyan]")
        toon_woorden_help()
        
        user_input = input("\nInvoer: ").strip().lower()

        if user_input == 'stop':
            speak_polish("Do widzenia")
            break

        elif user_input in ['categorieën', 'categorieen']:
            clear_screen()
            display_categories_tableR(data)
            input("\nDruk op Enter om terug te gaan.")

        elif user_input == 'categorie':
            clear_screen()
            display_categories_tableR(data)
            cat_choice = input("\nKies een nummer of typ de naam van de categorie: ").strip().lower()
            
            actual_cat = None

            # Check of de gebruiker een nummer heeft ingevoerd
            if cat_choice.isdigit():
                index = int(cat_choice) - 1  # -1 omdat we bij 1 beginnen te tellen in de tabel
                if 0 <= index < len(categorielijst):
                    actual_cat = categorielijst[index]
            else:
                # Zoek op naam (case insensitive) als het geen nummer is
                actual_cat = next((k for k in data if k.lower() == cat_choice), None)
            
            if actual_cat:
                while True:
                    clear_screen()
                    category_listR(actual_cat, data)
                    word_in = input("\nWelk woord wil je horen? (of 'stop'): ").strip().lower()
                    if word_in == 'stop': break
                    
                    if word_in in data[actual_cat]:
                        vertaling = word_translate(word_in, data[actual_cat])
                        rich.print(f"[bold green]{word_in}[/bold green] -> [bold magenta]{vertaling}[/bold magenta]")
                        speak_polish(vertaling)
                        input("Druk op Enter...")
            else:
                rich.print("[red]Ongeldige keuze. Voer een nummer uit de tabel in of de exacte naam.[/red]")
                time.sleep(1.5)

        # ... rest van de elif blokken (willekeurig, woorden) blijven hetzelfde ...
        elif user_input == 'willekeurig':
            while True:
                clear_screen()
                nl, pl = random.choice(list(alle_woorden.items()))
                rich.print(f"\n[bold yellow]Willekeurig:[/bold yellow] {nl} -> [bold cyan]{pl}[/bold cyan]")
                speak_polish(pl)
                if input("\nEnter voor volgende, 'stop' om te stoppen: ").lower() == 'stop':
                    break

        elif user_input == 'woorden':
            while True:
                clear_screen()
                word_in = input("Typ Nederlands woord (of 'stop'): ").strip().lower()
                if word_in == 'stop': break
                vertaling = word_translate(word_in, alle_woorden)
                rich.print(f"'{word_in}' is in het Pools: [bold cyan]{vertaling}[/bold cyan]")
                speak_polish(vertaling)
                input("\nVolgende...")

def zinnen_programma() -> None:
    """Onderdeel voor het leren van zinnen met nummer- en tekstzoekfunctie."""
    data = load_json('zinnen.json')
    if not data: return

    categorielijst = list(data.keys())

    while True:
        clear_screen()
        console.print("[bold magenta]--- Zinnen Leren ---[/bold magenta]")
        display_categories_tableR(data)
        
        cat_choice = input("\nKies categorie (nummer/naam) of 'stop': ").strip().lower()
        if cat_choice == 'stop': break

        actual_cat = None
        if cat_choice.isdigit():
            idx = int(cat_choice) - 1
            if 0 <= idx < len(categorielijst):
                actual_cat = categorielijst[idx]
        else:
            actual_cat = next((k for k in data if k.lower() == cat_choice), None)

        if actual_cat:
            zinnen_in_cat = list(data[actual_cat].items()) # Lijst van (NL, PL) tuples
            
            while True:
                clear_screen()
                category_listR(actual_cat, data)
                
                query = input("\nKies een nummer of typ een deel van de zin (of 'stop'): ").strip().lower()
                if query == 'stop': break
                if not query: continue

                gevonden_nl, gevonden_pl = None, None

                # 1. Zoeken op nummer
                if query.isdigit():
                    zins_index = int(query) - 1
                    if 0 <= zins_index < len(zinnen_in_cat):
                        gevonden_nl, gevonden_pl = zinnen_in_cat[zins_index]
                
                # 2. Zoeken op tekst (als er nog geen nummer-match was)
                if not gevonden_nl:
                    for nl, pl in zinnen_in_cat:
                        if query in nl.lower():
                            gevonden_nl, gevonden_pl = nl, pl
                            break

                if gevonden_nl:
                    rich.print(f"\n[bold green]Geselecteerd:[/bold green]")
                    rich.print(f"[cyan]{gevonden_nl}[/cyan] -> [bold magenta]{gevonden_pl}[/bold magenta]\n")
                    speak_polish(gevonden_pl)
                    input("Druk op Enter...")
                else:
                    rich.print("[red]Geen match gevonden voor deze invoer.[/red]")
                    time.sleep(1.2)
        else:
            rich.print("[red]Categorie niet gevonden.[/red]")
            time.sleep(1)

# --- MAIN ENTRY POINT ---

def main() -> None:
    """De start-functie met extra crash-beveiliging."""
    try:
        # Start het programma
        while True:
            clear_screen()
            console.print("[bold blue]=== Poolse Leerhulp 2026 ===[/bold blue]", justify="center")
            rich.print("\n1) [bold]Woorden[/bold] leren")
            rich.print("2) [bold]Zinnen[/bold] leren")
            rich.print("S) [bold red]Stoppen[/bold red]")
            
            keuze = input("\nKies een optie: ").strip().lower()
            
            if keuze == '1':
                woorden_programma()
            elif keuze == '2':
                zinnen_programma()
            elif keuze == 's':
                break
            elif not keuze:
                continue
            else:
                rich.print("[red]Ongeldige keuze.[/red]")
                time.sleep(1)

    except Exception as e:
        # DIT IS CRUCIAAL: Het houdt de foutmelding op je scherm!
        clear_screen()
        console.print("\n[bold white on red] HET PROGRAMMA IS GECRASHT! [/bold white on red]")
        console.print(f"\n[bold red]Foutmelding:[/bold red] {e}")
        console.print("\n[yellow]Details voor debugging:[/yellow]")
        import traceback
        console.print(traceback.format_exc())
        input("\nDruk op Enter om de terminal te sluiten...")

if __name__ == "__main__":
    main()