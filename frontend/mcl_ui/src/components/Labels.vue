<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Labels Overview</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <div class="dynamic-grid">
          <div v-for="(labels, type) in groupedLabels" :key="type" class="type-group">
            <h3>{{ type }}</h3>
            <div class="label-collage">
              <div
                v-for="label in labels"
                :key="label.id"
                :style="{ backgroundColor: label.preset_tag }"
                class="label-item"
              >
                {{ label.title }}
              </div>
            </div>
          </div>
        </div>
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
      return this.labels.reduce((acc, label) => {
        const type = label.preset_type === 'custom' && label.custom_preset_type
          ? label.custom_preset_type
          : label.preset_type;

        if (!acc[type]) {
          acc[type] = [];
        }
        acc[type].push(label);
        return acc;
      }, {});
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
  },
};
</script>

<style scoped>
.dynamic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  grid-auto-rows: 100px;
  gap: 10px;
}

.label-collage {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
}

.label-item {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 10px;
  color: white;
  font-weight: bold;
  border-radius: 8px; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; 
}

.green {
  background: #6fcf97
}

.yellow {
  background: #f2c94c
}

.orange {
  background: #f2994a
}
.red {
  background: #eb5757
}

.label-item:hover {
  transform: scale(1.05); 
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15); 
}

h1 {
  font-family: 'Poppins', sans-serif;
  font-size: 2.5rem;
  font-weight: 600;
  color: #333;
}

h3 {
  font-family: 'Poppins', sans-serif;
  font-size: 1.5rem;
  font-weight: 500;
  color: #555;
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
</style>

