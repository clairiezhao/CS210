import math
import re
from collections import Counter

# Input file names used for the program
DOC_LIST_FILE = "tfidf_docs.txt"
STOPWORDS_FILE = "stopwords.txt"


# Loads all input files inside of "tfidf_docs.txt"
def load_document_list():
    with open(DOC_LIST_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Loads provided stopwords given in "stopwords.txt"
def load_stopwords():
    stopwords = set()
    with open(STOPWORDS_FILE, "r") as f:
        for line in f:
            stopwords.update(line.strip().split())
    return stopwords


# Part 1. Preprocessing 


# Function to removes website links
def remove_links(text):
    return re.sub(r"https?://\S+", " ", text)

# Cleans text by removing non necessary whitespaces, website links and converts all words to lowercase
def clean_text(text):
    text = remove_links(text)
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)   # remove non-word characters
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Reduces words to their root forms by stemming & lemmatization
def stem(word):
    if word.endswith("ing"):
        return word[:-3]
    if word.endswith("ly"):
        return word[:-2]
    if word.endswith("ment"):
        return word[:-4]
    return word

# Preprocesses all files by using the previous functions to modify the data 
def preprocess(filename, stopwords):
    with open(filename, "r") as f:
        text = f.read()

    text = clean_text(text)
    words = text.split()

    processed = []
    for w in words:
        if w not in stopwords:
            processed.append(stem(w))

    return processed

# Saves the newly preprocessed files with modified data to new files with prefix "preproc_"  
def write_preprocessed(filename, words):
    out_file = "preproc_" + filename
    with open(out_file, "w") as f:
        f.write(" ".join(words))


# Part 2. Computing TF-IDF Scores


# Computes the term frequency for each distinct word in each of the preprocessed files
def compute_tf(words):
    total = len(words)
    word_counts = Counter(words)
    tf = {}
    for word in word_counts:
        tf[word] = word_counts[word] / total
    return tf

# Computes the inverse document frequency for each distinct word in each of the preprocessed files 
def compute_idf(all_docs):
    N = len(all_docs)
    idf = {}

    # counts how many documents each word appears in
    word_doc_count = {}
    for doc in all_docs:
        unique_words = set(doc)
        for w in unique_words:
            word_doc_count[w] = word_doc_count.get(w, 0) + 1

    for word in word_doc_count:
        idf[word] = math.log(N / word_doc_count[word]) + 1

    return idf

# Multiplies the TF & IDF togther then proceeeds to round each score 2 decimal places 
def compute_tfidf(tf, idf):
    tfidf = {}
    for word in tf:
        tfidf[word] = round(tf[word] * idf[word], 2)
    return tfidf

# Returns top 5 words using highest score from TF-IDF
def get_top_words(tfidf):
    # sort: highest score, then alphabetical
    sorted_words = sorted(tfidf.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words[:5]

# Saves the TF-IDF scores to new files with prefix "tfidf_"
def write_tfidf(filename, top5):
    out_file = "tfidf_" + filename
    with open(out_file, "w") as f:
        f.write(str(top5))


# Main function that runs everything step by step


def main():
    docs = load_document_list()
    stopwords = load_stopwords()

    all_processed = []

    # Preprocesses each document and creates the new "preproc_" files
    for doc in docs:
        words = preprocess(doc, stopwords)
        write_preprocessed(doc, words)
        all_processed.append(words)

    # Computes the term frequency for each preprocessed file 
    tf_list = []
    for words in all_processed:
        tf_list.append(compute_tf(words))

    # Computes the inverse document frequency using all the new preprocessed files
    idf = compute_idf(all_processed)

    # Computes TF-IDF, gets the top 5 words, and creates the new "tfidf_" files 
    for i, doc in enumerate(docs):
        tfidf = compute_tfidf(tf_list[i], idf)
        top5 = get_top_words(tfidf)
        write_tfidf(doc, top5)


if __name__ == "__main__":
    main()
