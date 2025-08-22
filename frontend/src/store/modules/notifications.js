import api from '@/services/api'

const state = {
  notifications: [],
  unreadCount: 0
}

const getters = {
  allNotifications: state => state.notifications,
  unreadNotifications: state => state.notifications.filter(n => !n.is_read),
  unreadCount: state => state.unreadCount
}

const mutations = {
  SET_NOTIFICATIONS(state, { notifications, unreadCount }) {
    state.notifications = notifications
    state.unreadCount = unreadCount
  },

  ADD_NOTIFICATION(state, notification) {
    state.notifications.unshift(notification)
    if (!notification.is_read) {
      state.unreadCount += 1
    }
  },

  MARK_NOTIFICATION_READ(state, notificationId) {
    const notification = state.notifications.find(n => n.notification_id === notificationId)
    if (notification && !notification.is_read) {
      notification.is_read = true
      state.unreadCount -= 1
    }
  },

  MARK_ALL_READ(state) {
    state.notifications.forEach(n => n.is_read = true)
    state.unreadCount = 0
  }
}

const actions = {
  async fetchNotifications({ commit }, unreadOnly = false) {
    try {
      const params = unreadOnly ? { unread_only: 'true' } : {}
      const response = await api.get('/notifications/', { params })
      commit('SET_NOTIFICATIONS', response.data)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async markNotificationRead({ commit }, notificationId) {
    try {
      const response = await api.put(`/notifications/${notificationId}/mark-read`)
      commit('MARK_NOTIFICATION_READ', notificationId)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async markAllNotificationsRead({ commit }) {
    try {
      const response = await api.put('/notifications/mark-all-read')
      commit('MARK_ALL_READ')
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async generateExamNotifications({ dispatch }) {
    try {
      const response = await api.post('/notifications/generate-exam-notifications')
      await dispatch('fetchNotifications')
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async requestResources({ dispatch }, { courseId, resourceType }) {
    try {
      const response = await api.post('/notifications/request-resources', {
        course_id: courseId,
        resource_type: resourceType
      })
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