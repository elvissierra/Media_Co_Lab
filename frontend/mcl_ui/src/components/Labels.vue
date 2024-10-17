<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" class="text-center mb-5">
        <h1 class="headline">Labels Overview</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="(labels, type) in groupedLabels"
        :key="type"
        cols="12"
        md="6"
        lg="4"
        class="mb-4"
      >
        <v-card outlined class="pa-3" elevation="2">
          <v-card-title class="subtitle-1 text-uppercase font-weight-bold d-flex justify-space-between align-center">
            <span>{{ type }}</span>
            <v-badge color="primary" :content="labels.length" class="ml-3"></v-badge>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="label-collage mt-3">
            <div v-for="label in labels" :key="label.id" class="label-item" :style="{ backgroundColor: label.preset_tag, color: getTextColor(label.preset_tag) }">
              {{ label.title }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'mclLabels',
  data() {
    return {
      labels: [],
    };
  },
  computed: {
    groupedLabels() {
      const grouped = this.labels.reduce((acc, label) => {
        const type =
          label.preset_type === 'custom' && label.custom_preset_type
            ? label.custom_preset_type
            : label.preset_type;

        if (!acc[type]) {
          acc[type] = [];
        }
        acc[type].push(label);
        return acc;
      }, {});

      return grouped;
    },
  },
  created() {
    this.fetchLabels();
  },
  methods: {
    async fetchLabels() {
      try {
        const response = await this.$axios.get('/labels/');
        this.labels = response.data;
      } catch (error) {
        console.error('Error fetching labels:', error);
      }
    },
    getTextColor(backgroundColor) {
      const darkColors = ['#000000', '#3a3a3a', '#4e4e4e'];
      return darkColors.includes(backgroundColor.toLowerCase())
        ? '#ffffff'
        : '#000000';
    },
  },
};
</script>

<style scoped>
.label-collage {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  max-height: 300px;
  overflow-y: auto;
  padding: 10px;
}

.label-item {
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  text-align: center;
  font-weight: bold;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.label-item:hover {
  transform: scale(1.05);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
</style>