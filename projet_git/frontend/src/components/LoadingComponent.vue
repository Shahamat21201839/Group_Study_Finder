<template>
  <div class="loading-container" :class="{ 'overlay': overlay }">
    <div class="d-flex flex-column align-items-center">
      <div class="spinner-border" :class="spinnerClass" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p v-if="message" class="mt-2 text-muted">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingComponent',
  props: {
    message: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large'].includes(value)
    },
    overlay: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    spinnerClass() {
      const sizeMap = {
        small: 'spinner-border-sm',
        medium: '',
        large: 'spinner-border-lg'
      }
      return `text-primary ${sizeMap[this.size]}`
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.loading-container.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 9999;
}

.spinner-border-lg {
  width: 3rem;
  height: 3rem;
}
</style>