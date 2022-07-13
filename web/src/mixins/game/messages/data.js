export default {
  props: {
    entry: {
      type: Object,
      required: false,
    },
    params: {
      type: Object,
      required: false,
    },
    seconds: {
      type: Number,
      required: false,
    },
  },
  computed: {
    filter() {
      if (this.isArray(this.tags)) {
        return [...this.tags];
      }
      return [];
    },
  },
  watch: {
    filter(newTags, oldTags) {
      const n = newTags.length - oldTags.length;
      if (n > 0) {
        newTags.slice(-n).forEach((tag) => {
          const message = {
            from: this.name,
            text: null,
            score: 0,
            valid: true,
          };
          if (this.keyInObj('name', tag)) {
            message.text = tag.name;
          }
          if (this.keyInObj('score', tag)) {
            message.score = tag.score;
          }
          if (this.keyInObj('valid', tag)) {
            message.valid = tag.valid;
          }
          this.$emit('add', message);
        });
      }
    },
  },
};
