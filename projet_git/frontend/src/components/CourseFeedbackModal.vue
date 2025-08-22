<template>
  <div class="modal fade" id="courseFeedbackModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-star me-2"></i>Course Feedback
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="submitFeedback">
            <div class="mb-3">
              <label class="form-label">Rating *</label>
              <div class="rating-input">
                <div class="d-flex gap-2">
                  <button
                    v-for="star in 5"
                    :key="star"
                    type="button"
                    class="btn btn-sm"
                    :class="star <= form.rating ? 'btn-warning' : 'btn-outline-warning'"
                    @click="form.rating = star"
                  >
                    <i class="fas fa-star"></i>
                  </button>
                </div>
                <small class="text-muted">{{ getRatingText(form.rating) }}</small>
              </div>
            </div>

            <div class="mb-3">
              <label for="comment" class="form-label">Comment (Optional)</label>
              <textarea
                id="comment"
                v-model="form.comment"
                class="form-control"
                rows="4"
                placeholder="Share your thoughts about this course..."
              ></textarea>
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
            @click="submitFeedback"
            :disabled="loading || !form.rating"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-paper-plane me-2"></i>
            {{ loading ? 'Submitting...' : 'Submit Feedback' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseFeedbackModal',
  props: {
    courseId: {
      type: Number,
      default: null
    }
  },
  emits: ['feedback-submitted'],
  data() {
    return {
      form: {
        rating: 0,
        comment: ''
      },
      loading: false
    }
  },
  methods: {
    async submitFeedback() {
      if (!this.form.rating || !this.courseId) return

      this.loading = true

      try {
        await this.$store.dispatch('courses/addCourseFeedback', {
          courseId: this.courseId,
          feedback: {
            rating: this.form.rating,
            comment: this.form.comment
          }
        })

        this.form = {
          rating: 0,
          comment: ''
        }

        const modal = document.getElementById('courseFeedbackModal')
        const bootstrapModal = bootstrap.Modal.getInstance(modal)
        if (bootstrapModal) {
          bootstrapModal.hide()
        }

        this.$emit('feedback-submitted')

      } catch (error) {
        this.$store.dispatch('setError', error.error || 'Failed to submit feedback')
      } finally {
        this.loading = false
      }
    },

    getRatingText(rating) {
      const texts = {
        0: 'No rating',
        1: 'Very Poor',
        2: 'Poor', 
        3: 'Average',
        4: 'Good',
        5: 'Excellent'
      }
      return texts[rating] || 'No rating'
    }
  }
}
</script>

<style scoped>
.rating-input .btn {
  border-radius: 50%;
  width: 40px;
  height: 40px;
}
</style>