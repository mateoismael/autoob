from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from models import Contratacion
from typing import Literal
import time
import re


class SEACEScraper:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://prod6.seace.gob.pe"

    def calcular_estado_tiempo(self, horas_restantes: float) -> Literal["rojo", "amarillo", "verde"]:
        """Calcula el estado del tiempo basado en las horas restantes"""
        if horas_restantes < 24:
            return "rojo"
        elif horas_restantes <= 72:
            return "amarillo"
        else:
            return "verde"

    def extraer_contrataciones(self, driver) -> list[Contratacion]:
        """Extrae las contrataciones del buscador público"""
        contrataciones = []

        try:
            # Ir al buscador público
            print("Navegando al buscador público...")
            driver.get(f"{self.base_url}/buscador-publico/")
            time.sleep(5)  # Dar tiempo para que cargue JavaScript

            # Esperar a que carguen los resultados
            print("Esperando que cargue la página...")
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except:
                print("Timeout esperando body, continuando...")
            
            time.sleep(3)

            # Extraer el HTML completo para análisis
            page_source = driver.page_source
            print(f"HTML cargado: {len(page_source)} bytes")

            # Método 1: Buscar todos los enlaces "Ver detalle"
            print("\n=== Método 1: Buscando enlaces 'Ver detalle' ===")
            links_detalle = driver.find_elements(By.PARTIAL_LINK_TEXT, "Ver detalle")
            print(f"Encontrados {len(links_detalle)} enlaces 'Ver detalle'")

            # Encontrar los contenedores padre de cada enlace
            items = []
            for link in links_detalle[:15]:  # Máximo 15 contrataciones
                try:
                    # Subir al contenedor padre que tiene toda la info
                    parent = link.find_element(By.XPATH, "./ancestor::*[contains(text(), 'CM-')]")
                    items.append(parent)
                except:
                    # Si no funciona, intentar con el padre directo
                    try:
                        parent = link.find_element(By.XPATH, "./../..")
                        items.append(parent)
                    except:
                        pass

            print(f"Contenedores encontrados: {len(items)}")

            # Si no encontramos con el método 1, intentar método 2
            if len(items) == 0:
                print("\n=== Método 2: Buscando por patrón CM- ===")
                # Buscar todos los elementos que contengan "CM-"
                all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'CM-')]")
                print(f"Elementos con 'CM-': {len(all_elements)}")
                
                for elem in all_elements[:15]:
                    try:
                        # Intentar obtener el contenedor completo
                        parent = elem.find_element(By.XPATH, "./..")
                        if len(parent.text) > 100:  # Debe tener contenido sustancial
                            items.append(parent)
                    except:
                        pass

            print(f"\n=== Procesando {len(items)} contrataciones ===")

            count = 0
            for item in items:
                try:
                    text_content = item.text.strip()

                    # Debug: Mostrar contenido
                    if count < 3:  # Solo primeros 3 para debugging
                        print(f"\n--- Contratación {count + 1} ---")
                        print(f"Texto: {text_content[:300]}")

                    # Extraer código (patrón CM-XXX-XXXX-...)
                    codigo_match = re.search(r'CM-[\d\w]+-[\d]+-[\w\-\.]+', text_content)
                    if not codigo_match:
                        codigo_match = re.search(r'CM-[\d]+-[\d]+-[\w]+', text_content)
                    codigo = codigo_match.group(0) if codigo_match else "N/A"

                    # Extraer líneas
                    lines = [l.strip() for l in text_content.split("\n") if l.strip()]

                    # Extraer entidad (línea después de "Vigente" o similar)
                    entidad = "Sin entidad"
                    for i, line in enumerate(lines):
                        if line in ["Vigente", "Publicado", "En proceso"]:
                            if i + 1 < len(lines):
                                entidad = lines[i + 1]
                                break
                        elif any(word in line.upper() for word in ["MUNICIPALIDAD", "MINISTERIO", "GOBIERNO", "EMPRESA", "UNIVERSIDAD", "REGION"]):
                            if len(line) > 15 and "CM-" not in line:
                                entidad = line
                                break

                    # Extraer descripción (línea que empieza con "Servicio:" o "Bien:")
                    descripcion = "Sin descripción"
                    for line in lines:
                        if line.startswith("Servicio:") or line.startswith("Bien:"):
                            descripcion = line
                            break

                    # Extraer fechas de cotización
                    fecha_text = ""
                    for line in lines:
                        if line.startswith("Cotizaciones:"):
                            fecha_text = line.replace("Cotizaciones:", "").strip()
                            break

                    # Parsear fecha límite
                    fecha_limite = datetime.now(timezone.utc) + timedelta(hours=48)
                    fecha_publicacion = None
                    
                    try:
                        if " - " in fecha_text:
                            partes = fecha_text.split(" - ")
                            fecha_fin_str = partes[1].strip()
                            
                            # Formato: DD/MM/YYYY HH:MM:SS
                            fecha_limite = datetime.strptime(fecha_fin_str, "%d/%m/%Y %H:%M:%S")
                            # Convertir a timezone aware (Perú es UTC-5)
                            fecha_limite = fecha_limite.replace(tzinfo=timezone.utc)
                            
                            # Fecha de inicio como fecha de publicación
                            fecha_inicio_str = partes[0].strip()
                            fecha_publicacion = datetime.strptime(fecha_inicio_str, "%d/%m/%Y %H:%M:%S")
                            fecha_publicacion = fecha_publicacion.replace(tzinfo=timezone.utc)
                    except Exception as e:
                        print(f"Error parseando fecha '{fecha_text}': {e}")

                    # Calcular tiempo restante
                    ahora = datetime.now(timezone.utc)
                    tiempo_restante = (fecha_limite - ahora).total_seconds() / 3600

                    # Calcular estado del tiempo
                    estado_tiempo = self.calcular_estado_tiempo(tiempo_restante)

                    # Buscar URL de detalle
                    url_detalle = f"{self.base_url}/buscador-publico/"
                    try:
                        link = item.find_element(By.PARTIAL_LINK_TEXT, "Ver detalle")
                        url_detalle = link.get_attribute("href")
                    except:
                        pass

                    contratacion = Contratacion(
                        codigo=codigo,
                        descripcion=descripcion,
                        entidad=entidad,
                        fecha_limite=fecha_limite,
                        tiempo_restante_horas=round(tiempo_restante, 2),
                        estado_tiempo=estado_tiempo,
                        url_detalle=url_detalle,
                        fecha_publicacion=fecha_publicacion
                    )

                    contrataciones.append(contratacion)
                    count += 1
                    
                    print(f"✓ Extraída: {codigo}")

                    if count >= 10:  # Limitar a 10
                        break

                except Exception as e:
                    print(f"Error extrayendo item: {e}")
                    continue

            print(f"\n{'='*60}")
            print(f"Total de contrataciones extraídas: {len(contrataciones)}")
            print(f"{'='*60}")

        except Exception as e:
            print(f"Error en extracción: {e}")
            import traceback
            traceback.print_exc()

        return contrataciones

    def scrape(self) -> list[Contratacion]:
        """Método principal de scraping usando Selenium"""
        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Configurar timeouts
        chrome_options.page_load_strategy = 'normal'

        driver = None
        max_retries = 2
        
        for intento in range(max_retries):
            try:
                print(f"Iniciando navegador Chrome (intento {intento + 1}/{max_retries})...")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Configurar timeouts
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)
                
                contrataciones = self.extraer_contrataciones(driver)
                
                if len(contrataciones) > 0:
                    return contrataciones
                elif intento < max_retries - 1:
                    print(f"No se encontraron contrataciones, reintentando...")
                    if driver:
                        driver.quit()
                        driver = None
                    time.sleep(2)
                else:
                    return contrataciones
                    
            except Exception as e:
                print(f"Error en scraping (intento {intento + 1}): {e}")
                if intento < max_retries - 1:
                    print("Reintentando...")
                    if driver:
                        try:
                            driver.quit()
                        except:
                            pass
                        driver = None
                    time.sleep(3)
                else:
                    import traceback
                    traceback.print_exc()
                    return []
            finally:
                if driver and intento == max_retries - 1:
                    try:
                        driver.quit()
                        print("Navegador cerrado")
                    except:
                        pass
        
        return []


def get_contrataciones(username: str, password: str) -> list[Contratacion]:
    """Función helper para obtener contrataciones"""
    scraper = SEACEScraper(username, password)
    return scraper.scrape()
