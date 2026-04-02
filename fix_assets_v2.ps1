$path = 'c:\Users\erick\.gemini\antigravity\scratch\FORXIME2\utils\assets_base64.py'
$content = [System.IO.File]::ReadAllText($path)

# Ensure it's not already fixed (idempotency)
if ($content.StartsWith("LOGO_B64 = '''")) {
    Write-Host "Already fixed."
    exit 0
}

# Replace the opening quote
$content = $content.Replace("LOGO_B64 = '", "LOGO_B64 = '''")

# Replace the closing quote
$lastQuoteIndex = $content.LastIndexOf("'")
if ($lastQuoteIndex -ge 0) {
    $content = $content.Substring(0, $lastQuoteIndex) + "'''" + $content.Substring($lastQuoteIndex + 1)
}

# Save without BOM
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $content, $Utf8NoBom)
Write-Host "Successfully fixed assets_base64.py syntax."
