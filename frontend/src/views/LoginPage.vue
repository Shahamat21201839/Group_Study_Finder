<template>
  <div class="login-page min-vh-100 d-flex align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <!-- Header -->
              <div class="text-center mb-4">
                <i class="fas fa-users display-4 text-primary mb-3"></i>
                <h2 class="h3 fw-bold">Welcome Back!</h2>
                <p class="text-muted">Sign in to continue studying with your peers</p>
              </div>

              <!-- Login Form -->
              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="email" class="form-label">Email Address</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-envelope"></i>
                    </span>
                    <input
                      id="email"
                      v-model="form.email"
                      type="email"
                      class="form-control"
                      :class="{ 'is-invalid': errors.email }"
                      placeholder="Enter your email"
                      required
                    >
                  </div>
                  <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
                </div>

                <div class="mb-4">
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-lock"></i>
                    </span>
                    <input
                      id="password"
                      v-model="form.password"
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      :class="{ 'is-invalid': errors.password }"
                      placeholder="Enter your password"
                      required
                    >
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showPassword = !showPassword"
                    >
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                  <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
                </div>

                <!-- Error Alert -->
                <AlertComponent
                  v-if="loginError"
                  type="error"
                  :message="loginError"
                  @close="loginError = null"
                />

                <!-- Submit Button -->
                <button
                  type="submit"
                  class="btn btn-primary w-100 py-2 mb-3"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-sign-in-alt me-2"></i>
                  {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>

                <!-- Sample Accounts -->
                <div class="alert alert-info">
                  <strong>Demo Accounts:</strong><br>
                  <small>Student: alice.j@g.bracu.ac.bd / password123</small><br>
                  <small>Teacher: john.smith@bracu.ac.bd / password123</small>
                </div>
              </form>

              <!-- Footer -->
              <div class="text-center">
                <p class="mb-0">Don't have an account?</p>
                <router-link to="/register" class="btn btn-link">
                  Create one now
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AlertComponent from '@/components/AlertComponent.vue'

export default {
  name: 'LoginPage',
  components: {
    AlertComponent
  },
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      errors: {},
      loginError: null,
      loading: false,
      showPassword: false
    }
  },
  methods: {
    async handleLogin() {
      this.errors = {}
      this.loginError = null

      if (!this.validateForm()) {
        return
      }

      this.loading = true

      try {
        await this.$store.dispatch('auth/login', this.form)

        // Redirect to intended page or dashboard
        const redirectPath = this.$route.query.redirect || '/dashboard'
        this.$router.push(redirectPath)

      } catch (error) {
        this.loginError = error.error || 'Login failed. Please try again.'
      } finally {
        this.loading = false
      }
    },

    validateForm() {
      let isValid = true

      if (!this.form.email) {
        this.errors.email = 'Email is required'
        isValid = false
      } else if (!this.isValidEmail(this.form.email)) {
        this.errors.email = 'Please enter a valid email'
        isValid = false
      }

      if (!this.form.password) {
        this.errors.password = 'Password is required'
        isValid = false
      }

      return isValid
    },

    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(email)
    }
  }
}
</script>

<style scoped>
.login-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card {
  border-radius: 15px;
}

.input-group-text {
  background-color: #f8f9fa;
  border-right: none;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  box-shadow: none;
  border-color: #80bdff;
}

.btn-primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border: none;
  border-radius: 8px;
  font-weight: 500;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
}

.btn-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.btn-link:hover {
  color: #0056b3;
}
</style>