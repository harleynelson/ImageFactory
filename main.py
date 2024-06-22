import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font

from factory_helpers import generate_dataset, generate_single_sample, create_new_deck, find_decks

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
        size_variation = size_variation_slider.get() / 100
        open_directory = open_directory_var.get()
        include_active_players = active_players_var.get()
        include_seated_players = seated_players_var.get()
        include_dealer_button = dealer_button_var.get()
        selected_model = model_selector.get()

        generate_dataset(deck_path, deck_name, num_images, train_split, valid_split, test_split, brightness_range,
                         grain_range, size_variation, open_directory, include_active_players, include_seated_players,
                         include_dealer_button, selected_model)

    def on_create_deck():
        deck_name = new_deck_name_entry.get()
        if deck_name:
            create_new_deck(deck_name)
        else:
            messagebox.showerror("Error", "Please enter a deck name.")

    def on_generate_sample():
        deck_name = deck_name_var.get()
        deck_path = deck_path_var.get()
        brightness_range = brightness_slider.get() / 100
        grain_range = grain_slider.get() / 100
        size_variation = size_variation_slider.get() / 100
        open_directory = open_directory_var.get()
        include_active_players = active_players_var.get()
        include_seated_players = seated_players_var.get()
        include_dealer_button = dealer_button_var.get()
        selected_model = model_selector.get()

        generate_single_sample(deck_path, deck_name, brightness_range, grain_range, size_variation, open_directory,
                               include_active_players, include_seated_players, include_dealer_button, selected_model)

    def on_seated_players_checked():
        if not seated_players_var.get():
            active_players_checkbutton.state(['disabled'])
            active_players_var.set(False)
            dealer_button_checkbutton.state(['disabled'])
            dealer_button_var.set(False)
        else:
            active_players_checkbutton.state(['!disabled'])
            dealer_button_checkbutton.state(['!disabled'])

    root = tk.Tk()
    root.title("Dataset Generator")

    mainframe = ttk.Frame(root, padding="20")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    deck_name_var = tk.StringVar()
    deck_path_var = tk.StringVar()
    open_directory_var = tk.BooleanVar(value=True)
    active_players_var = tk.BooleanVar(value=True)
    seated_players_var = tk.BooleanVar(value=True)
    dealer_button_var = tk.BooleanVar(value=True)

    section_padding = {'padx': 10, 'pady': 10}

    bold_font = Font(size=10, weight="bold")

    decks = find_decks()
    if decks:
        deck_name_var.set(decks[0])
        deck_path_var.set(os.path.join(os.getcwd(), 'deck', decks[0]))

    # Select Deck Section
    ttk.Label(mainframe, textvariable=deck_name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), **section_padding)
    select_deck_button = ttk.Button(mainframe, text="Select Deck", command=select_deck)
    select_deck_button.grid(row=0, column=0, sticky=tk.W, **section_padding)

    ttk.Separator(mainframe, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

    ttk.Label(mainframe, text="Number of Images:").grid(row=2, column=0, sticky=tk.W, **section_padding)
    num_images_entry = ttk.Entry(mainframe)
    num_images_entry.insert(0, "20")  # Default value
    num_images_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), **section_padding)

    # Generate Dataset Section
    ttk.Label(mainframe, text="Splits", font=bold_font).grid(row=3, column=0, columnspan=3, sticky=tk.W,
                                                             **section_padding)

    ttk.Label(mainframe, text="Train Split (0-1):").grid(row=4, column=0, sticky=tk.W, **section_padding)
    train_split_entry = ttk.Entry(mainframe)
    train_split_entry.insert(0, "0.7")  # Default value
    train_split_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), **section_padding)

    ttk.Label(mainframe, text="Valid Split (0-1):").grid(row=5, column=0, sticky=tk.W, **section_padding)
    valid_split_entry = ttk.Entry(mainframe)
    valid_split_entry.insert(0, "0.2")  # Default value
    valid_split_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), **section_padding)

    ttk.Label(mainframe, text="Test Split (0-1):").grid(row=6, column=0, sticky=tk.W, **section_padding)
    test_split_entry = ttk.Entry(mainframe)
    test_split_entry.insert(0, "0.1")  # Default value
    test_split_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), **section_padding)

    ttk.Label(mainframe, text="Variations", font=bold_font).grid(row=7, column=0, columnspan=3, sticky=tk.W, **section_padding)

    ttk.Label(mainframe, text="Brightness Variation (0-100%):").grid(row=8, column=0, sticky=tk.W, **section_padding)
    brightness_slider = ttk.Scale(mainframe, from_=0, to_=100, orient=tk.HORIZONTAL)
    brightness_slider.set(15)  # Default value
    brightness_slider.grid(row=8, column=1, sticky=(tk.W, tk.E), **section_padding)
    brightness_value_label = ttk.Label(mainframe, text="15%")
    brightness_value_label.grid(row=8, column=2, sticky=tk.W, **section_padding)
    brightness_slider.config(command=lambda v: brightness_value_label.config(text=f"{int(float(v))}%"))

    ttk.Label(mainframe, text="Grain Variation (0-100%):").grid(row=9, column=0, sticky=tk.W, **section_padding)
    grain_slider = ttk.Scale(mainframe, from_=0, to_=100, orient=tk.HORIZONTAL)
    grain_slider.set(0)  # Default value
    grain_slider.grid(row=9, column=1, sticky=(tk.W, tk.E), **section_padding)
    grain_value_label = ttk.Label(mainframe, text="0%")
    grain_value_label.grid(row=9, column=2, sticky=tk.W, **section_padding)
    grain_slider.config(command=lambda v: grain_value_label.config(text=f"{int(float(v))}%"))

    ttk.Label(mainframe, text="Size Variation (0-100%):").grid(row=10, column=0, sticky=tk.W, **section_padding)
    size_variation_slider = ttk.Scale(mainframe, from_=0, to_=100, orient=tk.HORIZONTAL)
    size_variation_slider.set(20)  # Default value
    size_variation_slider.grid(row=10, column=1, sticky=(tk.W, tk.E), **section_padding)
    size_variation_value_label = ttk.Label(mainframe, text="20%")
    size_variation_value_label.grid(row=10, column=2, sticky=tk.W, **section_padding)
    size_variation_slider.config(command=lambda v: size_variation_value_label.config(text=f"{int(float(v))}%"))

    ttk.Label(mainframe, text="Table Features", font=bold_font).grid(row=11, column=0, columnspan=3, sticky=tk.W, **section_padding)

    ttk.Checkbutton(mainframe, text="Seated Players", variable=seated_players_var,
                    command=on_seated_players_checked).grid(row=12, column=0, sticky=tk.W, **section_padding)
    active_players_checkbutton = ttk.Checkbutton(mainframe, text="Active Players", variable=active_players_var)
    active_players_checkbutton.grid(row=13, column=0, sticky=tk.W, padx=40, pady=0)
    dealer_button_checkbutton = ttk.Checkbutton(mainframe, text="Dealer Button", variable=dealer_button_var)
    dealer_button_checkbutton.grid(row=14, column=0, sticky=tk.W, padx=40, pady=0)

    # Model Selector
    ttk.Label(mainframe, text="Select Model:").grid(row=15, column=0, sticky=tk.W, **section_padding)
    model_selector = ttk.Combobox(mainframe, values=["yolov8", "yolov5"])
    model_selector.grid(row=15, column=1, sticky=(tk.W, tk.E), **section_padding)
    model_selector.current(0)  # Set default to yolov8

    ttk.Label(mainframe, text="").grid(row=16, column=0, columnspan=1, sticky=(tk.W, tk.E), pady=5)
    # Create a frame to hold the buttons
    button_frame = ttk.Frame(mainframe)
    button_frame.grid(row=17, column=0, columnspan=3, pady=5)

    # Create and place the buttons within the frame
    generate_sample_button = ttk.Button(button_frame, text="Generate Sample", command=on_generate_sample)
    generate_sample_button.grid(row=0, column=0, padx=5)

    generate_button = ttk.Button(button_frame, text="Generate Entire Dataset", command=on_generate)
    generate_button.grid(row=0, column=1, padx=5)

    # Center the frame within the mainframe
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid(row=17, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

    ttk.Checkbutton(mainframe, text="Open deck directory after generating dataset", variable=open_directory_var).grid(
        row=18, column=0, columnspan=3, sticky=tk.W, padx=50, pady=10)

    tk.Label(mainframe,
             text="Note: a large number of images (like 1000+) might lock up the main thread for a while too",
             wraplength=300).grid(row=19, column=0, columnspan=3, sticky=tk.W, padx=50, pady=10)

    ttk.Separator(mainframe, orient='horizontal').grid(row=20, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

    # Create Deck Section
    ttk.Label(mainframe, text="New Deck Name:").grid(row=21, column=0, sticky=tk.W, **section_padding)
    new_deck_name_entry = ttk.Entry(mainframe)
    new_deck_name_entry.grid(row=21, column=1, sticky=(tk.W, tk.E), **section_padding)

    create_deck_button = ttk.Button(mainframe, text="Create Deck", command=on_create_deck)
    create_deck_button.grid(row=21, column=2, sticky=(tk.W, tk.E), **section_padding)

    root.mainloop()


if __name__ == "__main__":
    start_gui()