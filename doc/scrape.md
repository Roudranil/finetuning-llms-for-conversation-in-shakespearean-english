# Scraping

- [Scraping](#scraping)
  - [Overview](#overview)
  - [Parsing each chapter](#parsing-each-chapter)
  - [Running the scraper](#running-the-scraper)


## Overview

The `ShakespeareSpider` class contains the code to crawl and scrape the webste. The first function that will be called is the `parse()` method. It passes the url of each book to be scraped to the `parse_book_url()` method. It scrapes the book if there are pages to be scraped. It sends the ur of each chapter to the `parse_chapter()` method.

## Parsing each chapter

First all the `div`s with the `.comparison-row` class is extracted. So each such `div` contains one original dialog and the corresponding translated dialog. Both dialogs are then extracted and cleaneed to remove further unicode characters (more cleaning needs to be done). 

I had a somewhat hacky way to save the files as I did not have enough time to figure out the intricacies of `scrapy` - I passed the dictionary of the dialogs to `_save_dialogs()` to be saved as json files in the appropriate format.

## Running the scraper

Navigate to the `src` directory and simply run 
```bash
python scraping.py
```