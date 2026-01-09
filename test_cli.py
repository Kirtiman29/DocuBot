import os
import sys
from src.pdf_reader import read_pdf
from src.chunker import create_chunks
from src.vectorizer import create_vectorizer
from src.similarity import get_most_similar

def run_test():
    print("="*30)
    print("   DocuBot CLI - Streaming   ")
    print("="*30)
    
    # 1. Get PDF Path
    pdf_path = input("\n📂 Enter path to PDF: ").strip()
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File '{pdf_path}' not found.")
        return

    # 2. Processing Pipeline
    try:
        print("\n[1/3] 📖 Reading PDF...")
        text = read_pdf(pdf_path)
        
        print("[2/3] ✂️  Creating Chunks...")
        chunks = create_chunks(text)
        print(f"      ({len(chunks)} chunks created)")
        
        print("[3/3] 🧠 Generating Vector Embeddings...")
        # Note: vectorizer is the SentenceTransformer model
        vectorizer, doc_vectors = create_vectorizer(chunks)
        print("✅ System Ready!")

    except Exception as e:
        print(f"❌ Initialization Failed: {e}")
        return

    # 3. Streaming Chat Loop
    print("\n" + "-"*40)
    print("Chat with your document! (Type 'exit' to quit)")
    print("-"*40)

    while True:
        try:
            user_query = input("\n👤 You: ").strip()
            
            if user_query.lower() in ['exit', 'quit']:
                print("Goodbye! 👋")
                break
                
            if not user_query:
                continue

            print("🤖 DocuBot: ", end="", flush=True)

            # Iterate over the streaming generator
            # This consumes the 'yield' from get_most_similar
            for word_chunk in get_most_similar(user_query, chunks, vectorizer, doc_vectors):
                print(word_chunk, end="", flush=True)
            
            print() # Move to next line after response finishes

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Chat Error: {e}")

if __name__ == "__main__":
    run_test()