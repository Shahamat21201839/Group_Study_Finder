<template>
  <div class="group-chat">
    <!-- Chat Messages -->
    <div 
      ref="messagesContainer"
      class="chat-messages-container"
      @scroll="onScroll"
    >
      <div v-if="messagesLoading" class="text-center py-2">
        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
      </div>

      <div v-if="messages.length === 0 && !messagesLoading" class="empty-chat text-center text-muted py-3">
        <i class="fas fa-comments mb-2"></i>
        <p class="mb-0 small">No group messages yet</p>
      </div>

      <div
        v-for="message in messages"
        :key="message.message_id"
        class="message mb-2"
        :class="{ 'own-message': message.sender_id === currentUser.user_id }"
      >
        <div class="message-bubble">
          <div class="message-header">
            <small class="sender-name">{{ message.sender_name }}</small>
            <small class="timestamp text-muted">{{ formatTime(message.sent_at) }}</small>
          </div>
          <div class="message-text">{{ message.message }}</div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="message-input-container">
      <form @submit.prevent="sendMessage">
        <div class="input-group input-group-sm">
          <input
            v-model="newMessage"
            type="text"
            class="form-control"
            placeholder="Type a message..."
            :disabled="!isConnected || sendingMessage"
            maxlength="500"
          >
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!newMessage.trim() || !isConnected || sendingMessage"
          >
            <i v-if="sendingMessage" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-paper-plane"></i>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GroupChat',
  props: {
    groupId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      newMessage: '',
      sendingMessage: false,
      messagesLoading: false,
      autoScroll: true
    }
  },
  computed: {
    currentUser() {
      return this.$store.getters['auth/user']
    },

    messages() {
      return this.$store.getters['chat/getGroupMessages'](this.groupId)
    },

    isConnected() {
      return this.$store.getters['chat/isConnected']
    }
  },
  async mounted() {
    await this.initializeGroupChat()

    this.$nextTick(() => {
      this.scrollToBottom()
    })
  },

  beforeUnmount() {
    this.$store.dispatch('chat/leaveGroupChat', this.groupId)
  },

  updated() {
    if (this.autoScroll) {
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    }
  },

  methods: {
    async initializeGroupChat() {
      try {
        this.$store.dispatch('chat/joinGroupChat', this.groupId)

        this.messagesLoading = true
        await this.$store.dispatch('chat/fetchGroupMessages', { 
          groupId: this.groupId 
        })
      } catch (error) {
        console.error('Failed to initialize group chat:', error)
      } finally {
        this.messagesLoading = false
      }
    },

    async sendMessage() {
      if (!this.newMessage.trim() || !this.isConnected || this.sendingMessage) return

      this.sendingMessage = true

      try {
        await this.$store.dispatch('chat/sendGroupMessage', {
          groupId: this.groupId,
          message: this.newMessage.trim()
        })
        this.newMessage = ''
        this.autoScroll = true
      } catch (error) {
        console.error('Failed to send group message:', error)
      } finally {
        this.sendingMessage = false
      }
    },

    onScroll() {
      const container = this.$refs.messagesContainer
      if (container) {
        const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 50
        this.autoScroll = isNearBottom
      }
    },

    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },

    formatTime(dateString) {
      return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.group-chat {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-messages-container {
  flex: 1;
  padding: 0.75rem;
  overflow-y: auto;
  background: #f8f9fa;
}

.message {
  display: flex;
}

.message.own-message {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 70%;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.own-message .message-bubble {
  background: #007bff;
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
  font-size: 0.75rem;
}

.own-message .message-header {
  color: rgba(255, 255, 255, 0.8);
}

.sender-name {
  font-weight: 600;
}

.message-text {
  font-size: 0.875rem;
  word-wrap: break-word;
}

.message-input-container {
  padding: 0.75rem;
  border-top: 1px solid #e9ecef;
  background: white;
}

.empty-chat {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>