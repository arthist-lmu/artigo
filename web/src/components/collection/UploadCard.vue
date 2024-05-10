<template>
  <CardBase
    v-model="card"
    :title="$t('user.upload.title')"
    theme="light"
    @close="close"
  >
    <p class="pb-4 text-body-2 text-grey-darken-1">
      {{ $t('user.upload.note') }}
    </p>

    <v-form
      v-model="isFormValid"
      @submit.prevent="upload"
    >
      <v-text-field
        v-model="collection.title.de"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        border="md"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="upload"
      >
        <template #append>
          <span>DE</span>
        </template>
      </v-text-field>

      <v-text-field
        v-model="collection.title.en"
        class="mt-2"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        border="md"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="upload"
      >
        <template #append>
          <span>EN</span>
        </template>
      </v-text-field>

      <UploadInput
        v-model="collection.files"
        class="mt-2"
        :rules="[rules.fileSize]"
      />
    </v-form>

    <template #helper>
      <v-btn
        :title="$t('user.upload.helper')"
        variant="text"
        density="comfortable"
        icon="mdi-help-circle-outline"
        @click="goTo('about', '#collections')"
      />
    </template>

    <template #actions>
      <v-row>
        <v-col>
          <v-btn
            :disabled="!isFormValid"
            type="submit"
            tabindex="0"
            class="bg-primary"
            rounded
            block
            @click="upload"
          >
            {{ $t("user.upload.title") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </CardBase>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'
import useStatus from '@/composables/useStatus'
import CardBase from '@/components/utils/CardBase.vue'
import UploadInput from '@/components/collection/UploadInput.vue'

const router = useRouter()
const store = useStore()
const { t } = useI18n()

const collection = ref({
  title: {
    de: null,
    en: null
  },
  files: []
})
const rules = {
  length: (v) => {
    if (v) {
      if (v.length < 4) {
        return t('rules.min', 4)
      }
      if (v.length > 75) {
        return t('rules.max', 75)
      }
      return true
    }
    return t('field.required')
  },
  fileSize(files) {
    if (files && files.length) {
      for (const file of files) {
        if (file.size >= (50 * 1024 * 1024)) {
          return t('rules.file-size', 50)
        }
      }
      return true
    }
    return t('field.required')
  }
}

const isFormValid = defineModel('isFormValid', {
  type: Boolean,
  default: false
})
function upload() {
  if (isFormValid.value) {
    console.log(collection)
    store.dispatch('collection/add', collection)
  }
}

function goTo(name, anchor = '') {
  window.open(`${router.resolve({ name }).href}${anchor}`, '_blank')
  close()
}

const emit = defineEmits(['close'])
function close() {
  emit('close')
}

const card = defineModel('card', {
  type: Boolean,
  default: false
})
watch(card, (value) => {
  if (!value) {
    store.dispatch('collections/post', {})
  }
})

const props = defineProps({
  isDialog: {
    type: Boolean,
    default: true
  }
})
const { isUpdated, isSuccessful } = useStatus()
watch(isUpdated, () => {
  if (isFormValid.value && isSuccessful.value) {
    router.push({ name: 'collections' })
    if (props.isDialog) {
      close()
    }
  }
})
</script>
