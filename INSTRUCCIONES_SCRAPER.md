# Instrucciones para Usar el Buscador de SEACE

## 🎯 Importante: NO necesitas hacer login

El buscador de contrataciones menores de SEACE tiene una **versión pública** que no requiere autenticación:

**URL del buscador público:** https://prod6.seace.gob.pe/buscador-publico/

Puedes acceder directamente desde tu navegador para ver las contrataciones disponibles.

---

## ❌ El problema del login que reportaste

La URL `https://prod6.seace.gob.pe/auth-entidad/` es para **entidades gubernamentales** que publican contrataciones, **NO** para buscar contratos.

Por eso el RUC `20614356040` probablemente te da error - esa sección es solo para entidades autorizadas.

---

## ✅ Cómo funciona tu scraper

Tu scraper está configurado para usar el **buscador público**, por lo que:

1. **No requiere credenciales válidas** (las del .env no se usan realmente)
2. **Accede directamente** a https://prod6.seace.gob.pe/buscador-publico/
3. **Extrae la información** usando Playwright (navegador automatizado)
4. **Muestra los resultados** en la aplicación web

---

## 🚀 Cómo iniciar el sistema

### Opción 1: Probar solo el scraper

```bash
cd backend

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Ejecutar prueba del scraper
python test_scraper.py
```

Esto mostrará en consola las contrataciones encontradas.

### Opción 2: Iniciar el sistema completo (Backend + Frontend)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
python main.py
```

El backend estará en: http://localhost:8002

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # Solo la primera vez
npm run dev
```

El frontend estará en: http://localhost:5173

**Uso:**
1. Abre http://localhost:5173 en tu navegador
2. Haz clic en "Actualizar"
3. El sistema hará scraping del buscador público
4. Verás las contrataciones con colores:
   - 🔴 Rojo: < 24 horas
   - 🟡 Amarillo: 24-72 horas
   - 🟢 Verde: > 72 horas

---

## 🔧 Solución de problemas

### Error: "ModuleNotFoundError"
**Causa:** El entorno virtual no está activado o faltan dependencias

**Solución:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

### Error: "ERR_TUNNEL_CONNECTION_FAILED" o problemas de red
**Causa:** Playwright no puede acceder a Internet (proxy, firewall, etc.)

**Soluciones:**
1. Verificar que tu computadora tenga acceso a Internet
2. Si estás detrás de un proxy corporativo, configurar:
   ```bash
   export HTTP_PROXY=http://tu-proxy:puerto
   export HTTPS_PROXY=http://tu-proxy:puerto
   ```
3. Probar acceder manualmente a https://prod6.seace.gob.pe/buscador-publico/ en tu navegador

### No aparecen contrataciones
**Posibles causas:**
1. No hay contrataciones activas en ese momento (normal)
2. La estructura del sitio SEACE cambió (requiere actualizar selectores CSS)
3. El buscador público requiere interacción adicional (ej: hacer clic en algún filtro)

**Solución:**
- Revisar los logs del backend para ver detalles
- Acceder manualmente al buscador público para verificar que haya contratos
- Si es necesario, actualizar `scraper.py` con nuevos selectores CSS

---

## 📊 Verificar que el buscador público funciona

**Manualmente:**
1. Abre en tu navegador: https://prod6.seace.gob.pe/buscador-publico/
2. Deberías ver una interfaz con filtros y resultados
3. No debería pedirte login

**Con el scraper:**
```bash
cd backend
source venv/bin/activate
python test_scraper.py
```

Deberías ver output como:
```
================================================================================
RESULTADOS: 5 contrataciones encontradas
================================================================================

1. Código: CM-XXX-2025-ENTIDAD
   Descripción: SERVICIO DE...
   Entidad: MUNICIPALIDAD...
   Tiempo restante: 45.2 horas
   Estado: AMARILLO
   URL: https://prod6.seace.gob.pe/...
```

---

## 🎯 Resumen

1. ✅ **No necesitas hacer login** - usa el buscador público
2. ✅ **El código ya está listo** - todo configurado correctamente
3. ✅ **Solo necesitas ejecutarlo en tu computadora local**
4. ❌ **No intentes usar auth-entidad** - esa sección es para entidades gubernamentales

---

## 📞 Si sigues teniendo problemas

1. Verifica que puedes acceder a https://prod6.seace.gob.pe/buscador-publico/ desde tu navegador
2. Revisa los logs del backend cuando ejecutes `python main.py`
3. Comprueba que el puerto 8002 no esté en uso por otra aplicación
4. Asegúrate de tener Python 3.9+ y Node.js 18+ instalados
