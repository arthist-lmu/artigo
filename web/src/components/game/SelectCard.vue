<template>
  <v-card
    max-width="625"
    flat
  >
    <v-card-title v-if="isDialog">
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

    <v-card-text :class="isDialog ? 'pt-4' : 'pt-0 px-0'">
      <SelectStepper
        v-model="params"
        :showMore="showMore"
      />
    </v-card-text>

    <v-card-actions :class="isDialog ? 'pb-6 px-6' : 'pb-8 px-0'">
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
    isDialog: {
      type: Boolean,
      default: true,
    },
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
