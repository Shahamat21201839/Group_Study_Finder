import api from '@/services/api'

const state = {
  allGroups: [],
  currentGroup: null,
  myGroups: [],
  joinRequests: []    // for pending requests
}

const getters = {
  allGroups: state => state.allGroups,
  currentGroup: state => state.currentGroup,
  myGroups: state => state.myGroups,
  joinRequests: state => state.joinRequests
}

const actions = {
  async fetchGroups({ commit }) {
    const { data } = await api.get('/groups')
    commit('SET_GROUPS', data.groups)
  },
  async fetchMyGroups({ commit }) {
    const { data } = await api.get('/groups/my-groups')
    commit('SET_MY_GROUPS', data.groups)
  },
  async fetchGroupDetail({ commit }, groupId) {
    const { data } = await api.get(`/groups/${groupId}`)
    commit('SET_CURRENT_GROUP', data.group)
  },
  async createGroup({ dispatch }, groupData) {
    await api.post('/groups', groupData)
    await dispatch('fetchGroups')
    await dispatch('fetchMyGroups')
  },
  async joinGroup({ dispatch }, groupId) {
    await api.post(`/groups/${groupId}/join-request`)
    dispatch('fetchGroupDetail', groupId)
  },
  async leaveGroup({ dispatch }, groupId) {
    await api.delete(`/groups/${groupId}/leave`)
    await dispatch('fetchGroups')
    await dispatch('fetchMyGroups')
  },
  async kickMember({ dispatch }, { groupId, userId }) {
    await api.delete(`/groups/${groupId}/members/${userId}`)
    dispatch('fetchGroupDetail', groupId)
  },
  // new actions for join requests
  async fetchJoinRequests({ commit }, groupId) {
    const { data } = await api.get(`/groups/${groupId}/join-requests`)
    commit('SET_JOIN_REQUESTS', data.requests)
  },
  async respondToJoinRequest(_, { requestId, action }) {
    await api.put(`/groups/join-requests/${requestId}/respond`, { action })
  }
}

const mutations = {
  SET_GROUPS(state, groups) {
    state.allGroups = groups
  },
  SET_MY_GROUPS(state, groups) {
    state.myGroups = groups
  },
  SET_CURRENT_GROUP(state, group) {
    state.currentGroup = group
  },
  SET_JOIN_REQUESTS(state, requests) {
    state.joinRequests = requests
  },
  CLEAR_CURRENT_GROUP(state) {
    state.currentGroup = null
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
