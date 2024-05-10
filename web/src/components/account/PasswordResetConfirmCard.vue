<template>
  <CardBase
    :title="$t('user.password-reset.title')"
    theme="light"
    @close="close"
  >
    <v-form
      v-model="isFormValid"
      @submit.prevent="resetPassword"
    >
      <v-text-field
        v-model="newPassword1"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="$t('user.fields.new-password')"
        :rules="[rules.length]"
        clear-icon="mdi-close"
        :append-icon="showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @click:append="showPassword = !showPassword"
      />

      <v-text-field
        v-model="newPassword2"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="$t('user.fields.password-repeat')"
        :rules="[rules.length, rules.repeat]"
        clear-icon="mdi-close"
        :append-icon="showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
        tabindex="0"
        counter="75"
        variant="outlined"
        density="compact"
        clearable
        rounded
        @click:append="showPassword = !showPassword"
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
            {{ $t("user.password-reset.title") }}
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

const newPassword1 = defineModel('newPassword1', { type: String })
const newPassword2 = defineModel('newPassword2', { type: String })
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
    if (v && v === newPassword1.value) {
      return true;
    }
    return t('rules.password-repeat')
  }
}

const isFormValid = defineModel('isFormValid', {
  type: Boolean,
  default: false
})
function resetPassword() {
  if (isFormValid.value) {
    let path = this.$route.path.split('/')
    path = path.filter((item) => item)

    store.dispatch('user/resetPasswordConfirm', {
      uid: path[path.length - 2],
      token: path[path.length - 1],
      new_password1: newPassword1,
      new_password2: newPassword2
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
