import { useState, useEffect } from 'react';
import LoginForm from './components/LoginForm';
import Dashboard from './components/DashBoard';

// Passo 1: Importe a sua imagem local a partir da pasta 'assets'.
// Certifique-se de que o nome do ficheiro ('fundo.jpg') corresponde ao nome da sua imagem.
import imagemDeFundo from './assets/MesaEscritorio1.jpg'; 

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('authToken'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }, [token]);

  const handleLoginSuccess = (newToken) => {
    setToken(newToken);
  };

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <div className="relative min-h-screen w-full bg-slate-900">
      {/* Camada de Fundo com Imagem */}
      <div
        className="absolute inset-0 bg-cover bg-center transition-opacity duration-1000"
        // Passo 2: Use a imagem importada aqui.
        style={{ backgroundImage: `url(${imagemDeFundo})` }} 
      />
      {/* Camada de Filtro Escuro e Desfoque */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />

      {/* Conteúdo Principal */}
      <div className="relative z-10 flex min-h-screen w-full flex-col items-center justify-center p-4">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-white drop-shadow-lg">Portal Ecomp Jr.</h1>
          <p className="text-slate-300 drop-shadow-md">Gestão de Clientes</p>
        </header>

        <main className={`w-full transition-all duration-500 ${token ? 'max-w-5xl' : 'max-w-md'}`}>
          {token ? (
            <Dashboard token={token} onLogout={handleLogout} />
          ) : (
            <LoginForm onLoginSuccess={handleLoginSuccess} />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;