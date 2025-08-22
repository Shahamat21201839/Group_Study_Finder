import api from './api'

export default {
  async searchUsers(courseCode, status = null) {
    try {
      const params = { course_code: courseCode }
      if (status) {
        params.status = status
      }

      const response = await api.get('/users/search', { params })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}