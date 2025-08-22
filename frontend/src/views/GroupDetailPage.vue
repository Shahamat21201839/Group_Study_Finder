<template>
  <div class="group-detail-page">
    <div class="container py-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <LoadingComponent message="Loading group details..." />
      </div>

      <!-- Group Content -->
      <div v-else-if="group" class="row">
        <!-- Main Group Info -->
        <div class="col-lg-8">
          <!-- Group Header -->
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <div>
                <h2 class="mb-0">{{ group.group_name }}</h2>
                <small class="text-muted">Created {{ formatDate(group.created_at) }}</small>
              </div>
              <span class="badge bg-primary fs-6">{{ group.course.course_code }}</span>
            </div>
            <div class="card-body">
              <p class="card-text">{{ group.description }}</p>

              <!-- Session Info -->
              <div v-if="group.session_start || group.session_end" class="alert alert-info">
                <i class="fas fa-clock me-2"></i>
                <strong>Scheduled Session:</strong>
                <br>
                <span v-if="group.session_start">
                  Start: {{ formatDateTime(group.session_start) }}
                </span>
                <span v-if="group.session_end">
                  <br>End: {{ formatDateTime(group.session_end) }}
                </span>
              </div>

              <!-- Group Actions -->
              <div class="d-flex gap-2 mt-3">
                <button
                  v-if="canJoin"
                  class="btn btn-success"
                  @click="joinGroup"
                  :disabled="actionLoading"
                >
                  <i class="fas fa-plus me-2"></i>
                  {{ actionLoading ? 'Joining...' : 'Join Group' }}
                </button>

                <button
                  v-if="isMember && !isLeader"
                  class="btn btn-outline-danger"
                  @click="leaveGroup"
                  :disabled="actionLoading"
                >
                  <i class="fas fa-sign-out-alt me-2"></i>
                  {{ actionLoading ? 'Leaving...' : 'Leave Group' }}
                </button>

                <button
                  v-if="hasPendingRequest"
                  class="btn btn-warning"
                  disabled
                >
                  <i class="fas fa-clock me-2"></i>
                  Request Pending
                </button>

                <button
                  v-if="isLeader"
                  class="btn btn-outline-primary"
                  @click="openManageModal"
                >
                  <i class="fas fa-cog me-2"></i>
                  Manage Group
                </button>
              </div>
            </div>
          </div>

          <!-- Course Details -->
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">
                <i class="fas fa-book me-2"></i>Course Information
              </h5>
            </div>
            <div class="card-body">
              <h6>{{ group.course.course_name }}</h6>
              <p class="text-muted mb-0">{{ group.course.course_code }}</p>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
          <!-- Group Stats -->
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">
                <i class="fas fa-chart-bar me-2"></i>Group Stats
              </h5>
            </div>
            <div class="card-body">
              <div class="d-flex justify-content-between mb-2">
                <span>Total Members:</span>
                <strong>{{ group.members.length }}</strong>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Group Leader:</span>
                <strong>{{ leaderName }}</strong>
              </div>
              <div class="d-flex justify-content-between">
                <span>Your Role:</span>
                <span class="badge bg-secondary">{{ myRole || 'Not a member' }}</span>
              </div>
            </div>
          </div>

          <!-- Members List -->
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">
                <i class="fas fa-users me-2"></i>Members ({{ group.members.length }})
              </h5>
            </div>
            <div class="card-body">
              <div class="list-group list-group-flush">
                <GroupMemberCard
                  v-for="member in group.members"
                  :key="member.user_id"
                  :member="member"
                  :is-leader="isLeader"
                  :current-user-id="currentUserId"
                  @kick-member="kickMember"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Group Not Found -->
      <div v-else class="text-center py-5">
        <i class="fas fa-exclamation-circle fa-3x text-muted mb-3"></i>
        <h3>Group Not Found</h3>
        <p class="text-muted">The group you're looking for doesn't exist or you don't have access to it.</p>
        <router-link to="/groups" class="btn btn-primary">
          <i class="fas fa-arrow-left me-2"></i>Back to Groups
        </router-link>
      </div>
    </div>

    <!-- Manage Group Modal -->
    <div
      v-if="showManageModal"
      class="modal fade show d-block"
      style="background: rgba(0,0,0,0.5);"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-user-plus me-2"></i>Manage Join Requests
            </h5>
            <button type="button" class="btn-close" @click="closeManageModal"></button>
          </div>
          <div class="modal-body">
            <!-- Pending Join Requests -->
            <div class="mb-4">
              <div v-if="loadingRequests" class="text-center py-3">
                <LoadingComponent message="Loading requests..." />
              </div>
              <div
                v-else-if="joinRequests.length === 0"
                class="text-center py-3 text-muted"
              >
                <i class="fas fa-inbox display-4 mb-2"></i>
                <p>No pending join requests</p>
              </div>
              <div v-else>
                <div
                  v-for="req in joinRequests"
                  :key="req.request_id"
                  class="card mb-2"
                >
                  <div class="card-body py-2 d-flex justify-content-between align-items-center">
                    <div>
                      <strong>{{ req.user.name }}</strong>
                      <small class="text-muted d-block">{{ req.user.email }}</small>
                      <small class="text-muted">
                        Requested {{ formatTime(req.created_at) }}
                      </small>
                    </div>
                    <div class="d-flex gap-2">
                      <button
                        class="btn btn-success btn-sm"
                        @click="respondToRequest(req.request_id, 'approve')"
                        :disabled="respondingTo === req.request_id"
                      >
                        <i class="fas fa-check me-1"></i>
                        {{ respondingTo === req.request_id ? 'Approving...' : 'Approve' }}
                      </button>
                      <button
                        class="btn btn-danger btn-sm"
                        @click="respondToRequest(req.request_id, 'reject')"
                        :disabled="respondingTo === req.request_id"
                      >
                        <i class="fas fa-times me-1"></i>
                        {{ respondingTo === req.request_id ? 'Rejecting...' : 'Reject' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeManageModal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoadingComponent from '@/components/LoadingComponent.vue'
import GroupMemberCard from '@/components/GroupMemberCard.vue'

export default {
  name: 'GroupDetailPage',
  components: { LoadingComponent, GroupMemberCard },
  props: { id: { type: String, required: true } },
  data() {
    return {
      loading: true,
      actionLoading: false,
      showManageModal: false,
      loadingRequests: false,
      joinRequests: [],
      respondingTo: null
    }
  },
  computed: {
    group() {
      return this.$store.getters['groups/currentGroup']
    },
    currentUserId() {
      return this.$store.getters['auth/user']?.user_id
    },
    isMember() {
      return this.group?.members.some(m => m.user_id === this.currentUserId)
    },
    isLeader() {
      const member = this.group?.members.find(m => m.user_id === this.currentUserId)
      return member?.role === 'leader'
    },
    myRole() {
      return this.group?.members.find(m => m.user_id === this.currentUserId)?.role
    },
    canJoin() {
      return this.group && !this.isMember && !this.group.has_pending_request
    },
    hasPendingRequest() {
      return this.group?.has_pending_request
    },
    leaderName() {
      return this.group?.members.find(m => m.role === 'leader')?.name || 'Unknown'
    }
  },
  async mounted() {
    await this.loadGroupDetails()
  },
  methods: {
    async loadGroupDetails() {
      this.loading = true
      try {
        await this.$store.dispatch('groups/fetchGroupDetail', this.id)
      } finally {
        this.loading = false
      }
    },
    async joinGroup() {
      this.actionLoading = true
      try {
        await this.$store.dispatch('groups/joinGroup', this.id)
        this.$store.dispatch('setSuccess', 'Join request sent!')
        await this.loadGroupDetails()
      } finally {
        this.actionLoading = false
      }
    },
    async leaveGroup() {
      if (!confirm('Are you sure you want to leave this group?')) return
      this.actionLoading = true
      try {
        await this.$store.dispatch('groups/leaveGroup', this.id)
        this.$store.dispatch('setSuccess', 'You have left the group')
        this.$router.push('/groups')
      } finally {
        this.actionLoading = false
      }
    },
    async kickMember(userId) {
      if (!confirm('Remove this member?')) return
      try {
        await this.$store.dispatch('groups/kickMember', { groupId: this.id, userId })
        this.$store.dispatch('setSuccess', 'Member removed')
        await this.loadGroupDetails()
      } catch {
        this.$store.dispatch('setError', 'Failed to remove member')
      }
    },
    openManageModal() {
      this.showManageModal = true
      this.loadJoinRequests()
    },
    closeManageModal() {
      this.showManageModal = false
      this.joinRequests = []
    },
    async loadJoinRequests() {
      this.loadingRequests = true
      try {
        await this.$store.dispatch('groups/fetchJoinRequests', this.id)
        this.joinRequests = this.$store.getters['groups/joinRequests']
      } finally {
        this.loadingRequests = false
      }
    },
    async respondToRequest(requestId, action) {
      this.respondingTo = requestId
      try {
        await this.$store.dispatch('groups/respondToJoinRequest', { requestId, action })
        this.$store.dispatch('setSuccess', `Request ${action}d`)
        // refresh both
        await this.loadGroupDetails()
        await this.loadJoinRequests()
      } finally {
        this.respondingTo = null
      }
    },
    formatDate(s) { return new Date(s).toLocaleDateString() },
    formatDateTime(s) { return new Date(s).toLocaleString() },
    formatTime(s) {
      const diff = Math.floor((Date.now() - new Date(s)) / (1000*60*60*24))
      return diff === 0 ? 'Today'
           : diff === 1 ? 'Yesterday'
           : diff < 7 ? `${diff} days ago`
           : new Date(s).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.group-detail-page .card { border: none; box-shadow:0 2px 10px rgba(0,0,0,0.1); }
.group-detail-page .card-header { background:#f8f9fa; border-bottom:1px solid #e9ecef }
.modal.show { display:block!important; }
</style>
