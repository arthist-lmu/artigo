<template>
  <DefaultSidebar
    :entry="entry"
    :params="params"
    :seconds="seconds"
  >
    <template #append-item>
      <v-row style="flex: 0;">
        <v-col>
          <v-combobox
            ref="input"
            v-model="tagName"
            :placeholder="$t('game.fields.tagging.post')"
            append-icon=""
            tabindex="0"
            density="compact"
            bg-color="surface"
            variant="solo"
            hide-details
            rounded
            flat
            @blur="blurInput"
            @keyup.enter="post"
          >
            <template #append>
              <v-btn
                class="post"
                color="primary"
                density="comfortable"
                variant="text"
                icon="mdi-send"
                @click="onButton"
              />
            </template>
          </v-combobox>
        </v-col>
      </v-row>
    </template>
  </DefaultSidebar>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'
import useInput from '@/composables/useInput'
import DefaultSidebar from '@/components/game/sidebar/DefaultSidebar.vue'

const store = useStore()
const { locale } = i18n.global

const props = defineProps({
  entry: {
    type: Object,
    default: null
  },
  params: {
    type: Object,
    default: null
  },
  seconds: {
    type: Number,
    default: 0
  }
})

const input = ref()
const {
  blurInput,
  focusInput
} = useInput(input)

function onButton() {
  blurInput()
  nextTick(() => {
    post()
  })
}

const tagName = defineModel('tagName', { type: String })
function post() {
  if (tagName.value) {
    const params = {
      tag: { name: tagName.value },
      game_language: locale.value,
      resource_id: props.entry.resource_id
    }
    store.dispatch('game/post', params).then(() => {
      tagName.value = null
      focusInput()
    })
  } else {
    focusInput()
  }
}

nextTick(() => focusInput())
</script>

<style scoped>
.v-btn.post {
  transform: rotate(-45deg);
  transition: transform .3s ease-in-out !important;
}

.v-btn.post:hover {
  transform: rotate(0deg);
}

.v-field input {
  padding-left: 18px;
}
</style>
