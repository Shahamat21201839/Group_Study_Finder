import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const HomePage = () => import('@/views/HomePage.vue')
const LoginPage = () => import('@/views/LoginPage.vue')
const RegisterPage = () => import('@/views/RegisterPage.vue')
const DashboardPage = () => import('@/views/DashboardPage.vue')
const ProfilePage = () => import('@/views/ProfilePage.vue')
const CoursesPage = () => import('@/views/CoursesPage.vue')
const GroupsPage = () => import('@/views/GroupsPage.vue')
const GroupDetailPage = () => import('@/views/GroupDetailPage.vue')
const ChatPage = () => import('@/views/ChatPage.vue')
const NotificationsPage = () => import('@/views/NotificationsPage.vue')
const UserSearchPage = () => import('@/views/UserSearchPage.vue')

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/login', name: 'Login', component: LoginPage, meta: { requiresGuest: true } },
  { path: '/register', name: 'Register', component: RegisterPage, meta: { requiresGuest: true } },
  { path: '/dashboard', name: 'Dashboard', component: DashboardPage, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/courses', name: 'Courses', component: CoursesPage, meta: { requiresAuth: true } },
  { path: '/groups', name: 'Groups', component: GroupsPage, meta: { requiresAuth: true } },
  { path: '/groups/:id', name: 'GroupDetail', component: GroupDetailPage, meta: { requiresAuth: true }, props: true },
  { path: '/chat', name: 'Chat', component: ChatPage, meta: { requiresAuth: true } },
  { path: '/notifications', name: 'Notifications', component: NotificationsPage, meta: { requiresAuth: true } },
  { path: '/users/search', name: 'UserSearch', component: UserSearchPage, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  if (!store.getters['auth/isAuthenticated']) {
    await store.dispatch('auth/checkAuth')
  }

  const isAuthenticated = store.getters['auth/isAuthenticated']

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }

  if (to.matched.some(record => record.meta.requiresGuest)) {
    if (isAuthenticated) {
      next({ name: 'Dashboard' })
      return
    }
  }

  next()
})

export default router