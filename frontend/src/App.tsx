import { useState } from "react";

// Tipos con literal types para mayor seguridad
const ESTADOS_TIEMPO = ["rojo", "amarillo", "verde"] as const;
type EstadoTiempo = typeof ESTADOS_TIEMPO[number];

interface Contratacion {
  codigo: string;
  descripcion: string;
  entidad: string;
  fecha_limite: string;
  tiempo_restante_horas: number;
  estado_tiempo: EstadoTiempo;
  url_detalle: string;
}

interface ContratacionResponse {
  contrataciones: Contratacion[];
  total: number;
  timestamp: string;
}

function App() {
  const [contrataciones, setContrataciones] = useState<Contratacion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);

  const fetchContrataciones = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8002/api/contrataciones");

      if (!response.ok) {
        throw new Error("Error al obtener las contrataciones");
      }

      const data: ContratacionResponse = await response.json();
      setContrataciones(data.contrataciones);
      setLastUpdate(new Date().toLocaleString("es-PE"));
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Error desconocido"
      );
    } finally {
      setLoading(false);
    }
  };

  // Mapa de colores con type-safety usando satisfies
  const COLOR_MAP = {
    rojo: "bg-red-100 text-red-800 border-red-300",
    amarillo: "bg-yellow-100 text-yellow-800 border-yellow-300",
    verde: "bg-green-100 text-green-800 border-green-300",
  } as const satisfies Record<EstadoTiempo, string>;

  const getColorClass = (estado: EstadoTiempo): string => {
    return COLOR_MAP[estado];
  };

  const formatTiempo = (horas: number) => {
    if (horas < 1) {
      return `${Math.round(horas * 60)} minutos`;
    } else if (horas < 24) {
      return `${Math.round(horas)} horas`;
    } else {
      const dias = Math.floor(horas / 24);
      const horasRestantes = Math.round(horas % 24);
      return `${dias} día${dias > 1 ? "s" : ""} ${horasRestantes}h`;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Buscador de Contrataciones SEACE
          </h1>
          <p className="text-gray-600">
            Contrataciones de tecnología y bienes/servicios en Lima
          </p>
        </div>

        {/* Control Panel */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-6 flex justify-between items-center">
          <div className="text-sm text-gray-600">
            {lastUpdate && (
              <span>Última actualización: {lastUpdate}</span>
            )}
            {contrataciones.length > 0 && (
              <span className="ml-4 font-semibold">
                {contrataciones.length} contrataciones encontradas
              </span>
            )}
          </div>
          <button
            onClick={fetchContrataciones}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            {loading ? "Actualizando..." : "Actualizar"}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Buscando contrataciones...</p>
          </div>
        )}

        {/* Table */}
        {!loading && contrataciones.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Estado
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Código
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Descripción
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Entidad
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tiempo Restante
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {contrataciones.map((item, index) => (
                    <tr
                      key={index}
                      className={`hover:bg-gray-50 transition-colors ${getColorClass(
                        item.estado_tiempo
                      )} bg-opacity-20`}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${getColorClass(
                            item.estado_tiempo
                          )}`}
                        >
                          {item.estado_tiempo === "rojo" && "🔴"}
                          {item.estado_tiempo === "amarillo" && "🟡"}
                          {item.estado_tiempo === "verde" && "🟢"}
                          <span className="ml-1 capitalize">
                            {item.estado_tiempo}
                          </span>
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {item.codigo}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-700 max-w-md">
                        {item.descripcion}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {item.entidad}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                        {formatTiempo(item.tiempo_restante_horas)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <a
                          href={item.url_detalle}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 font-medium"
                        >
                          Ver detalle →
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && contrataciones.length === 0 && !error && (
          <div className="text-center py-12 bg-white rounded-lg shadow-sm">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              No hay contrataciones
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Haz clic en "Actualizar" para buscar contrataciones
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
