# 🚀 Guía Rápida de Inicio

## Instalación y Ejecución en 5 pasos

### 1. Instalar dependencias del Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Instalar dependencias del Frontend

```bash
cd ../frontend
npm install
```

### 3. Iniciar el Backend

En una terminal (dentro de `backend/`):

```bash
venv\Scripts\activate
python main.py
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Iniciar el Frontend

En otra terminal (dentro de `frontend/`):

```bash
npm run dev
```

Deberías ver:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

### 5. Usar la aplicación

1. Abre tu navegador en `http://localhost:5173`
2. Haz clic en el botón **"Actualizar"**
3. Espera unos segundos mientras busca las contrataciones
4. ¡Listo! Verás la tabla con las contrataciones

## 🎨 Características

- **🔴 Rojo**: Menos de 24 horas para postular
- **🟡 Amarillo**: Entre 24-72 horas
- **🟢 Verde**: Más de 72 horas

## ⚠️ Troubleshooting

### Backend no inicia
```bash
# Verifica que estés en el directorio correcto
cd backend

# Verifica que el entorno virtual esté activado
venv\Scripts\activate

# Verifica las dependencias
pip list
```

### Frontend muestra error de conexión
- Asegúrate de que el backend esté corriendo en `http://localhost:8000`
- Verifica en la consola del navegador (F12) si hay errores

### No aparecen resultados
- El scraper puede tardar hasta 30 segundos
- Verifica los logs en la terminal del backend
- Puede que no haya contrataciones activas en ese momento

## 📝 Notas

- El archivo `.env` ya contiene las credenciales necesarias
- El backend usa el buscador público de SEACE (no requiere login)
- Los filtros están preconfigurados para Lima, tecnología y bienes/servicios

## 🔧 Tecnologías

- **Backend**: Python 3.9+, FastAPI, Playwright
- **Frontend**: React 19, TypeScript 5.8, Tailwind CSS 4
- **Mejores prácticas 2025**:
  - TypeScript strict mode
  - `satisfies` operator
  - `as const` para literal types
  - Utility types avanzados
