import json
import random
import sys
import pygame
import time
import os
from gtts import gTTS

# --- FUNCTIES ---
   
def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

def laad_json(bestand):
    """Laadt de data uit het JSON bestand."""
    with open(bestand, 'r', encoding='utf-8') as f:
        return json.load(f)

def speak_polish(text):
    if not text: return
    tts = gTTS(text=text, lang='pl')
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
    zinnen = laad_json('zinnen.json')

def woorden_programma():
    # --- Initialisatie van het wooorden programma ---
    # Inladen van de woorden
    data = laad_json('woorden.json')
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

    def woorden(word_input, word_category):
            if word_input in word_category:
                vertaling = word_category.get(word_input)
                print(f"'{word_input}' is in het Pools: {vertaling}")
                speak_polish(vertaling)
            else:
                print("Dat woord ken ik niet. bekijk de lijst om te zien wat ik weet.")
            return
    
    def category_list(cat_input):
            # Instellingen voor het vakje
            w = 20  # Breedte van elk vakje
            print(f"\n[{cat_input.upper()}]")
            print(f"{'Nederlands':^{w}}    {'Pools':^{w}}|{'Nederlands':^{w}}    {'Pools':^{w}}")
            print("-" * 100)  # Scheidingslijn
            for i, (nl, pl) in enumerate(data[cat_input].items()):
                print(f"{nl:^{w}} -> {pl:^{w}}", end="|")
                if i % 2 == 0:  # Na elke 2 woorden een nieuwe regel
                    print()
            return
    
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
                category_list(cat_input)
                word_input = input("\nWelk woord wil je uit deze categorie horen? (of 'stop' om terug te gaan) : ").strip().lower()
                if word_input == 'stop':
                    break
                elif word_input == 'lijst':
                    clear_screen()
                    category_list(cat_input)
                elif word_input in data[cat_input]:
                    woorden(word_input, data[cat_input])
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
                woorden(word_input, alle_woorden)
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