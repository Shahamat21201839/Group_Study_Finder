<template>
  <div class="chat-page">
    <div class="container py-4">
      <h1><i class="fas fa-comments me-2"></i>Global Chat</h1>
      <div class="row">
        <div class="col-lg-8 mx-auto">
          <div class="card">
            <div class="card-body">
              <div id="messages" class="messages-container mb-3" ref="messages">
                <div
                  v-for="message in globalMessages"
                  :key="message.message_id"
                  class="message mb-2"
                >
                  <strong>{{ message.sender_name }}</strong>: {{ message.message }}
                  <small class="text-muted d-block">
                    {{ formatTime(message.sent_at) }}
                  </small>
                </div>
              </div>
              <form @submit.prevent="sendMessage">
                <div class="input-group">
                  <input
                    v-model="newMessage"
                    type="text"
                    class="form-control"
                    placeholder="Type a message..."
                  >
                  <button type="submit" class="btn btn-primary" :disabled="!newMessage.trim()">
                    Send
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatPage',
  data() {
    return {
      newMessage: ''
    }
  },
  computed: {
    globalMessages() {
      return this.$store.getters['chat/globalMessages']
    }
  },
  async mounted() {
    await this.$store.dispatch('chat/fetchGlobalMessages')
    this.$store.dispatch('chat/initializeSocket')
    this.$nextTick(() => this.scrollToBottom())
  },
  methods: {
    async sendMessage() {
      if (!this.newMessage.trim()) return
      try {
        await this.$store.dispatch('chat/sendGlobalMessage', this.newMessage.trim())
        this.newMessage = ''
        this.$nextTick(() => this.scrollToBottom())
      } catch (error) {
        console.error('Failed to send message:', error)
      }
    },
    formatTime(dateString) {
      return new Date(dateString).toLocaleTimeString()
    },
    scrollToBottom() {
      const container = this.$refs.messages
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }
  }
}
</script>

<style scoped>
.messages-container {
  height: 400px;
  overflow-y: auto;
  border: 1px solid #e9ecef;
  padding: 1rem;
}
</style>
