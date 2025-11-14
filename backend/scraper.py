from datetime import datetime, timezone
from playwright.sync_api import sync_playwright, Page
from models import Contratacion
from typing import Literal
import time


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

    def extraer_contrataciones(self, page: Page) -> list[Contratacion]:
        """Extrae las contrataciones del buscador público"""
        contrataciones = []

        try:
            # Ir al buscador público
            print("Navegando al buscador público...")
            page.goto(f"{self.base_url}/buscador-publico/", wait_until="networkidle", timeout=60000)
            time.sleep(2)

            # Esperar a que carguen los resultados
            print("Esperando resultados...")
            page.wait_for_selector('[class*="MuiGrid-root"], [class*="card"]', timeout=10000)
            time.sleep(2)

            # Extraer el contenido HTML para análisis
            content = page.content()
            print(f"Página cargada, tamaño: {len(content)} bytes")

            # Buscar elementos de contratación
            # Intentar múltiples selectores según la estructura de SEACE
            items = page.query_selector_all('[class*="MuiPaper"], [class*="MuiCard"], div[class*="contrat"]')

            print(f"Encontrados {len(items)} elementos potenciales")

            # Si no encontramos nada con esos selectores, usar un approach más simple
            if len(items) == 0:
                # Buscar por estructura de tabla o lista
                items = page.query_selector_all('tr, li, article, section')
                print(f"Intento alternativo: {len(items)} elementos")

            count = 0
            for item in items[:20]:  # Procesar máximo 20 elementos
                try:
                    text_content = item.inner_text().strip()

                    # Filtrar solo elementos que parecen ser contrataciones
                    if len(text_content) < 50 or "CM-" not in text_content:
                        continue

                    print(f"\nProcesando elemento {count + 1}:")
                    print(f"Contenido: {text_content[:200]}")

                    # Extraer código (buscar patrón CM-XXX-XXXX)
                    codigo = "N/A"
                    for line in text_content.split("\n"):
                        if "CM-" in line:
                            codigo = line.strip()
                            break

                    # Extraer información básica del texto
                    lines = [l.strip() for l in text_content.split("\n") if l.strip()]

                    descripcion = "Sin descripción"
                    entidad = "Sin entidad"
                    fecha_text = ""

                    # Buscar entidad y descripción en las líneas
                    for i, line in enumerate(lines):
                        if "SERVICIO" in line.upper() or "BIEN" in line.upper():
                            descripcion = line[:200]
                        if i < len(lines) - 1 and len(line) > 20 and "MUNICIPALIDAD" in line.upper() or "MINISTERIO" in line.upper():
                            entidad = line
                        if "Cotizaciones:" in line or "/" in line and ":" in line:
                            fecha_text = line

                    # Parsear fecha (intentar varios formatos)
                    fecha_limite = datetime.now(timezone.utc)
                    try:
                        if " - " in fecha_text:
                            fecha_fin = fecha_text.split(" - ")[1].strip()
                            # Remover "Cotizaciones:" si existe
                            fecha_fin = fecha_fin.replace("Cotizaciones:", "").strip()
                            # Intentar parsear DD/MM/YYYY HH:MM:SS
                            if "/" in fecha_fin and ":" in fecha_fin:
                                parts = fecha_fin.split()
                                if len(parts) >= 2:
                                    fecha_limite = datetime.strptime(f"{parts[0]} {parts[1]}", "%d/%m/%Y %H:%M:%S")
                                    fecha_limite = fecha_limite.replace(tzinfo=timezone.utc)
                    except Exception as e:
                        print(f"Error parseando fecha: {e}")
                        # Usar fecha por defecto (48 horas en el futuro)
                        from datetime import timedelta
                        fecha_limite = datetime.now(timezone.utc) + timedelta(hours=48)

                    # Calcular tiempo restante
                    ahora = datetime.now(timezone.utc)
                    tiempo_restante = (fecha_limite - ahora).total_seconds() / 3600

                    # Calcular estado del tiempo
                    estado_tiempo = self.calcular_estado_tiempo(tiempo_restante)

                    # Buscar URL de detalle
                    url_detalle = f"{self.base_url}/buscador-publico/"
                    try:
                        link = item.query_selector('a[href*="detalle"], a[href*="contratacion"]')
                        if link:
                            href = link.get_attribute("href")
                            if href:
                                url_detalle = f"{self.base_url}{href}" if not href.startswith("http") else href
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
                        fecha_publicacion=None
                    )

                    contrataciones.append(contratacion)
                    count += 1

                    if count >= 10:  # Limitar a 10 resultados
                        break

                except Exception as e:
                    print(f"Error extrayendo item: {e}")
                    continue

            print(f"\nTotal de contrataciones extraídas: {len(contrataciones)}")

        except Exception as e:
            print(f"Error en extracción: {e}")
            import traceback
            traceback.print_exc()

        return contrataciones

    def scrape(self) -> list[Contratacion]:
        """Método principal de scraping"""
        with sync_playwright() as p:
            print("Iniciando navegador...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            try:
                contrataciones = self.extraer_contrataciones(page)
                return contrataciones
            finally:
                browser.close()
                print("Navegador cerrado")


def get_contrataciones(username: str, password: str) -> list[Contratacion]:
    """Función helper para obtener contrataciones"""
    scraper = SEACEScraper(username, password)
    return scraper.scrape()
