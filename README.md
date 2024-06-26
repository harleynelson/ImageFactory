# YOLOv8 Dataset Generator for Unique Decks of Cards

Automatically create datasets for training your YOLOv8 models with images of any cards without manually annotating.

![sample](https://github.com/harleynelson/ImageFactory/assets/12590891/c9602fea-fd88-4dc8-a21d-2cf1094004b6)


## Features

- **Support For Multiple Decks**: Add multiple different decks of cards to train for any game.
- **Dataset Generation**: Specify the number of images and split them into training, validation, and test sets.
- **Automatic Boundary Box Annotation**: Could always use Roboflow with the images generated if you need manual annotations.
- **Size, Brightness, Grain Variation**: Add random variations to your images.

## Getting Started

![Screenshot 2024-06-22 001941](https://github.com/harleynelson/ImageFactory/assets/12590891/d75c5dc4-3229-4661-8e8a-a2644c57b5fe)


1. **Create a New Deck**: Enter a name in the `New Deck Name` field and click `Create Deck` to make a new deck.
2. **Add Deck and Table Images**: Create a deck of 52 cards (no jokers) and place them in the `cards` directory.  
- Cards: Follow the same naming convention (5D.png = 5 of Diamonds, JS.png = Jack of Spades, etc...). 
- Note: if your image sizes are significantly different than the test ones you may have to edit image_factory.py to make the sizing jive.
- Active/Seated players and Dealer button: images are only required if you want to create a dataset with them.
- Active = PlayerActive.png
- Seated = doesn't matter, will randomly pick from seated directory
- Dealer Button = DealerButton.png
3. **Select a Deck**: If multiple decks are detected in the `deck` directory, select the desired deck using the `Select Deck` button.
4. **Set Parameters**: Adjust the number of images, train/valid/test split ratios, and variation parameters as needed.
5. **Generate Sample**: Click the `Sample` button to make sure you're diggin the results.
6. **Generate Dataset**: Click the `Generate` button to start creating your dataset.
7. **Upload to Google Drive**: Upload to `My Drive\Datasets`.  Or wherever, just change the data.yaml file to chase it...
8. **Train**: If using Google Colab: Make sure your Google Drive is Mounted (left folder looking icon).  Run these commands...
- !nvidia-smi
- !pip install ultralytics
- from ultralytics import YOLO
- !yolo task=detect mode=predict model=yolov8n.pt conf=0.25 source='https://ultralytics.com/images/bus.jpg'  # only if you want to test to make sure it's working
- !yolo task=detect mode=train model=yolov8n.pt data='../content/drive/MyDrive/Datasets/ImageFactory_{whateverYourDeckNameIs_{numberOfImagesYouGenerated}/data.yaml' epochs=50 imgsz=640 

9. **Go Ham**: Download best.pt in the runs/detect/train/weights/ directory and use it in your model

![val_batch2_labels](https://github.com/harleynelson/ImageFactory/assets/12590891/03afcd71-e51f-48f1-9b7b-eccb8ca8637b)![labels](https://github.com/harleynelson/ImageFactory/assets/12590891/0b990e35-244f-4ebd-9a5c-f1364d08771d)


## TODO
- [ ] Add support for more model types
- [ ] Fix grain variation
- [ ] Add support for additional image variations (rotation, skew, etc...)
- [ ] Probably could use some better error handling?
