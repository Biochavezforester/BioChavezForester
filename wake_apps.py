import time
from playwright.sync_api import sync_playwright

APPS = [
    {"name": "FORXIME", "url": "https://forxime2-0.streamlit.app/"},
    {"name": "ECOMETRICS", "url": "https://bioecometrics.streamlit.app/"}
]

def main():
    print("Iniciando Playwright para despertar las aplicaciones...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        for app in APPS:
            name = app["name"]
            url = app["url"]
            print(f"\n--- Procesando {name} ({url}) ---")
            page = context.new_page()
            
            try:
                print(f"Cargando la página...")
                page.goto(url, timeout=60000)
                
                # Esperar 15 segundos para asegurar que carguen los elementos iniciales de suspensión o de la app
                page.wait_for_timeout(15000)
                
                # Intentamos detectar el botón "Yes, get this app back up!"
                wake_button = page.get_by_role("button", name="Yes, get this app back up!")
                
                if wake_button.is_visible():
                    print("🚨 La aplicación está DORMIDA. Haciendo clic en 'Yes, get this app back up!'...")
                    wake_button.click()
                    
                    # Esperar 45 segundos para que la aplicación se despierte y cargue
                    print("Esperando 45 segundos para que se complete el despertar...")
                    page.wait_for_timeout(45000)
                    print("Revisando de nuevo...")
                    
                    if not wake_button.is_visible():
                        print("✅ ¡La aplicación se ha despertado con éxito!")
                    else:
                        print("⚠️ El botón sigue visible. Puede que esté tardando un poco más en arrancar.")
                else:
                    # Comprobamos si cargó Streamlit
                    st_app = page.locator("div.stApp")
                    if st_app.count() > 0 or page.locator("div[data-testid='stAppViewContainer']").count() > 0:
                        print("✅ La aplicación ya está DESPIERTA y funcionando correctamente.")
                    else:
                        print("ℹ️ No se detectó botón de suspensión. La app parece estar activa o cargando.")
                        
            except Exception as e:
                print(f"❌ Error al procesar {name}: {e}")
            finally:
                page.close()
                
        browser.close()
        print("\nProceso de keep-alive finalizado.")

if __name__ == "__main__":
    main()
