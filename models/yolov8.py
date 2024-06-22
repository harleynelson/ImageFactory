import os

import yaml


def save_annotations_and_metadata(output_dir, card_names, include_dealer_button, include_active_players, include_seated_players, deck_name, model, num_images):
    selected_classes = card_names[:]
    if include_dealer_button:
        selected_classes.append('DealerButton')
    if include_active_players:
        selected_classes.append('PlayerActive')
    if include_seated_players:
        selected_classes.append('PlayerSeated')

    data = {
        'path': f'../drive/MyDrive/Datasets/ImageFactory_{deck_name}_{model}_{num_images}',
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': len(selected_classes),
        'names': selected_classes
    }

    with open(os.path.join(output_dir, 'data.yaml'), 'w') as f:
        yaml.dump(data, f, default_flow_style=None)
