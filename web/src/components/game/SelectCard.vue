<template>
  <v-card
    max-width="625"
    flat
  >
    <v-card-title>
      {{ $t("game.fields.new-game") }}

      <v-col
        class="pa-0"
        align="right"
      >
        <v-btn
          @click="extend"
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

        <v-btn
          v-if="!persistent"
          @click="close"
          icon
        >
          <v-icon>mdi-close</v-icon>
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
    persistent: {
      type: Boolean,
      default: false,
    },
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
    extend() {
      this.showMore = !this.showMore;
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
