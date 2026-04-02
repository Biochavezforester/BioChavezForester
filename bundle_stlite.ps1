$BaseDir = "C:\Users\erick\.gemini\antigravity\scratch\FORXIME2"
$TargetHtml = "C:\Users\erick\.gemini\antigravity\scratch\WEBSITE_BIOCHAVEZ\forxime_app.html"

# Mapeo de archivos (Nombre -> Contenido puro en string)
$FilesConfig = @{}

function Add-File($RelativePath) {
    $FullPath = Join-Path $BaseDir $RelativePath
    if (Test-Path $FullPath) {
        # Usamos -Raw para leer como un solo string y -Encoding UTF8
        $Content = Get-Content -Path $FullPath -Raw -Encoding UTF8
        if ($null -eq $Content) { $Content = "" }
        
        # Normalizar saltos de línea y asegurar que sea un string plano
        # Para stlite, es más seguro pasar el contenido directamente como string si no usamos metadata
        $FilesConfig[$RelativePath.Replace("\", "/")] = $Content.Replace("`r`n", "`n")
    }
}

# Recopilar todos los archivos necesarios
Add-File "app.py"

$ModulesDir = Join-Path $BaseDir "modules"
if (Test-Path $ModulesDir) {
    Get-ChildItem -Path $ModulesDir -Filter *.py | ForEach-Object {
        Add-File (Join-Path "modules" $_.Name)
    }
}

$UtilsDir = Join-Path $BaseDir "utils"
if (Test-Path $UtilsDir) {
    Get-ChildItem -Path $UtilsDir -Filter *.py | ForEach-Object {
        Add-File (Join-Path "utils" $_.Name)
    }
}

$ConfigDir = Join-Path $BaseDir "config"
if (Test-Path $ConfigDir) {
    Get-ChildItem -Path $ConfigDir -Filter *.json | ForEach-Object {
        Add-File (Join-Path "config" $_.Name)
    }
}

# Configuración de stlite (Estructura mínima)
$StliteConfig = @{
    entrypoint = "app.py"
    requirements = @(
        "streamlit", "pandas", "numpy", "plotly", "folium", 
        "streamlit-folium", "openpyxl", "xlrd", "pyodide-http", "geopy"
    )
    files = $FilesConfig
}

# Convertir a JSON de forma compacta
$JsonConfig = $StliteConfig | ConvertTo-Json -Depth 20 -Compress

# Convertir a Base64
$Bytes = [System.Text.Encoding]::UTF8.GetBytes($JsonConfig)
$Base64Config = [Convert]::ToBase64String($Bytes)

$HtmlTemplate = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>FORXIME/2 - Análisis | BioChavez Forester</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.0/build/stlite.css" />
    <style>
        body, html, #root { height: 100vh; margin: 0; background: #f8f9fa; font-family: 'Outfit', sans-serif; overflow: hidden; }
        #loading-overlay { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: white; display: flex; flex-direction: column; 
            justify-content: center; align-items: center; z-index: 9999; 
            transition: opacity 0.5s; 
        }
        .spinner { 
            width: 50px; height: 50px; border: 5px solid #E8F5E9; 
            border-top: 5px solid #2E7D32; border-radius: 50%; 
            animation: spin 1s linear infinite; 
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .loading-text { margin-top: 20px; color: #2E7D32; font-weight: 600; }
        #error-diag { 
            display: none; margin-top: 20px; padding: 15px; 
            background: #FFF3E0; border: 1px solid #FFB74D; 
            color: #E65100; border-radius: 8px; max-width: 80%; 
            font-family: monospace; font-size: 11px; white-space: pre-wrap;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .debug-btn { 
            margin-top: 20px; padding: 12px 24px; background: #2E7D32; 
            color: white; border: none; border-radius: 6px; cursor: pointer;
            font-weight: 600; font-family: 'Outfit', sans-serif;
        }
    </style>
</head>
<body>
    <div id="loading-overlay">
        <div class="spinner"></div>
        <div class="loading-text">Iniciando aplicaci&oacute;n...</div>
        <div style="margin-top: 10px; color: #888; font-size: 0.8rem;" id="timer-text">Descodificando motor de an&aacute;lisis...</div>
        <div id="error-diag"></div>
        <button id="show-debug" class="debug-btn" style="display:none">Ver detalles t&eacute;cnicos</button>
    </div>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.0/build/stlite.js"></script>
    <script>
        const diag = document.getElementById('error-diag');
        const showBtn = document.getElementById('show-debug');
        const timerText = document.getElementById('timer-text');
        
        showBtn.onclick = () => diag.style.display = 'block';

        function log(msg) {
            console.log(msg);
            diag.innerText += "\n" + msg;
        }

        window.onerror = (msg) => {
            log("[App Error] " + msg);
            showBtn.style.display = 'block';
        };

        (async function() {
            try {
                log("Paso 1: Descodificando configuraci&oacute;n Base64...");
                const b64 = "${Base64Config}";
                
                // Descodificaci&oacute;n segura para UTF-8 (soporta acentos y emojis)
                const binString = atob(b64);
                const bytes = Uint8Array.from(binString, (m) => m.codePointAt(0));
                const json = new TextDecoder().decode(bytes);
                const config = JSON.parse(json);
                
                log("Paso 2: Montando motor stlite...");
                timerText.innerText = "Instalando paquetes internos...";
                
                await stlite.mount(config, document.getElementById("root"));
                
                log("Paso 3: Exito. Limpiando interfaz.");
                setTimeout(() => {
                    document.getElementById('loading-overlay').style.opacity = '0';
                    setTimeout(() => { document.getElementById('loading-overlay').style.display = 'none'; }, 500);
                }, 500);

            } catch (e) {
                log("[Fatal Error] " + e.message);
                showBtn.style.display = 'block';
                timerText.innerText = "Error en la inicializaci&oacute;n.";
            }
        })();

        // Timeout de ayuda
        setTimeout(() => {
            if (document.getElementById('loading-overlay').style.display !== 'none') {
                log("[Warning] La carga est&aacute; excediendo los 30 segundos. Verifique su conexi&oacute;n y memoria RAM.");
                showBtn.style.display = 'block';
            }
        }, 30000);
    </script>
</body>
</html>
"@

# IMPORTANTE: Guardar como UTF-8 SIN BOM para evitar basura en el título/botones
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($TargetHtml, $HtmlTemplate, $Utf8NoBom)
Write-Host "Successfully generated optimized $TargetHtml WITHOUT BOM."
