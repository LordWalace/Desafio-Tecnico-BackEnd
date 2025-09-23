import { useState, useEffect } from 'react';

const API_URL = 'http://127.0.0.1:8000';

function ListaEmpresas({ token, onLogout }) {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) {
        setLoading(false);
        return;
    };

    const fetchEmpresas = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_URL}/empresas/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
          throw new Error('Falha ao buscar dados. A sua sessão pode ter expirado.');
        }

        const data = await response.json();
        setEmpresas(data);
        setError(null);
      } catch (err) {
        setError(err.message);
        setEmpresas([]);
      } finally {
        setLoading(false);
      }
    };

    fetchEmpresas();
  }, [token]);

  if (loading) return <p className="text-center text-white animate-pulse">A carregar empresas...</p>;
  
  return (
    <div className="bg-white/95 backdrop-blur-md p-6 sm:p-8 rounded-xl shadow-2xl animate-fade-in border border-slate-300">
        <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-800">Empresas Clientes</h2>
            <button
                onClick={onLogout}
                className="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors text-sm font-medium"
            >
                Sair
            </button>
        </div>

        {error && <p className="text-red-500 bg-red-100 p-3 rounded text-center mb-4">{`Erro: ${error}`}</p>}

        <ul className="space-y-4">
            {empresas.length > 0 ? (
                empresas.map((empresa) => (
                    <li key={empresa.id} className="p-4 border border-gray-200 rounded-lg hover:shadow-md hover:border-indigo-300 transition-all duration-300">
                        <h3 className="text-xl font-semibold text-indigo-700">{empresa.nome}</h3>
                        <div className="flex items-center text-sm text-gray-600 mt-2 gap-4">
                            <span><strong>Cidade:</strong> {empresa.cidade}</span>
                            <span><strong>Ramo:</strong> {empresa.ramo_atuacao}</span>
                        </div>
                        <p className="text-sm text-gray-500 mt-2"><strong>Email:</strong> {empresa.email_contato}</p>
                    </li>
                ))
            ) : (
                !error && <p className="text-center text-gray-500 py-8">Nenhuma empresa encontrada.</p>
            )}
        </ul>
    </div>
  );
}

export default ListaEmpresas;