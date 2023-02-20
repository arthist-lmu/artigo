<template>
  <v-row
    :id="messageId"
    :class="message.from"
    justify="start"
  >
    <v-col>
      <v-card
        color="grey lighten-4"
        flat
      >
        <v-card-text class="px-4 py-2">
          <v-row>
            <v-col cols="auto">
              {{ message.text }}
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    message: Object,
    hide: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    messageId() {
      if (this.message.highlight) {
        return `highlight-${this.message.highlight}`;
      }
      return undefined;
    },
  },
};
</script>
