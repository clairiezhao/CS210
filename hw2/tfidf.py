import math
import re
from collections import Counter

DOC_LIST_FILE = "tfidf_docs.txt"
STOPWORDS_FILE = "stopwords.txt"


# =========================
# READ FILES
# =========================
def read_document_list():
    with open(DOC_LIST_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def read_stopwords():
    stopwords = set()
    with open(STOPWORDS_FILE, "r") as f:
        for line in f:
            stopwords.update(line.strip().split())
    return stopwords


# =========================
# PREPROCESSING
# =========================
def remove_links(text):
    return re.sub(r"https?://\S+", " ", text)


def clean_text(text):
    text = remove_links(text)
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)   # remove non-word chars
    text = re.sub(r"\s+", " ", text).strip()
    return text


def stem(word):
    if word.endswith("ing"):
        return word[:-3]
    if word.endswith("ly"):
        return word[:-2]
    if word.endswith("ment"):
        return word[:-4]
    return word


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


def write_preprocessed(filename, words):
    out_file = "preproc_" + filename
    with open(out_file, "w") as f:
        f.write(" ".join(words))


# =========================
# TF-IDF
# =========================
def compute_tf(words):
    total = len(words)
    counts = Counter(words)
    tf = {}
    for word in counts:
        tf[word] = counts[word] / total
    return tf


def compute_idf(all_docs):
    N = len(all_docs)
    idf = {}

    # count in how many docs each word appears
    word_doc_count = {}
    for doc in all_docs:
        unique_words = set(doc)
        for w in unique_words:
            word_doc_count[w] = word_doc_count.get(w, 0) + 1

    for word in word_doc_count:
        idf[word] = math.log(N / word_doc_count[word]) + 1

    return idf


def compute_tfidf(tf, idf):
    tfidf = {}
    for word in tf:
        tfidf[word] = round(tf[word] * idf[word], 2)
    return tfidf


def get_top5(tfidf):
    # sort: highest score, then alphabetical
    sorted_words = sorted(tfidf.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words[:5]


def write_tfidf(filename, top5):
    out_file = "tfidf_" + filename
    with open(out_file, "w") as f:
        f.write(str(top5))


# =========================
# MAIN (END-TO-END RUN)
# =========================
def main():
    docs = read_document_list()
    stopwords = read_stopwords()

    all_processed = []

    # PREPROCESS
    for doc in docs:
        words = preprocess(doc, stopwords)
        write_preprocessed(doc, words)
        all_processed.append(words)

    # TF
    tf_list = []
    for words in all_processed:
        tf_list.append(compute_tf(words))

    # IDF
    idf = compute_idf(all_processed)

    # TF-IDF + OUTPUT
    for i, doc in enumerate(docs):
        tfidf = compute_tfidf(tf_list[i], idf)
        top5 = get_top5(tfidf)
        write_tfidf(doc, top5)


if __name__ == "__main__":
    main()
