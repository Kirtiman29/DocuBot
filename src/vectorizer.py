from sklearn.feature_extraction.text import TfidfVectorizer

def create_vectorizer(processed_chunks):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(processed_chunks)
    return vectorizer, vectors
