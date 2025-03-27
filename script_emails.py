from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar Selenium con ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar en modo headless para mayor velocidad
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

# Archivo con los emails a verificar
input_file = "emails.txt"
output_file = "emails_verified.txt"

# XPath de los elementos
continue_xpath = "/html/body/div[1]/div/div/div/div/form/button[2]"
button_xpath = "/html/body/div[1]/div/div/div/div/form/button[2]"

# Función para verificar si un email está registrado en Figma
def check_email(email):
    url = f"https://www.figma.com/invites/auth?email={email}&is_not_gen_0=true&resource_type=file"
    driver.get(url)

    try:
        # Esperar hasta que el botón "Continue with email" esté visible
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, continue_xpath))).click()
        time.sleep(2)  # Pequeña espera para que la página cargue bien

        # Obtener el texto del botón final
        button_text = driver.find_element(By.XPATH, button_xpath).text

        if "Log in" in button_text:
            return "✅ Registrado"
        elif "Create account" in button_text:
            return "❌ No registrado"
        else:
            return "⚠️ No se pudo determinar"

    except Exception as e:
        return f"❌ Error: {e}"

# Leer los emails desde el archivo y verificar cada uno
with open(input_file, "r", encoding="utf-8") as file:
    emails = [line.strip() for line in file]

results = {}
for email in emails:
    status = check_email(email)
    results[email] = status
    print(f"{email} -> {status}")

    # Evitar detección por automatización con pausas
    time.sleep(3)

# Guardar los resultados en un archivo
with open(output_file, "w", encoding="utf-8") as file:
    for email, status in results.items():
        file.write(f"{email} -> {status}\n")

print(f"\n[✅] Verificación completada. Resultados guardados en {output_file}")

# Cerrar el navegador de Selenium
driver.quit()

