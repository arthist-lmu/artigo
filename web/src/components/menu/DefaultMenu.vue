<template>
  <template v-if="isUserAnonymous">
    <v-dialog max-width="450">
      <template #activator="{ props: activatorProps }">
        <v-btn
          v-bind="activatorProps"
          class="ml-2"
          border="secondary md opacity-100"
          color="secondary"
          variant="outlined"
          rounded
        >
          <span class="text-primary-darken-1">
            {{ $t("user.login.title") }}
          </span>
        </v-btn>
      </template>

      <template #default="{ isActive }">
        <LoginCard @close="isActive.value = false" />
      </template>
    </v-dialog>

    <v-dialog max-width="450">
      <template #activator="{ props: activatorProps }">
        <v-btn
          v-bind="activatorProps"
          class="ml-2 bg-primary"
          rounded
          flat
        >
          {{ $t("user.register.title") }}
        </v-btn>
      </template>

      <template #default="{ isActive }">
        <RegisterCard @close="isActive.value = false" />
      </template>
    </v-dialog>
  </template>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import LoginCard from '@/components/account/LoginCard.vue'
import RegisterCard from '@/components/account/RegisterCard.vue'

const store = useStore()

const isUserAnonymous = computed(() => store.state.user.isAnonymous)
</script>
