<template>
  <div class="list-group-item d-flex justify-content-between align-items-center">
    <div class="d-flex align-items-center">
      <div class="avatar me-3">
        <i class="fas fa-user-circle fa-2x text-muted"></i>
      </div>
      <div>
        <h6 class="mb-0">{{ member.name }}</h6>
        <small class="text-muted">{{ member.email }}</small>
      </div>
    </div>
    
    <div class="d-flex align-items-center gap-2">
      <span 
        class="badge"
        :class="member.role === 'leader' ? 'bg-warning text-dark' : 'bg-secondary'"
      >
        {{ member.role }}
      </span>
      
      <button
        v-if="isLeader && member.user_id !== currentUserId && member.role !== 'leader'"
        class="btn btn-sm btn-outline-danger"
        @click="$emit('kick-member', member.user_id)"
        title="Remove member"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GroupMemberCard',
  emits: ['kick-member'],
  props: {
    member: {
      type: Object,
      required: true
    },
    isLeader: {
      type: Boolean,
      default: false
    },
    currentUserId: {
      type: Number,
      required: true
    }
  }
}
</script>

<style scoped>
.list-group-item {
  border-left: none;
  border-right: none;
  padding: 1rem 0;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}

.avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
