<template>
  <div></div>
</template>

<script>
import tool from '@/mixins/game/messages/data';

export default {
  name: 'DefaultTool',
  mixins: [tool],
  data() {
    return {
      name: 'default',
      tags: [],
    };
  },
  computed: {
    gameType() {
      return this.params.game_type;
    },
    tabooTags() {
      if (this.keyInObj('taboo_tags', this.entry)) {
        return this.entry.taboo_tags.map(({ name }) => name);
      }
      return [];
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
  created() {
    this.tags.push({
      name: this.$t(
        `game.fields.${this.gameType}.intro`,
      ),
      created_after: 0,
    });
    if (this.tabooTags.length) {
      this.tags.push({
        name: this.$t(
          `game.fields.${this.gameType}.taboo`,
          { tags: this.tabooTags.join(', ') },
        ),
        created_after: 0,
        highlight: 1,
      });
    }
    const { game_round_duration: duration } = this.params;
    [0.5, 0.9].forEach((p) => {
      this.tags.push({
        name: this.$t(
          'game.fields.basic.seconds-left',
          { n: Math.floor((1 - p) * duration) },
        ),
        created_after: p * duration,
      });
    });
  },
};
</script>
