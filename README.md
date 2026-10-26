
# Mini Document Search Engine

## Features
- Upload multiple text documents.
- Add documents manually.
- Tokenization and stop-word removal.
- Stemming using the Porter Stemmer.
- Inverted index for keyword search.
- Character N-gram index for partial-word search.
- Display matching documents and query-term frequencies.
- Automatically update indexes when new documents are added.
- Compare search time using a table and bar chart.
- Explore the contents of both indexes.

## Technologies
- Python
- Streamlit
- NLTK
- Matplotlib

## Installation

Install Python 3.10 or later.

Open the terminal inside this folder and run:

    pip install -r requirements.txt

## Run the application

    streamlit run app.py

Open the local URL displayed in the terminal, usually:

    http://localhost:8501

## How it works

1. Text is converted to lowercase and tokenized.
2. Common stop words are removed.
3. Remaining words are stemmed.
4. The inverted index maps processed terms to documents.
5. The N-gram index maps character trigrams to documents.
6. New documents automatically update both indexes.
7. Search times are measured and displayed for comparison.

## Notes

The application uses OR-based keyword matching.
The N-gram search supports partial-word matching.
Measured search times depend on the document collection
and computer performance.
