import requests
import time
import psutil
import csv
import os

# Modelos a evaluar
MODELS = [
    "qwen2.5:7b-instruct-q8_0",
    "qwen2.5:7b-instruct-q4_K_M",
    "qwen2.5:7b-instruct-q3_K_M"
]

PROMPT = "Write a highly detailed 200-word essay about the history of artificial intelligence."
OLLAMA_API = "http://localhost:11434/api/generate"
CSV_FILE = "../data/measurements.csv"

def get_ollama_ram_mb():
    """Calcula el uso de RAM del proceso de Ollama."""
    total_ram = 0
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            if 'ollama' in proc.info['name'].lower():
                total_ram += proc.info['memory_info'].rss / (1024 * 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return total_ram

def run_benchmark():
    results = []

    # --- PARTE A: Baseline y Cuantización ---
    print("=== INICIANDO PARTE A ===")
    for model in MODELS:
        print(f"Evaluando: {model}...")
        payload = {"model": model, "prompt": PROMPT, "stream": False, "options": {"num_predict": 200, "num_ctx": 2048}}

        response = requests.post(OLLAMA_API, json=payload)

        if response.status_code == 200:
            data = response.json()
            peak_ram = get_ollama_ram_mb()
            eval_count = data.get("eval_count", 0)
            eval_duration_sec = data.get("eval_duration", 0) / 1e9
            tok_sec = eval_count / eval_duration_sec if eval_duration_sec > 0 else 0

            results.append({
                "Part": "A", "Model": model, "Quantization": model.split("-")[-1],
                "Context_Length": 2048, "Peak_RAM_MB": round(peak_ram, 2), "Tokens_Per_Sec": round(tok_sec, 2)
            })
            print(f"-> RAM: {peak_ram:.2f} MB | Vel: {tok_sec:.2f} tok/s")
        else:
            print(f"Error con {model}. ¿Lo descargaste?")

    # --- PARTE B: Experimento KV Cache ---
    print("\n=== INICIANDO PARTE B ===")
    best_model = "qwen2.5:7b-instruct-q4_K_M"
    context_lengths = [512, 2048, 8192, 16384]

    for ctx in context_lengths:
        print(f"Estresando contexto: {ctx} tokens...")
        payload = {"model": best_model, "prompt": "Repeat 'hello' 10 times.", "stream": False, "options": {"num_predict": 50, "num_ctx": ctx}}

        requests.post(OLLAMA_API, json=payload)
        time.sleep(2)
        peak_ram = get_ollama_ram_mb()

        results.append({
            "Part": "B", "Model": best_model, "Quantization": "q4_K_M",
            "Context_Length": ctx, "Peak_RAM_MB": round(peak_ram, 2), "Tokens_Per_Sec": "N/A"
        })
        print(f"-> Contexto: {ctx} | RAM: {peak_ram:.2f} MB")

    # Guardar en CSV
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, CSV_FILE)

    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\n¡Métricas guardadas en data/measurements.csv!")

if __name__ == "__main__":
    run_benchmark()