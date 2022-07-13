<template>
  <v-alert
    class="mb-0"
    dense
  >
    <template v-slot:prepend>
      <v-progress-circular
        :size="48"
        :width="2"
        :rotate="-90"
        :value="progress"
        color="primary"
      >
        {{ value }}
      </v-progress-circular>
    </template>

    <div
      :title="title"
      class="ml-4"
    >
      <template v-if="isSmAndDown">
        <v-icon>
          {{ icon }}
        </v-icon>
      </template>

      <template v-else>
        <div class="text-subtitle-1 grey--text text--darken-4">
          {{ title }}
        </div>

        <div
          v-if="subvalue > 0"
          class="mt-n2 text-caption grey--text"
        >
          {{ subvalue }} {{ subtitle }}
        </div>
      </template>
    </div>
  </v-alert>
</template>

<script>
export default {
  props: {
    icon: String,
    title: String,
    subtitle: String,
    value: {
      type: Number,
      default: 0,
    },
    subvalue: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      progress: 0,
    };
  },
  computed: {
    isSmAndDown() {
      return this.$vuetify.breakpoint.smAndDown;
    },
  },
  created() {
    setTimeout(() => {
      this.$nextTick(() => {
        this.progress = 100;
      });
    }, 250);
  },
};
</script>
