<template>
  <CardBase
    :title="$t('collections.fields.change')"
    :is-dialog="isDialog"
    theme="light"
    @close="close"
  >
    <p class="pb-4 text-body-2 text-grey-darken-1">
      {{ $t('collections.note') }}
    </p>

    <v-form
      v-model="isFormValid"
      @submit.prevent="change"
    >
      <v-text-field
        v-model="params.title.de"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="change"
      >
        <template #append>
          <span>DE</span>
        </template>
      </v-text-field>

      <v-text-field
        v-model="params.title.en"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        class="mt-2"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="change"
      >
        <template #append>
          <span>EN</span>
        </template>
      </v-text-field>

      <v-select
        v-model="params.access"
        :placeholder="$t('user.upload.fields.access')"
        :items="accessItems"
        item-title="name"
        item-value="value"
        class="mt-2"
        variant="outlined"
        density="compact"
        hide-details
        rounded
        @keydown.enter="change"
      />
    </v-form>

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
            @click="change"
          >
            {{ $t("collections.fields.change") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </CardBase>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'
import useStatus from '@/composables/useStatus'
import CardBase from '@/components/utils/CardBase.vue'

const store = useStore()
const { t } = useI18n()

const props = defineProps({
  item: {
    type: Object,
    default: null
  },
  isDialog: {
    type: Boolean,
    default: true
  }
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
  }
}

const accessItems = computed(() => {
  return [
    {
      name: t('collections.fields.accessOpen'),
      value: 'O'
    },
    {
      name: t('collections.fields.accessRestricted'),
      value: 'R'
    }
  ]
})

const isFormValid = defineModel('isFormValid', {
  type: Boolean,
  default: false
})
const params = ref({
  title: {
    de: null,
    en: null
  },
  access: null
})
function change() {
  if (isFormValid.value) {
    const entry = {
      hash_id: props.item.hash_id,
      ...params.value
    };
    store.dispatch('collection/change', entry)
  }
}
watch(() => props.item, (value) => {
  params.value = value
}, { immediate: true })

const emit = defineEmits(['close'])
function close() {
  emit('close')
}

const { isUpdated, isSuccessful } = useStatus()
watch(isUpdated, () => {
  store.dispatch('collections/post', {})
  if (isFormValid.value && isSuccessful.value) {
    if (props.isDialog) {
      close()
    }
  }
})
</script>
