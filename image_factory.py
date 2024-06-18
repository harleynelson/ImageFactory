import os
import random
import webbrowser
from PIL import Image, ImageEnhance, ImageFilter
import shutil
import yaml
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from multiprocessing import Pool

# List of card names
card_names = [
    '10C', '10D', '10H', '10S', '2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S',
    '5C', '5D', '5H', '5S', '6C', '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
    '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 'KS',
    'QC', 'QD', 'QH', 'QS'
]

# Function to load card images
def load_card_images(deck_path):
    card_images = {}
    card_images_dir = os.path.join(deck_path, 'cards')
    if not os.path.exists(card_images_dir):
        raise FileNotFoundError(f"Cards directory not found in {card_images_dir}")
    for filename in os.listdir(card_images_dir):
        if filename.endswith('.png'):
            card_name = filename[:-4]  # Remove the '.png' extension
            card_images[card_name] = Image.open(os.path.join(card_images_dir, filename)).convert("RGBA")
    return card_images

# Function to generate a random combination of cards
def generate_random_card_combination(args):
    output_image_path, output_label_path, card_images, table_image_path, num_cards, space_between, resize_proportion, brightness_range, grain_range = args

    # Load the table image
    table_image = Image.open(table_image_path).convert("RGBA")
    combined_image = table_image.copy()
    image_size = combined_image.size

    selected_cards = random.sample(list(card_images.keys()), num_cards)

    # Calculate the size of each card based on the resize proportion
    original_card_width = card_images[selected_cards[0]].width
    original_card_height = card_images[selected_cards[0]].height

    card_width = int(original_card_width * resize_proportion)
    card_height = int(original_card_height * resize_proportion)

    total_width = num_cards * card_width + (num_cards - 1) * space_between
    start_x = (image_size[0] - total_width) // 2
    y_position = (image_size[1] - card_height) // 2

    annotations = []

    for i, card_name in enumerate(selected_cards):
        card_image = card_images[card_name].copy()
        # Resize card image based on the resize proportion
        card_image = card_image.resize((card_width, card_height), Image.LANCZOS)

        # Apply brightness variation
        if brightness_range > 0:
            enhancer = ImageEnhance.Brightness(card_image)
            brightness_factor = random.uniform(1 - brightness_range, 1 + brightness_range)
            card_image = enhancer.enhance(brightness_factor)

        # Apply grain variation
        if grain_range > 0:
            grain_amount = random.uniform(0, grain_range)
            noise = Image.effect_noise(card_image.size, grain_amount)
            card_image = Image.composite(card_image, noise.convert('RGBA'), noise)

        # Calculate position for each card
        x_position = start_x + i * (card_width + space_between)

        # Paste card image onto the combined image
        combined_image.paste(card_image, (x_position, y_position), card_image)

        # Calculate bounding box for the annotation
        center_x = (x_position + card_width / 2) / image_size[0]
        center_y = (y_position + card_height / 2) / image_size[1]
        width = card_width / image_size[0]
        height = card_height / image_size[1]

        # Get the class index from the card name
        class_index = card_names.index(card_name)

        annotations.append(f"{class_index} {center_x} {center_y} {width} {height}")

    # Save the combined image
    combined_image.save(output_image_path, format='PNG')

    # Save the annotations
    with open(output_label_path, 'w') as f:
        f.write("\n".join(annotations))

# Function to generate the dataset
def generate_dataset(deck_path, deck_name, num_images, train_split, valid_split, test_split, brightness_range, grain_range, open_directory):
    try:
        card_images = load_card_images(deck_path)
        table_image_path = os.path.join(deck_path, 'table', 'table.png')
        if not os.path.exists(table_image_path):
            raise FileNotFoundError(f"Table image not found in {table_image_path}")
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
        return

    output_dir = os.path.join(deck_path, f'ImageFactory_{deck_name}_{num_images}')
    dirs = ['train/images', 'train/labels', 'valid/images', 'valid/labels', 'test/images', 'test/labels']
    for dir in dirs:
        os.makedirs(os.path.join(output_dir, dir), exist_ok=True)

    splits = {'train': train_split, 'valid': valid_split, 'test': test_split}
    split_counts = {k: int(v * num_images) for k, v in splits.items()}

    args_list = []
    for split, count in split_counts.items():
        for i in range(count):
            output_image_path = os.path.join(output_dir, f'{split}/images/{split}_{i}.png')
            output_label_path = os.path.join(output_dir, f'{split}/labels/{split}_{i}.txt')
            args = (output_image_path, output_label_path, card_images, table_image_path, 5, 30, 0.9, brightness_range, grain_range)
            args_list.append(args)

    # Use multiprocessing to generate images in parallel
    with Pool() as pool:
        pool.map(generate_random_card_combination, args_list)

    # Create the data.yaml file with the desired format
    data = {
        'path': f'../drive/MyDrive/Datasets/ImageFactory_{deck_name}_{num_images}',
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': 52,
        'names': card_names
    }

    with open(os.path.join(output_dir, 'data.yaml'), 'w') as f:
        yaml.dump(data, f, default_flow_style=None)

    # Open the directory if the option is selected
    if open_directory:
        webbrowser.open(output_dir)

# Function to create a new deck
def create_new_deck(deck_name):
    deck_path = os.path.join('deck', deck_name)
    try:
        os.makedirs(os.path.join(deck_path, 'cards'))
        os.makedirs(os.path.join(deck_path, 'table'))
        messagebox.showinfo("Success", f"New deck '{deck_name}' created with 'cards' and 'table' directories.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI for user input
def start_gui():
    def select_deck():
        selected_deck = filedialog.askdirectory(initialdir='ImageFactory/deck', title='Select Deck')
        if selected_deck:
            deck_name = os.path.basename(selected_deck)
            deck_name_var.set(deck_name)
            deck_path_var.set(selected_deck)

    def on_generate():
        deck_name = deck_name_var.get()
        deck_path = deck_path_var.get()
        num_images = int(num_images_entry.get())
        train_split = float(train_split_entry.get())
        valid_split = float(valid_split_entry.get())
        test_split = float(test_split_entry.get())
        brightness_range = brightness_slider.get() / 100
        grain_range = grain_slider.get() / 100
        open_directory = open_directory_var.get()

        generate_dataset(deck_path, deck_name, num_images, train_split, valid_split, test_split, brightness_range, grain_range, open_directory)

    def on_create_deck():
        deck_name = new_deck_name_entry.get()
        if deck_name:
            create_new_deck(deck_name)
        else:
            messagebox.showerror("Error", "Please enter a deck name.")

    def find_decks():
        decks_dir = os.path.join(os.getcwd(), 'deck')
        if not os.path.exists(decks_dir):
            return []
        return [d for d in os.listdir(decks_dir) if os.path.isdir(os.path.join(decks_dir, d))]

    root = tk.Tk()
    root.title("Dataset Generator")

    mainframe = ttk.Frame(root, padding="20")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    deck_name_var = tk.StringVar()
    deck_path_var = tk.StringVar()
    open_directory_var = tk.BooleanVar(value=True)

    section_padding = {'padx': 10, 'pady': 10}

    # Find decks and select one if available
    decks = find_decks()
    if decks:
        deck_name_var.set(decks[0])
        deck_path_var.set(os.path.join(os.getcwd(), 'deck', decks[0]))

    # Select Deck Section
    ttk.Label(mainframe, text="Selected Deck:").grid(row=0, column=0, sticky=tk.W, **section_padding)
    ttk.Label(mainframe, textvariable=deck_name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), **section_padding)
    select_deck_button = ttk.Button(mainframe, text="Select Deck", command=select_deck)
    select_deck_button.grid(row=0, column=2, sticky=tk.W, **section_padding)

    ttk.Separator(mainframe, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

    # Generate Dataset Section
    ttk.Label(mainframe, text="Number of Images:").grid(row=2, column=0, sticky=tk.W, **section_padding)
    num_images_entry = ttk.Entry(mainframe)
    num_images_entry.insert(0, "20")  # Default value
    num_images_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), **section_padding)

    ttk.Label(mainframe, text="Train Split (0-1):").grid(row=3, column=0, sticky=tk.W, **section_padding)
    train_split_entry = ttk.Entry(mainframe)
    train_split_entry.insert(0, "0.7")  # Default value
    train_split_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), **section_padding)

    ttk.Label(mainframe, text="Valid Split (0-1):").grid(row=4, column=0, sticky=tk.W, **section_padding)
    valid_split_entry = ttk.Entry(mainframe)
    valid_split_entry.insert(0, "0.2")  # Default value
    valid_split_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), **section_padding)

    ttk.Label(mainframe, text="Test Split (0-1):").grid(row=5, column=0, sticky=tk.W, **section_padding)
    test_split_entry = ttk.Entry(mainframe)
    test_split_entry.insert(0, "0.1")  # Default value
    test_split_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), **section_padding)

    ttk.Label(mainframe, text="Brightness Variation (0-100%):").grid(row=6, column=0, sticky=tk.W, **section_padding)
    brightness_slider = ttk.Scale(mainframe, from_=0, to_=100, orient=tk.HORIZONTAL)
    brightness_slider.set(15)  # Default value
    brightness_slider.grid(row=6, column=1, sticky=(tk.W, tk.E), **section_padding)
    brightness_value_label = ttk.Label(mainframe, text="15%")
    brightness_value_label.grid(row=6, column=2, sticky=tk.W, **section_padding)
    brightness_slider.config(command=lambda v: brightness_value_label.config(text=f"{int(float(v))}%"))

    ttk.Label(mainframe, text="Grain Variation (0-100%):").grid(row=7, column=0, sticky=tk.W, **section_padding)
    grain_slider = ttk.Scale(mainframe, from_=0, to_=100, orient=tk.HORIZONTAL)
    grain_slider.set(0)  # Default value
    grain_slider.grid(row=7, column=1, sticky=(tk.W, tk.E), **section_padding)
    grain_value_label = ttk.Label(mainframe, text="0%")
    grain_value_label.grid(row=7, column=2, sticky=tk.W, **section_padding)
    grain_slider.config(command=lambda v: grain_value_label.config(text=f"{int(float(v))}%"))
    ttk.Label(mainframe, text="** currently doesn't work **", font=('TkDefaultFont', 8), foreground='gray').grid(row=8,
                                                                                                                 column=1,
                                                                                                                 sticky=tk.W,
                                                                                                                 padx=20)

    ttk.Checkbutton(mainframe, text="Open deck directory after generating dataset", variable=open_directory_var).grid(
        row=9, column=0, columnspan=3, sticky=tk.W, **section_padding)

    generate_button = ttk.Button(mainframe, text="Generate", command=on_generate)
    generate_button.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), **section_padding)

    tk.Label(mainframe, text="Note: a large number of images will lock up the main thread for a while (ie over 300)",
             wraplength=300).grid(row=11, column=0, columnspan=3, sticky=tk.W, **section_padding)

    ttk.Separator(mainframe, orient='horizontal').grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

    # Create Deck Section
    ttk.Label(mainframe, text="New Deck Name:").grid(row=13, column=0, sticky=tk.W, **section_padding)
    new_deck_name_entry = ttk.Entry(mainframe)
    new_deck_name_entry.grid(row=13, column=1, sticky=(tk.W, tk.E), **section_padding)

    create_deck_button = ttk.Button(mainframe, text="Create Deck", command=on_create_deck)
    create_deck_button.grid(row=13, column=2, sticky=(tk.W, tk.E), **section_padding)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    start_gui()
