<template>
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
              class="pt-1"
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
</template>

<script>
export default {
  props: {
    message: Object,
  },
};
</script>
