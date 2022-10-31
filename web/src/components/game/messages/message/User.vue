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
        <v-chip color="primary">
          {{ message.text }}
        </v-chip>
      </v-col>

      <v-col
        v-else
        cols="9"
      >
        <v-card
          color="primary"
          dark
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
                  small
                  left
                >
                  mdi-check-all
                </v-icon>

                {{ $tc('game.fields.basic.score', message.score) }}
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
          @click="post(name)"
          class="mr-1 mb-1"
          color="primary"
          outlined
          small
        >
          {{ name }}
        </v-chip>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  props: {
    entry: Object,
    message: Object,
  },
  methods: {
    post(name) {
      const params = {
        tag: { name, suggested: true },
        language: this.$i18n.locale,
        resource_id: this.entry.resource_id,
      };
      this.$store.dispatch('game/post', params);
    },
  },
};
</script>
