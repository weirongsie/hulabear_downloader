# Hulabear Downloader
Download atricles from telnet://hulabear.twbbs.org

## Getting Started
### Prerequisites

Python 2.7

### Usage

```
python run.py -a [hula account] -p [hula password] -b [board] -s [starting article number] -e [ending article number]
```

For example, if you want to download No.2 ~ No.5 article in board Cs11:
```
python run.py -a account -p password -b Cs11 -s 2 -e 5
```
Or if you only want to download article No.30:
```
python run.py -a account -p password -b Cs11 -s 30 -e 30
```

### Download Folder

A Folder `download_[board]` will be auto created under the root folder.

For example, if you download articles from Cs11, the articles will be in:
```
hulabear_downloader\download_Cs11
```

### Config

In config.ini, there are some config you can try:
```
[host]
timeout = 6

[data]
page_splitter =
```
If your connection to hulabear is too slow, you can increase the `timeout` limit.
If you want to know the range of a page within an article, you can change `page_splitter` to `--`

## Features
* Save each article as a single text file.
* Remove BBS color code
* Auto skiping board opening page
* Skip F(friend only) or L(locked) articles
* Delete duplicated account login

## Known Issues
Waiting for your pull request to fix these issues :)
* Do not support most of the BBS control code
* lines hit the end of the page will appear twice
  (because hulabear copies the ending line of a page to the next page as a begining line)
* Unexpected spaces in article (due to BBS control code)

## Acknowledgments

The reformat part I reference the craler by [geniusturtle](https://github.com/geniusturtle6174/hulabear-crawler)

