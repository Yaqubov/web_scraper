# Web Scraper

Web Scraper is a tool for counting the number of images and leaf paragraphs in HTML document
represents only the last paragraphs in the nested paragraph structures. A client sends the website to a server, the server count images and appropriate paragraphs and respond to the client.

## Installation

Use following command to get files

```bash
git clone https://github.com/Yaqubov/web_scraper
```

After, install packages with:

```bash
pip install requirements.txt
```

## Usage

For running server:

```bash
python3 web_scraper.py server
```

For sending website name to server for processing:

```bash
python3 web_scraper.py -p [website]
```

Example:

```bash
python3 web_scraper.py -p www.booking.com
```