<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">Platform Admin — Pending Organizations</h1>
      </v-col>
    </v-row>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>
    <v-alert v-if="successMsg" type="success" class="mb-4">{{ successMsg }}</v-alert>

    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <v-card v-if="!loading && pendingOrgs.length === 0" class="pa-6 text-center">
      <v-icon size="48" color="success" class="mb-3">mdi-check-circle</v-icon>
      <p class="text-body-1">No pending organizations.</p>
    </v-card>

    <v-table v-if="pendingOrgs.length > 0">
      <thead>
        <tr>
          <th>Organization</th>
          <th>Creator</th>
          <th>Submitted</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="org in pendingOrgs" :key="org.id">
          <td>{{ org.title }}</td>
          <td>{{ org.creator_email || "—" }}</td>
          <td>{{ formatDate(org.created_at) }}</td>
          <td>
            <v-btn
              size="small"
              color="success"
              variant="tonal"
              class="mr-2"
              :loading="actionLoading === org.id + '-approve'"
              @click="approve(org)"
            >Approve</v-btn>
            <v-btn
              size="small"
              color="error"
              variant="tonal"
              :loading="actionLoading === org.id + '-deny'"
              @click="deny(org)"
            >Deny</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
import axios from "@/axios";

export default {
  name: "PlatformAdmin",
  data() {
    return {
      pendingOrgs: [],
      loading: false,
      actionLoading: null,
      error: null,
      successMsg: null,
    };
  },
  mounted() {
    this.fetchPending();
  },
  methods: {
    async fetchPending() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/organizations/pending/");
        this.pendingOrgs = response.data;
      } catch {
        this.error = "Failed to load pending organizations.";
      } finally {
        this.loading = false;
      }
    },
    async approve(org) {
      this.actionLoading = org.id + "-approve";
      this.error = null;
      try {
        await axios.post(`/api/organizations/${org.id}/approve/`);
        this.pendingOrgs = this.pendingOrgs.filter((o) => o.id !== org.id);
        this.successMsg = `"${org.title}" approved.`;
      } catch {
        this.error = "Failed to approve organization.";
      } finally {
        this.actionLoading = null;
      }
    },
    async deny(org) {
      this.actionLoading = org.id + "-deny";
      this.error = null;
      try {
        await axios.post(`/api/organizations/${org.id}/deny/`);
        this.pendingOrgs = this.pendingOrgs.filter((o) => o.id !== org.id);
        this.successMsg = `"${org.title}" denied and removed.`;
      } catch {
        this.error = "Failed to deny organization.";
      } finally {
        this.actionLoading = null;
      }
    },
    formatDate(iso) {
      if (!iso) return "—";
      return new Date(iso).toLocaleDateString();
    },
  },
};
</script>
