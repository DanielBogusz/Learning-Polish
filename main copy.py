import json
import random
import pygame
import time
import os
from gtts import gTTS

# --- FUNCTIES ---

def laad_woorden():
    """Laadt de woorden uit het JSON bestand."""
    with open('woorden.json', 'r', encoding='utf-8') as f:
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
    # Inladen van de data
    data = laad_woorden()
    
    # Maak een platte lijst van alle woorden voor de 'willekeurig' functie
    alle_woorden = {}
    for categorie in data.values():
        alle_woorden.update(categorie)

    print("--- Poolse Leerhulp ---")
    print(f"Categorieën beschikbaar: {', '.join(data.keys())}")
    print("Typ een woord, 'willekeurig', 'lijst' of 'stop'.")

    while True:
        user_input = input("\nInvoer: ").strip().lower()

        if user_input == 'stop':
            print("Do widzenia!")
            speak_polish("Do widzenia")
            break

        elif user_input == 'lijst':
            for cat, woorden in data.items():
                print(f"\n[{cat.upper()}]")
                for nl, pl in woorden.items():
                    print(f"  {nl} -> {pl}")
            continue

        elif user_input == 'willekeurig':
            nl, pl = random.choice(list(alle_woorden.items()))
            print(f"Willekeurig: {nl} -> {pl}")
            speak_polish(pl)
            continue

        # Zoek het woord in de grote lijst
        vertaling = alle_woorden.get(user_input)
        if vertaling:
            print(f"'{user_input}' is in het Pools: {vertaling}")
            speak_polish(vertaling)
        else:
            print("Dat woord ken ik niet. Typ 'lijst' om te zien wat ik weet.")

if __name__ == "__main__":
    main()