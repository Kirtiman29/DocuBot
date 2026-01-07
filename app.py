# from flask import Flask, render_template, request, jsonify
# from src.pdf_reader import read_pdf
# from src.chunker import create_chunks
# from src.vectorizer import create_vectorizer
# from src.similarity import get_most_similar

# app = Flask(__name__)

# # Load PDF once
# PDF_PATH = "data/documents/notes.pdf"
# text = read_pdf(PDF_PATH)
# chunks = create_chunks(text)
# vectorizer, doc_vectors = create_vectorizer(chunks)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     user_query = request.json["message"]

#     answer = get_most_similar(
#         user_query, chunks, vectorizer, doc_vectors
#     )

#     return jsonify({"reply": answer})


# if __name__ == "__main__":
#     app.run(debug=True)


import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from src.pdf_reader import read_pdf
from src.chunker import create_chunks
from src.vectorizer import create_vectorizer
from src.similarity import get_most_similar

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
CONFIG_FILE = "config.txt"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

chunks = []
vectorizer = None
doc_vectors = None


# 🔁 Load last PDF on startup
def load_last_pdf():
    global chunks, vectorizer, doc_vectors

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            path = f.read().strip()

        if path and os.path.exists(path):
            text = read_pdf(path)
            chunks = create_chunks(text)
            vectorizer, doc_vectors = create_vectorizer(chunks)
            print(f"✅ Loaded last PDF: {path}")


@app.route("/")
def home():
    return render_template("index.html")


# ⭐ ADD THIS NEW ENDPOINT
@app.route("/check-pdf", methods=["GET"])
def check_pdf():
    """Check if a PDF is currently loaded"""
    pdf_loaded = bool(chunks)
    current_pdf = ""
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            path = f.read().strip()
            if path and os.path.exists(path):
                current_pdf = os.path.basename(path)
    
    return jsonify({
        "pdf_loaded": pdf_loaded,
        "current_pdf": current_pdf
    })


@app.route("/upload", methods=["POST"])
def upload_pdf():
    global chunks, vectorizer, doc_vectors

    # ✅ SAFETY CHECKS
    if "pdf" not in request.files:
        return jsonify({"message": "No file part in request"}), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(path)

    # Save path permanently
    with open(CONFIG_FILE, "w") as f:
        f.write(path)

    text = read_pdf(path)
    chunks = create_chunks(text)
    vectorizer, doc_vectors = create_vectorizer(chunks)

    print(f"📄 PDF uploaded: {path}")

    return jsonify({"message": f"PDF '{filename}' uploaded successfully"})


@app.route("/chat", methods=["POST"])
def chat():
    if not chunks:
        return jsonify({"reply": "No PDF loaded. Please upload a PDF."})

    user_query = request.json["message"]
    answer = get_most_similar(
        user_query, chunks, vectorizer, doc_vectors
    )
    return jsonify({"reply": answer})


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    load_last_pdf()   # ⭐ Load PDF on startup
    app.run(debug=True)