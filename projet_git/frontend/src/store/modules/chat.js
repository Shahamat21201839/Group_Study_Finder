import api from '@/services/api'
import { io } from 'socket.io-client'

const state = {
  globalMessages: [],
  groupMessages: {},
  socket: null,
  connected: false
}

const getters = {
  globalMessages: state => state.globalMessages,
  getGroupMessages: state => groupId => state.groupMessages[groupId] || [],
  isConnected: state => state.connected
}

const mutations = {
  SET_GLOBAL_MESSAGES(state, messages) {
    state.globalMessages = messages
  },

  ADD_GLOBAL_MESSAGE(state, message) {
    state.globalMessages.push(message)
  },

  SET_GROUP_MESSAGES(state, { groupId, messages }) {
    state.groupMessages = {
      ...state.groupMessages,
      [groupId]: messages
    }
  },

  ADD_GROUP_MESSAGE(state, { groupId, message }) {
    if (!state.groupMessages[groupId]) {
      state.groupMessages[groupId] = []
    }
    state.groupMessages[groupId].push(message)
  },

  SET_SOCKET(state, socket) {
    state.socket = socket
  },

  SET_CONNECTED(state, status) {
    state.connected = status
  }
}

const actions = {
  initializeSocket({ commit, dispatch }) {
    const socket = io('http://localhost:5000', {
      withCredentials: true,
      transports: ['websocket', 'polling']
    })

    socket.on('connect', () => {
      console.log('Connected to chat server')
      commit('SET_CONNECTED', true)
    })

    socket.on('disconnect', () => {
      console.log('Disconnected from chat server')
      commit('SET_CONNECTED', false)
    })

    socket.on('global_message', (message) => {
      commit('ADD_GLOBAL_MESSAGE', message)
    })

    socket.on('group_message', (message) => {
      commit('ADD_GROUP_MESSAGE', { groupId: message.group_id, message })
    })

    commit('SET_SOCKET', socket)
  },

  disconnectSocket({ state, commit }) {
    if (state.socket) {
      state.socket.disconnect()
      commit('SET_SOCKET', null)
      commit('SET_CONNECTED', false)
    }
  },

  joinGroupChat({ state }, groupId) {
    if (state.socket && state.connected) {
      state.socket.emit('join_group', { group_id: groupId })
    }
  },

  leaveGroupChat({ state }, groupId) {
    if (state.socket && state.connected) {
      state.socket.emit('leave_group', { group_id: groupId })
    }
  },

  async fetchGlobalMessages({ commit }, { limit = 50, offset = 0 } = {}) {
    try {
      const response = await api.get('/chat/global', { params: { limit, offset } })
      commit('SET_GLOBAL_MESSAGES', response.data.messages)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async sendGlobalMessage({ commit }, message) {
    try {
      const response = await api.post('/chat/global', { message })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async fetchGroupMessages({ commit }, { groupId, limit = 50, offset = 0 }) {
    try {
      const response = await api.get(`/chat/group/${groupId}`, { params: { limit, offset } })
      commit('SET_GROUP_MESSAGES', { groupId, messages: response.data.messages })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async sendGroupMessage(_, { groupId, message }) {
    try {
      const response = await api.post(`/chat/group/${groupId}`, { message })
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