import { useState, useEffect } from 'react';
import { getDespesas } from './services/api';  // Importando a função para buscar as despesas
import LoginForm from './components/LoginForm';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

function App() {
  const [despesas, setDespesas] = useState<any[]>([]);  // Estado para armazenar as despesas
  const [error, setError] = useState<string | null>(null);

  // **Estado para controlar se o usuário está logado**
  const [isLoggedIn, setIsLoggedIn] = useState(false);  
  const [usuarioLogado, setUsuarioLogado] = useState<{ nome: string } | null>(null);

  // Faz a requisição quando o componente carrega
  useEffect(() => {
    const fetchDespesas = async () => {
      try {
        const data = await getDespesas();  // Mudando para buscar as despesas
        setDespesas(data);  // Armazenando as despesas no estado
      } catch (err) {
        setError('Erro ao buscar despesas');
        console.error(err);
      }
    };

    fetchDespesas();
  }, []);

  // **Função para definir o usuário logado**
  const handleLogin = (usuario: { nome: string }) => {
    setUsuarioLogado(usuario);
    setIsLoggedIn(true);  // **Marcar como logado**
  };

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>

      {/* **Exibe a mensagem de boas-vindas ou a tela de login, dependendo do estado do login** */}
      <h1>{isLoggedIn ? `Bem-vindo, ${usuarioLogado?.nome}` : 'Tela de Login'}</h1>

      {/* **Se o usuário estiver logado, exibe as despesas cadastradas** */}
      {isLoggedIn ? (
        <div className="card">
          {error && <p>{error}</p>}
          {despesas.length > 0 ? (
            <ul>
              {despesas.map((despesa) => (
                <li key={despesa.id}>
                  <strong>{despesa.descricao}</strong> - {despesa.valor} - {despesa.data} - {despesa.categoria}
                </li>
              ))}
            </ul>
          ) : (
            <p>Nenhuma despesa encontrada.</p>
          )}
        </div>
      ) : (
        // **Se não estiver logado, exibe o formulário de login**
        <LoginForm onLogin={handleLogin} />
      )}
    </>
  );
}

export default App;
