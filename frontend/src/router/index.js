import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import Layout from '../components/Layout.vue';
import DashboardView from '../views/DashboardView.vue';
import TransacoesView from '../views/TransacoesView.vue';
import GraficosView from '../views/GraficosView.vue';
import DataModuleView from '../views/DataModuleView.vue';
import PerfilView from '../views/PerfilView.vue';
import CategoriasView from '../views/CategoriasView.vue';
import LandingView from '../views/LandingView.vue';
import CadastroView from '../views/CadastroView.vue';
import AdminView from '../views/AdminView.vue';
import AssinaturaView from '../views/AssinaturaView.vue';

const routes = [
  {
    path: '/pricing',
    name: 'Pricing',
    component: LandingView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/cadastro',
    name: 'Cadastro',
    component: CadastroView,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/app',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: DashboardView,
        meta: { title: 'Visão Geral' }
      },
      {
        path: 'transacoes',
        name: 'Transacoes',
        component: TransacoesView,
        meta: { title: 'Gerenciar Transações' }
      },
      {
        path: 'graficos',
        name: 'Graficos',
        component: GraficosView,
        meta: { title: 'Análise Patrimonial' }
      },
      {
        path: 'data',
        name: 'DataModule',
        component: DataModuleView,
        meta: { title: 'Importação e Exportação' }
      },
      {
        path: 'perfil',
        name: 'Perfil',
        component: PerfilView,
        meta: { title: 'Meu Perfil' }
      },
      {
        path: 'categorias',
        name: 'Categorias',
        component: CategoriasView,
        meta: { title: 'Gerenciar Categorias' }
      },
      {
        path: 'assinatura',
        name: 'Assinatura',
        component: AssinaturaView,
        meta: { title: 'Minha Assinatura' }
      },
      {
        path: 'admin',
        name: 'AdminPanel',
        component: AdminView,
        meta: { title: 'Painel Administrativo' }
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Route Guard - Verifica se a rota precisa de Auth e checa o localStorage
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' });
  } else if (to.name === 'Login' && token) {
    next({ name: 'Dashboard' });
  } else if ((to.name === 'Pricing' || to.name === 'Cadastro') && token) {
    // Se está logado, podemos mandar pro app se tentar acessar landing/cadastro?
    // Opcional: next({ name: 'Dashboard' }) ou deixar livre
    next();
  } else {
    next();
  }
});

export default router;
