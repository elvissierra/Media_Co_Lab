<template>
  <v-container class="pa-4">
    <v-row justify="center">
      <v-col cols="12" md="8" class="text-center">
        <h1 class="headline mb-5">Organization Overview: {{ organization?.title }}</h1>
      </v-col>
    </v-row>

    <v-tabs v-if="isOrgAdmin" v-model="activeTab" class="mt-6">
      <v-tab value="overview">Overview</v-tab>
      <v-tab value="members">Members <v-badge v-if="pendingMembers.length" :content="pendingMembers.length" color="warning" inline /></v-tab>
    </v-tabs>

    <v-window v-if="isOrgAdmin" v-model="activeTab" class="mt-4">
      <v-window-item value="overview">
        <v-row>
          <v-col cols="12" class="mb-4">
            <h2 class="text-center mb-4">Teams</h2>
          </v-col>
          <v-col
            v-for="team in organization?.teams"
            :key="team.title"
            cols="12"
            sm="6"
            md="4"
            class="mb-4"
          >
            <v-card outlined elevation="3" class="pa-3 team-card">
              <v-card-title class="text-uppercase font-weight-bold d-flex align-center justify-center">
                <v-icon left class="mr-2">mdi-account-group</v-icon>
                {{ team.title }}
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text class="pt-3">
                <v-img
                  v-if="team.image"
                  :src="team.image"
                  height="150px"
                  class="mb-3"
                  contain
                ></v-img>
                <p>{{ team.description }}</p>
                <v-divider class="my-2"></v-divider>

                <h4 class="subtitle-2 mb-3">Users</h4>
                <v-chip-group
                  column
                  class="d-flex flex-wrap"
                >
                  <v-chip
                    v-for="user in team.users"
                    :key="user.id"
                    class="ma-1 d-flex align-center user-chip"
                    outlined
                    color="primary"
                    ripple="false"
                    size="large"
                  >
                    <v-avatar left size="32" class="mr-2 ml-n2">
                      <v-img
                        :src="getFullImageUrl(user.avatar)"
                        alt="user avatar"
                        height="40"
                        width="40"
                        aspect-ratio="1"
                        class="rounded-circle"
                      />
                    </v-avatar>
                    {{ user.first_name }}
                  </v-chip>
                </v-chip-group>
                <p v-if="!team.users.length" class="text-grey">No users in this team</p>

                <v-divider class="my-4"></v-divider>

                <h4 class="subtitle-2 mb-3">Media Collage</h4>
                <v-row>
                  <v-col
                    v-for="media in team.medias"
                    :key="media.uuid"
                    cols="6"
                    sm="4"
                    md="3"
                    class="mb-3"
                  >
                    <v-hover v-slot:default="{ props }">
                      <v-card
                        v-bind="props"
                        @click="viewMedia(media.uuid)"
                        class="media-thumbnail"
                        elevation="2"
                        tile
                      >
                        <v-img
                          v-if="isImage(media.content)"
                          :src="getFullImageUrl(media.content)"
                          :alt="media.title"
                          aspect-ratio="1"
                          class="hover-effect"
                        />
                      </v-card>
                    </v-hover>
                  </v-col>
                </v-row>
                <p v-if="!team.medias.length" class="text-grey">No media in this team</p>

                <v-card-actions class="justify-center mt-4">
                  <v-btn color="blue darken-2" class="white---text" @click="viewTeam(team.id)">View Team</v-btn>
                </v-card-actions>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row v-if="organization?.labels && organization.labels.length">
          <v-col cols="12" class="mb-4">
            <h2 class="text-center mb-4">Labels</h2>
          </v-col>
          <v-col
            v-for="label in organization.labels"
            :key="label.id"
            cols="12"
            sm="6"
            md="4"
            class="mb-4"
          >
            <v-card outlined class="pa-3" :color="label.color || 'grey lighten-4'">
              <v-card-title class="font-weight-medium">
                <v-chip color="primary" text-color="white">{{ label.name }}</v-chip>
              </v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>

      <v-window-item value="members">
        <h3 class="text-h6 mb-4">Pending Requests</h3>

        <v-alert v-if="memberError" type="error" class="mb-3">{{ memberError }}</v-alert>
        <v-alert v-if="memberSuccess" type="success" class="mb-3">{{ memberSuccess }}</v-alert>

        <v-card v-if="pendingMembers.length === 0" class="pa-4 text-center mb-6">
          <p class="text-body-2 text-medium-emphasis">No pending requests.</p>
        </v-card>

        <v-list v-else class="mb-6">
          <v-list-item
            v-for="member in pendingMembers"
            :key="member.id"
            :title="member.first_name + ' ' + member.last_name"
            :subtitle="member.email"
          >
            <template #append>
              <v-btn size="small" color="success" variant="tonal" class="mr-2"
                :loading="memberActionLoading === member.id + '-approve'"
                @click="approveMember(member)">Approve</v-btn>
              <v-btn size="small" color="error" variant="tonal"
                :loading="memberActionLoading === member.id + '-deny'"
                @click="denyMember(member)">Deny</v-btn>
            </template>
          </v-list-item>
        </v-list>

        <h3 class="text-h6 mb-4">Approved Members</h3>
        <v-list>
          <v-list-item
            v-for="member in approvedMembers"
            :key="member.id"
            :title="member.first_name + ' ' + member.last_name"
            :subtitle="member.email"
          >
            <template #prepend>
              <v-avatar color="primary" size="36">
                <span class="text-caption">{{ member.first_name[0] }}{{ member.last_name[0] }}</span>
              </v-avatar>
            </template>
          </v-list-item>
        </v-list>
      </v-window-item>
    </v-window>

    <template v-if="!isOrgAdmin">
      <v-row>
        <v-col cols="12" class="mb-4">
          <h2 class="text-center mb-4">Teams</h2>
        </v-col>
        <v-col
          v-for="team in organization?.teams"
          :key="team.title"
          cols="12"
          sm="6"
          md="4"
          class="mb-4"
        >
          <v-card outlined elevation="3" class="pa-3 team-card">
            <v-card-title class="text-uppercase font-weight-bold d-flex align-center justify-center">
              <v-icon left class="mr-2">mdi-account-group</v-icon>
              {{ team.title }}
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pt-3">
              <v-img
                v-if="team.image"
                :src="team.image"
                height="150px"
                class="mb-3"
                contain
              ></v-img>
              <p>{{ team.description }}</p>
              <v-divider class="my-2"></v-divider>

              <h4 class="subtitle-2 mb-3">Users</h4>
              <v-chip-group
                column
                class="d-flex flex-wrap"
              >
                <v-chip
                  v-for="user in team.users"
                  :key="user.id"
                  class="ma-1 d-flex align-center user-chip"
                  outlined
                  color="primary"
                  ripple="false"
                  size="large"
                >
                  <v-avatar left size="32" class="mr-2 ml-n2">
                    <v-img
                      :src="getFullImageUrl(user.avatar)"
                      alt="user avatar"
                      height="40"
                      width="40"
                      aspect-ratio="1"
                      class="rounded-circle"
                    />
                  </v-avatar>
                  {{ user.first_name }}
                </v-chip>
              </v-chip-group>
              <p v-if="!team.users.length" class="text-grey">No users in this team</p>

              <v-divider class="my-4"></v-divider>

              <h4 class="subtitle-2 mb-3">Media Collage</h4>
              <v-row>
                <v-col
                  v-for="media in team.medias"
                  :key="media.uuid"
                  cols="6"
                  sm="4"
                  md="3"
                  class="mb-3"
                >
                  <v-hover v-slot:default="{ props }">
                    <v-card
                      v-bind="props"
                      @click="viewMedia(media.uuid)"
                      class="media-thumbnail"
                      elevation="2"
                      tile
                    >
                      <v-img
                        v-if="isImage(media.content)"
                        :src="getFullImageUrl(media.content)"
                        :alt="media.title"
                        aspect-ratio="1"
                        class="hover-effect"
                      />
                    </v-card>
                  </v-hover>
                </v-col>
              </v-row>
              <p v-if="!team.medias.length" class="text-grey">No media in this team</p>

              <v-card-actions class="justify-center mt-4">
                <v-btn color="blue darken-2" class="white---text" @click="viewTeam(team.id)">View Team</v-btn>
              </v-card-actions>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-if="organization?.labels && organization.labels.length">
        <v-col cols="12" class="mb-4">
          <h2 class="text-center mb-4">Labels</h2>
        </v-col>
        <v-col
          v-for="label in organization.labels"
          :key="label.id"
          cols="12"
          sm="6"
          md="4"
          class="mb-4"
        >
          <v-card outlined class="pa-3" :color="label.color || 'grey lighten-4'">
            <v-card-title class="font-weight-medium">
              <v-chip color="primary" text-color="white">{{ label.name }}</v-chip>
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import axios from "@/axios";

export default {
  name: 'OrganizationOverview',
  data() {
    return {
      organization: null,
      activeTab: "overview",
      pendingMembers: [],
      approvedMembers: [],
      memberError: null,
      memberSuccess: null,
      memberActionLoading: null,
    };
  },
  computed: {
    isOrgAdmin() {
      return this.$store.getters.isOrgAdmin;
    },
  },
  async created() {
    try {
      const response = await this.$axios.get('/organizations/ov/');
      this.organization = response.data;
      console.log(this.organization);
    } catch (error) {
      console.error('Error fetching organizational information:', error);
    }
  },
  mounted() {
    if (this.isOrgAdmin) {
      this.fetchPendingMembers();
      this.fetchApprovedMembers();
    }
  },
  methods: {
    viewMedia(mediaId) {
      this.$router.push({ name: 'MediaDetail', params: { uuid: mediaId } });
    },
    viewTeam(teamId) {
      this.$router.push({ name: 'TeamDetail', params: { team_id: teamId } });
    },
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    getFullImageUrl(relativeUrl) {
      return `${process.env.VUE_APP_BASE_URL}${relativeUrl}`;
    },
    async fetchPendingMembers() {
      try {
        const response = await axios.get("/api/organizations/members/pending/");
        this.pendingMembers = response.data;
      } catch {
        this.memberError = "Failed to load pending members.";
      }
    },
    async fetchApprovedMembers() {
      try {
        const response = await axios.get("/api/users/");
        this.approvedMembers = response.data.filter(
          (u) => u.org_status === "approved" && !u.is_org_admin
        );
      } catch {
        this.memberError = "Failed to load members.";
      }
    },
    async approveMember(member) {
      this.memberActionLoading = member.id + "-approve";
      this.memberError = null;
      try {
        await axios.post(`/api/users/${member.id}/approve/`);
        this.pendingMembers = this.pendingMembers.filter((m) => m.id !== member.id);
        this.memberSuccess = `${member.first_name} ${member.last_name} approved.`;
        await this.fetchApprovedMembers();
      } catch {
        this.memberError = "Failed to approve member.";
      } finally {
        this.memberActionLoading = null;
      }
    },
    async denyMember(member) {
      this.memberActionLoading = member.id + "-deny";
      this.memberError = null;
      try {
        await axios.post(`/api/users/${member.id}/deny/`);
        this.pendingMembers = this.pendingMembers.filter((m) => m.id !== member.id);
        this.memberSuccess = `${member.first_name} ${member.last_name} denied.`;
      } catch {
        this.memberError = "Failed to deny member.";
      } finally {
        this.memberActionLoading = null;
      }
    },
  }
};
</script>

<style>
.v-card {
  transition: transform 0.3s;
}

.v-card:hover {
  transform: scale(1.05);
}

.team-card {
  border: 2px solid #1976D2;
  border-radius: 8px;
  pointer-events: none;
}

.team-card .v-card-actions,
.team-card .v-btn {
  pointer-events: auto;
}

h1, h2, h4 {
  color: #1976D2;
}

.mb-4 {
  margin-bottom: 20px;
}

.mb-5 {
  margin-bottom: 40px;
}
.media-thumbnail {
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.media-thumbnail:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15)
}

.text-grey {
  color: #9e9e9e
}

.hover-effect {
  transition: transform 0.3s ease-in-out;
}
.hover-effect:hover {
  transform: scale(1.05);
}
</style>