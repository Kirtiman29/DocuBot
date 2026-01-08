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

# from authlib.integrations.flask_client import OAuth
# from dotenv import load_dotenv
# from flask import session, redirect, url_for
# from functools import wraps
# import os
# from flask import Flask, render_template, request, jsonify
# from werkzeug.utils import secure_filename

# from src.pdf_reader import read_pdf
# from src.chunker import create_chunks
# from src.vectorizer import create_vectorizer
# from src.similarity import get_most_similar

# app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# CONFIG_FILE = "config.txt"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# chunks = []
# vectorizer = None
# doc_vectors = None


# # 🔁 Load last PDF on startup
# def load_last_pdf():
#     global chunks, vectorizer, doc_vectors

#     if os.path.exists(CONFIG_FILE):
#         with open(CONFIG_FILE, "r") as f:
#             path = f.read().strip()

#         if path and os.path.exists(path):
#             text = read_pdf(path)
#             chunks = create_chunks(text)
#             vectorizer, doc_vectors = create_vectorizer(chunks)
#             print(f"✅ Loaded last PDF: {path}")


# @app.route("/")
# def home():
#     return render_template("index.html")


# # ⭐ ADD THIS NEW ENDPOINT
# @app.route("/check-pdf", methods=["GET"])
# def check_pdf():
#     """Check if a PDF is currently loaded"""
#     pdf_loaded = bool(chunks)
#     current_pdf = ""
    
#     if os.path.exists(CONFIG_FILE):
#         with open(CONFIG_FILE, "r") as f:
#             path = f.read().strip()
#             if path and os.path.exists(path):
#                 current_pdf = os.path.basename(path)
    
#     return jsonify({
#         "pdf_loaded": pdf_loaded,
#         "current_pdf": current_pdf
#     })


# @app.route("/upload", methods=["POST"])
# def upload_pdf():
#     global chunks, vectorizer, doc_vectors

#     # ✅ SAFETY CHECKS
#     if "pdf" not in request.files:
#         return jsonify({"message": "No file part in request"}), 400

#     file = request.files["pdf"]

#     if file.filename == "":
#         return jsonify({"message": "No file selected"}), 400

#     filename = secure_filename(file.filename)
#     path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

#     file.save(path)

#     # Save path permanently
#     with open(CONFIG_FILE, "w") as f:
#         f.write(path)

#     text = read_pdf(path)
#     chunks = create_chunks(text)
#     vectorizer, doc_vectors = create_vectorizer(chunks)

#     print(f"📄 PDF uploaded: {path}")

#     return jsonify({"message": f"PDF '{filename}' uploaded successfully"})


# @app.route("/chat", methods=["POST"])
# def chat():
#     if not chunks:
#         return jsonify({"reply": "No PDF loaded. Please upload a PDF."})

#     user_query = request.json["message"]
#     answer = get_most_similar(
#         user_query, chunks, vectorizer, doc_vectors
#     )
#     return jsonify({"reply": answer})


# if __name__ == "__main__":
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     load_last_pdf()   # ⭐ Load PDF on startup
#     app.run(debug=True)







import os
from functools import wraps

from flask import (
    Flask, render_template, request, jsonify,
    session, redirect, url_for
)
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

from src.pdf_reader import read_pdf
from src.chunker import create_chunks
from src.vectorizer import create_vectorizer
from src.similarity import get_most_similar


# ─────────────────────────────────────
# App & Config
# ─────────────────────────────────────
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

UPLOAD_FOLDER = "uploads"
CONFIG_FILE = "config.txt"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─────────────────────────────────────
# Global State (single-user version)
# ─────────────────────────────────────
chunks = []
vectorizer = None
doc_vectors = None


# ─────────────────────────────────────
# Google OAuth Setup
# ─────────────────────────────────────
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# ─────────────────────────────────────
# Auth Guard
# ─────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────
# Load last PDF on startup
# ─────────────────────────────────────
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


# ─────────────────────────────────────
# Routes
# ─────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html", user=session.get("user"))


# ─────── AUTH ───────
@app.route("/login")
def login():
    return google.authorize_redirect(
        url_for("auth_callback", _external=True)
    )


@app.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()
    user = token["userinfo"]

    session["user"] = {
        "name": user["name"],
        "email": user["email"],
        "picture": user["picture"],
    }

    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ─────── PDF STATUS ───────
@app.route("/check-pdf", methods=["GET"])
@login_required
def check_pdf():
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


# ─────── UPLOAD ───────
@app.route("/upload", methods=["POST"])
@login_required
def upload_pdf():
    global chunks, vectorizer, doc_vectors

    if "pdf" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    with open(CONFIG_FILE, "w") as f:
        f.write(path)

    text = read_pdf(path)
    chunks = create_chunks(text)
    vectorizer, doc_vectors = create_vectorizer(chunks)

    print(f"📄 PDF uploaded: {path}")

    return jsonify({
        "success": True,
        "message": f"PDF '{filename}' uploaded successfully"
    })


# ─────── CHAT ───────
@app.route("/chat", methods=["POST"])
@login_required
def chat():
    if not chunks:
        return jsonify({
            "success": False,
            "reply": "No PDF loaded. Please upload a PDF."
        })

    user_query = request.json.get("message", "")
    answer = get_most_similar(
        user_query, chunks, vectorizer, doc_vectors
    )

    return jsonify({
        "success": True,
        "reply": answer
    })


# ─────── CLEAR ───────
@app.route("/clear", methods=["POST"])
@login_required
def clear_data():
    global chunks, vectorizer, doc_vectors

    data = request.get_json()
    clear_type = data.get("type")

    if clear_type == "pdf":
        chunks = []
        vectorizer = None
        doc_vectors = None

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                f.write("")

        return jsonify({
            "success": True,
            "message": "PDF cleared successfully"
        })

    if clear_type == "chat":
        return jsonify({
            "success": True,
            "message": "Chat cleared successfully"
        })

    return jsonify({
        "success": False,
        "message": "Invalid clear type"
    }), 400


# ─────────────────────────────────────
# Main
# ─────────────────────────────────────
if __name__ == "__main__":
    load_last_pdf()
    app.run(debug=True)
