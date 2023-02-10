<template>
  <v-card flat>
    <v-card-title>
      {{ $t("game.fields.new-game-default") }}

      <v-col
        class="pa-0"
        align="right"
      >
        <v-btn
          @click="goTo('about')"
          :title="$t('about.title')"
          icon
        >
          <v-icon>
            mdi-help-circle-outline
          </v-icon>
        </v-btn>
      </v-col>
    </v-card-title>

    <v-card-text class="my-4 pb-0">
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
      showMore: true,
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
    goTo(name) {
      const route = this.$router.resolve({ name });
      window.open(route.href, '_blank');
    },
  },
  components: {
    SelectStepper: () => import('./SelectStepper.vue'),
  },
};
</script>
