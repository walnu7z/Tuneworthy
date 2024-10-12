# Tuneworthy
Tuneworthy is a music library manager with an intuitive graphical interface that allows you to manage and explore your music collection with ease. You can search through your music library using ID3v2.4 tags such as title, artist, album, year, genre, and track number. The application also provides tools for mining and configuring your music directory.

## Features
- **Search**: Search by title, artist, album, year, genre, or track number using simple commands.
- **Music Mining**: Extract ID3v2 tags from your music files.
- **Music Library Management**: Customize and organize your library's location and manage your song metadata.

## Requirements
- Python 3.9 or higher
- [Poetry](https://python-poetry.org/) for managing dependencies and virtual environments
- System dependencies (GTK, Cairo, etc.)

## Installation

### Step 1: Install Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Alternatively, follow the [official instructions](https://python-poetry.org/docs/#installation) to install Poetry.

### Step 2: Clone the repository and install project dependencies
```bash
git clone https://github.com/walnu7z/Tuneworthy.git
cd Tuneworthy
poetry install
```

**Note**: Testing dependencies are optional, but recommended for running tests.

### Step 3: Install system dependencies
```bash
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0
```

## Running the Application

To start the application, run the following command:

```bash
poetry run Tuneworthy
```

### GUI Overview

When the application starts, you will see three buttons in the window title bar:
- **Search Button (Left)**: Search for songs in the library using various fields.
- **Mine Button (Right)**: Press this button to mine your music library for ID3v2 tags.
- **Configure Button (Right)**: Change the directory where your music library is stored (default is `~/Music`). Make sure to change the directory **before** starting the mining process.

When mining is in progress, a status bar will display. Once completed, the window will update to show a list of songs in your library with their corresponding ID3v2 tags.

## Search Commands

To search for songs, you can use the following commands:
- `title:NAME` or `t:NAME` — Search by title.
- `artist:NAME` or `a:NAME` — Search by artist.
- `album:NAME` or `d:NAME` — Search by album.
- `year:NAME` or `y:NAME` — Search by year.
- `genre:NAME` or `g:NAME` — Search by genre.
- `track:NAME` or `n:NAME` — Search by track number.

You can combine multiple search terms (e.g., `t:Bohemian a:Queen`). If no tag is provided, the search will go through all fields.

## Running Tests

To run tests, simply use:

```bash
poetry run pytest
```

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE](./LICENSE) file for details.
