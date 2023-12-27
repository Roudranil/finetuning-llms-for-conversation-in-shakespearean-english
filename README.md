# Shakespearen Chabot with opensource LLM's

<!--toc:start-->

- [Shakespearen Chabot with opensource LLM's](#shakespearen-chabot-with-opensource-llms)
  - [Introduction](#introduction)
  - [Setup](#setup)
  - [Dataset creation](#dataset-creation)
    - [Overview](#overview)
    - [Scraping](#scraping)
<!--toc:end-->

## Introduction

For now the goal is to simply finetune a chat model, such that it can converse
with us in Shakespearean english, even if we are prompting in plain english. The
goal is to try out with some small models first ($1$B - $1.5$B)

## Setup

Run the following commands to get started with the environment.
```bash
python -m venv .env
source .env/scripts/bin/activate
pip install -r requirements.txt
```

## Dataset creation

### Overview

A quick internet search will lead to 2 primary sources for datasets containing works of Shakespeare:
- [Tiny Shakespeare from Andrej Karpathy's repository](https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt) [`[🤗 Datasets]`](https://huggingface.co/datasets/Trelis/tiny-shakespeare)
- Translation of complete works of Shakespeare - [Shakescleare](https://www.litcharts.com/shakescleare/shakespeare-translations) [`[Kaggle datasets]`](https://www.kaggle.com/datasets/garnavaurha/shakespearify)

However for my purpose I needed a dataset where I have both a dialog, its translation and its response pair of original dialog and translation. In the tiny shakespeare dataset, there are no translations. The translated dataset does not have dialogs in the correct sequence. Hence rather than hack some way to do what I want, I decided to scrape the site myself.

### Scraping

[src/scraping.py](src/scraping.py) contains the code to scrape [Shakescleare](https://www.litcharts.com/shakescleare/shakespeare-translations). The code is highly inspired by [shakespeare_crawler.py](https://github.com/ToruOwO/style-transfer-writing/blob/9119fae3f56312d4c202945051bdfd3761aed63b/data/shakespeare_crawler/shakespeare_crawler/spiders/shakespeare_crawler.py) from [ToruOwO/style-transfer-writing](https://github.com/ToruOwO/style-transfer-writing). The scraping is done in a very specific format. Below is the structure of the data directory. Each folder in it corresponds to one book's worth of translated dialogs. In each book, there are separate json files containing the dialogs corresponding to their chapters.
```
data
├── book_name
│   ├── chatpter_name.json
.   .
.   .
.   .
```
Each json file as the following structure
```json
{
    "dialogs":[
        {
            "original": "original dialog here",
            "translated": "translated dialog here"
        },
        { ... },
        .
        .
        .
    ]
}
```
Note that the array of dialogs is in the same order as they occur in the books. Meaning any dialog can be taken as the **repsonse** to the dialog that comesjust before it in the array.
