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
          :hide-avatar="hideAvatar(i)"
          :blur-content="blurContent(i)"
        />
      </template>
    </transition-group>

    <v-row v-if="waiter">
      <v-col>
        <WaiterTemplate />
      </v-col>
    </v-row>

    <UserMessageData
      @add="add"
    />

    <DefaultMessageData
      :entry="entry"
      :params="params"
      :seconds="seconds"
      @add="add"
    />

    <OpponentMessageData
      :entry="entry"
      :seconds="seconds"
      @add="add"
    />
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import UserMessageData from './UserMessageData.vue'
import DefaultMessageData from './DefaultMessageData.vue'
import OpponentMessageData from './OpponentMessageData.vue'
import UserMessage from './UserMessage.vue'
import DefaultMessage from './DefaultMessage.vue'
import OpponentMessage from './OpponentMessage.vue'
import WaiterTemplate from './WaiterTemplate.vue'

const props = defineProps({
  entry: {
    type: Object,
    default: null
  },
  params: {
    type: Object,
    default: null
  },
  seconds: {
    type: Number,
    default: 0
  }
})

const waiter = ref(false)
const messages = ref([])

const emit = defineEmits(['update'])
function add(message) {
  const values = {
    from: message.from,
    messages: messages.value.filter(({ highlight }) => highlight)
  }
  if (message.from === 'user') {
    messages.value.push({
      timestamp: props.seconds,
      ...message
    })
    emit('update', values)
  } else {
    waiter.value = true
    emit('update', values)
    setTimeout(() => {
      nextTick(() => {
        waiter.value = false
        messages.value.push({
          timestamp: props.seconds,
          ...message
        })
        emit('update', values)
      })
    }, 750)
  }
}

function hideAvatar(index) {
  if (index > 0) {
    const froms = messages.value.map(({ from }) => from)
    if (froms[index] === froms[index - 1]) {
      return true
    }
  }
  return false
}

function blurContent(index) {
  if (index > 0) {
    const texts = messages.value.map(({ text }) => text)
    texts.splice(index, 1)
    if (texts.includes(messages.value[index].text)) {
      return false
    }
  }
  return true
}
</script>

<style>
.v-row.user + .v-row.user,
.v-row.default + .v-row.default,
.v-row.opponent + .v-row.opponent {
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
