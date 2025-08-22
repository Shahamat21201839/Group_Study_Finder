<template>
  <div class="modal fade" id="createGroupModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-plus-circle me-2"></i>Create Study Group
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

          <form @submit.prevent="createGroup">
            <!-- Course Selection -->
            <div class="mb-3">
              <label for="courseId" class="form-label">Course *</label>
              <select
                id="courseId"
                v-model="form.courseId"
                class="form-select"
                required
              >
                <option value="">Select a course</option>
                <option
                  v-for="course in userCourses"
                  :key="course.course_id"
                  :value="course.course_id"
                >
                  {{ course.course_code }} - {{ course.course_name }}
                </option>
              </select>
            </div>

            <!-- Group Name -->
            <div class="mb-3">
              <label for="groupName" class="form-label">Group Name *</label>
              <input
                id="groupName"
                v-model="form.groupName"
                type="text"
                class="form-control"
                placeholder="Enter a descriptive group name"
                required
                maxlength="100"
              >
            </div>

            <!-- Description -->
            <div class="mb-3">
              <label for="description" class="form-label">Description *</label>
              <textarea
                id="description"
                v-model="form.description"
                class="form-control"
                rows="4"
                placeholder="Describe your study group's purpose and goals"
                required
              ></textarea>
            </div>

            <!-- Session Scheduling -->
            <div class="card mb-3">
              <div class="card-header">
                <div class="form-check">
                  <input
                    id="enableScheduling"
                    v-model="form.enableScheduling"
                    class="form-check-input"
                    type="checkbox"
                  >
                  <label class="form-check-label" for="enableScheduling">
                    <i class="fas fa-clock me-2"></i>Schedule study sessions
                  </label>
                </div>
              </div>

              <div v-if="form.enableScheduling" class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label for="sessionStart" class="form-label">Start Date & Time</label>
                      <input
                        id="sessionStart"
                        v-model="form.sessionStart"
                        type="datetime-local"
                        class="form-control"
                      >
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label for="sessionEnd" class="form-label">End Date & Time</label>
                      <input
                        id="sessionEnd"
                        v-model="form.sessionEnd"
                        type="datetime-local"
                        class="form-control"
                      >
                    </div>
                  </div>
                </div>
              </div>
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
            @click="createGroup"
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-plus me-2"></i>
            {{ loading ? 'Creating...' : 'Create Group' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import AlertComponent from '@/components/AlertComponent.vue'

export default {
  name: 'CreateGroupModal',
  components: { AlertComponent },
  emits: ['group-created'],
  data() {
    return {
      form: {
        courseId: '',
        groupName: '',
        description: '',
        enableScheduling: false,
        sessionStart: '',
        sessionEnd: ''
      },
      loading: false,
      error: null
    }
  },
  computed: {
    userCourses() {
      const doing = this.$store.getters['courses/doingCourses']
      const done  = this.$store.getters['courses/doneCourses']
      return [...doing, ...done]   // these are full course objects
    },
    isFormValid() {
      return this.form.courseId && this.form.groupName.trim() && this.form.description.trim()
    }
  },
  async mounted() {
    await this.$store.dispatch('courses/fetchUserCourses')
  },
  methods: {
    async createGroup() {
      if (!this.isFormValid) return
      this.loading = true
      this.error   = null

      try {
        const groupData = {
          course_id:     parseInt(this.form.courseId),
          group_name:    this.form.groupName.trim(),
          description:   this.form.description.trim()
        }
        if (this.form.enableScheduling) {
          if (this.form.sessionStart) groupData.session_start = this.form.sessionStart
          if (this.form.sessionEnd)   groupData.session_end   = this.form.sessionEnd
        }

        await this.$store.dispatch('groups/createGroup', groupData)
        this.resetForm()

        // Hide Bootstrap modal via JS API
        const bsModal = bootstrap.Modal.getInstance(document.getElementById('createGroupModal'))
        if (bsModal) bsModal.hide()

        this.$emit('group-created')
        this.$store.dispatch('setSuccess', 'Study group created successfully!')
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create study group'
      } finally {
        this.loading = false
      }
    },
    resetForm() {
      this.form = {
        courseId: '',
        groupName: '',
        description: '',
        enableScheduling: false,
        sessionStart: '',
        sessionEnd: ''
      }
      this.error = null
    },
    clearError() {
      this.error = null
    }
  }
}
</script>
