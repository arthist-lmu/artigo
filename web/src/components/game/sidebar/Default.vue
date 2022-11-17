<template>
  <v-container>
    <v-row>
      <v-col class="text-center">
        <span class="text-caption grey--text">
          {{ $t("game.fields.basic.rounds", { i: roundId, total: rounds }) }}
        </span>

        <v-btn
          v-if="roundId <= rounds"
          @click="next"
          :title="$t('game.fields.basic.skip')"
          class="ml-2"
          color="grey"
          x-small
          icon
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-row
      ref="container"
      class="mb-0 align-end"
    >
      <v-col class="pt-0">
        <slot name="messages">
          <Messages
            v-bind="$props"
            @update="scroll"
          />
        </slot>
      </v-col>
    </v-row>

    <slot name="append-item"></slot>
  </v-container>
</template>

<script>
import { mapState } from 'vuex';

export default {
  props: {
    entry: Object,
    params: Object,
    seconds: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      focus: false,
    };
  },
  methods: {
    next() {
      this.$emit('next');
    },
    scroll() {
      this.$nextTick(() => {
        const { scrollHeight } = this.$refs.container;
        this.$refs.container.scrollTop = scrollHeight;
        this.focusInput();
      });
    },
    onBlur() {
      this.$nextTick(() => {
        this.focusInput();
      });
    },
    blurInput() {
      if (this.$refs.input !== undefined) {
        this.$refs.input.blur();
      }
    },
    focusInput() {
      window.setTimeout(() => {
        if (this.$refs.input !== undefined) {
          this.$refs.input.focus();
        }
      }, 0);
    },
  },
  computed: {
    ...mapState('game', [
      'roundId',
      'rounds',
    ]),
  },
  watch: {
    focus(value) {
      this.$store.commit('game/updateInput', { focus: value });
    },
  },
  components: {
    Messages: () => import('@/components/game/messages/Default.vue'),
  },
};
</script>

<style scoped>
.container {
  flex-direction: column;
  display: flex;
}

.row:not(.align-end) {
  flex: 0;
}

.row.align-end {
  overflow-y: auto;
  margin-right: 0;
  height: 0;
}
</style>
