<template>
  <v-hover
    v-if="!isDisabled"
    v-slot="{ props: activatorProps }"
  >
    <div
      v-bind="activatorProps"
      class="grid-item"
      :disabled="isDisabled ? true : undefined"
      @click="goTo('session')"
      @keyDown="goTo('session')"
    >
      <img
        :src="item.path"
        alt=""
        @error="onError"
      >

      <v-container class="overlay">
        <v-row style="flex: 0;">
          <v-col class="pa-4">
            <div class="text-subtitle-1 white--text">
              <b>{{ itemDate }}</b>
            </div>

            <div class="text-caption">
              <v-icon
                class="mr-1"
                color="white"
                size="x-small"
              >
                mdi-clock-outline
              </v-icon>

              <span>{{ itemTime }}</span>
            </div>
          </v-col>
        </v-row>

        <v-row />

        <v-row style="flex: 0;">
          <v-col
            class="pa-4"
            align="right"
          >
            <v-btn
              color="primary"
              rounded
              flat
            >
              <v-icon class="mr-2">
                mdi-tag-outline
              </v-icon>

              {{ item.annotations }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-hover>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import i18n from '@/plugins/i18n'
import useResource from '@/composables/useResource'

const router = useRouter()
const { locale } = i18n.global

const props = defineProps({
  item: {
    type: Object,
    default: null,
    required: true
  },
  height: {
    type: String,
    default: '225'
  }
})

const {
  isDisabled,
  onError
} = useResource(props.item)

function goTo(name) {
  router.push({
    name,
    params: {
      id: props.item.id
    }
  })
}

const itemDate = computed(() => {
  const created = new Date(props.item.created)
  return created.toLocaleDateString(locale.value)
})
const itemTime = computed(() => {
  const created = new Date(props.item.created)
  return created.toLocaleTimeString(locale.value)
})
</script>

<style scoped>
.v-container {
  position: absolute;
  flex-direction: column;
  display: flex;
  width: 100%;
  height: 100%;
  bottom: 0;
  left: 0;
}

.v-container .overlay {
  background: linear-gradient(to bottom, black, #0000 40%);
  transform: translate(-50%, -50%);
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #fff;
  height: 100%;
  left: 50%;
  top: 50%;
}

.v-container .overlay .v-col > * {
  text-overflow: ellipsis;
  line-height: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}
</style>
