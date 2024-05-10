<template>
  <v-snackbar
    v-if="messageDetails"
    v-model="showSnackbar"
    class="mb-5"
    timeout="5000"
    :color="messageType === 'error' ? 'error' : 'primary'"
    :dark="messageType !== 'error'"
    rounded
  >
    <span
      v-for="messageDetail in messageDetails"
      :key="messageDetail"
    >
      {{ $t(`messages.${messageDetail}`) ? $t(`messages.${messageDetail}`) : $t("messages.unknown_error") }}
    </span>
  </v-snackbar>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

import useStatus from '@/composables/useStatus'
const { isUpdated } = useStatus()
const showSnackbar = ref(false)
watch(isUpdated, () => {
  showSnackbar.value = true
})
watch(showSnackbar, () => {
  store.dispatch('utils/setMessage', {})
})

const messageDetails = computed(() => store.state.utils.message.details)
const messageType = computed(() => store.state.utils.message.type)
</script>
