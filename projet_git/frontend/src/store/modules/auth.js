import api from '@/services/api'

const state = {
  user: null,
  isAuthenticated: false
}

const getters = {
  user: state => state.user,
  isAuthenticated: state => state.isAuthenticated,
  isTeacher: state => state.user?.role === 'teacher',
  isStudent: state => state.user?.role === 'student'
}

const mutations = {
  SET_USER(state, user) {
    state.user = user
    state.isAuthenticated = !!user
  },

  CLEAR_USER(state) {
    state.user = null
    state.isAuthenticated = false
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await api.post('/auth/login', credentials)
      commit('SET_USER', response.data.user)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async register({ commit }, userData) {
    try {
      const response = await api.post('/auth/register', userData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async logout({ commit }) {
    try {
      await api.post('/auth/logout')
      commit('CLEAR_USER')
    } catch (error) {
      commit('CLEAR_USER')
      throw error.response?.data || error.message
    }
  },

  async checkAuth({ commit }) {
    try {
      const response = await api.get('/auth/check-auth')
      if (response.data.authenticated) {
        commit('SET_USER', response.data.user)
      } else {
        commit('CLEAR_USER')
      }
      return response.data
    } catch (error) {
      commit('CLEAR_USER')
      return { authenticated: false }
    }
  },

  async updateProfile({ commit }, profileData) {
    try {
      const response = await api.put('/users/profile', profileData)
      commit('SET_USER', response.data.user)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async changePassword(_, passwordData) {
    try {
      const response = await api.put('/users/change-password', passwordData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}