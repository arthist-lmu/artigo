<template>
  <v-img
    v-bind="computedProps"
    v-on:load="loaded"
  >
    <template v-slot:placeholder>
      <slot name="placeholder"></slot>
    </template>

    <div class="canvas-container">
      <div v-if="activeTool">
        <PointTool
          v-model="activeTool"
          :scale="scale"
          @export="update"
        />

        <BrushTool
          v-model="activeTool"
          :scale="scale"
          @export="update"
        />

        <RectangleTool
          v-model="activeTool"
          :scale="scale"
          @export="update"
        />
      </div>

      <canvas ref="canvas" />
    </div>
  </v-img>
</template>

<script>
import paper from 'paper';
import { VImg } from 'vuetify/lib';

export default {
  extends: VImg,
  props: {
    ...VImg.props,
    value: Object,
  },
  data() {
    return {
      ...VImg.data,
      activeTool: '',
      scale: {
        width: 0,
        height: 0,
      },
      client: {
        width: 0,
        height: 0,
      },
    };
  },
  methods: {
    getScale(image) {
      const { naturalHeight, naturalWidth } = image;
      const scaleHeight = this.client.height / naturalHeight;
      const scaleWidth = this.client.width / naturalWidth;
      const scale = Math.min(scaleHeight, scaleWidth);
      return {
        height: naturalHeight * scale,
        width: naturalWidth * scale,
      };
    },
    loaded(src) {
      const image = new Image();
      image.onload = () => {
        /* istanbul ignore if */
        if (image.decode) {
          image.decode();
        } else {
          this.onLoad();
        }
      };
      image.src = src;
      this.$nextTick(() => {
        this.client.height = this.$el.clientHeight;
        this.client.width = this.$el.clientWidth;
        const { width, height } = this.getScale(image);
        if (width > 0 && height > 0) {
          this.scale.width = width;
          this.scale.height = height;
          this.scope.view.viewSize.width = width;
          this.scope.view.viewSize.height = height;
        }
      });
    },
    update(values) {
      console.log(this.activeTool, values);
    },
    reset(scope) {
      scope.project.activeLayer.removeChildren();
    },
  },
  computed: {
    computedProps() {
      return { ...this.$props };
    },
  },
  watch: {
    src() {
      this.reset(this.scope);
    },
  },
  mounted() {
    this.scope = new paper.PaperScope();
    this.scope.setup(this.$refs.canvas);
  },
  components: {
    PointTool: () => import('@/components/annotator/tools/PointTool.vue'),
    BrushTool: () => import('@/components/annotator/tools/BrushTool.vue'),
    RectangleTool: () => import('@/components/annotator/tools/RectangleTool.vue'),
  },
};
</script>

<style scoped>
.canvas-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
