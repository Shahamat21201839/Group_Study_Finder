import api from '@/services/api'

const state = {
  courses: [],
  userCourses: { doing: [], done: [] }
}

const getters = {
  allCourses: state => state.courses,
  doingCourses: state => state.userCourses.doing,
  doneCourses: state => state.userCourses.done
}

const mutations = {
  SET_COURSES(state, courses) {
    state.courses = courses
  },

  SET_USER_COURSES(state, userCourses) {
    state.userCourses = userCourses
  }
}

const actions = {
  async fetchCourses({ commit }) {
    try {
      const response = await api.get('/courses/')
      commit('SET_COURSES', response.data.courses)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async fetchUserCourses({ commit }) {
    try {
      const response = await api.get('/users/courses')
      commit('SET_USER_COURSES', response.data)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async addUserCourse({ commit }, { courseId, status }) {
    try {
      const response = await api.post('/users/courses', {
        course_id: courseId,
        status: status
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async removeUserCourse({ commit }, courseId) {
    try {
      const response = await api.delete(`/users/courses/${courseId}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async searchCourses(_, query) {
    try {
      const response = await api.get('/courses/search', { params: { q: query } })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async createCourse({ commit }, courseData) {
    try {
      const response = await api.post('/courses/', courseData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async addCourseFeedback(_, { courseId, feedback }) {
    try {
      const response = await api.post(`/courses/${courseId}/feedback`, feedback)
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
