<template>
  <div class="modal fade" id="createCourseModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-plus-circle me-2"></i>Create New Course
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <AlertComponent
            v-if="error"
            type="error"
            :message="error"
            @close="clearError"
          />

          <form @submit.prevent="createCourse">
            <div class="mb-3">
              <label for="courseCode" class="form-label">Course Code *</label>
              <input
                id="courseCode"
                v-model="form.courseCode"
                type="text"
                class="form-control"
                placeholder="e.g., CSE470, MAT120"
                required
                maxlength="10"
              >
            </div>

            <div class="mb-3">
              <label for="courseName" class="form-label">Course Name *</label>
              <input
                id="courseName"
                v-model="form.courseName"
                type="text"
                class="form-control"
                placeholder="e.g., Software Engineering"
                required
                maxlength="100"
              >
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="createCourse"
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-plus me-2"></i>
            {{ loading ? 'Creating...' : 'Create Course' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AlertComponent from '@/components/AlertComponent.vue'

export default {
  name: 'CreateCourseModal',
  components: {
    AlertComponent
  },
  emits: ['course-created'],
  data() {
    return {
      form: {
        courseCode: '',
        courseName: ''
      },
      loading: false,
      error: null
    }
  },
  computed: {
    isFormValid() {
      return this.form.courseCode.trim() && this.form.courseName.trim()
    }
  },
  methods: {
    async createCourse() {
      if (!this.isFormValid) return

      this.loading = true
      this.error = null

      try {
        const courseData = {
          course_code: this.form.courseCode.trim(),
          course_name: this.form.courseName.trim()
        }

        await this.$store.dispatch('courses/createCourse', courseData)

        this.resetForm()

        const modal = document.getElementById('createCourseModal')
        const bootstrapModal = bootstrap.Modal.getInstance(modal)
        if (bootstrapModal) {
          bootstrapModal.hide()
        }

        this.$emit('course-created')
        this.$store.dispatch('setSuccess', 'Course created successfully!')

      } catch (error) {
        this.error = error.error || 'Failed to create course'
      } finally {
        this.loading = false
      }
    },

    resetForm() {
      this.form = {
        courseCode: '',
        courseName: ''
      }
      this.error = null
    },

    clearError() {
      this.error = null
    }
  }
}
</script>