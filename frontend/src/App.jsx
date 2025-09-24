import { useState, useEffect } from 'react';
import ListaEmpresas from "./components/ListaEmpresas";
import LoginForm from './components/LoginForm';

// URL da imagem de fundo está agora definida aqui no código
const BACKGROUND_IMAGE_URL = 'https://images.unsplash.com/photo-1487017159836-4e23ece2e4cf?q=80&w=2071&auto=format&fit=crop';

function App() {
  const [token, setToken] = useState(null);

  const handleLoginSuccess = (newToken) => {
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
  };

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []); // O array vazio [] garante que isto só é executado uma vez, quando a app carrega.

  return (
    <div
      className="min-h-screen w-full bg-cover bg-center bg-fixed"
      style={{ backgroundImage: `url(${BACKGROUND_IMAGE_URL})` }}
    >
      {/* Este container principal organiza o layout em coluna e ocupa a tela toda */}
      <div className="min-h-screen w-full flex flex-col items-center justify-center p-4 backdrop-blur-md bg-black/50">
        
        <header className="mb-8 text-center shrink-0">
          <h1 className="text-4xl md:text-5xl font-bold text-white drop-shadow-lg">
            Portal Ecomp Jr.
          </h1>
          <p className="text-slate-300 mt-2 drop-shadow-md">
            Gestão de Clientes
          </p>
        </header>

        {/* A área principal agora cresce para preencher o espaço, centrando o seu conteúdo */}
        <main className="w-full flex-grow flex items-center justify-center">
          {/* Este div controla a largura do conteúdo, adaptando-se à tela */}
          <div className={`w-full transition-all duration-500 ease-in-out ${!token ? 'max-w-md' : 'max-w-4xl'}`}>
            {!token ? (
              <LoginForm onLoginSuccess={handleLoginSuccess} />
            ) : (
              <ListaEmpresas token={token} onLogout={handleLogout} />
            )}
          </div>
        </main>
        
        <footer className="py-4 text-center text-white/70 text-sm shrink-0">
          <p>Desafio Técnico - Processo Seletivo 2025.2</p>
        </footer>

      </div>
    </div>
  )
}

export default App;