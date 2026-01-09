# from sklearn.feature_extraction.text import TfidfVectorizer

# def create_vectorizer(processed_chunks):
#     vectorizer = TfidfVectorizer()
#     vectors = vectorizer.fit_transform(processed_chunks)
#     return vectorizer, vectors



from sentence_transformers import SentenceTransformer

# Load the model globally so it doesn't reload every time
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_vectorizer(chunks):
    """
    Converts list of text chunks into numerical embeddings.
    """
    if not chunks:
        return None, None
    
    # Generate embeddings for all chunks
    # This returns a numpy array of vectors
    doc_vectors = model.encode(chunks, show_progress_bar=True)
    
    return model, doc_vectors