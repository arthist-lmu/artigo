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

      <v-col
        class="pa-0"
        align="right"
      >
        <slot name="helper" />

        <v-btn
          v-if="isDialog"
          @click="close"
          icon
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-col>
    </v-card-title>

    <v-card-text
      v-if="$slots.default"
      :class="[isDialog ? undefined : 'px-6', 'pt-4']"
    >
      <slot />
    </v-card-text>

    <v-card-actions
      v-if="$slots.actions"
      :class="[$slots.default ? 'pb-6 px-6' : 'pa-0']"
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
