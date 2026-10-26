
import re
import time
from collections import Counter, defaultdict

import matplotlib.pyplot as plt
import streamlit as st
from nltk.stem import PorterStemmer


# -------------------- PAGE SETUP --------------------

st.set_page_config(
    page_title="Mini Document Search Engine",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Mini Document Search Engine")
st.write("Assignment 1: Document Indexing and Search Engine")


# -------------------- TEXT PREPROCESSING --------------------

STOP_WORDS = set("""
a an the and or but if while with to of at by for from up about
into over after is are was were be been being am do does did have
has had i you he she it we they them this that these those as on
in out not no so than too very can could should would will your
our their my his her its
""".split())

stemmer = PorterStemmer()


def tokenize(text):
    """Convert text to lowercase tokens."""
    return re.findall(r"[a-z0-9]+", text.lower())


def preprocess(text):
    """Tokenization, stop-word removal and stemming."""
    words = tokenize(text)
    words = [word for word in words if word not in STOP_WORDS]
    return [stemmer.stem(word) for word in words]


def generate_ngrams(word, n=3):
    """Generate character N-grams."""
    if len(word) <= n:
        return {word}

    return {
        word[i:i + n]
        for i in range(len(word) - n + 1)
    }


# -------------------- SEARCH ENGINE --------------------

class SearchEngine:

    def __init__(self):
        self.documents = {}
        self.processed_documents = {}

        # Inverted index: term -> documents
        self.inverted_index = defaultdict(set)

        # N-gram index: character gram -> documents
        self.ngram_index = defaultdict(set)

    def add_document(self, name, text):
        """Add a document and update both indexes automatically."""

        name = name.strip() or "Untitled.txt"
        original_name = name
        number = 2

        # Avoid overwriting documents with identical names.
        while name in self.documents:
            name = f"{original_name} ({number})"
            number += 1

        self.documents[name] = text

        # Preprocess document for the inverted index.
        processed_words = preprocess(text)
        self.processed_documents[name] = processed_words

        for word in set(processed_words):
            self.inverted_index[word].add(name)

        # Build N-gram index from original words.
        original_words = set(tokenize(text))

        for word in original_words:
            for gram in generate_ngrams(word):
                self.ngram_index[gram].add(name)

        return name

    def search_inverted(self, query):
        """Search using the inverted index."""

        query_terms = preprocess(query)

        if not query_terms:
            return {}, query_terms

        matching_documents = set()

        for term in query_terms:
            matching_documents.update(
                self.inverted_index.get(term, set())
            )

        results = {}

        for name in matching_documents:
            word_counts = Counter(
                self.processed_documents[name]
            )

            # Total frequency of query terms in the document.
            frequency = sum(
                word_counts[term] for term in query_terms
            )

            results[name] = frequency

        results = dict(
            sorted(
                results.items(),
                key=lambda item: (-item[1], item[0])
            )
        )

        return results, query_terms

    def search_ngram(self, query):
        """Search using N-grams for partial-word matching."""

        query_words = tokenize(query)

        if not query_words:
            return {}

        candidates = set()

        for word in query_words:

            # Short queries may not contain a full trigram.
            if len(word) < 3:
                candidates.update(self.documents.keys())
            else:
                for gram in generate_ngrams(word):
                    candidates.update(
                        self.ngram_index.get(gram, set())
                    )

        results = {}

        for name in candidates:
            document_words = tokenize(self.documents[name])

            # Verify actual substring matches.
            matched_count = sum(
                1
                for query_word in query_words
                if any(
                    query_word in document_word
                    for document_word in document_words
                )
            )

            if matched_count > 0:
                results[name] = matched_count

        return dict(
            sorted(
                results.items(),
                key=lambda item: (-item[1], item[0])
            )
        )


# -------------------- SAMPLE DOCUMENTS --------------------

def create_sample_engine():
    engine = SearchEngine()

    sample_documents = {
        "Information Retrieval.txt": (
            "Information retrieval systems organize documents "
            "and help users find relevant information. "
            "An inverted index maps terms to documents."
        ),

        "Search Engines.txt": (
            "A search engine processes keywords, ranks documents, "
            "and returns useful results. Tokenization and stemming "
            "improve keyword search."
        ),

        "Text Mining.txt": (
            "Text mining discovers patterns in text documents. "
            "N-gram indexing supports partial word matching "
            "and approximate lookup."
        ),

        "Data Structures.txt": (
            "Hash maps and inverted indexes provide efficient lookup. "
            "Index structures reduce the time needed to search "
            "a document collection."
        )
    }

    for name, content in sample_documents.items():
        engine.add_document(name, content)

    return engine


if "engine" not in st.session_state:
    st.session_state.engine = SearchEngine()

engine = st.session_state.engine


# -------------------- ADD DOCUMENTS --------------------

st.sidebar.header("Add Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload text files",
    type=["txt"],
    accept_multiple_files=True
)

if st.sidebar.button(
    "Add Uploaded Documents",
    disabled=not uploaded_files
):
    for uploaded_file in uploaded_files:
        content = uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace"
        )

        added_name = engine.add_document(
            uploaded_file.name,
            content
        )

        st.sidebar.success(f"Added: {added_name}")

with st.sidebar.form("manual_document_form"):
    document_name = st.text_input(
        "Document name",
        placeholder="notes.txt"
    )

    document_text = st.text_area(
        "Document content",
        height=150
    )

    add_manual_document = st.form_submit_button(
        "Add Text Document"
    )

    if add_manual_document:
        if document_text.strip():
            added_name = engine.add_document(
                document_name or "Untitled.txt",
                document_text
            )

            st.sidebar.success(f"Added: {added_name}")
        else:
            st.sidebar.warning("Please enter document text.")


# -------------------- APPLICATION TABS --------------------

tab1, tab2, tab3 = st.tabs([
    "Keyword Search",
    "Index Comparison",
    "Index Explorer"
])


# -------------------- Q1: KEYWORD SEARCH --------------------

with tab1:

    st.header("Search Documents")

    query = st.text_input(
        "Enter a keyword or partial word",
        placeholder="Example: retrieval"
    )

    search_method = st.radio(
        "Choose indexing technique",
        [
            "Inverted Index",
            "N-gram Index"
        ],
        horizontal=True
    )

    if st.button("Search Documents", type="primary"):

        start_time = time.perf_counter()

        if search_method == "Inverted Index":
            results, query_terms = engine.search_inverted(query)
        else:
            results = engine.search_ngram(query)
            query_terms = []

        elapsed_time = (
            time.perf_counter() - start_time
        ) * 1000

        st.write(
            f"Search time: {elapsed_time:.4f} milliseconds"
        )

        if not query.strip():
            st.warning("Please enter a search query.")

        elif not results:
            st.warning("No matching documents found.")

        else:
            st.success(
                f"Found {len(results)} matching document(s)."
            )

            for name, score in results.items():

                with st.expander(
                    f"{name} | Match score: {score}"
                ):
                    st.write(engine.documents[name])

                    if search_method == "Inverted Index":

                        counts = Counter(
                            engine.processed_documents[name]
                        )

                        st.write("Query-term frequencies:")

                        st.json({
                            term: counts[term]
                            for term in query_terms
                        })

                    else:
                        st.write(
                            "Number of matched query words:",
                            score
                        )


# -------------------- Q2: TECHNIQUE COMPARISON --------------------

with tab2:

    st.header("Compare Indexing Techniques")

    comparison_query = st.text_input(
        "Enter a query",
        value="retriev",
        key="comparison_query"
    )

    query_type = st.selectbox(
        "Select query type",
        [
            "Exact keyword",
            "Partial word",
            "Multiple keywords"
        ]
    )

    if st.button("Compare Techniques", type="primary"):

        if query_type == "Exact keyword":
            comparison_query = "index"

        elif query_type == "Partial word":
            comparison_query = "retriev"

        elif query_type == "Multiple keywords":
            comparison_query = "search document"

        results_data = []

        techniques = [
            ("Inverted Index", engine.search_inverted),
            ("N-gram Index", engine.search_ngram)
        ]

        timing_values = []

        for technique_name, search_function in techniques:

            start_time = time.perf_counter()

            output = search_function(comparison_query)

            elapsed_time = (
                time.perf_counter() - start_time
            ) * 1000

            # Inverted search returns (results, query_terms).
            if technique_name == "Inverted Index":
                results = output[0]
            else:
                results = output

            timing_values.append(elapsed_time)

            results_data.append({
                "Technique": technique_name,
                "Matching Documents": len(results),
                "Search Time (ms)": round(elapsed_time, 4),
                "Documents Found": (
                    ", ".join(results.keys()) or "None"
                )
            })

        st.write("Query:", comparison_query)

        st.dataframe(
            results_data,
            use_container_width=True,
            hide_index=True
        )

        # Graphical comparison of measured search times.
        figure, axis = plt.subplots()

        axis.bar(
            ["Inverted Index", "N-gram Index"],
            timing_values
        )

        axis.set_ylabel("Search Time (milliseconds)")
        axis.set_title("Search Time Comparison")

        st.pyplot(figure)

        st.caption(
            "Timings depend on document collection size and "
            "computer performance. Repeat tests for more reliable "
            "measurements."
        )


# -------------------- INDEX EXPLORER --------------------

with tab3:

    st.header("Explore the Indexes")

    left_column, right_column = st.columns(2)

    with left_column:

        st.subheader("Inverted Index")

        term = st.text_input(
            "Enter a term to inspect",
            key="inspect_term"
        )

        if term:

            processed_terms = preprocess(term)

            for processed_term in processed_terms:

                documents = sorted(
                    engine.inverted_index.get(
                        processed_term,
                        set()
                    )
                )

                st.write(
                    f"{processed_term} → {documents}"
                )

    with right_column:

        st.subheader("N-gram Index")

        gram = st.text_input(
            "Enter a character N-gram",
            max_chars=3,
            key="inspect_gram"
        )

        if gram:

            documents = sorted(
                engine.ngram_index.get(
                    gram.lower(),
                    set()
                )
            )

            st.write(f"{gram.lower()} → {documents}")

    st.divider()

    st.subheader("Indexed Documents")

    document_data = []

    for name, content in engine.documents.items():

        document_data.append({
            "Document": name,
            "Characters": len(content),
            "Processed Tokens": len(
                engine.processed_documents[name]
            )
        })

    st.dataframe(
        document_data,
        use_container_width=True,
        hide_index=True
    )

    st.write(
        f"Total documents indexed: {len(engine.documents)}"
    )
