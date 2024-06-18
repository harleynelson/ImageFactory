# YOLOv8 Dataset Generator for Unique Decks of Cards

### ** For Educational Purposes Only **
Helps you create datasets for training your YOLOv8 models with images of card combinations on a table background. Basic variations can be applied for brightness and graininess.

## Features

- **Auto Deck Detection**: Automatically detects decks in the `deck` directory. If multiple decks are found, you can select which one to use.
- **Dataset Generation**: Specify the number of images and split them into training, validation, and test sets.
- **Brightness Variation**: Add random brightness variations to your images.
- **Grain Variation**: Add random graininess to your images (currently broke af with transparency from png files).


## Getting Started

1. **Create a New Deck**: Enter a name in the "New Deck Name" field and click "Create Deck" to make a new deck.
2. **Add Deck and Table Images**: Create a deck of 52 cards (no jokers) and place them in the 'cards' directory.  Place an empty looking poker table image 'table.png' in the 'table' directory.  Note: if your image sizes are significantly different than mine you may have to edit the image_factory.py to make everything jive.
3. **Select a Deck**: If multiple decks are detected in the `deck` directory, select the desired deck using the "Select Deck" button.
4. **Set Parameters**: Adjust the number of images, train/valid/test split ratios, and variation parameters as needed.
5. **Generate Dataset**: Click the "Generate" button to start creating your dataset.
6. **Upload to Google Drive**: Upload to "My Drive\Datasets".  Or wherever, just change the data.yaml file to chase it...
7. **Train**: If using Google Colab:make sure your Google Drive is mounted (left folder looking icon)
- !nvidia-smi
- !pip install ultralytics
- from ultralytics import YOLO
- !yolo task=detect mode=predict model=yolov8n.pt conf=0.25 source='https://ultralytics.com/images/bus.jpg'
- !yolo task=detect mode=train model=yolov8n.pt data='../content/drive/MyDrive/Datasets/ImageFactory_{whateverYourDeckNameIs_{numberOfImagesYouGenerated}/data.yaml' epochs=50 imgsz=640 

8. **Go Ham**: Download best.pt in the weights/ directory and use it in your model

## TODO

- [ ] Fix grain variation
- [ ] Add support for additional image variations (rotation, etc...)
- [ ] Probably could use some error handling?