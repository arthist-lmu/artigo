<template>
  <CardBase
    theme="light"
    @close="close"
  >
    <template #actions>
      <v-col cols="6">
        <v-btn
          tabindex="0"
          class="bg-primary"
          rounded
          block
          @click="remove"
        >
          {{ $t("collections.fields.remove") }}
        </v-btn>
      </v-col>

      <v-col cols="6">
        <v-btn
          tabindex="0"
          rounded
          block
          @click="close"
        >
          {{ $t("field.abort") }}
        </v-btn>
      </v-col>
    </template>
  </CardBase>
</template>

<script setup>
import { useStore } from 'vuex'
import CardBase from '@/components/utils/CardBase.vue'

const store = useStore()

const props = defineProps({
  item: {
    type: Object,
    default: null
  }
})

function remove() {
  const entry = { hash_id: props.item.hash_id }
  store.dispatch('collection/remove', entry).then(() => {
    store.dispatch('collections/post', {})
    close()
  })
}

const emit = defineEmits(['close'])
function close() {
  emit('close')
}
</script>
