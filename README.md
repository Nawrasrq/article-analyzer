# Article Analyzer

A Python-based project for scraping and analyzing articles from various websites. The project utilizes Natural Language Processing (NLP) techniques to perform analysis such as word and phrase count, overall and aspect based sentiment analysis.

## Features
- Scrapes article text from specified URLs.
- Extracts total and unique word count along with top 10 common words, phrases and their count.
- Analyzes overall and word or phrase sentiment from articles using VADER sentiment analysis.
- Allows cmd input of new words to use in aspect based sentiment analysis

## Project Structure
```
article-analyzer/
│
├── article_analyzer.py           # Main script for analyzing articles
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## Setup

### Prerequisites
- Python 3.7 or higher
- pip for installing Python packages
- NLTK library resources for stopwords and sentiment analysis

### Installation
Clone the repository:

```bash
git clone https://github.com/yourusername/article-analyzer.git
cd article-analyzer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
To scrape an article and analyze it:

```bash
python scripts/analysis.py
```
You will be prompted to enter the URL of the article you wish to analyze and afterwards, any more words or phrases for sentiment analysis.

```
Enter new aspect(s) to analyze (comma-separated or 'exit' to quit):
difficulty, storm, shoes
```

## Example Usage

```
Paste a url to analyze its text (or 'exit' to quit):
https://www.orlandosentinel.com/2024/11/03/hurricane-center-tracks-growing-caribbean-system-that-could-threaten-florida-next-week/

Total Words (excluding stopwords): 753
Unique Words: 224

Top 10 Most Common Words: [('storm', 21), ('next', 17), ('system', 13), ('caribbean', 13), ('tropical', 13), ('atlantic', 12), ('forecast', 11), ('low', 10), ('center', 9), ('couple', 9)]

Top 10 2-grams (excluding title):
 next couple - 7
 tropical storm - 7
 subtropical storm - 6
 low pressure - 6
 western caribbean - 6
 nhc gives - 6
 named storm - 6
 eastern atlantic - 4
 disorganized showers - 4
 development system - 4

Top 10 3-grams (excluding title):
 next couple days - 4
 nhc gives chance - 4
 gives chance development - 4
 chance development next - 4
 development next two - 4
 next two seven - 4
 atlantic named storm - 4
 tropical storm watches - 3
 storm watches warnings - 3
 watches warnings could - 3

Overall Sentiment Analysis: {'neg': 0.063, 'neu': 0.9, 'pos': 0.037, 'compound': -0.9926}
Aspect-Based Sentiment Analysis: {'storm', 'tropical storm', 'next', 'system', 'next couple days', 'low pressure', 'subtropical storm', 'western caribbean', 'next couple'}
 Avg Sentiment for 'storm': -0.42
 Avg Sentiment for 'tropical storm': -0.45
 Avg Sentiment for 'next': -0.41
 Avg Sentiment for 'system': -0.37
 No sentences found for aspect 'next couple days'.
 Avg Sentiment for 'low pressure': -0.63
 Avg Sentiment for 'subtropical storm': -0.59
 Avg Sentiment for 'western caribbean': -0.29
 Avg Sentiment for 'next couple': -0.65

Total execution time: 2.17 seconds

Enter new aspect(s) to analyze (comma-separated or 'exit' to quit): hurricane
Aspect-Based Sentiment Analysis: {'hurricane'}
 Avg Sentiment for 'hurricane': -0.11

Enter new aspect(s) to analyze (comma-separated or 'exit' to quit): exit
Exiting...
```