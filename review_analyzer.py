from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import urllib.parse
import requests
import time
import nltk
import re

def _download_nltk_resources():
    """Check and download necessary NLTK resources"""
    resources = [
        "corpora/stopwords",
        "sentiment/vader_lexicon.zip",
        "corpora/wordnet"
    ]

    for resource in resources:
        try:
            nltk.data.find(resource)
            print(f"{resource} already downloaded.")
        except LookupError:
            print(f"{resource} not found. Downloading...")
            try:
                nltk.download(resource.split('/')[-1])
            except Exception as e:
                print(f"Error downloading {resource}: {e}")

def get_article(url):
    """Scrape the article from a url, returning the full text for analysis"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            article_text = "\n".join(p.get_text() for p in soup.find_all("p"))
            if not article_text.strip():  # Check if the article text is empty
                print("No article text found at the provided URL.")
                return ""
            return article_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the article: {e}")
        return ""

def analyze_text(text, url):
    """Analyze the text using different techniques, such as  
    word count, frequency analysis, and sentiment analysis"""
    global aspects
    
    # Text preprocessing: make lowercase, split, and remove stopwords
    words = text.lower().split()
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Extract the game title from the URL (this is a basic example; adjust as necessary)
    game_title = url.split('/')[-1].replace('-', ' ').replace('article', '').title().strip().lower()
    title_words = set(game_title.split())  # Create a set of title words for comparison

    # Filter out title words from tokens
    tokens = [word for word in tokens if word not in title_words]

    # Total words and unique words
    total_words = len(tokens)
    unique_words = len(set(tokens))
    print(f"\nTotal Words (excluding stopwords): {total_words}")
    print(f"Unique Words: {unique_words}\n")

    # Word Frequency Analysis
    word_count = Counter(tokens)
    most_common_words = word_count.most_common(10)
    print("Top 10 Most Common Words:", most_common_words)

    # Add up to the first three most common words to aspects
    for word, _ in most_common_words[:3]:
        aspects.add(word)
    
    # Phrase analysis
    phrase_analysis(tokens)
    
    # Sentiment Analysis
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    print("Overall Sentiment Analysis:", sentiment_scores)
    
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentiment_based_analysis(sentences, aspects)
    
    return sentences
   
def phrase_analysis(tokens):
    """Perform phrase analysis on the filtered tokens and add the most common phrases to aspects for sentiment analysis."""
    global aspects
    
    # Phrase Analysis
    for n in (2, 3):  # Bigrams and trigrams
        n_grams = ngrams(tokens, n)
        ngram_counts = Counter(n_grams)
        
        # Adding the top n-grams to aspects
        top_ngrams = ngram_counts.most_common(10)
        
        if n == 2:  # For bigrams
            # Add the top 5 bigrams to aspects
            for i in range(min(5, len(top_ngrams))):
                bigram_str = " ".join(top_ngrams[i][0])  # top_ngrams[i][0] gives you the n-gram tuple
                aspects.add(bigram_str)

        elif n == 3:  # For trigrams
            if top_ngrams:  # Only add if there are trigrams available
                trigram_str = " ".join(top_ngrams[0][0])  # Add the top trigram
                aspects.add(trigram_str)

        # Print the top n-grams
        print(f"\nTop 10 {n}-grams (excluding title):")
        for ngram, freq in top_ngrams:
            print(f" {" ".join(ngram)} - {freq}")
    print()
    
def sentiment_based_analysis(sentences, aspects):
    """Perform aspect-based sentiment analysis for a list of aspects in the article text."""
    sid = SentimentIntensityAnalyzer()
    aspect_sentiments = {}

    for aspect in aspects:
        aspect_scores = []
        lemmatized_aspect = lemmatizer.lemmatize(aspect)  # Lemmatize the aspect term

        # Find sentences containing the aspect keyword
        for sentence in sentences:
            lemmatized_sentence = " ".join([lemmatizer.lemmatize(word) for word in sentence.lower().split()])  # Lemmatize each word in the sentence
            if lemmatized_aspect in lemmatized_sentence:
                # Calculate sentiment for the sentence
                sentiment = sid.polarity_scores(sentence)
                aspect_scores.append(sentiment['compound'])  # Use compound score for overall sentiment

        # Calculate average sentiment for this aspect
        if aspect_scores:
            avg_sentiment = sum(aspect_scores) / len(aspect_scores)
            aspect_sentiments[aspect] = avg_sentiment
        else:
            aspect_sentiments[aspect] = None  # No sentences found for this aspect
    
    # Print aspect-based sentiment results
    print(f"Aspect-Based Sentiment Analysis: {aspects}")
    for aspect, sentiment in aspect_sentiments.items():
        if sentiment is not None:
            print(f" Avg Sentiment for '{aspect}': {sentiment:.2f}")
        else:
            print(f" No sentences found for aspect '{aspect}'.")

def run_analysis(url):
    """Get the text and run an analysis"""
    start_time = time.time()
    
    article = get_article(url)
    sentences = analyze_text(article, url)
    print()

    # Get the runtime
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds\n")
    
    # After running the analysis, allow for user input to add new aspects
    while True:
        new_aspect_input = input("Enter new aspect(s) to analyze (comma-separated or 'exit' to quit): ")

        if new_aspect_input.lower() == 'exit':
            print("Exiting...")
            break

        # Split the input into individual aspects, removing extra spaces
        input_aspects = set([aspect.strip() for aspect in new_aspect_input.split(',') if aspect.strip()])
        sentiment_based_analysis(sentences, input_aspects)
        print()

def main():
    _download_nltk_resources()
    global lemmatizer, aspects
    lemmatizer = WordNetLemmatizer()
    aspects = set()
    
    url = input("\nPaste a url to analyze its text (or 'exit' to quit):\n")
    
    if url == "exit":
        print("Exiting...")
        return
    
    # Validate URL format
    if not urllib.parse.urlparse(url).scheme:
        print("Invalid URL. Please include the protocol (http/https).")
        return

    run_analysis(url)

if __name__ == "__main__":
    main()