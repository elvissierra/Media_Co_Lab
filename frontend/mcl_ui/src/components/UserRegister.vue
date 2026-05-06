<template>
  <v-container class="py-8" max-width="560">
    <!-- Path chooser -->
    <div v-if="!registrationPath" class="text-center">
      <h1 class="text-h4 mb-2">Get Started</h1>
      <p class="text-body-1 mb-8 text-medium-emphasis">How would you like to use Media Co-Lab?</p>
      <v-row justify="center" class="gap-4">
        <v-col cols="12" sm="5">
          <v-card
            class="pa-6 text-center cursor-pointer"
            elevation="2"
            hover
            @click="registrationPath = 'create_org'"
          >
            <v-icon size="48" color="primary" class="mb-3">mdi-domain</v-icon>
            <div class="text-h6 mb-1">Create an Organization</div>
            <div class="text-body-2 text-medium-emphasis">Register a new org — you'll be its admin</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="5">
          <v-card
            class="pa-6 text-center cursor-pointer"
            elevation="2"
            hover
            @click="registrationPath = 'join'"
          >
            <v-icon size="48" color="secondary" class="mb-3">mdi-account-group</v-icon>
            <div class="text-h6 mb-1">Join an Organization</div>
            <div class="text-body-2 text-medium-emphasis">Request access to an existing org</div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Registration form -->
    <v-card v-else class="pa-8" elevation="2">
      <v-btn variant="text" class="mb-4" @click="registrationPath = null">
        <v-icon start>mdi-arrow-left</v-icon> Back
      </v-btn>

      <h2 class="text-h5 mb-6">
        {{ registrationPath === 'create_org' ? 'Register Your Organization' : 'Join an Organization' }}
      </h2>

      <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

      <v-form @submit.prevent="submit" ref="form">
        <!-- Org name (create_org path only) -->
        <v-text-field
          v-if="registrationPath === 'create_org'"
          v-model="orgName"
          label="Organization Name"
          :rules="[v => !!v || 'Organization name is required']"
          variant="outlined"
          class="mb-3"
          required
        />

        <!-- Org selector (join path only) -->
        <v-select
          v-if="registrationPath === 'join'"
          v-model="selectedOrgId"
          :items="approvedOrgs"
          item-title="title"
          item-value="id"
          label="Select Organization"
          :rules="[v => !!v || 'Please select an organization']"
          variant="outlined"
          class="mb-3"
          :loading="orgsLoading"
          required
        />

        <v-text-field
          v-model="firstName"
          label="First Name"
          :rules="[v => !!v || 'First name is required']"
          variant="outlined"
          class="mb-3"
          required
        />
        <v-text-field
          v-model="lastName"
          label="Last Name"
          :rules="[v => !!v || 'Last name is required']"
          variant="outlined"
          class="mb-3"
          required
        />
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          :rules="emailRules"
          variant="outlined"
          class="mb-3"
          required
        />
        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          :rules="[v => !!v || 'Password is required', v => v.length >= 8 || 'Minimum 8 characters']"
          variant="outlined"
          class="mb-6"
          required
        />

        <v-btn type="submit" color="primary" block :loading="loading" size="large">
          {{ registrationPath === 'create_org' ? 'Register Organization' : 'Request Access' }}
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axiosPublic from "@/axiosPublic";
import axios from "@/axios";

export default {
  name: "UserRegister",
  data() {
    return {
      registrationPath: null,
      orgName: "",
      selectedOrgId: null,
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      approvedOrgs: [],
      orgsLoading: false,
      loading: false,
      error: null,
      emailRules: [
        (v) => !!v || "Email is required",
        (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "Must be a valid email",
      ],
    };
  },
  watch: {
    registrationPath(val) {
      if (val === "join" && this.approvedOrgs.length === 0) {
        this.fetchOrgs();
      }
    },
  },
  methods: {
    async fetchOrgs() {
      this.orgsLoading = true;
      try {
        const response = await axiosPublic.get("/api/organizations/");
        this.approvedOrgs = response.data;
      } catch {
        this.error = "Failed to load organizations.";
      } finally {
        this.orgsLoading = false;
      }
    },
    async submit() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      this.loading = true;
      this.error = null;

      try {
        if (this.registrationPath === "create_org") {
          await this.registerWithOrg();
        } else {
          await this.joinOrg();
        }
      } catch (err) {
        this.error =
          err.response?.data?.detail ||
          Object.values(err.response?.data || {})[0]?.[0] ||
          "Registration failed. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    async registerWithOrg() {
      // Step 1: create the org
      const orgResponse = await axiosPublic.post("/api/organizations/register/", {
        title: this.orgName,
      });
      const orgId = orgResponse.data.id;

      // Step 2: register the user as org admin
      await axiosPublic.post("/api/users/create/", {
        first_name: this.firstName,
        last_name: this.lastName,
        email: this.email,
        password: this.password,
        organization_id: orgId,
        registration_type: "create_org",
      });

      this.$router.push("/login?registered=org");
    },
    async joinOrg() {
      await axiosPublic.post("/api/users/create/", {
        first_name: this.firstName,
        last_name: this.lastName,
        email: this.email,
        password: this.password,
        organization_id: this.selectedOrgId,
        registration_type: "join",
      });

      this.$router.push("/login?registered=member");
    },
  },
};
</script>
