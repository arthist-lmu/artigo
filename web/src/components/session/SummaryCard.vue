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
        <span class="font-weight-medium">
          {{ value }}
        </span>
      </v-progress-circular>
    </template>

    <div
      :title="title"
      class="ml-4"
    >
      <div class="text-subtitle-1 grey--text text--darken-4">
        {{ title }}
      </div>

      <div
        v-if="subvalue > 0"
        class="mt-n2 text-caption grey--text"
      >
        {{ subvalue.toFixed(2) }} {{ subtitle }}
      </div>
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
  created() {
    setTimeout(() => {
      this.$nextTick(() => {
        this.progress = 100;
      });
    }, 250);
  },
};
</script>

<style scoped>
.v-alert .v-progress-circular {
  background-color: transparent;
  border-radius: 24px;
  -webkit-transition: background-color 0.25s linear;
  -ms-transition: background-color 0.25s linear;
  transition: background-color 0.25s linear;
}

.v-alert:hover .v-progress-circular {
  background-color: rgba(66, 71, 152, 0.15);
}
</style>
