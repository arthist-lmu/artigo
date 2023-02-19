<template>
  <v-row
    :class="[{ highlight: message.highlight }, message.from]"
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
};
</script>
