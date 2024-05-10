<template>
  <v-app-bar
    v-if="isVisible"
    class="py-2 px-4"
    style="position: fixed;"
    order="1"
    flat
  >
    <v-container
      :class="{ opaque: opaque }"
      class="py-1 px-4"
    >
      <v-row>
        <v-col
          style="position: relative;"
          cols="6"
          align-self="center"
        >
          <LogoTemplate />
        </v-col>

        <v-col
          cols="6"
          align-self="center"
          align="right"
        >
          <DefaultMenu v-if="!mobile" />

          <v-btn
            v-if="!hideSearchBar"
            :title="$t('search.title')"
            class="ml-2"
            color="primary"
            density="comfortable"
            icon="mdi-magnify"
            @click="goTo('search')"
          />

          <AccountMenu />
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import goTo from '@/composables/useGoTo'
import LogoTemplate from '@/components/LogoTemplate.vue'
import DefaultMenu from '@/components/menu/DefaultMenu.vue'
import AccountMenu from '@/components/menu/AccountMenu.vue'

const route = useRoute()
const store = useStore()

defineProps({
  opaque: {
    type: Boolean,
    default: false
  },
  hideSearchBar: {
    type: Boolean,
    default: false
  }
})

const { mobile, smAndUp } = useDisplay()
const isVisible = computed(() => {
  if (
    route.name !== 'game'
    || smAndUp
  ) {
    return true
  }
  return store.state.game.input.focus
})

const emit = defineEmits(['mounted'])
onMounted(() => emit('mounted'))
</script>

<style scoped>
.v-toolbar .v-container {
  z-index: 99;
  transition: opacity .5s ease-out;
}

.v-toolbar .v-container.opaque {
  opacity: 0.25;
}

.v-toolbar .v-container:hover {
  opacity: 1;
}
</style>
