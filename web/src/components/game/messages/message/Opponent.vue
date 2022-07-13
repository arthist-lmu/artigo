<template>
  <v-row
    :class="message.from"
    justify="start"
  >
    <v-col
      class="pr-0"
      cols="auto"
    >
      <v-avatar
        :class="hideAvatar ? 'hide' : undefined"
        color="grey lighten-4"
        size="32"
      >
        <v-icon
          color="grey darken-4"
          small
        >
          mdi-account-outline
        </v-icon>
      </v-avatar>
    </v-col>

    <v-col cols="auto">
      <v-chip
        :class="blurContent ? 'blur' : undefined"
        color="grey lighten-4"
      >
        {{ message.text }}
      </v-chip>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    message: Object,
    hideAvatar: {
      type: Boolean,
      default: false,
    },
    blurContent: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
