<template>
  <div></div>
</template>

<script>
import tool from '@/mixins/game/messages/data';

export default {
  name: 'UserTool',
  mixins: [tool],
  data() {
    return {
      name: 'user',
    };
  },
  computed: {
    tags() {
      return this.$store.state.game.tags;
    },
  },
};
</script>
