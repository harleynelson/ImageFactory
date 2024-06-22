import os
import random
import webbrowser
from PIL import Image, ImageEnhance
from multiprocessing import Pool
from tqdm import tqdm
from models import yolov8, yolov5

card_names = [
    '10C', '10D', '10H', '10S', '2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S',
    '5C', '5D', '5H', '5S', '6C', '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
    '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 'KS',
    'QC', 'QD', 'QH', 'QS'
]

model_modules = {
    'yolov8': yolov8,
    'yolov5': yolov5
}

def load_card_images(deck_path):
    card_images = {}
    card_images_dir = os.path.join(deck_path, 'assets', 'cards')
    if not os.path.exists(card_images_dir):
        raise FileNotFoundError(f"Cards directory not found in {card_images_dir}")
    for filename in os.listdir(card_images_dir):
        if filename.endswith('.png'):
            card_name = filename[:-4]
            card_images[card_name] = Image.open(os.path.join(card_images_dir, filename)).convert("RGBA")
    return card_images

def generate_single_sample(deck_path, deck_name, brightness_range, grain_range, size_variation, open_directory, include_active_players, include_seated_players, include_dealer_button, selected_model):
    try:
        card_images = load_card_images(deck_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    output_dir = os.path.join(deck_path, f'generated_datasets/ImageFactory_{deck_name}_{selected_model}_sample')
    os.makedirs(output_dir, exist_ok=True)

    output_image_path = os.path.join(output_dir, 'sample_image.png')
    output_label_path = os.path.join(output_dir, 'sample_label.txt')
    args = (
        output_image_path, output_label_path, card_images, None, 5, 40, 0.9, brightness_range, grain_range, size_variation, deck_path, include_active_players, include_seated_players, include_dealer_button, selected_model
    )

    generate_random_card_combination(*args)

    if open_directory:
        webbrowser.open(output_dir)

def generate_dataset(deck_path, deck_name, num_images, train_split, valid_split, test_split, brightness_range,
                     grain_range, size_variation, open_directory, include_active_players, include_seated_players, include_dealer_button, selected_model):
    try:
        card_images = load_card_images(deck_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    output_dir = os.path.join(deck_path, f'generated_datasets/ImageFactory_{deck_name}_{selected_model}_{num_images}')
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
            args = (output_image_path, output_label_path, card_images, None, 5, 40, 0.9, brightness_range, grain_range,
                    size_variation, deck_path, include_active_players, include_seated_players, include_dealer_button, selected_model)
            args_list.append(args)

    with Pool() as pool:
        for _ in tqdm(pool.imap_unordered(generate_random_card_combination_wrapper, args_list), total=len(args_list)):
            pass

    model_module = model_modules[selected_model]
    model_module.save_annotations_and_metadata(output_dir, card_names, include_dealer_button, include_active_players, include_seated_players, deck_name, selected_model, num_images)

    if open_directory:
        webbrowser.open(output_dir)

def generate_random_card_combination_wrapper(args):
    generate_random_card_combination(*args)

def create_new_deck(deck_name):
    deck_path = os.path.join('deck', deck_name)
    try:
        os.makedirs(os.path.join(deck_path, 'assets', 'cards'))
        os.makedirs(os.path.join(deck_path, 'assets', 'table'))
        os.makedirs(os.path.join(deck_path, 'assets', 'players', 'active'))
        os.makedirs(os.path.join(deck_path, 'assets', 'players', 'seated'))
        print(
            f"New deck '{deck_name}' created with 'cards', 'table', 'players/active', and 'players/seated' directories.")
        webbrowser.open(deck_path)  # Open the new deck directory
    except Exception as e:
        print(f"Error: {e}")

def load_player_images(deck_path):
    seated_images = []
    active_image = None
    dealer_button = None

    seated_dir = os.path.join(deck_path, 'assets', 'players', 'seated')
    active_path = os.path.join(deck_path, 'assets', 'players', 'active', 'PlayerActive.png')
    dealer_path = os.path.join(deck_path, 'assets', 'table', 'DealerButton.png')

    if not os.path.exists(seated_dir) or not os.path.exists(active_path) or not os.path.exists(dealer_path):
        raise FileNotFoundError("One of the required directories or files for players is missing.")

    for filename in os.listdir(seated_dir):
        if filename.endswith('.png'):
            seated_images.append(Image.open(os.path.join(seated_dir, filename)).convert("RGBA"))

    active_image = Image.open(active_path).convert("RGBA")
    dealer_button = Image.open(dealer_path).convert("RGBA")

    return seated_images, active_image, dealer_button

def generate_random_gradient(image_size):
    def random_color_within_range(base_color, variation):
        return tuple(
            max(0, min(255, base_color[i] + random.randint(-variation, variation))) for i in range(3)
        )

    base_color = tuple(random.randint(50, 100) for _ in range(3))  # base darker color
    variation = 25  # variation range to keep colors close

    start_color = random_color_within_range(base_color, variation)
    end_color = random_color_within_range(base_color, variation)

    base = Image.new('RGBA', image_size, start_color)
    top = Image.new('RGBA', image_size, end_color)
    mask = Image.new('L', image_size)
    mask_data = []

    for y in range(image_size[1]):
        mask_data.extend([int(255 * (y / image_size[1]))] * image_size[0])
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def generate_random_card_combination(output_image_path, output_label_path, card_images, _, num_cards, space_between, resize_proportion, brightness_range, grain_range, size_variation, deck_path, include_active_players, include_seated_players, include_dealer_button, selected_model):
    image_size = (1024, 768)  # Set your desired image size
    combined_image = generate_random_gradient(image_size)

    selected_cards = random.sample(list(card_images.keys()), num_cards)
    annotations = []

    def apply_filters(image, brightness_range, size_variation):
        actual_resize_proportion = random.uniform(1 - size_variation, 1 + size_variation)
        new_width = int(image.width * actual_resize_proportion)
        new_height = int(image.height * actual_resize_proportion)
        image = image.resize((new_width, new_height), Image.LANCZOS)

        if brightness_range > 0:
            enhancer = ImageEnhance.Brightness(image)
            brightness_factor = random.uniform(1 - brightness_range, 1 + brightness_range)
            image = enhancer.enhance(brightness_factor)

        return image

    space_between += 10  # Increase spacing between cards

    for i, card_name in enumerate(selected_cards):
        card_image = card_images[card_name].copy()
        card_image = apply_filters(card_image, brightness_range, size_variation)

        card_width, card_height = card_image.size
        x_position = (image_size[0] - num_cards * (card_width + space_between)) // 2 + i * (card_width + space_between)
        y_position = (image_size[1] - card_height) // 2
        combined_image.paste(card_image, (x_position, y_position), card_image)

        center_x = (x_position + card_width / 2) / image_size[0]
        center_y = (y_position + card_height / 2) / image_size[1]
        width = card_width / image_size[0]
        height = card_height / image_size[1]
        class_index = card_names.index(card_name)
        annotations.append(f"{class_index} {center_x} {center_y} {width} {height}")

    seated_images, active_image, dealer_button = load_player_images(deck_path)

    player_seated_class_index = len(card_names)  # Assuming PlayerSeated is the next class index after cards
    player_active_class_index = len(card_names) + 1  # Assuming PlayerActive is the next class index after PlayerSeated
    dealer_button_class_index = len(card_names) + 2  # Assuming DealerButton is the next class index after PlayerActive

    if include_seated_players:
        num_seated = random.randint(2, 6)
        slots = [
            ("top_left", (image_size[0] // 8, 180)),
            ("top_middle", (image_size[0] // 2, 150)),
            ("top_right", (7 * image_size[0] // 8, 180)),
            ("bottom_left", (image_size[0] // 8, image_size[1] - 180)),
            ("bottom_middle", (image_size[0] // 2, image_size[1] - 100)),
            ("bottom_right", (7 * image_size[0] // 8, image_size[1] - 180))
        ]

        random.shuffle(slots)
        selected_slots = slots[:num_seated]

        seated_positions = []
        for slot, (seat_x, seat_y) in selected_slots:
            seated_image = seated_images[selected_slots.index((slot, (seat_x, seat_y))) % len(seated_images)]
            seated_image = apply_filters(seated_image, brightness_range, size_variation)

            combined_image.paste(seated_image, (seat_x - seated_image.width // 2, seat_y - seated_image.height // 2), seated_image)

            center_x = (seat_x) / image_size[0]
            center_y = (seat_y) / image_size[1]
            width = seated_image.width / image_size[0]
            height = seated_image.height / image_size[1]
            annotations.append(f"{player_seated_class_index} {center_x} {center_y} {width} {height}")

            seated_positions.append((seat_x, seat_y, seated_image.width, seated_image.height, slot))

    if include_active_players:
        for (seat_x, seat_y, seat_width, seat_height, slot) in seated_positions:
            if random.choice([True, False]):
                active_x = seat_x - active_image.width // 2
                active_y = seat_y - active_image.height - seat_height // 2 - 20
                active_image_filtered = apply_filters(active_image.copy(), brightness_range, size_variation)
                combined_image.paste(active_image_filtered, (active_x, active_y), active_image_filtered)

                center_x = (active_x + active_image_filtered.width / 2) / image_size[0]
                center_y = (active_y + active_image_filtered.height / 2) / image_size[1]
                width = active_image_filtered.width / image_size[0]
                height = active_image_filtered.height / image_size[1]
                annotations.append(f"{player_active_class_index} {center_x} {center_y} {width} {height}")

    if include_dealer_button:
        dealer_position = random.choice(seated_positions)
        seat_x, seat_y, seat_width, seat_height, slot = dealer_position
        offset = 20

        if slot == "top_left":
            dealer_x = seat_x + seat_width // 2 + offset
            dealer_y = seat_y + seat_height // 2 + offset
        elif slot == "top_middle":
            dealer_x = seat_x
            dealer_y = seat_y + seat_height // 2 + offset
        elif slot == "top_right":
            dealer_x = seat_x - seat_width // 2 - offset
            dealer_y = seat_y + seat_height // 2 + offset
        elif slot == "bottom_left":
            dealer_x = seat_x + seat_width // 2 + offset
            dealer_y = seat_y - seat_height // 2 - offset
        elif slot == "bottom_middle":
            dealer_x = seat_x + seat_width // 2 + offset
            dealer_y = seat_y - seat_height // 2 - offset
        else:  # bottom_right
            dealer_x = seat_x - seat_width // 2 - offset
            dealer_y = seat_y - seat_height // 2 - offset

        dealer_button_filtered = apply_filters(dealer_button.copy(), brightness_range, size_variation)
        combined_image.paste(dealer_button_filtered, (dealer_x - dealer_button_filtered.width // 2, dealer_y - dealer_button_filtered.height // 2), dealer_button_filtered)

        center_x = (dealer_x) / image_size[0]
        center_y = (dealer_y) / image_size[1]
        width = dealer_button_filtered.width / image_size[0]
        height = dealer_button_filtered.height / image_size[1]
        annotations.append(f"{dealer_button_class_index} {center_x} {center_y} {width} {height}")

    combined_image.save(output_image_path, format='PNG')

    with open(output_label_path, 'w') as f:
        f.write("\n".join(annotations))

def find_decks():
    decks_dir = os.path.join(os.getcwd(), 'deck')
    if not os.path.exists(decks_dir):
        return []
    return [d for d in os.listdir(decks_dir) if os.path.isdir(os.path.join(decks_dir, d))]
