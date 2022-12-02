<template>
  <v-card flat>
    <v-card-title>
      {{ $t("game.fields.new-game-default") }}

      <v-col
        class="pa-0"
        align="right"
      >
        <v-btn
          @click="showMore = !showMore;"
          :title="$t('game.fields.settings')"
          icon
        >
          <v-icon v-if="showMore">
            mdi-cog-off-outline
          </v-icon>
          <v-icon v-else>
            mdi-cog-outline
          </v-icon>
        </v-btn>
      </v-col>
    </v-card-title>

    <v-card-text class="pt-4">
      <SelectStepper
        v-model="params"
        :showMore="showMore"
        :defaultParams="defaultParams"
      />
    </v-card-text>

    <v-card-actions class="pb-6 px-6">
      <v-btn
        @click="play"
        tabindex="0"
        color="primary"
        depressed
        rounded
        block
      >
        {{ $t("game.title") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    defaultParams: Object,
  },
  data() {
    return {
      params: {},
      showMore: false,
    };
  },
  methods: {
    play() {
      this.$store.dispatch('game/get', this.params).then(() => {
        this.close();
        this.$router.push({ name: 'game' });
      });
    },
    close() {
      this.$emit('input', false);
    },
  },
  components: {
    SelectStepper: () => import('./SelectStepper.vue'),
  },
};
</script>
