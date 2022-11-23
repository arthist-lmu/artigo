export default {
  props: {
    entry: {
      type: Object,
      required: true,
    },
    opaque: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isLoaded: false,
      isDisabled: false,
    };
  },
  methods: {
    onLoad() {
      this.isLoaded = true;
    },
    onError() {
      this.isDisabled = true;
      this.$emit('disabled', true);
    },
    showDialog() {
      this.$store.commit('resource/updateData', this.entry);
    },
  },
  computed: {
    title() {
      const titles = [];
      this.entry.meta.forEach(({ name, value_str }) => {
        if (name === 'titles' && value_str) {
          titles.push(value_str);
        }
      });
      if (titles.length > 0) {
        if (this.multiple) {
          return Array.from(new Set(titles));
        }
        return titles[0];
      }
      if (this.multiple) {
        return [this.$t('resource.default.title')];
      }
      return this.$t('resource.default.title');
    },
    creators() {
      const creators = [];
      this.entry.meta.forEach(({ name, value_str }) => {
        if (name === 'creators' && value_str) {
          creators.push(value_str);
        }
      });
      if (creators.length > 0) {
        return Array.from(new Set(creators));
      }
      return [this.$t('resource.default.creator')];
    },
    tags() {
      return this.entry.tags || [];
    },
  },
};
