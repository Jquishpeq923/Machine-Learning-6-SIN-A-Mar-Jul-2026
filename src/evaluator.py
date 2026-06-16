import json
import time
import requests

def run_robust_evaluation():
    print("--- Iniciando Evaluación Automática de Jarvis ---")
    
    try:
        with open('data/test_set.json', 'r', encoding='utf-8') as f:
            tests = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró 'data/test_set.json'. Asegúrate de crearlo.")
        return

    results = []
    total_tests = len(tests)
    
    for i, test in enumerate(tests, 1):
        print(f"\n[{i}/{total_tests}] Evaluando: {test['prompt'][:50]}...")
        
        start = time.time()
        
        payload = {
            "model": "qwen2.5:7b-instruct-q3_K_M", 
            "prompt": test['prompt'], 
            "stream": False,
            "options": {"num_ctx": 1024} 
        }
        
        try:
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=180)
            if response.status_code == 200:
                latency = time.time() - start
                
                # --- LA SOLUCIÓN ESTÁ AQUÍ ---
                answer_text = response.json().get("response", "Error al leer texto")
                
                print(f"-> ¡Éxito! (Tardó {latency:.2f} segundos)")
                print(f"-> Jarvis respondió: {answer_text[:80]}...") # Imprime una vista previa
                
                results.append({
                    "prompt": test['prompt'],
                    "category": test['category'],
                    "latency": round(latency, 2),
                    "jarvis_answer": answer_text, # <- Guardamos la respuesta completa
                    "success": "pending_review"
                })
            else:
                print(f"-> Error: {response.status_code}")
        except Exception as e:
            print(f"-> Demasiado tiempo o error de conexión.")

        # Guarda progreso por cada pregunta
        with open('data/eval_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
    print("\n--- ¡Evaluación completada con éxito! ---")

if __name__ == "__main__":
    run_robust_evaluation()