<template>
  <div class="profile-page">
    <div class="container py-4">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <!-- Profile Information Card -->
          <div class="card mb-4">
            <div class="card-header">
              <h4 class="card-title mb-0">
                <i class="fas fa-user me-2"></i>Profile Information
              </h4>
            </div>
            <div class="card-body">
              <form @submit.prevent="updateProfile">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="name" class="form-label">Full Name</label>
                    <input
                      type="text"
                      class="form-control"
                      id="name"
                      v-model="profileForm.name"
                      required
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="email" class="form-label">Email Address</label>
                    <input
                      type="email"
                      class="form-control-plaintext"
                      id="email"
                      v-model="profileForm.email"
                      readonly
                    >
                    <small class="text-muted">Email cannot be changed</small>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="role" class="form-label">Role</label>
                    <input
                      type="text"
                      class="form-control-plaintext"
                      id="role"
                      :value="profileForm.role"
                      readonly
                    >
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="loadingStates.profile"
                >
                  <i class="fas fa-save me-2"></i>
                  {{ loadingStates.profile ? 'Updating...' : 'Update Profile' }}
                </button>
              </form>
            </div>
          </div>

          <!-- Password Change Card -->
          <div class="card mb-4">
            <div class="card-header">
              <h4 class="card-title mb-0">
                <i class="fas fa-lock me-2"></i>Change Password
              </h4>
            </div>
            <div class="card-body">
              <form @submit.prevent="changePassword">
                <div class="mb-3">
                  <label for="currentPassword" class="form-label">Current Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="currentPassword"
                    v-model="passwordForm.currentPassword"
                    required
                  >
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="newPassword" class="form-label">New Password</label>
                    <input
                      type="password"
                      class="form-control"
                      id="newPassword"
                      v-model="passwordForm.newPassword"
                      required
                      minlength="8"
                    >
                    <small class="text-muted">Minimum 8 characters</small>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="confirmPassword" class="form-label">Confirm New Password</label>
                    <input
                      type="password"
                      class="form-control"
                      id="confirmPassword"
                      v-model="passwordForm.confirmPassword"
                      required
                      :class="{ 'is-invalid': passwordForm.newPassword && passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword }"
                    >
                    <div class="invalid-feedback">
                      Passwords do not match
                    </div>
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-warning"
                  :disabled="loadingStates.password || passwordForm.newPassword !== passwordForm.confirmPassword || !passwordForm.currentPassword || !passwordForm.newPassword"
                >
                  <i class="fas fa-key me-2"></i>
                  {{ loadingStates.password ? 'Changing...' : 'Change Password' }}
                </button>
              </form>
            </div>
          </div>

          <!-- Course Management Card -->
          <div class="card">
            <div class="card-header">
              <h4 class="card-title mb-0">
                <i class="fas fa-graduation-cap me-2"></i>My Courses
              </h4>
            </div>
            <div class="card-body">
              <!-- Courses Doing -->
              <div class="mb-4">
                <h5 class="text-success">
                  <i class="fas fa-play-circle me-2"></i>Currently Taking
                </h5>
                <div v-if="userCourses.doing.length === 0" class="text-muted">
                  No courses currently enrolled
                </div>
                <div v-else class="row g-2">
                  <div 
                    v-for="course in userCourses.doing" 
                    :key="`doing-${course.course_id}`"
                    class="col-md-6"
                  >
                    <div class="course-badge doing">
                      <span>{{ course.course_code }} - {{ course.course_name }}</span>
                      <button 
                        class="btn btn-sm btn-outline-danger ms-2"
                        @click="removeCourse(course.course_id)"
                        title="Remove course"
                      >
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Courses Done -->
              <div class="mb-4">
                <h5 class="text-primary">
                  <i class="fas fa-check-circle me-2"></i>Completed
                </h5>
                <div v-if="userCourses.done.length === 0" class="text-muted">
                  No completed courses
                </div>
                <div v-else class="row g-2">
                  <div 
                    v-for="course in userCourses.done" 
                    :key="`done-${course.course_id}`"
                    class="col-md-6"
                  >
                    <div class="course-badge done">
                      <span>{{ course.course_code }} - {{ course.course_name }}</span>
                      <button 
                        class="btn btn-sm btn-outline-danger ms-2"
                        @click="removeCourse(course.course_id)"
                        title="Remove course"
                      >
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Add Course Button -->
              <button 
                class="btn btn-outline-primary"
                @click="showAddCourseModal = true"
              >
                <i class="fas fa-plus me-2"></i>Add Course
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Course Modal -->
    <div 
      class="modal fade" 
      :class="{ show: showAddCourseModal }" 
      :style="{ display: showAddCourseModal ? 'block' : 'none' }"
      tabindex="-1"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Course</h5>
            <button type="button" class="btn-close" @click="showAddCourseModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="courseSelect" class="form-label">Select Course</label>
              <select 
                class="form-select" 
                id="courseSelect"
                v-model="addCourseForm.courseId"
                required
              >
                <option value="">Choose a course...</option>
                <option 
                  v-for="course in availableCourses" 
                  :key="course.course_id"
                  :value="course.course_id"
                >
                  {{ course.course_code }} - {{ course.course_name }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="courseStatus" class="form-label">Status</label>
              <select 
                class="form-select" 
                id="courseStatus"
                v-model="addCourseForm.status"
                required
              >
                <option value="">Choose status...</option>
                <option value="doing">Currently Taking</option>
                <option value="done">Completed</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showAddCourseModal = false">
              Cancel
            </button>
            <button 
              type="button" 
              class="btn btn-primary"
              @click="addCourse"
              :disabled="!addCourseForm.courseId || !addCourseForm.status"
            >
              Add Course
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'ProfilePage',
  data() {
    return {
      profileForm: { name: '', email: '', role: '' },
      passwordForm: { currentPassword: '', newPassword: '', confirmPassword: '' },
      addCourseForm: { courseId: '', status: '' },
      loadingStates: { profile: false, password: false, courses: false },
      showAddCourseModal: false,
      availableCourses: [],
      userCourses: { doing: [], done: [] }
    }
  },
  async mounted() {
    const user = this.$store.getters['auth/user']
    this.profileForm = { name: user.name, email: user.email, role: user.role }
    await this.loadCourses()
    await this.loadProfileData()
  },
  methods: {
    async updateProfile() {
      this.loadingStates.profile = true
      try {
        await this.$store.dispatch('auth/updateProfile', { name: this.profileForm.name })
        this.$store.dispatch('setSuccess', 'Profile updated successfully!')
      } catch {
        this.$store.dispatch('setError', 'Failed to update profile')
      } finally {
        this.loadingStates.profile = false
      }
    },

    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.$store.dispatch('setError', 'New passwords do not match')
        return
      }
      this.loadingStates.password = true
      try {
        await api.put('/users/change-password', {
          current_password: this.passwordForm.currentPassword,
          new_password: this.passwordForm.newPassword
        })
        this.passwordForm = { currentPassword: '', newPassword: '', confirmPassword: '' }
        this.$store.dispatch('setSuccess', 'Password changed successfully')
      } catch (e) {
        this.$store.dispatch('setError', e.response?.data?.error || 'Failed to change password')
      } finally {
        this.loadingStates.password = false
      }
    },

    async loadCourses() {
      try {
        const res = await api.get('/courses')
        this.availableCourses = res.data.courses
      } catch {
        console.error('Failed to load courses')
      }
    },

    async loadProfileData() {
      try {
        await this.$store.dispatch('courses/fetchUserCourses')
        this.userCourses = {
          doing: this.$store.getters['courses/doingCourses'],
          done: this.$store.getters['courses/doneCourses']
        }
      } catch {
        console.error('Failed to load profile data')
      }
    },

    async addCourse() {
      this.loadingStates.courses = true
      try {
        await api.post('/users/courses', {
          course_id: this.addCourseForm.courseId,
          status: this.addCourseForm.status
        })
        this.addCourseForm = { courseId: '', status: '' }
        this.showAddCourseModal = false
        await this.loadCourses()
        await this.loadProfileData()
        this.$store.dispatch('setSuccess', 'Course added successfully')
      } catch {
        this.$store.dispatch('setError', 'Failed to add course')
      } finally {
        this.loadingStates.courses = false
      }
    },

    async removeCourse(courseId) {
      if (!confirm('Are you sure?')) return
      try {
        await api.delete(`/users/courses/${courseId}`)
        await this.loadProfileData()
        this.$store.dispatch('setSuccess', 'Course removed successfully')
      } catch {
        this.$store.dispatch('setError', 'Failed to remove course')
      }
    }
  }
}
</script>

<style scoped>
.course-badge { display: flex; justify-content: space-between; align-items: center; padding: .5rem 1rem; border-radius: 8px; margin-bottom: .5rem; }
.course-badge.doing { background: #d1f2eb; border:1px solid #a3e4d7; color:#0e6655 }
.course-badge.done  { background: #d1ecf1; border:1px solid #b8daff; color:#0c5460 }
.modal.show { background: rgba(0,0,0,0.5) }
.card { box-shadow:0 4px 6px rgba(0,0,0,.1); border:none }
.card-header { background:#f8f9fa; border-bottom:1px solid #e9ecef }
.form-control:focus { border-color:#007bff; box-shadow:0 0 0 .2rem rgba(0,123,255,.25) }
.btn-warning:hover { background:#e0a800; border-color:#d39e00 }
</style>



