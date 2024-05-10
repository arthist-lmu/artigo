<template>
  <v-card>
    <template #title>
      {{ $t("game.fields.newGameDefault") }}
    </template>

    <template #append>
      <v-btn
        :title="$t('about.title')"
        density="comfortable"
        icon="mdi-help-circle-outline"
        variant="text"
        @click="goTo('about', openInNewTab = true)"
      />
    </template>
    
    <template #text>
      <p
        v-if="Object.keys(defaultParams).length"
        class="pb-4 text-body-2 text-grey-darken-1"
      >
        {{ $t('game.note') }}
      </p>

      <SelectStepper
        v-model="params"
        :show-more="showMore"
        :default-params="defaultParams"
      />

      <v-row
        v-if="!showMore"
        justify="center"
        no-gutters
      >
        <v-col cols="auto">
          <v-btn
            density="comfortable"
            icon="mdi-plus-circle-outline"
            variant="text"
            @click="showMore = true;"
          />
        </v-col>
      </v-row>
    </template>

    <v-card-actions class="pb-6 px-6">
      <v-btn
        tabindex="0"
        class="bg-primary"
        rounded
        block
        @click="play"
      >
        {{ $t("game.title") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import goTo from '@/composables/useGoTo'
import SelectStepper from './SelectStepper.vue'

const router = useRouter()
const store = useStore()

const params = defineModel('params', {
  type: Object,
  default: {}
})
const showMore = ref(false)

defineProps({
  defaultParams: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])
function close() {
  emit('update:modelValue', false)
}

function play() {
  store.dispatch('game/get', params.value).then(() => {
    close()
    router.push({ name: 'game' })
  })
}
</script>
