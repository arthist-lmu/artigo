<template>
  <div></div>
</template>

<script>
import tool from '@/mixins/game/messages/data';

export default {
  name: 'OpponentTool',
  mixins: [tool],
  data() {
    return {
      name: 'opponent',
    };
  },
  computed: {
    tags() {
      return this.entry.opponent_tags;
    },
    filter() {
      if (this.isArray(this.tags)) {
        return this.tags.filter((tag) => (
          tag.created_after <= this.seconds
        ));
      }
      return [];
    },
  },
};
</script>
