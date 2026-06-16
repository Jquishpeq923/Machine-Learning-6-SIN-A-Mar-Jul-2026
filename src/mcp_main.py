import json
import requests
# 1. ACTUALIZACIÓN: Importamos las nuevas herramientas
from mcp_tools import list_files, read_file, web_search, open_browser, play_spotify, launch_any_app

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b-instruct-q4_K_M"

# 2. Definimos las herramientas en el formato JSON Schema que exige Ollama (MCP)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lista los archivos disponibles en el directorio local de datos (data folder). Úsalo cuando el usuario pregunte qué archivos hay.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido de un archivo de texto o CSV específico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "El nombre exacto del archivo a leer, ej. measurements.csv"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Busca en internet información reciente, noticias o datos que no sabes. Úsalo si te preguntan por la actualidad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "El término o frase de búsqueda para encontrar en internet."
                    }
                },
                "required": ["query"]
            }
        }
    },
    # --- NUEVAS HERRAMIENTAS INTEGRADAS ---
    {
        "type": "function",
        "function": {
            "name": "open_browser",
            "description": "Abre el navegador web para ir a una página específica o buscar algo en Google.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "La URL a visitar o el término a buscar (ej: 'youtube.com' o 'fotos de perros')."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_spotify",
            "description": "Abre Spotify y busca una canción, artista o podcast específico. Úsalo cuando el usuario quiera escuchar música.",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "El nombre de la canción y/o artista (ej: 'Bohemian Rhapsody Queen')."
                    }
                },
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "launch_any_app",
            "description": "Busca y abre cualquier aplicación instalada en el sistema de Windows (ej: Excel, Discord, Word, Calculadora).",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "Nombre de la aplicación a abrir (ej: 'excel', 'spotify', 'chrome')."
                    }
                },
                "required": ["app_name"]
            }
        }
    }
]

def chat_with_tools(prompt):
    """
    Envía el prompt y las herramientas al LLM. El LLM decide autónomamente si necesita 
    usar una herramienta o si puede responder directamente.
    """
    print("Jarvis está pensando y decidiendo...")

    messages = [{"role": "user", "content": prompt}]

    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "stream": False
    }

    try:
        # Hacemos la petición a la API de Chat de Ollama
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        message = response_data.get("message", {})

        # 3. Verificar si el modelo DECIDIÓ usar una herramienta (Tool Calling real)
        if "tool_calls" in message and message["tool_calls"]:
            tool_call = message["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            print(f"\n⚙️  [MCP] Jarvis decidió invocar la herramienta: {function_name}({arguments})")

            # 4. Ejecutar la herramienta correspondiente
            if function_name == "list_files":
                return list_files()
            elif function_name == "read_file":
                return read_file(arguments.get("filename", ""))
            elif function_name == "web_search":
                return web_search(arguments.get("query", ""))
            # --- CONEXIÓN DE LAS NUEVAS HERRAMIENTAS ---
            elif function_name == "open_browser":
                return open_browser(arguments.get("query", ""))
            elif function_name == "play_spotify":
                return play_spotify(arguments.get("song_name", ""))
            elif function_name == "launch_any_app":
                return launch_any_app(arguments.get("app_name", ""))
            else:
                return f"Error: El modelo intentó usar una herramienta desconocida ({function_name})"

        # 5. Si el modelo no usó herramientas, devolvemos su respuesta de texto normal
        else:
            return message.get("content", "")

    except Exception as e:
        return f"Error al comunicarse con Ollama: {e}"

# --- Bucle principal para interactuar con Jarvis ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("JARVIS INICIADO (IRON MAN MODE)")
    print("Acceso total al sistema operativo confirmado.")
    print("="*50 + "\n")
    print("Prueba con:")
    print(" - 'Abre spotify y pon AC/DC'")
    print(" - 'Abre el navegador en youtube.com'")
    print(" - 'Abre Excel'")
    print(" - 'Busca noticias sobre IA'\n")
    
    while True:
        user_input = input("Usuario: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Apagando a Jarvis...")
            break
            
        resultado = chat_with_tools(user_input)
        print(f"\nJarvis: {resultado}\n")