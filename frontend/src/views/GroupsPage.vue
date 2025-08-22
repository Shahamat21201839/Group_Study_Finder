<template>
  <div class="groups-page">
    <div class="container py-4">
      <div class="row mb-4">
        <div class="col-md-8">
          <h1><i class="fas fa-users me-2"></i>Study Groups</h1>
        </div>
        <div class="col-md-4 text-md-end">
          <button
            class="btn btn-primary"
            data-bs-toggle="modal"
            data-bs-target="#createGroupModal"
          >
            <i class="fas fa-plus me-2"></i>Create Group
          </button>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <LoadingComponent message="Loading groups..." />
      </div>

      <div v-else class="row g-4">
        <div
          v-for="group in groups"
          :key="group.group_id"
          class="col-md-6 col-lg-4"
        >
          <router-link
            :to="`/groups/${group.group_id}`"
            class="text-decoration-none h-100 d-block"
          >
            <GroupCard
              :group="group"
              :isMember="group.is_member"
              :myRole="group.my_role"
              @request-join.stop="requestJoin"
            />
          </router-link>
        </div>
      </div>
    </div>

    <CreateGroupModal @group-created="loadGroups" />
  </div>
</template>

<script>
import GroupCard from '@/components/GroupCard.vue'
import CreateGroupModal from '@/components/CreateGroupModal.vue'
import LoadingComponent from '@/components/LoadingComponent.vue'

export default {
  name: 'GroupsPage',
  components: { GroupCard, CreateGroupModal, LoadingComponent },
  data() {
    return {
      loading: false
    }
  },
  computed: {
    groups() {
      return this.$store.getters['groups/allGroups']
    }
  },
  async mounted() {
    await this.loadGroups()
  },
  methods: {
    async loadGroups() {
      this.loading = true
      try {
        await this.$store.dispatch('groups/fetchGroups')
      } catch (error) {
        console.error('Failed to load groups:', error)
      } finally {
        this.loading = false
      }
    },
    async requestJoin(groupId) {
      try {
        await this.$store.dispatch('groups/requestToJoinGroup', groupId)
        this.$store.dispatch('setSuccess', 'Join request sent!')
      } catch (error) {
        this.$store.dispatch('setError', 'Failed to send join request')
      }
    }
  }
}
</script>

<style scoped>
.groups-page .card {
  cursor: pointer;
}
</style>
