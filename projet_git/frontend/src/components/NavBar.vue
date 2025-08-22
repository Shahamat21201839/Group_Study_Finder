<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/">
        <i class="fas fa-users me-2"></i>Group Study Finder
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <router-link class="nav-link" to="/dashboard">
              <i class="fas fa-tachometer-alt me-1"></i>Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/courses">
              <i class="fas fa-book me-1"></i>Courses
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/groups">
              <i class="fas fa-users me-1"></i>Groups
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/chat">
              <i class="fas fa-comments me-1"></i>Chat
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link position-relative" to="/notifications">
              <i class="fas fa-bell me-1"></i>Notifications
              <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/users/search">
              <i class="fas fa-search me-1"></i>Search
            </router-link>
          </li>
          <li class="nav-item dropdown">
            <a
              href="#"
              class="nav-link dropdown-toggle"
              role="button"
              id="userDropdown"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="fas fa-user-circle me-1"></i>{{ user.name }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <router-link class="dropdown-item" to="/profile">
                  <i class="fas fa-user-edit me-2"></i>Profile
                </router-link>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a href="#" class="dropdown-item" @click.prevent="logout">
                  <i class="fas fa-sign-out-alt me-2"></i>Logout
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    user() {
      return this.$store.getters['auth/user']
    },
    unreadCount() {
      return this.$store.getters['notifications/unreadCount'] || 0
    }
  },
  async mounted() {
    // Load notifications count on navbar mount
    try {
      await this.$store.dispatch('notifications/fetchNotifications')
    } catch (error) {
      console.error('Failed to load notifications:', error)
    }
  },
  methods: {
    async logout() {
      try {
        await this.$store.dispatch('auth/logout')
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout failed:', error)
      }
    }
  }
}
</script>

<style scoped>
.navbar-brand {
  font-size: 1.4rem;
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
  font-weight: bold;
}

.nav-link {
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: rgba(255, 255, 255, 0.8);
}

.dropdown-menu {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>