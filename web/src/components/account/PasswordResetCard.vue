<template>
  <CardBase
    :title="$t('user.passwordReset.title')"
    theme="light"
    @close="close"
  >
    <p class="pb-4 text-body-2 text-grey-darken-1">
      {{ $t('user.passwordReset.note') }}
    </p>

    <v-form
      v-model="isFormValid"
      @submit.prevent="resetPassword"
    >
      <v-text-field
        v-model="email"
        :placeholder="$t('user.fields.email')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        border="md"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="resetPassword"
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
            @click="resetPassword"
          >
            {{ $t("user.passwordReset.title") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </CardBase>
</template>

<script setup>
import { watch } from 'vue'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'
import { useI18n } from 'vue-i18n'
import CardBase from '@/components/utils/CardBase.vue'

const store = useStore()
const { t } = useI18n()
const { locale } = i18n.global

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

const email = defineModel('email', { type: String })
const isFormValid = defineModel('isFormValid', {
  type: Boolean,
  default: false
})
function resetPassword() {
  if (isFormValid.value) {
    store.dispatch('user/resetPassword', {
      email: email.value,
      lang: locale.value
    });
  }
}

const emit = defineEmits(['close'])
function close() {
  emit('close')
}
import useStatus from '@/composables/useStatus'
const { isUpdated, isSuccessful } = useStatus()
watch(isUpdated, () => {
  if (isSuccessful.value) {
    close()
  }
})
</script>
