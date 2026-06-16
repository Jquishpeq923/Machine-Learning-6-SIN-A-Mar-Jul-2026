import os
import subprocess
import platform
import webbrowser
import urllib.parse
from ddgs import DDGS

# --- HERRAMIENTAS DE SISTEMA DE ARCHIVOS ---

def list_files(directory="data"):
    """Lista todos los archivos en el directorio data, buscando desde la raíz del proyecto."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    target_dir = os.path.join(project_root, directory)
    
    try:
        files = os.listdir(target_dir)
        return f"Archivos en {target_dir}: {', '.join(files)}"
    except Exception as e:
        return f"Error listando archivos en {target_dir}: {str(e)}"

def read_file(filename, directory="data"):
    """Lee el contenido de un archivo específico dentro de la carpeta data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, directory, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo el archivo {filename}: {str(e)}"

# --- HERRAMIENTA DE BÚSQUEDA WEB GRATUITA ---

def web_search(query):
    """Busca información actualizada en la web usando DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            # Busca los 3 resultados principales
            results = list(ddgs.text(query, max_results=3))
            summaries = [f"{r['title']}: {r['body']}" for r in results]
            return " | ".join(summaries)
    except Exception as e:
        return f"Error en búsqueda: {str(e)}"

# --- NUEVAS HERRAMIENTAS DE SISTEMA (IRON MAN MODE) ---

def open_browser(query):
    """Abre el navegador en una URL o busca en Google."""
    if "." in query and " " not in query:
        url = query if query.startswith("http") else f"https://{query}"
        webbrowser.open(url)
        return f"Sistema: Se ha abierto la web {url}."
    else:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Sistema: Buscando '{query}' en tu navegador."

def play_spotify(song_name):
    """Abre Spotify buscando una canción o artista."""
    query = urllib.parse.quote(song_name)
    uri = f"spotify:search:{query}"
    try:
        os.startfile(uri)
        return f"Sistema: Abriendo Spotify para buscar '{song_name}'."
    except Exception as e:
        return "Sistema: Error. Asegúrate de tener Spotify instalado en tu PC."

def launch_any_app(app_name):
    """Busca y abre aplicaciones en el Menú Inicio de Windows."""
    paths = [
        os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs"),
        os.path.join(os.environ.get("PROGRAMDATA", ""), r"Microsoft\Windows\Start Menu\Programs")
    ]
    for path in paths:
        if not os.path.exists(path):
            continue
        for root, dirs, files in os.walk(path):
            for file in files:
                if app_name.lower() in file.lower() and file.endswith(".lnk"):
                    file_path = os.path.join(root, file)
                    try:
                        os.startfile(file_path)
                        return f"Sistema: Abriendo {file.replace('.lnk', '')}..."
                    except:
                        pass
    return f"Sistema: No encontré la aplicación '{app_name}' en tu computadora."

# --- DEFINICIÓN DE HERRAMIENTAS PARA EL MODELO ---

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lista los archivos disponibles en el directorio de datos",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido de un archivo de texto",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Nombre del archivo a leer"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Busca información actualizada en la web",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Término de búsqueda"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_browser",
            "description": "Abre el navegador web para ir a una página o buscar en Google.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "URL o término a buscar"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_spotify",
            "description": "Abre Spotify y busca una canción o artista.",
            "parameters": {
                "type": "object",
                "properties": {"song_name": {"type": "string", "description": "Nombre de la canción"}},
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "launch_any_app",
            "description": "Abre aplicaciones instaladas en la computadora (como Excel, Word, Discord).",
            "parameters": {
                "type": "object",
                "properties": {"app_name": {"type": "string", "description": "Nombre del programa"}},
                "required": ["app_name"]
            }
        }
    }
]