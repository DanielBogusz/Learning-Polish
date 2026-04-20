from tkinter.filedialog import test
from gtts import gTTS
import random
import pygame
import time

# A dictionary of Polish words
polish_text = {
    "1": "jeden",
    "2": "dwa",
    "3": "trzy",
    "4": "cztery",
    "5": "pięć",
    "6": "sześć",
    "7": "siedem",
    "8": "osiem",
    "9": "dziewięć",
    "10": "dziesięć",
    "hallo": "cześć",
    "dankjewel": "dziękuję",
    "tot ziens": "do widzenia",
    "hoe gaat het?": "jak się masz?",
    "eet smakelijk": "smacznego",
    "proost": "na zdrowie",
    "welkom": "witamy",
    "goedemorgen": "dzień dobry",
    "goedenavond": "dobry wieczór",
    "goedenacht": "dobranoc",
    "alsjeblieft": "proszę",
    "sorry": "przepraszam",
    "ik hou van je": "kocham cię",
    "vriend": "przyjaciel",
    "familie": "rodzina",
    "school": "szkoła",
    "werk": "praca",
    "huis": "dom",
    "auto": "samochód",
    "fiets": "rower",
    "boek": "książka",
    "computer": "komputer",
    "telefoon": "telefon",
    "water": "woda",
    "eten": "jedzenie",
    "drinken": "picie",
    "vriendelijk": "przyjazny",
    "mooi": "piękny",
    "slecht": "zły",
    "groot": "duży",
    "klein": "mały",
    "snel": "szybki",
    "langzaam": "wolny",
    "nieuw": "nowy",
    "oud": "stary",
    "goed": "dobry",
    "wat": "co",
    "waar": "gdzie",
    "wie": "kto",
    "wanneer": "kiedy",
    "waarom": "dlaczego",
    "hoe": "jak",
    "ja": "tak",
    "nee": "nie",
    "misschien": "może",
    "altijd": "zawsze",
    "nooit": "nigdy"
}

def speak_polish(text):
    # 1. Generate the audio
    tts = gTTS(text=text, lang='pl')
    filename = "temp_audio.mp3"
    tts.save(filename)

    # 2. Initialize the mixer
    pygame.mixer.init()
    
    # 3. Load and Play
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # 4. Wait for it to finish so the script doesn't close too early
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # 5. Clean up (Optional: unload so you can delete the file later)
    pygame.mixer.music.unload()

def get_polish_word(text):
    polish = polish_text.get(text)
    
    if text:
        print(f"'{text}' in het Pools is: {polish}")
        speak_polish(polish)
    else:
        print("Dat woord of getal ken ik nog niet!")


if __name__ == "__main__":
    # Try it out!
    while True:
        user_input = str(input("Voer een Woord of getal in (zoals, 1-10): "))
        # Stop de loop als de gebruiker 'quit' typt
        if user_input == 'willekeurig':
            # Kies een willekeurige key uit de dictionary
            text = random.choice(list(polish_text.keys()))
            word = polish_text[text]
            print(f"Willekeurig gekozen: {text} -> {word}")
            speak_polish(word)
            continue # Spring terug naar het begin van de loop
        if user_input == 'stop':
            print("Do widzenia! (Tot ziens!)")
            speak_polish("Do widzenia!")
            break
        get_polish_word(user_input)





