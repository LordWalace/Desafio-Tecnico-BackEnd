const API_URL = 'http://127.0.0.1:8000';

/**
 * Função para fazer login e obter um token.
 * @param {string} username - O nome do utilizador.
 * @param {string} password - A senha.
 * @returns {Promise<string>} O token de acesso.
 */
export const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Utilizador ou senha inválidos.');
  }

  const data = await response.json();
  return data.access_token;
};

/**
 * Função para buscar a lista de empresas, com filtros opcionais.
 * @param {string} token - O token JWT de autenticação.
 * @param {object} filtros - Um objeto com os filtros (nome, cidade, ramo_atuacao).
 * @returns {Promise<Array>} A lista de empresas.
 */
export const getEmpresas = async (token, filtros = {}) => {
  const queryParams = new URLSearchParams(filtros).toString();
  
  const response = await fetch(`${API_URL}/empresas/?${queryParams}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error('Falha ao buscar empresas. Verifique a sua sessão.');
  }

  return response.json();
};

/**
 * Função para criar uma nova empresa.
 * @param {object} empresaData - Os dados da nova empresa.
 * @param {string} token - O token JWT.
 * @returns {Promise<object>} Os dados da empresa criada.
 */
export const createEmpresa = async (empresaData, token) => {
    const response = await fetch(`${API_URL}/empresas/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(empresaData)
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Falha ao criar empresa.');
    }
    return response.json();
};

/**
 * Função para atualizar uma empresa existente.
 * @param {number} id - O ID da empresa a ser atualizada.
 * @param {object} empresaData - Os novos dados da empresa.
 * @param {string} token - O token JWT.
 * @returns {Promise<object>} Os dados da empresa atualizada.
 */
export const updateEmpresa = async (id, empresaData, token) => {
    const response = await fetch(`${API_URL}/empresas/${id}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(empresaData)
    });
    if (!response.ok) {
        throw new Error('Falha ao atualizar empresa.');
    }
    return response.json();
};

/**
 * Função para excluir uma empresa.
 * @param {number} id - O ID da empresa a ser excluída.
 * @param {string} token - O token JWT.
 * @returns {Promise<void>}
 */
export const deleteEmpresa = async (id, token) => {
    const response = await fetch(`${API_URL}/empresas/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!response.ok && response.status !== 204) { // 204 No Content é uma resposta de sucesso para DELETE
        throw new Error('Falha ao excluir empresa.');
    }
};