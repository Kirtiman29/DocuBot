# from sklearn.metrics.pairwise import cosine_similarity

# def find_best_match(query_vector, document_vectors):
#     similarities = cosine_similarity(query_vector, document_vectors)
#     best_index = similarities.argmax()
#     best_score = similarities[0][best_index]
#     return best_index, best_score


from sklearn.metrics.pairwise import cosine_similarity

def get_most_similar(query, chunks, vectorizer, doc_vectors):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, doc_vectors)[0]
    best_index = similarities.argmax()
    return chunks[best_index]
