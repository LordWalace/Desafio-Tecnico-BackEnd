import { useState, useEffect } from 'react';

function EmpresaModal({ isOpen, onClose, onSave, empresa }) {
  const [formData, setFormData] = useState({
    nome: '',
    cnpj: '',
    cidade: '',
    ramo_atuacao: '',
    telefone: '',
    email_contato: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionError, setSubmissionError] = useState(null);

  const isEditing = !!empresa;

  useEffect(() => {
    if (isOpen) {
      if (isEditing) {
        setFormData({
          nome: empresa.nome || '',
          cnpj: empresa.cnpj || '',
          cidade: empresa.cidade || '',
          ramo_atuacao: empresa.ramo_atuacao || '',
          telefone: empresa.telefone || '',
          email_contato: empresa.email_contato || ''
        });
      } else {
        setFormData({
          nome: '',
          cnpj: '',
          cidade: '',
          ramo_atuacao: '',
          telefone: '',
          email_contato: ''
        });
      }
      setSubmissionError(null);
    }
  }, [empresa, isEditing, isOpen]);


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmissionError(null);

    try {
      const dataToSend = isEditing 
        ? { nome: formData.nome, cidade: formData.cidade, ramo_atuacao: formData.ramo_atuacao, telefone: formData.telefone, email_contato: formData.email_contato } 
        : formData;
      await onSave(dataToSend);
      onClose();
    } catch (err) {
      setSubmissionError(err.message || 'Ocorreu um erro. Verifique os dados e tente novamente.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50 animate-fade-in-fast">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-lg">
        <h2 className="text-2xl font-bold mb-6 text-center">{isEditing ? 'Editar Empresa' : 'Adicionar Nova Empresa'}</h2>
        
        <form onSubmit={handleSubmit}>
          
          {isEditing ? (
            // Layout para EDIÇÃO (5 campos) com estrutura explícita
            <div className="space-y-4">
              {/* CORREÇÃO: Removida a div extra para permitir a centralização correta do input */}
              <div className="flex flex-col items-center">
                <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Empresa</label>
                <input id="nome" name="nome" value={formData.nome} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center w-full sm:w-3/4"/>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="cidade" className="block text-sm font-medium text-gray-700">Cidade</label>
                  <input id="cidade" name="cidade" value={formData.cidade} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
                </div>
                <div>
                  <label htmlFor="ramo_atuacao" className="block text-sm font-medium text-gray-700">Ramo de Atuação</label>
                  <input id="ramo_atuacao" name="ramo_atuacao" value={formData.ramo_atuacao} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
                </div>
                <div>
                  <label htmlFor="telefone" className="block text-sm font-medium text-gray-700">Telefone</label>
                  <input id="telefone" name="telefone" value={formData.telefone} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
                </div>
                <div>
                  <label htmlFor="email_contato" className="block text-sm font-medium text-gray-700">Email de Contato</label>
                  <input id="email_contato" type="email" name="email_contato" value={formData.email_contato} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
                </div>
              </div>
            </div>
          ) : (
            // Layout para CRIAÇÃO (6 campos)
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Empresa</label>
                <input id="nome" name="nome" value={formData.nome} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
              </div>
              <div>
                <label htmlFor="cnpj" className="block text-sm font-medium text-gray-700">CNPJ</label>
                <input id="cnpj" name="cnpj" value={formData.cnpj} onChange={handleChange} placeholder="Apenas 14 dígitos" required pattern="\d{14}" title="O CNPJ deve conter 14 dígitos numéricos." className="form-input mt-1 bg-gray-50 text-center"/>
              </div>
              <div>
                <label htmlFor="cidade" className="block text-sm font-medium text-gray-700">Cidade</label>
                <input id="cidade" name="cidade" value={formData.cidade} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
              </div>
              <div>
                <label htmlFor="ramo_atuacao" className="block text-sm font-medium text-gray-700">Ramo de Atuação</label>
                <input id="ramo_atuacao" name="ramo_atuacao" value={formData.ramo_atuacao} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
              </div>
              <div>
                <label htmlFor="telefone" className="block text-sm font-medium text-gray-700">Telefone</label>
                <input id="telefone" name="telefone" value={formData.telefone} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
              </div>
              <div>
                <label htmlFor="email_contato" className="block text-sm font-medium text-gray-700">Email de Contato</label>
                <input id="email_contato" type="email" name="email_contato" value={formData.email_contato} onChange={handleChange} required className="form-input mt-1 bg-gray-50 text-center"/>
              </div>
            </div>
          )}

          {submissionError && (
            <div className="text-red-600 bg-red-100 p-3 rounded-md text-center text-sm mt-4">
                {submissionError}
            </div>
          )}

          <div className="flex justify-end space-x-4 pt-6">
            <button type="button" onClick={onClose} disabled={isSubmitting} className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-lg disabled:opacity-50">Cancelar</button>
            <button type="submit" disabled={isSubmitting} className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg disabled:bg-indigo-400">
              {isSubmitting ? 'A guardar...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EmpresaModal;