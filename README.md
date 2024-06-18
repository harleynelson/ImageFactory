# YOLOv8 Dataset Generator for Unique Decks of Cards

### ** For Educational Purposes Only **
Create datasets for training your YOLOv8 models with images of any cards. Basic variations can be applied for size, brightness, and graininess.
![Screenshot 2024-06-18 164950](https://github.com/harleynelson/ImageFactory/assets/12590891/13008594-9786-4a98-84a0-52c98cceb3fe)

![sample](https://github.com/harleynelson/ImageFactory/assets/12590891/5f62ce21-114b-4096-92fc-8256a3d638d2)

## Features

- **Create For Multiple Decks**: Add multiple different decks of cards to train for any game.
- **Dataset Generation**: Specify the number of images and split them into training, validation, and test sets.
- **Size, Brightness, Grain Variation**: Add random variations to your images.

## Getting Started

1. **Create a New Deck**: Enter a name in the "New Deck Name" field and click "Create Deck" to make a new deck.
2. **Add Deck and Table Images**: Create a deck of 52 cards (no jokers) and place them in the 'cards' directory.  Follow the same naming convention (5D.png = 5 of Diamonds, JS.png = Jack of Spades, etc...). Place an empty looking poker table image 'table.png' in the 'table' directory.  Note: if your image sizes are significantly different than the test ones you may have to edit image_factory.py to make the sizing jive.
3. **Select a Deck**: If multiple decks are detected in the `deck` directory, select the desired deck using the "Select Deck" button.
4. **Set Parameters**: Adjust the number of images, train/valid/test split ratios, and variation parameters as needed.
5. **Generate Dataset**: Click the "Generate" button to start creating your dataset.
6. **Upload to Google Drive**: Upload to "My Drive\Datasets".  Or wherever, just change the data.yaml file to chase it...
7. **Train**: If using Google Colab: Make sure your Google Drive is Mounted (left folder looking icon).  Run these commands...
- !nvidia-smi
- !pip install ultralytics
- from ultralytics import YOLO
- !yolo task=detect mode=predict model=yolov8n.pt conf=0.25 source='https://ultralytics.com/images/bus.jpg'  # only if you want to test to make sure it's working
- !yolo task=detect mode=train model=yolov8n.pt data='../content/drive/MyDrive/Datasets/ImageFactory_{whateverYourDeckNameIs_{numberOfImagesYouGenerated}/data.yaml' epochs=50 imgsz=640 

8. **Go Ham**: Download best.pt in the weights/ directory and use it in your model

## TODO

- [ ] Fix grain variation
- [ ] Add support for additional image variations (rotation, etc...)
- [ ] Probably could use some error handling?
