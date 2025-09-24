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

  const isEditing = !!empresa;

  useEffect(() => {
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
      // Limpar formulário para adicionar novo
      setFormData({
        nome: '',
        cnpj: '',
        cidade: '',
        ramo_atuacao: '',
        telefone: '',
        email_contato: ''
      });
    }
  }, [empresa, isEditing]);


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dataToSend = isEditing ? { nome: formData.nome, cidade: formData.cidade, ramo_atuacao: formData.ramo_atuacao, telefone: formData.telefone } : formData;
    onSave(dataToSend);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-lg">
        <h2 className="text-2xl font-bold mb-6">{isEditing ? 'Editar Empresa' : 'Adicionar Nova Empresa'}</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          
          <input name="nome" value={formData.nome} onChange={handleChange} placeholder="Nome da Empresa" required className="form-input"/>
          <input name="cidade" value={formData.cidade} onChange={handleChange} placeholder="Cidade" required className="form-input"/>
          <input name="ramo_atuacao" value={formData.ramo_atuacao} onChange={handleChange} placeholder="Ramo de Atuação" required className="form-input"/>
          <input name="telefone" value={formData.telefone} onChange={handleChange} placeholder="Telefone" required className="form-input"/>
          
          {/* CNPJ e Email só são editáveis na criação */}
          {!isEditing && (
            <>
              <input name="cnpj" value={formData.cnpj} onChange={handleChange} placeholder="CNPJ (14 dígitos)" required pattern="\d{14}" title="O CNPJ deve conter 14 dígitos numéricos." className="form-input"/>
              <input type="email" name="email_contato" value={formData.email_contato} onChange={handleChange} placeholder="Email de Contato" required className="form-input"/>
            </>
          )}

          <div className="flex justify-end space-x-4 mt-8">
            <button type="button" onClick={onClose} className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-lg">Cancelar</button>
            <button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EmpresaModal;