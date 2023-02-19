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

        <v-btn
          @click="finish"
          :title="$t('game.fields.basic.finish')"
          color="grey"
          x-small
          icon
        >
          <v-icon>mdi-page-last</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-row v-if="highlights && highlights.length">
      <v-col class="pt-0">
        <transition-group name="fade">
          <template v-for="(message, i) in highlights">
            <DefaultMessage
              v-if="message.from === 'default'"
              :key="i"
              :message="message"
            />
          </template>
        </transition-group>
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

    <slot name="append-item" />
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
      scrollTop: 0,
      highlights: [],
    };
  },
  methods: {
    next() {
      this.$emit('next');
    },
    finish() {
      this.$emit('finish');
    },
    scroll({ from, messages }) {
      // only scroll down if the user has not scrolled up
      const { scrollHeight, scrollTop } = this.$refs.container;
      if (from === 'user' || scrollTop + 50 >= this.scrollTop) {
        this.$nextTick(() => {
          this.$refs.container.scrollTop = scrollHeight;
          this.scrollTop = this.$refs.container.scrollTop;
          this.focusInput();
        });
      }
      // highlight messages that are outside the viewport
      const element = this.$refs.container.querySelector('.highlight');
      if (element !== undefined && element !== null) {
        const { bottom } = element.getBoundingClientRect();
        const { top } = this.$refs.container.getBoundingClientRect();
        console.log(bottom, top);
        if (bottom - 25 <= top) {
          const texts = this.highlights.map(({ text }) => text);
          messages.forEach((message) => {
            if (texts.indexOf(message.text) === -1) {
              this.highlights.push(message);
            }
          });
        }
      }
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
    DefaultMessage: () => import('@/components/game/messages/message/Default.vue'),
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

.fade-enter-active,
.fade-leave-active {
  transition: all 1s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
