import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import Layout from '../components/Layout.vue';
import DashboardView from '../views/DashboardView.vue';
import TransacoesView from '../views/TransacoesView.vue';
import GraficosView from '../views/GraficosView.vue';
import DataModuleView from '../views/DataModuleView.vue';
import PerfilView from '../views/PerfilView.vue';
import CategoriasView from '../views/CategoriasView.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
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
  } else {
    next();
  }
});

export default router;
