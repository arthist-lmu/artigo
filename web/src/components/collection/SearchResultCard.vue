<template>
  <v-hover
    v-if="!isDisabled"
    v-slot="{ isHovering, props: activatorProps }"
  >
    <v-card
      v-bind="activatorProps"
      class="grid-item"
      :disabled="isDisabled ? true : undefined"
      flat
      @click="play"
      @keydown="play"
    >
      <img
        :src="item.path"
        alt=""
        @error="onError"
      >

      <v-fade-transition>
        <v-container v-if="isHovering && item.status === 'F'">
          <v-row
            justify="center"
            align="center"
          >
            <v-col cols="auto">
              <v-btn
                color="primary"
                icon="mdi-play"
                large
                fab
              />
            </v-col>
          </v-row>
        </v-container>
      </v-fade-transition>

      <v-container class="overlay">
        <v-row style="flex: 0;">
          <v-col
            cols="9"
            class="pa-4"
          >
            <div class="text-subtitle-1 white--text">
              <b :title="item.title[locale]">
                {{ item.title[locale] }}
              </b>

              <v-icon
                v-if="item.access === 'O'"
                :title="$t('collections.fields.accessOpen')"
                class="ml-2 mb-1"
                color="white"
                size="small"
              >
                mdi-lock-open-variant-outline
              </v-icon>

              <v-icon
                v-if="item.access === 'P'"
                :title="$t('collections.fields.accessPending')"
                class="ml-2 mb-1"
                color="white"
                size="small"
              >
                mdi-progress-pencil
              </v-icon>

              <v-icon
                v-if="item.access === 'R'"
                :title="$t('collections.fields.accessRestricted')"
                class="ml-2 mb-1"
                color="white"
                size="small"
              >
                mdi-lock-outline
              </v-icon>
            </div>

            <div class="text-caption">
              <v-icon
                class="mr-1"
                color="white"
                size="x-small"
              >
                mdi-clock-outline
              </v-icon>

              <span>{{ itemDate }}</span>
            </div>
          </v-col>

          <v-col
            cols="3"
            align="right"
          >
            <v-menu @click.stop.prevent>
              <template #activator="{ props: activatorPropsMenu }">
                <v-btn
                  v-bind="activatorPropsMenu"
                  color="white"
                  variant="text"
                  density="comfortable"
                  icon="mdi-dots-vertical"
                />
              </template>

              <v-list>
                <v-dialog max-width="400">
                  <template #activator="{ props: activatorPropsChange }">
                    <v-list-item v-bind="activatorPropsChange">
                      <v-list-item-title>
                        {{ $t('collections.fields.change') }}
                      </v-list-item-title>
                    </v-list-item>
                  </template>

                  <template #default="{ isActive }">
                    <ChangeConfirmCard
                      :item="item"
                      @close="isActive.value = false"
                    />
                  </template>
                </v-dialog>

                <v-dialog max-width="400">
                  <template #activator="{ props: activatorPropsRemove }">
                    <v-list-item v-bind="activatorPropsRemove">
                      <v-list-item-title>
                        {{ $t('collections.fields.remove') }}
                      </v-list-item-title>
                    </v-list-item>
                  </template>

                  <template #default="{ isActive }">
                    <RemoveConfirmCard
                      :item="item"
                      @close="isActive.value = false"
                    />
                  </template>
                </v-dialog>
              </v-list>
            </v-menu>
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
              @click.stop=""
            >
              <v-icon class="mr-2">
                mdi-file-image-outline
              </v-icon>

              {{ item.resources.length }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-hover>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import i18n from '@/plugins/i18n'
import useResource from '@/composables/useResource'
import ChangeConfirmCard from '@/components/collection/ChangeConfirmCard.vue'
import RemoveConfirmCard from '@/components/collection/RemoveConfirmCard.vue'

const router = useRouter()
const store = useStore()
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

function play() {
  const params = {
    resource_inputs: this.entry.resources,
    resource_type: 'custom_resource',
    resource_max_last_played: 0,
    resource_min_tags: 0
  }
  store.commit('game/updateDialog', { params })
  router.push({ name: 'game' })
}

const itemDate = computed(() => {
  const created = new Date(props.item.created)
  return created.toLocaleDateString(locale.value)
})

watch(() => props.item.status, (value) => {
  if (value === 'F') {
    isDisabled.value = false
  } else {
    isDisabled.value = true
  }
}, { immediate: true })
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
