<template>
  <div v-if="message" :class="alertClass" class="alert alert-dismissible fade show" role="alert">
    <i :class="iconClass" class="me-2"></i>
    <slot>{{ message }}</slot>
    <button 
      type="button" 
      class="btn-close" 
      aria-label="Close" 
      @click="$emit('close')"
    ></button>
  </div>
</template>

<script>
export default {
  name: 'AlertComponent',
  emits: ['close'],
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'info',
      validator: value => ['success', 'error', 'warning', 'info'].includes(value)
    }
  },
  computed: {
    alertClass() {
      const typeMap = {
        success: 'alert-success',
        error: 'alert-danger',
        warning: 'alert-warning',
        info: 'alert-info'
      }
      return `alert ${typeMap[this.type]}`
    },
    iconClass() {
      const iconMap = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
      }
      return iconMap[this.type]
    }
  }
}
</script>

<style scoped>
.alert {
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>