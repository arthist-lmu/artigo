<template>
  <div
    ref="container"
    style="position: relative;"
  >
    <slot name="prepend-item"></slot>

    <Canvas
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
    entry: Object,
    params: Object,
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
    Canvas: () => import('@/components/annotator/Canvas.vue'),
  },
};
</script>
