import requests
import time
import psutil

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b-instruct-q4_K_M" # Usamos el modelo balanceado
CONTEXT_SIZE = 8192 # Un contexto grande para forzar el uso de RAM

def get_ollama_ram_mb():
    total_ram = 0
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            if 'ollama' in proc.info['name'].lower():
                total_ram += proc.info['memory_info'].rss / (1024 * 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return total_ram

def test_kv_cache():
    print(f"=== INICIANDO PRUEBA DE KV CACHE ({CONTEXT_SIZE} tokens) ===")
    
    # Prompt gigante para llenar el contexto
    long_prompt = "Repite la palabra 'ingenieria' mil veces. " * 500 

    # 1. Prueba Normal (Por defecto suele usar FP16 para el KV Cache)
    print("\n1. Lanzando inferencia estándar...")
    payload_normal = {
        "model": MODEL,
        "prompt": long_prompt,
        "stream": False,
        "options": {
            "num_predict": 10,
            "num_ctx": CONTEXT_SIZE
        }
    }
    
    requests.post(OLLAMA_API, json=payload_normal)
    ram_normal = get_ollama_ram_mb()
    print(f"-> RAM Pico (Estándar): {ram_normal:.2f} MB")
    
    time.sleep(3) # Pausa para dejar que la memoria se estabilice

    # 2. Prueba Optimizada
    # Nota: Ollama a veces gestiona esto automáticamente según la RAM libre, 
    # pero enviamos parámetros restrictivos para simular/forzar baja memoria.
    print("\n2. Lanzando inferencia con optimización/restricción de contexto...")
    payload_q8 = {
        "model": MODEL,
        "prompt": long_prompt,
        "stream": False,
        "options": {
            "num_predict": 10,
            "num_ctx": CONTEXT_SIZE,
            "low_vram": True # Fuerza a Ollama a optimizar memoria
        }
    }

    requests.post(OLLAMA_API, json=payload_q8)
    ram_optimizada = get_ollama_ram_mb()
    print(f"-> RAM Pico (Optimizada): {ram_optimizada:.2f} MB")

    # Resultados
    ahorro = ram_normal - ram_optimizada
    print("\n=== RESULTADOS ===")
    if ahorro > 0:
        print(f"¡Éxito! Ahorraste {ahorro:.2f} MB de RAM.")
    else:
        print("El sistema ya estaba optimizando la memoria al máximo o la diferencia es marginal en este modelo.")

if __name__ == "__main__":
    test_kv_cache()