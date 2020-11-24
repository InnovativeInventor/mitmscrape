## mitmscrape
A little utility designed to scrape and find resources fetched on a JS-heavy site.

## Setup
To set this up, get the latest chrome(ium) driver for your version of Google Chrome/chromium: https://chromedriver.chromium.org/downloads and unzip it.
Then, rename the driver to be `chromedriver`.

## Usage
Enviroment setup
```bash
poetry shell
```

Running
```bash
python3 mitmscrape.py [url] [recursion_depth]
```

Filtering results (needs `ripgrep`)
```bash
mitmdump -nC results | rg "\.json"
```

## Example usage
```
python3 mitmscrape.py https://results.enr.clarityelections.com/GA/105369 2
mitmdump -nC results | rg "\.json"
```
