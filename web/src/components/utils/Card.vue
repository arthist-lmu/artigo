<template>
  <v-card
    max-width="900"
    flat
  >
    <v-card-title
      v-if="title"
      :class="{ 'pt-6 px-6': !isDialog }"
    >
      {{ title }}

      <v-btn
        v-if="isDialog"
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="[isDialog ? undefined : 'px-6', 'pt-4']">
      <slot />
    </v-card-text>

    <v-card-actions
      class="pb-6 px-6"
      style="display: block;"
    >
      <slot name="actions" />
    </v-card-actions>

    <slot name="dialogs" />
  </v-card>
</template>

<script>
export default {
  props: {
    value: Boolean,
    title: String,
    isDialog: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    close() {
      this.$emit('input', false);
    },
  },
  computed: {
    status() {
      const { error, loading } = this.$store.state.utils.status;
      return !loading && !error;
    },
    timestamp() {
      return this.$store.state.utils.status.timestamp;
    },
  },
};
</script>
