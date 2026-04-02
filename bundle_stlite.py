import os
import json
import base64

def get_file_content(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

base_dir = r"C:\Users\erick\.gemini\antigravity\scratch\FORXIME2"
target_html = r"C:\Users\erick\.gemini\antigravity\scratch\WEBSITE_BIOCHAVEZ\forxime_app.html"

files_config = {}

# Main app
files_config["app.py"] = {"content": get_file_content(os.path.join(base_dir, "app.py"))}

# Modules
modules_dir = os.path.join(base_dir, "modules")
for filename in os.listdir(modules_dir):
    if filename.endswith(".py"):
        rel_path = os.path.join("modules", filename).replace("\\", "/")
        files_config[rel_path] = {"content": get_file_content(os.path.join(modules_dir, filename))}

# Utils
utils_dir = os.path.join(base_dir, "utils")
for filename in os.listdir(utils_dir):
    if filename.endswith(".py"):
        rel_path = os.path.join("utils", filename).replace("\\", "/")
        files_config[rel_path] = {"content": get_file_content(os.path.join(utils_dir, filename))}

# Config
config_dir = os.path.join(base_dir, "config")
if os.path.exists(config_dir):
    for filename in os.listdir(config_dir):
        if filename.endswith(".json"):
            rel_path = os.path.join("config", filename).replace("\\", "/")
            files_config[rel_path] = {"content": get_file_content(os.path.join(config_dir, filename))}

# Requirements - OPTIMIZADO PARA CARGA RÁPIDA
# Solo incluimos lo estrictamente necesario para la interfaz inicial
# Las librerías pesadas (scipy, sklearn, matplotlib) se cargarán bajo demanda en el código
filtered_reqs = [
    "streamlit",
    "pandas",
    "numpy",
    "plotly",
    "folium",
    "streamlit-folium",
    "openpyxl",
    "pyodide-http",  # Necesario para que 'requests' funcione en el navegador
    "geopy"
]

stlite_config = {
    "entrypoint": "app.py",
    "files": files_config,
    "requirements": filtered_reqs
}

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>FORXIME/2 - Aplicación de Análisis | BioChavez Forester</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.0/build/stlite.css" />
    <style>
        body, html, #root {{
            height: 100vh;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            font-family: 'Outfit', sans-serif;
        }}
        /* Overlay de carga personalizado */
        #loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.5s;
        }}
        .spinner {{
            width: 50px;
            height: 50px;
            border: 5px solid #E8F5E9;
            border-top: 5px solid #2E7D32;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .loading-text {{
            margin-top: 20px;
            color: #2E7D32;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div id="loading-overlay">
        <div class="spinner"></div>
        <div class="loading-text">Iniciando FORXIME/2...</div>
        <div style="margin-top: 10px; color: #666; font-size: 0.8rem; max-width: 300px; text-align: center;">
            La primera vez puede tardar un poco mientras se carga el motor de Python en el navegador.
        </div>
    </div>

    <div id="root"></div>

    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.0/build/stlite.js"></script>
    <script>
        const stliteConfig = {json.dumps(stlite_config)};
        
        stlite.mount(stliteConfig, document.getElementById("root")).then(() => {{
            // Ocultar el overlay una vez cargado
            setTimeout(() => {{
                document.getElementById('loading-overlay').style.opacity = '0';
                setTimeout(() => {{
                    document.getElementById('loading-overlay').style.display = 'none';
                }}, 500);
            }}, 1000);
        }});
    </script>
</body>
</html>
"""

with open(target_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated {target_html}")
