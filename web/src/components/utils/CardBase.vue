<template>
  <v-card
    max-width="900"
    variant="flat"
  >
    <template
      v-if="title"
      #title
    >
      {{ title }}
    </template>

    <template
      v-if="title"
      #append
    >
      <slot name="helper" />

      <v-btn
        v-if="isDialog"
        variant="text"
        density="comfortable"
        icon="mdi-close"
        @click="close"
      />
    </template>

    <v-card-text
      v-if="$slots.default"
      :class="[isDialog ? undefined : 'px-6']"
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

<script setup>
defineProps({
  title: {
    type: String,
    default: null
  },
  isDialog: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])
function close() {
  emit('close')
}
</script>

<style scope>
.v-card-item + .v-card-text {
  padding-top: 1rem !important;
}
</style>
