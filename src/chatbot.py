from src.preprocess import preprocess_text
from src.similarity import find_best_match

def chatbot_response(query, vectorizer, doc_vectors, chunks):
    processed_query = preprocess_text(query)
    query_vector = vectorizer.transform([processed_query])

    best_index, best_score = find_best_match(query_vector, doc_vectors)

    if best_score < 0.2:
        return "Sorry, answer not found in the document."
    else:
        return chunks[best_index]
