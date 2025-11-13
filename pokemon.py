import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Fetch a list of Pokémon
def get_pokemon_list(limit=20):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url).json()
    return response['results']  # List of dicts: {'name': ..., 'url': ...}

# Fetch details for one Pokémon
def fetch_pokemon_details(url):
    response = requests.get(url).json()
    name = response['name'].title()
    poke_id = response['id']
    types = ', '.join([t['type']['name'].title() for t in response['types']])
    abilities = ', '.join([a['ability']['name'].title() for a in response['abilities']])
    image_url = response['sprites']['front_default']
    
    img_data = requests.get(image_url).content
    img = Image.open(BytesIO(img_data)).resize((150, 150))
    img_tk = ImageTk.PhotoImage(img)
    
    # Display details
    label_name.config(text=f"Name: {name}")
    label_id.config(text=f"ID: {poke_id}")
    label_types.config(text=f"Types: {types}")
    label_abilities.config(text=f"Abilities: {abilities}")
    label_image.config(image=img_tk)
    label_image.image = img_tk

# Create main window
root = tk.Tk()
root.title("Pokédex")
root.geometry("800x500")

# Left frame: Pokémon cards
frame_cards = tk.Frame(root)
frame_cards.pack(side="left", fill="both", expand=True)

# Right frame: Pokémon details
frame_details = tk.Frame(root, width=300)
frame_details.pack(side="right", fill="y")

label_name = tk.Label(frame_details, text="Name: ", font=("Arial", 12))
label_name.pack(pady=5)
label_id = tk.Label(frame_details, text="ID: ", font=("Arial", 12))
label_id.pack(pady=5)
label_types = tk.Label(frame_details, text="Types: ", font=("Arial", 12))
label_types.pack(pady=5)
label_abilities = tk.Label(frame_details, text="Abilities: ", font=("Arial", 12))
label_abilities.pack(pady=5)
label_image = tk.Label(frame_details)
label_image.pack(pady=10)

# Load Pokémon list and create cards
pokemons = get_pokemon_list(20)
card_images = []  # Keep reference to images

for i, p in enumerate(pokemons):
    # Fetch small image for card
    data = requests.get(p['url']).json()
    img_url = data['sprites']['front_default']
    img_data = requests.get(img_url).content
    img = Image.open(BytesIO(img_data)).resize((80, 80))
    img_tk = ImageTk.PhotoImage(img)
    card_images.append(img_tk)  # prevent garbage collection

    # Create card button
    btn = tk.Button(frame_cards, text=p['name'].title(), image=img_tk, compound="top",
                    command=lambda url=p['url']: fetch_pokemon_details(url))
    btn.grid(row=i//4, column=i%4, padx=5, pady=5)

root.mainloop()
