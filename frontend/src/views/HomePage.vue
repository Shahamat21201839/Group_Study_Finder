<template>
  <div class="home-page">
    <section class="hero-section bg-primary text-white">
      <div class="container">
        <div class="row align-items-center min-vh-100">
          <div class="col-lg-6">
            <h1 class="display-4 fw-bold mb-4">Group Study Finder</h1>
            <p class="lead mb-4">
              Connect with fellow students, form study groups, and excel together. 
              Find study partners based on courses, share resources, and collaborate 
              effectively for academic success.
            </p>
            <div class="d-flex flex-wrap gap-3 mb-4">
              <router-link to="/register" class="btn btn-light btn-lg px-4">
                <i class="fas fa-user-plus me-2"></i>Get Started
              </router-link>
              <router-link to="/login" class="btn btn-outline-light btn-lg px-4">
                <i class="fas fa-sign-in-alt me-2"></i>Sign In
              </router-link>
            </div>
          </div>
          <div class="col-lg-6 text-center">
            <i class="fas fa-users display-1 mb-4"></i>
            <div class="feature-stats">
              <div class="stat-item">
                <h3 class="h4 fw-bold">Study Together</h3>
                <p>Form groups with classmates</p>
              </div>
              <div class="stat-item">
                <h3 class="h4 fw-bold">Share Resources</h3>
                <p>Exchange study materials</p>
              </div>
              <div class="stat-item">
                <h3 class="h4 fw-bold">Real-time Chat</h3>
                <p>Communicate instantly</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="features-section py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-12 text-center mb-5">
            <h2 class="h1 fw-bold">Why Choose Group Study Finder?</h2>
            <p class="lead text-muted">Everything you need to succeed academically</p>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card h-100">
              <div class="feature-icon">
                <i class="fas fa-search text-primary"></i>
              </div>
              <h4>Find Study Partners</h4>
              <p>Search for students taking the same courses or who have completed them. 
                 Connect with peers who share your academic goals.</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="feature-card h-100">
              <div class="feature-icon">
                <i class="fas fa-users text-success"></i>
              </div>
              <h4>Create Study Groups</h4>
              <p>Form study groups for your courses with scheduling features. 
                 Manage group members and organize study sessions effectively.</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="feature-card h-100">
              <div class="feature-icon">
                <i class="fas fa-comments text-info"></i>
              </div>
              <h4>Real-time Communication</h4>
              <p>Chat with your study group members or join global discussions. 
                 Stay connected and share insights instantly.</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="feature-card h-100">
              <div class="feature-icon">
                <i class="fas fa-book text-warning"></i>
              </div>
              <h4>Course Management</h4>
              <p>Track your ongoing and completed courses. 
                 Get feedback on courses and help others with your experience.</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="feature-card h-100">
              <div class="feature-icon">
                <i class="fas fa-bell text-danger"></i>
              </div>
              <h4>Smart Notifications</h4>
              <p>Get notified about group activities, exam schedules, 
                 and resource sharing opportunities.</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="feature-card h-100">
              <div class="feature-icon">
                <i class="fas fa-share-alt text-purple"></i>
              </div>
              <h4>Resource Sharing</h4>
              <p>Request study materials from students who completed courses. 
                 Share your resources and help others succeed.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-section bg-light py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h2 class="h1 fw-bold mb-4">Ready to Start Studying Together?</h2>
            <p class="lead mb-4">
              Join Group Study Finder today and connect with your classmates. 
              Academic success is better achieved together.
            </p>
            <router-link to="/register" class="btn btn-primary btn-lg px-5">
              <i class="fas fa-rocket me-2"></i>Join Now - It's Free!
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  mounted() {
    if (this.$store.getters['auth/isAuthenticated']) {
      this.$router.push('/dashboard')
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
}

.feature-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 8px;
}

.features-section {
  background: #f8f9fa;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.text-purple {
  color: #6f42c1 !important;
}

.btn-lg {
  padding: 0.75rem 2rem;
}

@media (max-width: 768px) {
  .display-4 {
    font-size: 2.5rem;
  }

  .feature-stats {
    margin-top: 2rem;
  }
}
</style>