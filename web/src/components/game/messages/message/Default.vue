<template>
  <v-row
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
    message: {
      type: Object,
      default: null,
    },
    hide: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
