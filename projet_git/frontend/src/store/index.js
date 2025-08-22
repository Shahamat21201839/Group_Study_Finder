import { createStore } from 'vuex'
import auth from './modules/auth'
import courses from './modules/courses'
import groups from './modules/groups'
import notifications from './modules/notifications'
import chat from './modules/chat'

export default createStore({
  state: {
    loading: false,
    error: null,
    success: null
  },

  getters: {
    isLoading: state => state.loading,
    error: state => state.error,
    success: state => state.success
  },

  mutations: {
    SET_LOADING(state, status) {
      state.loading = status
    },

    SET_ERROR(state, error) {
      state.error = error
    },

    SET_SUCCESS(state, message) {
      state.success = message
    },

    CLEAR_MESSAGES(state) {
      state.error = null
      state.success = null
    }
  },

  actions: {
    setLoading({ commit }, status) {
      commit('SET_LOADING', status)
    },

    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },

    setSuccess({ commit }, message) {
      commit('SET_SUCCESS', message)
    },

    clearMessages({ commit }) {
      commit('CLEAR_MESSAGES')
    }
  },

  modules: {
    auth,
    courses,
    groups,
    notifications,
    chat
  }
})