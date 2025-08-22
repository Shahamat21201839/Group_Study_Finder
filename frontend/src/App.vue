<template>
  <div id="app">
    <NavBar v-if="$store.getters['auth/isAuthenticated']" />

    <!-- Global notifications -->
    <div v-if="globalError" class="container-fluid">
      <AlertComponent 
        type="error" 
        :message="globalError" 
        @close="clearGlobalError" 
      />
    </div>

    <div v-if="globalSuccess" class="container-fluid">
      <AlertComponent 
        type="success" 
        :message="globalSuccess" 
        @close="clearGlobalSuccess" 
      />
    </div>

    <router-view />

    <!-- Global loading overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import AlertComponent from '@/components/AlertComponent.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    AlertComponent
  },
  computed: {
    loading() {
      return this.$store.state.loading
    },
    globalError() {
      return this.$store.state.error
    },
    globalSuccess() {
      return this.$store.state.success
    }
  },
  async created() {
    await this.$store.dispatch('auth/checkAuth')
  },
  methods: {
    clearGlobalError() {
      this.$store.dispatch('setError', null)
    },
    clearGlobalSuccess() {
      this.$store.dispatch('setSuccess', null)
    }
  }
}
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.75rem;
  min-width: 18px;
  text-align: center;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: none;
}
</style>