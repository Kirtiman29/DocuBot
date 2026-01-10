# 📄 DocuBot: AI-Powered PDF Assistant

DocuBot is a local-first, Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and have natural, point-wise conversations about their content. It combines high-speed vector search with local Large Language Models (LLMs) to provide private and accurate document insights.



---

## 🚀 Features

* **Intelligent Extraction:** Reads and chunks complex PDF text for precise retrieval.
* **Vector Search:** Utilizes `all-MiniLM-L6-v2` to convert text into numerical embeddings for lightning-fast similarity matching.
* **Local LLM Processing:** Powered by **Ollama (Llama 3.2:3b)**—your data never leaves your machine during the chat phase.
* **ChatGPT-Style Experience:** * **Real-time Streaming:** Words appear as they are generated using Server-Sent Events (SSE).
    * **Markdown Rendering:** Support for bold text, lists, and code blocks.
* **Google OAuth:** Secure user authentication and session management.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python / Flask |
| **Embeddings** | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| **LLM Engine** | Ollama (`llama3.2:3b`) |
| **Frontend** | Tailwind CSS / JavaScript (ES6+) |
| **Markdown** | Marked.js |
| **Auth** | Google OAuth 2.0 (Authlib) |

---

## 🏗️ Project Architecture

The application follows the **RAG (Retrieval-Augmented Generation)** pattern to ensure the AI only answers based on your uploaded document.



1.  **PDF Ingestion:** Text is extracted and broken into 500-character overlapping chunks.
2.  **Vectorization:** Chunks are converted into 384-dimensional vectors.
3.  **Retrieval:** The user's query is vectorized to find the most mathematically similar text chunk.
4.  **Augmentation:** The retrieved chunk is sent to the LLM as "Context."
5.  **Generation:** The LLM generates a human-like response which is streamed to the UI.

---

## 🏁 Getting Started

### 1. Prerequisites
* Python 3.10 or higher
* [Ollama installed](https://ollama.com/)
* Google Cloud Console credentials (for OAuth)

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd chatbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

### 3. Pull the AI Model
Ensure Ollama is running in the background and pull the Llama 3.2 model:
ollama pull llama3.2:3b



Here is the complete Markdown code for your README.md. You can copy this directly into a file named README.md in your project root.

Markdown

# 📄 DocuBot: AI-Powered PDF Assistant

DocuBot is a local-first, Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and have natural, point-wise conversations about their content. It combines high-speed vector search with local Large Language Models (LLMs) to provide private and accurate document insights.



---

## 🚀 Features

* **Intelligent Extraction:** Reads and chunks complex PDF text for precise retrieval.
* **Vector Search:** Utilizes `all-MiniLM-L6-v2` to convert text into numerical embeddings for lightning-fast similarity matching.
* **Local LLM Processing:** Powered by **Ollama (Llama 3.2:3b)**—your data never leaves your machine during the chat phase.
* **ChatGPT-Style Experience:** * **Real-time Streaming:** Words appear as they are generated using Server-Sent Events (SSE).
    * **Markdown Rendering:** Support for bold text, lists, and code blocks.
* **Google OAuth:** Secure user authentication and session management.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python / Flask |
| **Embeddings** | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| **LLM Engine** | Ollama (`llama3.2:3b`) |
| **Frontend** | Tailwind CSS / JavaScript (ES6+) |
| **Markdown** | Marked.js |
| **Auth** | Google OAuth 2.0 (Authlib) |

---

## 🏗️ Project Architecture

The application follows the **RAG (Retrieval-Augmented Generation)** pattern to ensure the AI only answers based on your uploaded document.



1.  **PDF Ingestion:** Text is extracted and broken into 500-character overlapping chunks.
2.  **Vectorization:** Chunks are converted into 384-dimensional vectors.
3.  **Retrieval:** The user's query is vectorized to find the most mathematically similar text chunk.
4.  **Augmentation:** The retrieved chunk is sent to the LLM as "Context."
5.  **Generation:** The LLM generates a human-like response which is streamed to the UI.

---

## 🏁 Getting Started

### 1. Prerequisites
* Python 3.10 or higher
* [Ollama installed](https://ollama.com/)
* Google Cloud Console credentials (for OAuth)

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd chatbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt



3. Pull the AI Model
Ensure Ollama is running in the background and pull the Llama 3.2 model:

Bash

ollama pull llama3.2:3b
4. Environment Setup
Create a .env file in the root directory:

Code snippet

FLASK_SECRET_KEY=your_random_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
5. Run the Application
Bash

python app.py
Open your browser and navigate to http://127.0.0.1:5000.

🖥️ Usage
Login: Sign in using your Google account.

Upload: Click the "Upload PDF" button and select your document (e.g., Python Notes).

Wait for Analysis: The bot will notify you once the vector embeddings are generated.

Chat: Ask questions like "What is a list?" or "Summarize chapter 3."

Streaming Response: Watch the bot respond in real-time, point-by-point.

📜 License
Distributed under the MIT License. See LICENSE for more information.


Would you like me to help you generate a **`requirements.txt`** file that matches all the libraries used in this project?
