<template>
  <div
    ref="container"
    style="position: relative;"
  >
    <slot name="prepend-item"></slot>

    <AnnotatorCanvas
      :key="entry.path"
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
    AnnotatorCanvas: () => import('@/components/annotator/Canvas.vue'),
  },
};
</script>
