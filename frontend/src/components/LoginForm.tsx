import React, { useState } from 'react';

// Tipagem da função onLogin que será passada como prop
interface LoginFormProps {
  onLogin: (usuario: { nome: string }) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const loginData = { email, senha };

    try {
      const response = await fetch('http://127.0.0.1:8000/login', {  // Substitua pela URL correta do seu backend
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });

      if (!response.ok) {
        throw new Error('Credenciais inválidas ou erro no servidor');
      }

      const data = await response.json();
      console.log('Token:', data.access_token);

      // Aqui, simula-se o login com um nome do usuário
      // Isso pode ser adaptado dependendo da resposta do seu backend
      const usuario = { nome: email }; // Altere conforme a resposta real do seu backend

      // Chamando a função onLogin passando o nome do usuário
      onLogin(usuario);

      // Armazenar o token no localStorage (ou onde for necessário)
      localStorage.setItem('access_token', data.access_token);
    } catch (err) {
      setError('Erro ao fazer login');
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="senha">Senha:</label>
        <input
          type="password"
          id="senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
      </div>
      {error && <p>{error}</p>}
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
