<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card max-width="520" class="pa-8 text-center" elevation="2">
      <v-icon size="64" color="warning" class="mb-4">mdi-clock-outline</v-icon>

      <v-card-title class="text-h5 mb-2">
        {{ title }}
      </v-card-title>

      <v-card-text class="text-body-1 mb-6">
        {{ message }}
      </v-card-text>

      <v-btn variant="outlined" color="primary" @click="checkStatus" :loading="checking" class="mr-3">
        Check Status
      </v-btn>
      <v-btn variant="text" color="error" @click="logout">
        Log Out
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "@/axios";

export default {
  name: "PendingApproval",
  data() {
    return { checking: false };
  },
  computed: {
    ...mapGetters(["isPendingApproval", "isDenied", "orgIsApproved"]),
    type() {
      return this.$route.query.type || "member";
    },
    title() {
      return this.type === "org"
        ? "Organization Pending Review"
        : "Membership Pending Approval";
    },
    message() {
      if (this.type === "org") {
        return "Your organization registration is under review. You will be able to access the platform once it is approved by our team.";
      }
      const orgName = this.$store.state.user?.organization?.title || "your organization";
      return `Your membership request to ${orgName} is pending approval from the organization admin.`;
    },
  },
  methods: {
    async checkStatus() {
      this.checking = true;
      try {
        const userId = this.$store.state.user?.id;
        if (!userId) return;
        const response = await axios.get(`/api/users/${userId}/`);
        this.$store.commit("setUser", response.data);
        this.redirectIfUnblocked(response.data);
      } finally {
        this.checking = false;
      }
    },
    redirectIfUnblocked(user) {
      if (user.is_staff) {
        this.$router.push("/platform-admin");
      } else if (user.org_status === "approved" && user.organization?.is_approved) {
        this.$router.push("/medias");
      } else if (user.org_status === "denied") {
        this.$router.push("/denied");
      }
    },
    logout() {
      this.$store.commit("setAuthToken", null);
      this.$store.commit("setUser", null);
      this.$router.push("/login");
    },
  },
};
</script>
