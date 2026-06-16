import os
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# === CONFIGURACIÓN ===
PDF_PATH = "../data/corpus/MANUAL-DE-MECANICA-BASICA.pdf" 
DB_DIR = "../data/chroma_db"
OLLAMA_API = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2.5:7b-instruct-q4_K_M"

def query_ollama(prompt):
    payload = {"model": LLM_MODEL, "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_API, json=payload)
        return response.json().get("response", "")
    except Exception as e:
        return f"Error conectando con Ollama: {e}"

def build_rag():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_full_path = os.path.join(script_dir, DB_DIR)
    pdf_full_path = os.path.join(script_dir, PDF_PATH)
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Verificación de base de datos existente
    if os.path.exists(db_full_path) and len(os.listdir(db_full_path)) > 0:
        print("[Sistema]: Base de datos vectorial detectada. Cargando conocimiento previo...")
        return Chroma(persist_directory=db_full_path, embedding_function=embeddings)

    # Si no existe, procesar PDF
    if not os.path.exists(pdf_full_path):
        print(f"[Error]: No encuentro el archivo en {pdf_full_path}")
        return None
    
    print("[Sistema]: No tengo memoria de este manual. Entrando al archivo PDF...")
    loader = PyPDFLoader(pdf_full_path)
    
    print("[Sistema]: Fragmentando el texto para entenderlo mejor...")
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(loader.load())
    
    print("[Sistema]: Aprendiendo y guardando en mi memoria local (esto puede tardar)...")
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_full_path)
    print("[Sistema]: ¡Memoria actualizada! Ya estoy listo para leer el documento.")
    return vectorstore

if __name__ == "__main__":
    db = build_rag()
    
    if db:
        print("\n✨ [Jarvis]: ¡Hola! Estoy listo para ayudarte con tu manual. Escribe 'salir' para cerrar.")
        while True:
            pregunta = input("\n👤 Pregunta: ")
            if pregunta.lower() == 'salir': break
            if not pregunta.strip(): continue
            
            # 1. SIN RAG
            print("\n[Jarvis]: Accediendo a mi base de conocimientos general...")
            print(f"Respuesta: {query_ollama(pregunta)}")
            
            # 2. CON RAG
            print("\n[Jarvis]: Buscando en el manual de mecánica...")
            docs = db.similarity_search(pregunta, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            print("[Jarvis]: Leyendo fragmentos relevantes y redactando respuesta...")
            prompt_final = f"Responde a la pregunta basándote SOLO en este contexto:\n{context}\n\nPregunta: {pregunta}"
            
            print(f"Respuesta (con el manual): {query_ollama(prompt_final)}")
            print("-" * 50)