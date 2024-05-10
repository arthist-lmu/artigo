<template>
  <v-row
    :id="message.highlight ? `highlight-${message.highlight}` : undefined"
    :class="message.from"
    justify="start"
  >
    <v-col>
      <v-card
        color="surface"
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

<script setup>
defineProps({
  message: {
    type: Object,
    default: null
  }
})
</script>
