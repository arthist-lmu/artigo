<template>
  <div>
    <v-row
      :class="message.from"
      justify="end"
    >
      <v-col
        v-if="message.score === 0"
        cols="auto"
      >
        <v-chip
          color="primary"
          variant="flat"
        >
          {{ message.text }}
        </v-chip>
      </v-col>

      <v-col
        v-else
        cols="9"
      >
        <v-card
          color="primary"
          flat
        >
          <v-card-text class="px-4 py-2">
            <v-row>
              <v-col
                class="pb-0"
                cols="auto"
              >
                {{ message.text }}
              </v-col>
            </v-row>

            <v-row
              class="mt-0 text-caption"
              justify="end"
            >
              <v-col
                class="pt-2"
                cols="auto"
              >
                <v-icon
                  class="mr-1"
                  size="small"
                >
                  mdi-check-all
                </v-icon>

                {{ $t('game.fields.basic.score', message.score) }}
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col
        v-if="!message.valid"
        class="pl-0"
        cols="auto"
      >
        <v-avatar
          :title="$t('game.fields.basic.invalid')"
          size="32"
        >
          <v-icon color="error">
            mdi-alert-circle-outline
          </v-icon>
        </v-avatar>
      </v-col>
    </v-row>

    <v-row
      v-if="message.suggest && message.suggest.length"
      :class="[message.from, 'mt-0']"
      justify="end"
    >
      <v-col
        cols="auto"
        class="pr-0"
      >
        <v-avatar
          :title="$t('game.fields.basic.suggest')"
          size="32"
        >
          <v-icon>
            mdi-lightbulb-variant-outline
          </v-icon>
        </v-avatar>
      </v-col>

      <v-col cols="9">
        <v-chip
          v-for="name in message.suggest"
          :key="name"
          class="mr-1 mb-1"
          color="primary"
          variant="outlined"
          size="small"
          @click="post(name)"
        >
          {{ name }}
        </v-chip>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'

const store = useStore()
const { locale } = i18n.global

const props = defineProps({
  entry: {
    type: Object,
    default: null
  },
  message: {
    type: Object,
    default: null
  }
})

function post(name) {
  const params = {
    tag: {
      name,
      suggested: true
    },
    language: locale.value,
    resource_id: props.entry.resource_id
  }
  store.dispatch('game/post', params)
}
</script>
