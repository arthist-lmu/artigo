<template>
  <v-menu
    v-model="showMenu"
    class="account"
    min-width="275"
    max-width="425"
  >
    <template #activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        class="ml-2"
        color="primary"
        density="comfortable"
        icon="mdi-account-circle-outline"
      />
    </template>

    <v-list
      density="compact"
      theme="light"
    >
      <template v-if="!isUserAnonymous">
        <v-list-item>
          <v-list-item-content class="justify-center px-4 py-6">
            <div class="mx-auto text-center">
              <v-avatar color="error">
                <span class="text-h5">
                  {{ userInitials }}
                </span>
              </v-avatar>

              <p class="text-caption mt-2">
                {{ userData.email }}
              </p>

              <p class="text-caption mt-0">
                <i>{{ userJoined }}</i>
              </p>
            </div>
          </v-list-item-content>
        </v-list-item>

        <v-divider />
      </template>

      <template v-if="isUserAnonymous && mobile">
        <v-dialog
          max-width="450"
          scrollable
        >
          <template #activator="{ props: activatorProps }">
            <v-list-item v-bind="activatorProps">
              <v-list-item-content>
                {{ $t("user.register.title") }}
              </v-list-item-content>
            </v-list-item>
          </template>

          <template #default="{ isActive }">
            <RegisterCard @close="isActive.value = false" />
          </template>
        </v-dialog>

        <v-dialog
          max-width="450"
          scrollable
        >
          <template #activator="{ props: activatorProps }">
            <v-list-item v-bind="activatorProps">
              <v-list-item-content>
                {{ $t("user.login.title") }}
              </v-list-item-content>
            </v-list-item>
          </template>

          <template #default="{ isActive }">
            <LoginCard @close="isActive.value = false" />
          </template>
        </v-dialog>
      </template>

      <v-list-item
        v-if="userData.n_gamesessions > 0"
        @click="goTo('sessions')"
      >
        <v-list-item-content>
          {{ $t("sessions.title") }}
        </v-list-item-content>

        <template #append>
          <v-chip
            class="ml-2"
            border="secondary md opacity-100"
            color="secondary"
            variant="outlined"
            size="small"
          >
            <span class="text-primary-darken-1">
              {{ userData.n_gamesessions }}
            </span>
          </v-chip>
        </template>
      </v-list-item>

      <template v-if="!isUserAnonymous">
        <v-list-item @click="goTo('collections')">
          <v-list-item-content>
            {{ $t("collections.title") }}
          </v-list-item-content>

          <template #append>
            <v-dialog
              max-width="450"
              scrollable
            >
              <template #activator="{ props: activatorProps }">
                <v-icon
                  v-bind="activatorProps"
                  :title="$t('user.upload.title')"
                  color="primary"
                  class="ml-2"
                >
                  mdi-cloud-upload-outline
                </v-icon>
              </template>

              <template #default="{ isActive }">
                <CollectionUploadCard @close="isActive.value = false" />
              </template>
            </v-dialog>

            <v-chip
              v-if="userData.n_collections > 0"
              class="ml-2"
              border="secondary md opacity-100"
              color="secondary"
              variant="outlined"
              size="small"
            >
              <span class="text-primary-darken-1">
                {{ userData.n_collections }}
              </span>
            </v-chip>
          </template>
        </v-list-item>

        <v-list-item @click="logout">
          <v-list-item-content>
            {{ $t("user.logout.title") }}
          </v-list-item-content>
        </v-list-item>
      </template>

      <v-dialog
        max-width="450"
        scrollable
      >
        <template #activator="{ props: activatorProps }">
          <v-list-item v-bind="activatorProps">
            <v-list-item-content>
              {{ $t("user.score.title") }}
            </v-list-item-content>
          </v-list-item>
        </template>

        <template #default="{ isActive }">
          <ScoreCard @close="isActive.value = false" />
        </template>
      </v-dialog>

      <v-divider />

      <LanguageMenu />
    </v-list>
  </v-menu>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'
import { useDisplay } from 'vuetify'
import goTo from '@/composables/useGoTo'
import keyInObj from '@/composables/useKeyInObj'
import ScoreCard from '@/components/account/ScoreCard.vue'
import LoginCard from '@/components/account/LoginCard.vue'
import LanguageMenu from '@/components/menu/LanguageMenu.vue'
import RegisterCard from '@/components/account/RegisterCard.vue'
import CollectionUploadCard from '@/components/collection/UploadCard.vue'

const store = useStore()
const { t } = useI18n()
const { mobile } = useDisplay()

function logout() {
  store.dispatch('user/logout').then(() => {
    goTo('home');
  });
}

const isUserAnonymous = computed(() => store.state.user.isAnonymous)

const userData = computed(() => store.state.user.data)
const userJoined = computed(() => {
  const diff = new Date() - new Date(userData.value.date_joined)
  const nDays = Math.round(diff / (1000 * 60 * 60 * 24))
  return t('user.menu.joined', nDays)
})
const userInitials = computed(() => {
  if (keyInObj('username', userData.value)) {
    return userData.value.username.slice(0, 2)
  }
  if (keyInObj('email', userData.value)) {
    return userData.value.email.slice(0, 2)
  }
  return ''
})

const showMenu = defineModel('showMenu', { type: Boolean })
watch(showMenu, (value) => {
  if (value) {
    store.dispatch('user/get')
  }
})
</script>

<style>
.v-overlay.account > div {
  min-width: 275px !important;
}

.v-overlay.account .v-list {
  background-color: #fff; 
}
</style>
