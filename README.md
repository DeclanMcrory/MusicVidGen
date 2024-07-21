Music Video Generator

A music video generation tool using deep learning.

## Overview

This project includes the necessary files to train and generate music videos based on audio features, character profiles, and video elements.

## Files

- `main.py`: Main entry point for the project.
- `train.py`: Script to train the model.
- `config.json`: Configuration file for the project.
- `web_interface/`: Contains the web interface files (`index.html`, `styles.css`).
- `utils/`: Utility functions (`random_generator.py`).
- `lyrics_generator/`: Lyrics generation script (`lyrics_generator.py`).
- `models/`: Model definition (`music_vid_gen.py`).
- `data/`: Dataset class (`music_vid_synth_dataset.py`).

## How to Use

1. **Training the Model**:
   ```sh
   python train.py
   ```

2. **Generating a Music Video**:
   - Open `web_interface/index.html` in a web browser.
   - Click the "
