<template>
  <div class="card group-card h-100">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="card-title mb-0">{{ group.group_name }}</h5>
      <span 
        v-if="myRole" 
        class="badge"
        :class="myRole === 'leader' ? 'bg-warning text-dark' : 'bg-secondary'"
      >
        {{ myRole }}
      </span>
    </div>

    <div class="card-body">
      <div class="mb-2">
        <span class="badge bg-primary me-2">{{ group.course.course_code }}</span>
        <small class="text-muted">{{ group.course.course_name }}</small>
      </div>

      <p class="card-text">{{ group.description }}</p>

      <!-- Session Information -->
      <div v-if="group.session_start || group.session_end" class="mb-2">
        <small class="text-muted">
          <i class="fas fa-clock me-1"></i>
          <span v-if="group.session_start">
            {{ formatDateTime(group.session_start) }}
          </span>
          <span v-if="group.session_end">
            - {{ formatDateTime(group.session_end) }}
          </span>
        </small>
      </div>

      <!-- Group Stats -->
      <div class="d-flex justify-content-between align-items-center text-muted small mb-3">
        <span>
          <i class="fas fa-users me-1"></i>
          {{ group.members_count }} member{{ group.members_count !== 1 ? 's' : '' }}
        </span>
        <span>
          <i class="fas fa-calendar me-1"></i>
          {{ formatDate(group.created_at) }}
        </span>
      </div>
    </div>

    <div class="card-footer bg-transparent">
      <div class="d-flex gap-2">
        <button
          class="btn btn-primary flex-fill"
          @click="$emit('view-group', group.group_id)"
        >
          <i class="fas fa-eye me-1"></i>View Details
        </button>

        <button
          v-if="!isMember && !group.has_pending_request"
          class="btn btn-success"
          @click="$emit('request-join', group.group_id)"
        >
          <i class="fas fa-plus me-1"></i>Join
        </button>

        <span
          v-else-if="group.has_pending_request"
          class="btn btn-warning disabled"
        >
          <i class="fas fa-clock me-1"></i>Pending
        </span>

        <span
          v-else-if="isMember"
          class="btn btn-secondary disabled"
        >
          <i class="fas fa-check me-1"></i>Member
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GroupCard',
  emits: ['view-group', 'request-join'],
  props: {
    group: {
      type: Object,
      required: true
    },
    isMember: {
      type: Boolean,
      default: false
    },
    myRole: {
      type: String,
      default: null
    }
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },

    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style scoped>
.group-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  border: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.group-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.card-footer {
  border-top: 1px solid #e9ecef;
}

.card-text {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>