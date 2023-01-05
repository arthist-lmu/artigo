<template>
  <div
    ref="container"
    style="position: relative;"
  >
    <slot name="prepend-item" />

    <GameCanvas
      :key="key"
      :src="entry.path"
      :tool="tool"
      v-on="$listeners"
      class="grey lighten-2"
      :height="height"
      contain
    />
  </div>
</template>

<script>
export default {
  props: {
    tool: {
      type: String,
      default: 'select',
    },
    entry: {
      type: Object,
      default: null,
    },
    params: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      height: 0,
    };
  },
  methods: {
    setHeight() {
      if (this.$refs.container !== undefined) {
        this.height = this.$refs.container.offsetHeight;
      }
    },
  },
  computed: {
    key() {
      return `${this.entry.path}-${this.height}`;
    },
  },
  watch: {
    'entry.path'() {
      this.setHeight();
    },
  },
  mounted() {
    this.setHeight();
  },
  created() {
    window.addEventListener('resize', this.setHeight);
  },
  destroyed() {
    window.removeEventListener('resize', this.setHeight);
  },
  components: {
    GameCanvas: () => import('../../annotator/Canvas.vue'),
  },
};
</script>
