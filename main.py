from gettext import translation
import json
import random
import sys
import pygame
import time
import os
from gtts import gTTS
from rich.console import Console
from rich.table import Table
from rich import box

# --- FUNCTIES ---
   
def clear_screen():
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

def load_json(bestand):
    """Laadt de data uit het JSON bestand."""
    with open(bestand, 'r', encoding='utf-8') as f:
        return json.load(f)

def word_translate(word_input, word_category):
        """Translate a Base language word to Translation language using the provided category dictionary."""
        if word_input in word_category:
            translation = word_category.get(word_input)
            return translation
        return ("Unknown")

def category_list(cat_input, list = 'woorden.json', w: int = 20, base_language: str = "Nederlands", translation_language: str = "Pools"):
        """Show a category in a formatted table.
         - cat_input: The category to display.
         - w: The column width (default is 20 characters).
         - base_language: The name of the base language (default is "Nederlands").
         - translation_language: The name of the translation language (default is "Pools").
        """
        data = load_json(list)
        print(f"\n[{cat_input.upper()}]")
        print(f"{base_language:^{w}}    {translation_language:^{w}}|{base_language:^{w}}    {translation_language:^{w}}")
        print("-" * (w * 4 + 7))  # Scheidingslijn
        for i, (nl, pl) in enumerate(data[cat_input].items()):
            print(f"{nl:^{w}} -> {pl:^{w}}", end="|")
            if (i + 1) % 2 == 0:  # After every 2 words, start a new line
                print()
        return

def category_listR(cat_input, list_file='woorden.json', num_columns: int = 2, base_language: str = "Nederlands", translation_language: str = "Pools"):
    """
    Toont een categorie in een prachtig opgemaakte tabel met Rich.
    - num_columns: Hoeveel woordenparen er naast elkaar moeten staan.
    """
    console = Console()
    
    # Data laden (ervan uitgaande dat load_json elders is gedefinieerd)
    try:
        with open(list_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        console.print(f"[bold red]Fout:[/bold red] Bestand {list_file} niet gevonden.")
        return

    if cat_input not in data:
        console.print(f"[bold yellow]Waarschuwing:[/bold yellow] Categorie '{cat_input}' niet gevonden.")
        return

    # Maak de tabel aan
    table = Table(title=f"\n[bold blue]{cat_input.upper()}[/bold blue]", box=box.ROUNDED)

    # Voeg kolommen toe op basis van het gewenste aantal paren
    # We voegen per paar twee kolommen toe (Bron en Vertaling)
    for i in range(num_columns):
        table.add_column(base_language, style="cyan", justify="center")
        table.add_column(translation_language, style="magenta", justify="center")

    # Verzamel de items uit de json
    items = list(data[cat_input].items())
    
    # Verdeel de items in rijen op basis van num_columns
    for i in range(0, len(items), num_columns):
        row_data = []
        # Pak een 'slice' van de data voor deze rij
        current_chunk = items[i : i + num_columns]
        
        for nl, pl in current_chunk:
            row_data.extend([nl, pl])
            
        # Als de laatste rij niet vol is, vul aan met lege strings
        while len(row_data) < num_columns * 2:
            row_data.extend(["", ""])
            
        table.add_row(*row_data)

    console.print(table)

# Voorbeeld van gebruik:
# category_listR("Fruit", num_columns=3)

def speak_polish(text, language: str = 'pl'):
    """Play the given text as speech in the specified language (default is Polish)."""
    if not text: return
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

# --- MAIN PROGRAM ---

def main():
    while True:
        try:
            # Je bestaande code hier, bijvoorbeeld:
            clear_screen()
            print("--- Poolse Leerhulp ---")
            print("1) Woorden leren")
            print("2) Zinnen leren")
            print("S) Stoppen")
            keuze = input("Kies een optie (1 of 2): ").strip()
            if keuze == '1':
                woorden_programma()
            elif keuze == '2':
                zinnen_programma()
            elif keuze == 'S' or keuze == 's':
                print("Programma gestopt.")
                break
            else:
                print("Ongeldige keuze. Start het programma opnieuw.")
        # ... rest van je logica ...
        
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt gedetecteerd.")
            # sys.exit(0)

def zinnen_programma():
    # Inladen van de zinnen
    zinnen = load_json('zinnen.json')

def woorden_programma():
    # --- Initialisatie van het wooorden programma ---
    # Inladen van de woorden
    data = load_json('woorden.json')
    # Maak een platte lijst van alle woorden voor de 'willekeurig' functie
    alle_woorden = {}
    for categorie in data.values():
        alle_woorden.update(categorie)

    # --- Functies binnen het woorden programma ---
    # Instructies:
    def help():
        print("\n--- Woorden leren ---")
        print("Welkom bij de Poolse woorden leerhulp!")
        print("Wat wil je doen? de volgende opties zijn beschikbaar:")
        print("'woorden' om een woord te vertalen en te horen.")
        print("'categorieën' om de beschikbare categorieën te zien.")
        print("'categorie' om woorden van een specifieke categorie te leren.")
        print("'willekeurig' om een willekeurig woord te horen en lezen in het Pools.")
        print("'help' voor deze instructies.")
        print("'stop' om het programma te verlaten.")
          

    
    # print(f"Categorieën beschikbaar: {', '.join(data.keys())}")

    # --- Hoofd loop van het woorden programma ---
    while True:
        clear_screen()
        help()
        user_input = input("\nInvoer: ").strip().lower()

        if user_input == 'stop':
            print("Do widzenia!")
            speak_polish("Do widzenia")
            break

        elif user_input == 'lijst':
            clear_screen()
            for cat, woorden in data.items():
                print(f"\n[{cat.upper()}]")
                for nl, pl in woorden.items():
                    print(f"  {nl} -> {pl}")
            input("\nDruk op Enter om terug te gaan.")
            continue

        elif user_input == 'willekeurig':
            while True:
                clear_screen()
                nl, pl = random.choice(list(alle_woorden.items()))
                print(f"Willekeurig: {nl} -> {pl}")
                speak_polish(pl)
                user_choice = input("Druk op Enter om door te gaan. (Of typ 'stop' om terug te gaan.)\n").strip().lower()
                if user_choice == 'stop':
                    break

        elif user_input == 'categorieën' or user_input == 'categorieen':
            print(f"Categorieën: {', '.join(data.keys())}")
            continue

        elif user_input == 'categorie':
            clear_screen()
            print(f"Beschikbare categorieën:\n {', '.join(data.keys())}")
            cat_input = input("Welke categorie wil je zien? : ").strip().lower()
            while cat_input in data:
                clear_screen()
                # before: category_list(cat_input)
                category_listR(cat_input, num_columns=2)
                word_input = input("\nWelk woord wil je uit deze categorie horen? (of 'stop' om terug te gaan) : ").strip().lower()
                if word_input == 'stop':
                    break
                elif word_input == 'lijst':
                    clear_screen()
                    category_listR(cat_input, num_columns=2)
                elif word_input in data[cat_input]:
                    vertaling = word_translate(word_input, data[cat_input])
                    print(f"'{word_input}' is in het Pools: {vertaling}")
                    speak_polish(vertaling)
                    input("Druk op Enter om door te gaan.")
            else:
                print("Ongeldige categorie. Probeer het opnieuw.")
                input("Druk op Enter om terug te gaan.")    
            continue

        elif user_input == 'help':
            help()
            continue

        elif user_input == 'woorden':
            while True:
                clear_screen()
                print("Typ een Nederlands woord om de Poolse vertaling te horen.")
                # Zoek het woord in de grote lijst
                word_input = input("\nWelk woord? : ").strip().lower()
                vertaling = word_translate(word_input, alle_woorden)
                print(f"'{word_input}' is in het Pools: {vertaling}")
                speak_polish(vertaling)
                another_word = input("Wil je nog een woord vertalen? (ja/nee) ").strip().lower()
                if another_word == 'ja':
                    continue
                else:
                    break
        
        else:
            print("Ongeldige invoer. Typ 'help' voor de opties.")
            continue
        
if __name__ == "__main__":
    main()