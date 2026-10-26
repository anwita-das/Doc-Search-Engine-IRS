
# Assignment 1: Document Indexing and Search Engine

## 1. Aim

To develop a mini document search engine that searches multiple
text documents using keywords and partial words and compares
two indexing techniques.

## 2. Objectives

- Implement text preprocessing.
- Build an inverted index.
- Build an N-gram index.
- Search documents using exact and partial keywords.
- Display matching documents and query-term frequencies.
- Automatically update indexes when documents are added.
- Compare search time using a table and graph.

## 3. Tools and Technologies

- Python
- Streamlit
- NLTK Porter Stemmer
- Matplotlib

## 4. Q1: Mini Document Search Engine

### Text preprocessing

Text preprocessing consists of three main steps in addition
to converting text to lowercase.

1. Tokenization: Splits text into individual words.
2. Stop-word removal: Removes common words such as "the",
   "is", and "and".
3. Stemming: Reduces words to their stem using the Porter
   stemming algorithm.

### Inverted index

An inverted index maps each processed term to the documents
that contain it.

Example:

| Term | Documents |
|---|---|
| index | Information Retrieval, Data Structures |
| search | Search Engines |
| document | Information Retrieval, Text Mining |

The index makes keyword lookup efficient because the system
does not need to scan every document for each query.

### Searching and frequency

The query undergoes the same preprocessing as the documents.
The system retrieves documents containing one or more query
terms and displays their frequency in each matching document.

### Automatic updates

When a user uploads a text file or adds text manually, the
application processes the document and updates both indexes
immediately.

## 5. Q2: Multiple Indexing Techniques

### Inverted index

The inverted index maps stemmed words to documents. It is
suitable for exact and stemmed keyword searches.

### N-gram index

The N-gram index divides words into overlapping sequences
of three characters, called trigrams.

For example, the word "search" produces:

- sea
- ear
- arc
- rch

These character sequences help identify documents containing
partial words. The system verifies candidate matches against
the original document words.

### Comparison

| Feature | Inverted Index | N-gram Index |
|---|---|---|
| Index key | Stemmed word | Character trigram |
| Exact keyword search | Suitable | Possible |
| Partial-word search | Limited | Suitable |
| Storage | Generally compact | Can require more storage |
| Search operation | Direct term lookup | Candidate lookup and verification |

## 6. Experimental Methodology

The application compares both indexing techniques using
the same query.

It records search time using Python's time.perf_counter()
and displays the results in a table and bar chart.

Three query types are tested:

1. Exact keyword: index
2. Partial word: retriev
3. Multiple keywords: search document

The application measures elapsed time in milliseconds.

## 7. Results and Discussion

Run the application and record the actual values displayed
in the comparison table.

| Query Type | Technique | Matching Documents | Search Time (ms) |
|---|---|---|---|
| Exact keyword | Inverted Index | Fill after running | Fill after running |
| Exact keyword | N-gram Index | Fill after running | Fill after running |
| Partial word | Inverted Index | Fill after running | Fill after running |
| Partial word | N-gram Index | Fill after running | Fill after running |
| Multiple keywords | Inverted Index | Fill after running | Fill after running |
| Multiple keywords | N-gram Index | Fill after running | Fill after running |

The inverted index is designed for direct keyword lookup.
The N-gram index is useful for partial-word matching, but
it may require additional candidate verification.

Search timings can vary with document collection size,
computer performance, and system load. A larger collection
and repeated trials provide a more useful comparison.

## 8. Conclusion

The mini document search engine implements an inverted index
and an N-gram index. It supports text preprocessing, keyword
search, partial-word search, frequency display, and automatic
index updates.

The comparison interface measures search time and visualizes
the results using a table and bar chart. The experiment
demonstrates how different indexing techniques serve
different search requirements.

## 9. Execution

Install the required libraries:

    pip install -r requirements.txt

Run the application:

    streamlit run app.py
