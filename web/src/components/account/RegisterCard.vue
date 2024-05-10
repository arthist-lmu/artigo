<template>
  <CardBase
    :title="$t('user.register.title')"
    theme="light"
    @close="close"
  >
    <v-form
      v-model="isFormValid"
      @submit.prevent="register"
    >
      <v-text-field
        v-model="username"
        :placeholder="$t('user.fields.username')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="register"
      />

      <v-text-field
        v-model="email"
        class="mt-2"
        :placeholder="$t('user.fields.email')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="register"
      />

      <v-text-field
        v-model="password1"
        class="mt-2"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="$t('user.fields.password')"
        :rules="[rules.length]"
        :append-inner-icon="showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
        clear-icon="mdi-close"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="register"
        @click:append-inner="showPassword = !showPassword"
      />

      <v-text-field
        v-model="password2"
        class="mt-2"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="$t('user.fields.passwordRepeat')"
        :rules="[rules.length, rules.repeat]"
        :append-inner-icon="showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @keydown.enter="register"
        @click:append-inner="showPassword = !showPassword"
      />

      <v-checkbox
        v-model="privacyPolicy"
        :rules="[rules.required]"
        true-icon="mdi-check-circle-outline"
        false-icon="mdi-checkbox-blank-circle-outline"
        tabindex="0"
        color="primary"
        density="compact"
        hide-details
      >
        <template #label>
          <v-btn
            href="https://www.kunstgeschichte.uni-muenchen.de/funktionen/datenschutz/index.html"
            target="_blank"
            rel="noopener noreferrer"
            variant="plain"
            density="comfortable"
            @click.stop
          >
            {{ $t('user.fields.privacyPolicy') }}
          </v-btn>
        </template>
      </v-checkbox>
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
            @click="register"
          >
            {{ $t("user.register.title") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </CardBase>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'
import CardBase from '@/components/utils/CardBase.vue'

const store = useStore()
const { t } = useI18n()

const username = defineModel('username', { type: String })
const email = defineModel('email', { type: String })
const password1 = defineModel('password1', { type: String })
const password2 = defineModel('password2', { type: String })
const privacyPolicy = defineModel('privacyPolicy', { type: String })
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
  },
  repeat: (v) => {
    if (v && v === password1.value) {
      return true
    }
    return t('rules.password-repeat')
  },
  required: (v) => {
    if (v) {
      return true
    }
    return t('field.required')
  }
}

const isFormValid = defineModel('isFormValid', {
  type: Boolean,
  default: false
})
function register() {
  if (isFormValid.value) {
    store.dispatch('user/register', {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value
    })
  }
}

const props = defineProps({
  isDialog: {
    type: Boolean,
    default: true
  }
})
const emit = defineEmits(['close'])
function close() {
  emit('close')
}
import useStatus from '@/composables/useStatus'
const { isUpdated, isSuccessful } = useStatus()
import goTo from '@/composables/useGoTo'
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
