<template>
  <v-dialog
    v-model="showDialog"
    :retain-focus="false"
    max-width="625"
    scrollable
    persistent
  >
    <SelectCard
      v-model="showDialog"
      :default-params="defaultParams"
    />
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import SelectCard from './SelectCard.vue'

const store = useStore()

const defaultParams = computed(() => store.state.game.dialog.params)

const emit = defineEmits(['update:modelValue'])
const showDialog = ref(false)
watch(showDialog, (value) => {
  if (!value) {
    store.commit('game/updateDialog', { params: {} })
  }
  emit('update:modelValue', value)
})

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})
watch(() => props.modelValue, (value) => {
  showDialog.value = value
}, { immediate: true })
</script>
