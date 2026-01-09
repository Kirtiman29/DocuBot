

# from sklearn.metrics.pairwise import cosine_similarity

# def get_most_similar(query, chunks, vectorizer, doc_vectors):
#     query_vector = vectorizer.transform([query])
#     similarities = cosine_similarity(query_vector, doc_vectors)[0]
#     best_index = similarities.argmax()
#     return chunks[best_index]



# from sentence_transformers import util

# def get_most_similar(user_query, chunks, model, doc_vectors):
#     """
#     Finds the most relevant chunk from the PDF for the user's query.
#     """
#     if not chunks or doc_vectors is None:
#         return "No document data available."

#     # 1. Convert user query into a vector
#     query_vector = model.encode(user_query)

#     # 2. Compute similarity between query and all document chunks
#     # util.cos_sim returns a matrix of scores
#     cos_scores = util.cos_sim(query_vector, doc_vectors)[0]

#     # 3. Get the index of the highest score
#     top_result_index = cos_scores.argmax().item()
    
#     # Optional: Set a threshold for "I don't know"
#     if cos_scores[top_result_index] < 0.3:
#         return "I couldn't find a relevant answer in the PDF."

#     return chunks[top_result_index]




# import requests
# import json
# from sentence_transformers import util

# def get_most_similar(user_query, chunks, model, doc_vectors):
#     if not chunks or doc_vectors is None:
#         yield "No document loaded."
#         return

#     # --- Step 1: Find the relevant text (Vector Search) ---
#     query_vector = model.encode(user_query)
#     cos_scores = util.cos_sim(query_vector, doc_vectors)[0]
#     top_result_index = cos_scores.argmax().item()
#     context = chunks[top_result_index]

#     # --- Step 2: Ask Ollama (Streaming Response) ---
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/chat",
#             json={
#                 "model": "llama3.2:3b",
#                 "messages": [
#                     {
#                         "role": "system", 
#                         "content": "You are DocuBot. Use the context to answer. If it's a greeting, reply politely. If the question isn't in the context, use your own knowledge but mention it's not in the PDF."
#                     },
#                     {
#                         "role": "user", 
#                         "content": f"Context: {context}\n\nQuestion: {user_query}"
#                     }
#                 ],
#                 "stream": True  # Enable streaming
#             },
#             stream=True
#         )

#         for line in response.iter_lines():
#             if line:
#                 chunk = json.loads(line)
#                 if 'message' in chunk:
#                     yield chunk['message']['content']
#                 if chunk.get('done'):
#                     break

#     except Exception as e:
#         yield f"Error: {str(e)}"

import requests
import json
from sentence_transformers import util

def get_most_similar(user_query, chunks, model, doc_vectors):
    if not chunks or doc_vectors is None:
        yield "No document loaded. Please upload a PDF first."
        return

    # 1. Search for context
    query_vector = model.encode(user_query)
    cos_scores = util.cos_sim(query_vector, doc_vectors)[0]
    top_result_index = cos_scores.argmax().item()
    context = chunks[top_result_index]

    # 2. Stream from Ollama with Point-Wise Instruction
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2:3b",
                "messages": [
                    {
                        "role": "system", 
                        "content": (
                            "You are DocuBot. You must answer questions using the provided context. "
                            "FOLLOW THESE RULES: "
                            "1. Use clear bullet points for your answer. "
                            "2. Keep points concise and informative. "
                            "3. If it's a greeting, be friendly but then ask for a question. "
                            "4. If the answer isn't in the context, use your knowledge but clearly state 'Not in PDF' at the start."
                        )
                    },
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_query}"}
                ],
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if 'message' in chunk:
                    yield chunk['message']['content']
                if chunk.get('done'):
                    break
    except Exception as e:
        yield f"Error: {str(e)}"