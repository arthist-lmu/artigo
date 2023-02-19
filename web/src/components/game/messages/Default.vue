<template>
  <div>
    <transition-group name="fade">
      <template v-for="(message, i) in messages">
        <UserMessage
          v-if="message.from === 'user'"
          :key="i"
          :entry="entry"
          :message="message"
        />

        <DefaultMessage
          v-if="message.from === 'default'"
          :key="i"
          :message="message"
        />

        <OpponentMessage
          v-if="message.from === 'opponent'"
          :key="i"
          :message="message"
          :hideAvatar="hideAvatar(i)"
          :blurContent="blurContent(i)"
        />
      </template>
    </transition-group>

    <v-row v-if="waiter">
      <v-col>
        <Waiter />
      </v-col>
    </v-row>

    <UserData
      @add="add"
    />

    <DefaultData
      :entry="entry"
      :params="params"
      :seconds="seconds"
      @add="add"
    />

    <OpponentData
      :entry="entry"
      :seconds="seconds"
      @add="add"
    />
  </div>
</template>

<script>
export default {
  props: {
    entry: Object,
    params: Object,
    seconds: Number,
  },
  data() {
    return {
      waiter: false,
      messages: [],
    };
  },
  methods: {
    add(message) {
      const values = {
        from: message.from,
        messages: this.messages.filter(({ highlight }) => highlight),
      };
      if (message.from === 'user') {
        this.messages.push({
          timestamp: this.seconds,
          ...message,
        });
        this.$emit('update', values);
      } else {
        this.waiter = true;
        this.$emit('update', values);
        setTimeout(() => {
          this.$nextTick(() => {
            this.waiter = false;
            this.messages.push({
              timestamp: this.seconds,
              ...message,
            });
            this.$emit('update', values);
          });
        }, 750);
      }
    },
    hideAvatar(index) {
      if (index > 0) {
        const froms = this.messages.map(({ from }) => from);
        if (froms[index] === froms[index - 1]) {
          return true;
        }
      }
      return false;
    },
    blurContent(index) {
      if (index > 0) {
        const texts = this.messages.map(({ text }) => text);
        texts.splice(index, 1);
        if (texts.includes(this.messages[index].text)) {
          return false;
        }
      }
      return true;
    },
  },
  components: {
    UserData: () => import('./data/User.vue'),
    DefaultData: () => import('./data/Default.vue'),
    OpponentData: () => import('./data/Opponent.vue'),
    UserMessage: () => import('./message/User.vue'),
    DefaultMessage: () => import('./message/Default.vue'),
    OpponentMessage: () => import('./message/Opponent.vue'),
    Waiter: () => import('@/components/Waiter.vue'),
  },
};
</script>

<style>
.row.user + .row.user,
.row.default + .row.default,
.row.opponent + .row.opponent {
  margin-top: -16px;
}
</style>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 1s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
