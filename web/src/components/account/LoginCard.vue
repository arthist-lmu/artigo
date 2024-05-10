<template>
  <CardBase
    :title="$t('user.login.title')"
    :is-dialog="isDialog"
    theme="light"
    @close="close"
  >
    <p class="pb-4 text-body-2 text-grey-darken-1">
      {{ $t('user.login.note') }}
    </p>

    <v-form
      v-model="isFormValid"
      @submit.prevent="login"
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
        @keydown.enter="login"
      />

      <v-text-field
        v-model="password"
        class="mt-2"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="$t('user.fields.password')"
        :rules="[rules.length]"
        :append-inner-icon="showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        border="md"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="login"
        @click:append-inner="showPassword = !showPassword"
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
            @click="login"
          >
            {{ $t("user.login.title") }}
          </v-btn>

          <v-dialog max-width="400">
            <template #activator="{ props: activatorProps }">
              <v-btn
                v-bind="activatorProps"
                class="mt-2 ml-0"
                tabindex="0"
                variant="plain"
                size="small"
                rounded
                block
              >
                {{ $t("user.password-reset.title") }}
              </v-btn>
            </template>

            <template #default="{ isActive }">
              <PasswordResetCard @close="isActive.value = false" />
            </template>
          </v-dialog>
        </v-col>
      </v-row>
    </template>
  </CardBase>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'
import goTo from '@/composables/useGoTo'
import useStatus from '@/composables/useStatus'
import CardBase from '@/components/utils/CardBase.vue'
import PasswordResetCard from '@/components/account/PasswordResetCard.vue'

const store = useStore()
const { t } = useI18n()

const email = defineModel('email', { type: String })
const password = defineModel('password', { type: String })
const showPassword = ref(false)
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

const isFormValid = defineModel('isFormValid', {
  type: Boolean,
  default: false
})
function login() {
  if (isFormValid.value) {
    store.dispatch('user/login', {
      email: email.value,
      password: password.value
    })
  }
}

const emit = defineEmits(['close'])
function close() {
  emit('close')
}

const props = defineProps({
  isDialog: {
    type: Boolean,
    default: true
  }
})
const { isUpdated, isSuccessful } = useStatus()
watch(isUpdated, () => {
  if (isFormValid.value && isSuccessful.value) {
    if (props.isDialog) {
      close()
    } else {
      goTo('home')
    }
  }
})
</script>
