<template>
  <div class="login-container">
    <div class="glass-panel login-box animate-fade-in">
      <div class="login-header">
        <div class="logo">
          <div class="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8 14V9a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v5"/>
              <path d="M12 2v20"/>
              <path d="M12 7h5a3 3 0 0 1 3 3v3a3 3 0 0 1-3 3h-5"/>
              <path d="M12 11H7a3 3 0 0 0-3 3v3a3 3 0 0 0 3 3h5"/>
            </svg>
          </div>
          <h2 class="font-serif brand-title">Caktus Finance</h2>
        </div>
        <p class="subtitle">Faça login para continuar.</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">E-mail</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="form-control" 
            placeholder="admin@example.com" 
          />
        </div>

        <div class="form-group">
          <label for="senha">Senha</label>
          <input 
            type="password" 
            id="senha" 
            v-model="senha" 
            class="form-control" 
            placeholder="••••••••" 
          />
        </div>

        <div v-if="erro" class="alert-error">
          {{ erro }}
        </div>

        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? 'Autenticando...' : 'Entrar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/axios';

const email = ref('');
const senha = ref('');
const erro = ref('');
const loading = ref(false);
const router = useRouter();

const handleLogin = async () => {
  // Validação simples de JS (Não deixa enviar vazio)
  if (!email.value || !senha.value) {
    erro.value = 'Preencha todos os campos.';
    return;
  }
  
  loading.value = true;
  erro.value = '';
  
  try {
    const response = await api.post('/usuarios/login', {
      email: email.value,
      senha: senha.value
    });
    
    // Sucesso! Armazenamos o token e os dados básicos no Storage
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('user', JSON.stringify(response.data.usuario));
    
    // Redireciona direto para o Dashboard
    router.push('/app');
  } catch (err) {
    erro.value = err.response?.data?.mensagem || 'Erro ao conectar. Tente novamente.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1rem;
}

.login-box {
  width: 100%;
  max-width: 420px;
  padding: 3rem 2.5rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.logo-icon {
  width: 34px;
  height: 34px;
  background: var(--primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.brand-title {
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
}

.btn-block {
  width: 100%;
  margin-top: 1rem;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 1rem;
}
</style>
