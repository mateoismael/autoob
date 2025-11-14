# Automatizador de Búsqueda SEACE

Sistema automatizado para buscar y visualizar contrataciones menores de tecnología y bienes/servicios en SEACE (Sistema Electrónico de Contrataciones del Estado) de Perú.

## Características

- 🔍 Búsqueda automática de contrataciones menores a 8 UIT
- 🎯 Filtros: Tecnología, Bienes/Servicios, Lima
- ⏱️ Sistema de alertas por tiempo:
  - 🔴 Rojo: Menos de 24 horas
  - 🟡 Amarillo: 24-72 horas
  - 🟢 Verde: Más de 72 horas
- 🔄 Actualización manual bajo demanda
- 📊 Interfaz web moderna y responsiva

## Arquitectura

```
autoob/
├── backend/          # API Python (FastAPI + Playwright)
│   ├── main.py       # Servidor FastAPI
│   ├── scraper.py    # Lógica de scraping
│   ├── models.py     # Modelos Pydantic
│   └── requirements.txt
├── frontend/         # Aplicación React
│   ├── src/
│   │   ├── App.tsx   # Componente principal
│   │   └── ...
│   └── package.json
└── .env              # Credenciales
```

## Requisitos

- Python 3.9+
- Node.js 18+
- npm o yarn

## Instalación

### 1. Clonar/Descargar el proyecto

```bash
cd autoob
```

### 2. Configurar credenciales

Ya existe un archivo `.env` en la raíz del proyecto con las credenciales:

```env
user=20614356040
pass=Mamibeca11#$
```

### 3. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar navegadores de Playwright
playwright install
```

### 4. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install
```

## Uso

### Iniciar Backend

```bash
cd backend
venv\Scripts\activate  # Activar entorno virtual
python main.py
```

El backend estará disponible en: `http://localhost:8000`

### Iniciar Frontend

En otra terminal:

```bash
cd frontend
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

### Usar la aplicación

1. Abre el navegador en `http://localhost:5173`
2. Haz clic en el botón "Actualizar" para buscar contrataciones
3. Espera a que carguen los resultados
4. Visualiza las contrataciones con:
   - **Estado por color** (rojo, amarillo, verde)
   - **Código** de la contratación
   - **Descripción** del objeto
   - **Entidad** contratante
   - **Tiempo restante** para postular
   - **Enlace directo** al detalle en SEACE

## API Endpoints

### GET `/api/contrataciones`

Obtiene las contrataciones vigentes de tecnología y bienes/servicios en Lima.

**Response:**
```json
{
  "contrataciones": [
    {
      "codigo": "CM-117-2025-CPMP",
      "descripcion": "SERVICIO DE RENOVACIÓN...",
      "entidad": "CAJA DE PENSIONES MILITAR",
      "fecha_limite": "2025-11-19T15:00:00Z",
      "tiempo_restante_horas": 23.5,
      "estado_tiempo": "rojo",
      "url_detalle": "https://prod6.seace.gob.pe/...",
      "fecha_publicacion": null
    }
  ],
  "total": 1,
  "timestamp": "2025-11-13T10:00:00Z"
}
```

### GET `/health`

Verifica el estado del servidor.

## Tecnologías

### Backend
- FastAPI 0.121.2
- Playwright 1.56.0
- Pydantic 2.12.4
- Uvicorn 0.38.0

### Frontend
- React 19.1.0
- TypeScript 5.8.3
- Tailwind CSS 4.1.11
- Vite 7.0.4

## Troubleshooting

### El backend no inicia

- Verifica que el entorno virtual esté activado
- Verifica que todas las dependencias estén instaladas: `pip list`
- Verifica que Playwright esté instalado: `playwright install`

### El frontend no se conecta al backend

- Verifica que el backend esté corriendo en `http://localhost:8000`
- Verifica la consola del navegador para errores de CORS
- Verifica que ambos servidores estén en ejecución

### No aparecen contrataciones

- Verifica que las credenciales en `.env` sean correctas
- Revisa los logs del backend en la consola
- Puede que no haya contrataciones activas en ese momento

## Desarrollo

### Estructura del código

- `backend/scraper.py`: Contiene la lógica de scraping con Playwright
- `backend/main.py`: Define los endpoints de FastAPI
- `frontend/src/App.tsx`: Componente principal con la UI

### Próximas mejoras

- [ ] Agregar filtros personalizables desde el frontend
- [ ] Implementar notificaciones push
- [ ] Guardar historial de contrataciones
- [ ] Agregar modo de ejecución periódica automática
- [ ] Mejorar los selectores del scraper según la estructura real de SEACE

## Licencia

Proyecto de uso interno.
