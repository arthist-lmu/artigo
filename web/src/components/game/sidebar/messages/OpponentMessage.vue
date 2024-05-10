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
        color="surface"
        size="32"
      >
        <v-icon size="small">
          mdi-account-outline
        </v-icon>
      </v-avatar>
    </v-col>

    <v-col cols="auto">
      <v-chip
        :class="blurContent ? 'blur' : undefined"
        color="surface"
        variant="flat"
      >
        {{ message.text }}
      </v-chip>
    </v-col>
  </v-row>
</template>

<script setup>
defineProps({
  message: {
    type: Object,
    default: null
  },
  hideAvatar: {
    type: Boolean,
    default: false
  },
  blurContent: {
    type: Boolean,
    default: false
  }
})
</script>
