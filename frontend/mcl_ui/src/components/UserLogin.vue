<template>
  <v-container class="py-8" max-width="480">
    <v-card class="pa-8" elevation="2">
      <h1 class="text-h4 mb-2 text-center">Sign In</h1>

      <v-alert v-if="registeredMsg" type="success" class="mb-4">{{ registeredMsg }}</v-alert>
      <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

      <v-form @submit.prevent="submit" ref="form">
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
          :rules="[v => !!v || 'Password is required']"
          variant="outlined"
          class="mb-6"
          required
        />
        <v-btn type="submit" color="primary" block :loading="loading" size="large">
          Sign In
        </v-btn>
      </v-form>

      <div class="text-center mt-4">
        <span class="text-body-2">Don't have an account? </span>
        <router-link to="/register" class="text-primary">Register</router-link>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import axiosPublic from "@/axiosPublic";
import axios from "@/axios";

export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      error: null,
      emailRules: [
        (v) => !!v || "Email is required",
        (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "Must be a valid email",
      ],
    };
  },
  computed: {
    registeredMsg() {
      const type = this.$route.query.registered;
      if (type === "org") return "Organization registered! Sign in to continue — platform approval may take 1-2 business days.";
      if (type === "member") return "Request submitted! Sign in to check your status.";
      return null;
    },
  },
  methods: {
    async submit() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      this.loading = true;
      this.error = null;

      try {
        const loginResponse = await axiosPublic.post("/api/auth/login/", {
          email: this.email,
          password: this.password,
        });

        const token = loginResponse.data.token;
        this.$store.commit("setAuthToken", token);

        // Fetch full user to determine routing
        const meResponse = await axios.get("/api/users/me/");
        const user = meResponse.data;
        this.$store.commit("setUser", user);

        this.routeAfterLogin(user);
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          err.response?.data?.detail ||
          "Invalid credentials.";
      } finally {
        this.loading = false;
      }
    },
    routeAfterLogin(user) {
      if (user.is_staff) {
        this.$router.push("/platform-admin");
      } else if (!user.organization) {
        this.$router.push("/organizations/reg");
      } else if (!user.organization.is_approved) {
        this.$router.push("/pending?type=org");
      } else if (user.org_status === "pending") {
        this.$router.push("/pending?type=member");
      } else if (user.org_status === "denied") {
        this.$router.push("/denied");
      } else {
        this.$router.push("/medias");
      }
    },
  },
};
</script>
