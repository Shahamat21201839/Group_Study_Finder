import api from '@/services/api'
import { io } from 'socket.io-client'

const state = {
  globalMessages: [],          // for global chat
  groupMessages: {},           // keyed by groupId
  loadingGlobal: false,
  loadingGroup: false,
  socket: null
}

const getters = {
  globalMessages: state => state.globalMessages,
  getGroupMessages: state => groupId => state.groupMessages[groupId] || [],
  isLoadingGlobal: state => state.loadingGlobal,
  isLoadingGroup: state => state.loadingGroup
}

const actions = {
  // Global chat
  async fetchGlobalMessages({ commit }) {
    commit('SET_LOADING_GLOBAL', true)
    try {
      const { data } = await api.get('/chat/global')
      commit('SET_GLOBAL_MESSAGES', data.messages)
    } finally {
      commit('SET_LOADING_GLOBAL', false)
    }
  },
  async sendGlobalMessage({ /* no commit here */ }, message) {
    await api.post('/chat/global', { message })
  },
  initializeSocket({ commit, dispatch, state }) {
    if (state.socket) return
    const socket = io(`${process.env.VUE_APP_API_URL || 'http://localhost:5000'}`, {
      withCredentials: true
    })
    socket.on('global_message', msg => {
      dispatch('addGlobalMessage', msg)
    })
    commit('SET_SOCKET', socket)
  },
  addGlobalMessage({ commit }, message) {
    commit('ADD_GLOBAL_MESSAGE', message)
  },

  // Group chat
  async fetchGroupMessages({ commit }, groupId) {
    commit('SET_LOADING_GROUP', true)
    try {
      const { data } = await api.get(`/chat/group/${groupId}`)
      commit('SET_GROUP_MESSAGES', { groupId, messages: data.messages })
    } finally {
      commit('SET_LOADING_GROUP', false)
    }
  },
  async sendGroupMessage(_, { groupId, message }) {
    await api.post(`/chat/group/${groupId}`, { message })
  },
  addGroupMessage({ commit }, { groupId, message }) {
    commit('ADD_GROUP_MESSAGE', { groupId, message })
  }
}

const mutations = {
  SET_LOADING_GLOBAL(state, loading) {
    state.loadingGlobal = loading
  },
  SET_GLOBAL_MESSAGES(state, messages) {
    state.globalMessages = messages
  },
  ADD_GLOBAL_MESSAGE(state, message) {
    state.globalMessages.push(message)
  },
  SET_SOCKET(state, socket) {
    state.socket = socket
  },

  SET_LOADING_GROUP(state, loading) {
    state.loadingGroup = loading
  },
  SET_GROUP_MESSAGES(state, { groupId, messages }) {
    state.groupMessages = { ...state.groupMessages, [groupId]: messages }
  },
  ADD_GROUP_MESSAGE(state, { groupId, message }) {
    const existing = state.groupMessages[groupId] || []
    state.groupMessages = {
      ...state.groupMessages,
      [groupId]: [...existing, message]
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
