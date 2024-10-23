
# NFT Generation Project

This repository provides tools to generate randomized NFTs, metadata, and associated media, including images and videos. The system allows for the combination of multiple layers of traits with configurable rarity, which can be exported as images or videos.

## Table of Contents
- [Features](#features)
- [Configuration](#configuration)
- [Installation](#installation)
- [Usage](#usage)
  - [Setting Up](#setting-up)
  - [Generating NFTs](#generating-nfts)
  - [Generating Metadata](#generating-metadata)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Features

- **Layered Asset Support**: Combines multiple asset layers to create unique NFTs.
- **Configurable Rarity**: Allows setting rarity for each trait or assigning rarity weights randomly.
- **Image and Video Support**: Outputs NFTs in both image and video formats, with layers composited on a video background.
- **Metadata Generation**: Generates metadata in JSON format, compatible with platforms like OpenSea.

## Configuration

The main configuration is done in the `config.py` file. Here, you define layers, their asset directories, and rarity weights for traits.

Each layer must have:
1. `id`: Unique identifier for the layer.
2. `name`: The name of the layer (not necessarily the folder name).
3. `directory`: The folder inside the `assets/` folder containing the traits for this layer.
4. `required`: Whether the layer is required or optional.
5. `rarity_weights`: Defines the rarity of traits either as `None` (all traits equally rare), `random`, or an array of weights.

Check the example in `config.py` for detailed instructions.

## Installation

Clone the repository and install the required dependencies.

\`\`\`bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
pip install -r requirements.txt
\`\`\`

## Usage

### Setting Up

1. Prepare your assets and organize them into folders by layers within an `assets/` directory.
2. Configure the `config.py` file to match your layer setup, as described in the configuration section.

### Generating NFTs

To generate NFTs, run the `nft.py` script. It will use the configuration to generate the specified number of NFTs.

\`\`\`bash
python nft.py
\`\`\`

You will be prompted to:
- Enter the number of avatars to generate.
- Name the edition.

NFTs will be saved in the `output/` folder, categorized by edition.

### Generating Metadata

After generating the NFTs, run the `metadata.py` script to generate metadata for the NFTs.

\`\`\`bash
python metadata.py
\`\`\`

This script will prompt you to specify which edition to generate metadata for. Metadata will be stored in `output/edition_x/metadata.csv` and the JSON files will be placed in `output/edition_x/json`.

## Dependencies

- Python 3.x
- Required Python packages (install via `requirements.txt`):
  - `pandas`
  - `numpy`
  - `PIL` (Python Imaging Library)
  - `progressbar`
  - `moviepy`

Install the dependencies with:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
