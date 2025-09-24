import { useState, useEffect, useCallback } from 'react';
import ListaEmpresas from './ListaEmpresas';
import EmpresaModal from './EmpresaModal';
import * as api from '../services/api';

function Dashboard({ token, onLogout }) {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [empresaAtual, setEmpresaAtual] = useState(null);
  const [filtros, setFiltros] = useState({ nome: '', cidade: '', ramo_atuacao: '' });

  const fetchEmpresas = useCallback(async () => {
    try {
      setLoading(true);
      const filtrosAtivos = Object.fromEntries(
        Object.entries(filtros).filter(([, value]) => value !== '')
      );
      const data = await api.getEmpresas(token, filtrosAtivos);
      setEmpresas(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [token, filtros]);

  useEffect(() => {
    fetchEmpresas();
  }, [fetchEmpresas]);

  const handleOpenModal = (empresa = null) => {
    setEmpresaAtual(empresa);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEmpresaAtual(null);
  };

  const handleSaveEmpresa = async (empresaData) => {
    try {
      if (empresaAtual) {
        await api.updateEmpresa(empresaAtual.id, empresaData, token);
      } else {
        await api.createEmpresa(empresaData, token);
      }
      handleCloseModal();
      fetchEmpresas();
    } catch (err) {
      alert(`Erro: ${err.message}`);
    }
  };
  
  const handleDeleteEmpresa = async (id) => {
    if (window.confirm('Tem a certeza de que deseja excluir esta empresa?')) {
        try {
            await api.deleteEmpresa(id, token);
            fetchEmpresas();
        } catch (err) {
            alert(`Erro: ${err.message}`);
        }
    }
  };

  const handleFiltroChange = (e) => {
    const { name, value } = e.target;
    setFiltros(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="bg-white/90 backdrop-blur-lg p-6 md:p-8 rounded-xl shadow-2xl animate-fade-in">
      {/* Cabeçalho do Painel */}
      <div className="flex justify-between items-center border-b border-gray-200 pb-4 mb-6">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-800">Painel de Clientes</h2>
        <button onClick={onLogout} className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg transition-colors text-sm">
          Sair
        </button>
      </div>

      {/* Painel de Ações: Filtros e Botão Adicionar */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <input type="text" name="nome" value={filtros.nome} onChange={handleFiltroChange} placeholder="Buscar por nome..." className="form-input"/>
          <input type="text" name="cidade" value={filtros.cidade} onChange={handleFiltroChange} placeholder="Filtrar por cidade..." className="form-input"/>
          <input type="text" name="ramo_atuacao" value={filtros.ramo_atuacao} onChange={handleFiltroChange} placeholder="Filtrar por ramo..." className="form-input"/>
        </div>
        <div className="flex justify-center mt-4">
          <button onClick={() => handleOpenModal()} className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg transition-colors">
            + Adicionar Nova Empresa
          </button>
        </div>
      </div>

      {/* Divisor e Título da Lista */}
      <div className="border-t border-gray-200 pt-6">
        <h3 className="text-xl font-semibold text-gray-700 mb-4">Empresas Registadas</h3>
        {loading && <p className="text-center text-gray-500">A carregar empresas...</p>}
        {error && <p className="text-center text-red-500 bg-red-100 p-3 rounded-md">{error}</p>}
        {!loading && !error && (
          <ListaEmpresas 
            empresas={empresas} 
            onEdit={handleOpenModal} 
            onDelete={handleDeleteEmpresa} 
          />
        )}
      </div>

      <EmpresaModal 
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSave={handleSaveEmpresa}
        empresa={empresaAtual}
      />
    </div>
  );
}

export default Dashboard;