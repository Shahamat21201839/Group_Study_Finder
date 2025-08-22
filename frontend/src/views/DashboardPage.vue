<template>
  <div class="dashboard-page">
    <div class="container py-4">
      <!-- Welcome Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-card">
            <h1 class="h2 fw-bold mb-2">
              Welcome back, {{ user.name }}!
              <span class="badge bg-primary ms-2">{{ user.role }}</span>
            </h1>
            <p class="text-muted mb-0">
              <i class="fas fa-calendar me-2"></i>
              {{ currentDate }}
            </p>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="row g-4 mb-4">
        <div class="col-md-3">
          <div class="stat-card text-center">
            <div class="stat-icon bg-primary text-white">
              <i class="fas fa-book"></i>
            </div>
            <h3 class="stat-number">{{ stats.totalCourses }}</h3>
            <p class="stat-label">Total Courses</p>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card text-center">
            <div class="stat-icon bg-success text-white">
              <i class="fas fa-users"></i>
            </div>
            <h3 class="stat-number">{{ stats.myGroups }}</h3>
            <p class="stat-label">My Groups</p>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card text-center">
            <div class="stat-icon bg-warning text-white">
              <i class="fas fa-bell"></i>
            </div>
            <h3 class="stat-number">{{ stats.notifications }}</h3>
            <p class="stat-label">Notifications</p>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card text-center">
            <div class="stat-icon bg-info text-white">
              <i class="fas fa-graduation-cap"></i>
            </div>
            <h3 class="stat-number">{{ stats.doingCourses }}</h3>
            <p class="stat-label">Ongoing Courses</p>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h4 class="card-title mb-0">
                <i class="fas fa-rocket me-2"></i>Quick Actions
              </h4>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-2 col-6">
                  <button
                    class="btn btn-primary w-100 d-flex flex-column align-items-center p-3"
                    data-bs-toggle="modal"
                    data-bs-target="#createGroupModal"
                  >
                    <i class="fas fa-plus-circle fs-4 mb-2"></i>
                    <span>Create Group</span>
                  </button>
                </div>
                <div class="col-md-2 col-6">
                  <router-link
                    to="/groups"
                    class="btn btn-success w-100 d-flex flex-column align-items-center p-3"
                  >
                    <i class="fas fa-search fs-4 mb-2"></i>
                    <span>Find Groups</span>
                  </router-link>
                </div>
                <div class="col-md-2 col-6">
                  <router-link
                    to="/courses"
                    class="btn btn-info w-100 d-flex flex-column align-items-center p-3"
                  >
                    <i class="fas fa-book fs-4 mb-2"></i>
                    <span>My Courses</span>
                  </router-link>
                </div>
                <div class="col-md-2 col-6">
                  <router-link
                    to="/chat"
                    class="btn btn-warning w-100 d-flex flex-column align-items-center p-3"
                  >
                    <i class="fas fa-comments fs-4 mb-2"></i>
                    <span>Global Chat</span>
                  </router-link>
                </div>
                <div class="col-md-2 col-6">
                  <router-link
                    to="/users/search"
                    class="btn btn-secondary w-100 d-flex flex-column align-items-center p-3"
                  >
                    <i class="fas fa-user-friends fs-4 mb-2"></i>
                    <span>Find Users</span>
                  </router-link>
                </div>
                <div class="col-md-2 col-6">
                  <router-link
                    to="/notifications"
                    class="btn btn-danger w-100 d-flex flex-column align-items-center p-3 position-relative"
                  >
                    <i class="fas fa-bell fs-4 mb-2"></i>
                    <span>Notifications</span>
                    <span
                      v-if="stats.notifications > 0"
                      class="notification-badge"
                    >
                      {{ stats.notifications }}
                    </span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- My Study Groups -->
      <div class="row g-4">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-users me-2"></i>My Study Groups
              </h5>
              <router-link to="/groups" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="loading.groups" class="text-center py-4">
                <LoadingComponent message="Loading groups..." />
              </div>
              <div
                v-else-if="myGroups.length === 0"
                class="text-center py-4 text-muted"
              >
                <i class="fas fa-users-slash display-4 mb-3"></i>
                <p>You haven't joined any study groups yet.</p>
                <button
                  class="btn btn-primary"
                  data-bs-toggle="modal"
                  data-bs-target="#createGroupModal"
                >
                  Create Your First Group
                </button>
              </div>
              <div v-else>
                <div
                  v-for="group in myGroups.slice(0, 3)"
                  :key="group.group_id"
                  class="group-item mb-3"
                >
                  <h6 class="mb-1">
                    <router-link
                      :to="`/groups/${group.group_id}`"
                      class="text-decoration-none"
                    >
                      {{ group.group_name }}
                    </router-link>
                  </h6>
                  <p class="text-muted small mb-1">{{ group.course.course_name }}</p>
                  <div class="d-flex align-items-center text-muted small">
                    <span class="me-3">
                      <i class="fas fa-users me-1"></i>{{ group.members_count }}
                    </span>
                    <span
                      class="badge"
                      :class="group.my_role === 'leader' ? 'bg-warning text-dark' : 'bg-secondary'"
                    >
                      {{ group.my_role }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Notifications -->
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-bell me-2"></i>Recent Notifications
              </h5>
              <router-link to="/notifications" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="loading.notifications" class="text-center py-4">
                <LoadingComponent message="Loading notifications..." />
              </div>
              <div
                v-else-if="recentNotifications.length === 0"
                class="text-center py-4 text-muted"
              >
                <i class="fas fa-bell-slash display-4 mb-3"></i>
                <p>No notifications yet.</p>
              </div>
              <div v-else>
                <div
                  v-for="notification in recentNotifications.slice(0, 4)"
                  :key="notification.notification_id"
                  class="notification-item mb-3"
                  :class="{ unread: !notification.is_read }"
                >
                  <div class="d-flex">
                    <div class="flex-grow-1">
                      <p class="mb-1 small">{{ notification.message }}</p>
                      <small class="text-muted">
                        {{ formatTime(notification.created_at) }}
                      </small>
                    </div>
                    <div v-if="!notification.is_read" class="ms-2">
                      <span class="badge bg-primary">New</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CreateGroupModal @group-created="onGroupCreated" />
  </div>
</template>

<script>
import LoadingComponent from '@/components/LoadingComponent.vue'
import CreateGroupModal from '@/components/CreateGroupModal.vue'

export default {
  name: 'DashboardPage',
  components: {
    LoadingComponent,
    CreateGroupModal
  },
  data() {
    return {
      loading: {
        groups: false,
        notifications: false
      }
    }
  },
  computed: {
    user() {
      return this.$store.getters['auth/user'] || {}
    },
    currentDate() {
      return new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },
    doingCourses() {
      return this.$store.getters['courses/doingCourses'] || []
    },
    doneCourses() {
      return this.$store.getters['courses/doneCourses'] || []
    },
    myGroups() {
      return this.$store.getters['groups/myGroups'] || []
    },
    recentNotifications() {
      return this.$store.getters['notifications/allNotifications'] || []
    },
    stats() {
      return {
        totalCourses: this.doingCourses.length + this.doneCourses.length,
        doingCourses: this.doingCourses.length,
        myGroups: this.myGroups.length,
        notifications: this.$store.getters['notifications/unreadCount'] || 0
      }
    }
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      this.loading.groups = true
      this.loading.notifications = true
      try {
        await Promise.all([
          this.$store.dispatch('courses/fetchUserCourses'),
          this.$store.dispatch('groups/fetchMyGroups'),
          this.$store.dispatch('notifications/fetchNotifications')
        ])
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        this.loading.groups = false
        this.loading.notifications = false
      }
    },
    formatTime(dateString) {
      const now = new Date()
      const date = new Date(dateString)
      const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
      if (diffDays === 0) return 'Today'
      if (diffDays === 1) return 'Yesterday'
      if (diffDays < 7) return `${diffDays} days ago`
      return date.toLocaleDateString()
    },
    async onGroupCreated() {
      await this.loadDashboardData()
    }
  }
}
</script>

<style scoped>
.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 0;
}
.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
}
.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.5rem;
}
.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}
.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0;
}
.group-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}
.notification-item {
  padding: 0.75rem;
  border-radius: 8px;
  background: #f8f9fa;
}
.notification-item.unread {
  background: #e3f2fd;
  border-left: 3px solid #2196f3;
}
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: none;
}
.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}
.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.7rem;
  min-width: 16px;
  text-align: center;
}
</style>
