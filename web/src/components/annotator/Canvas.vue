<template>
  <v-img
    class="image-wrapper"
    v-bind="$props"
    v-on:load="onLoad"
    v-on:error="onError"
    alt=""
  >
    <template v-slot:placeholder>
      <slot name="placeholder" />
    </template>

    <v-avatar
      v-if="avatarText"
      class="ma-4"
      color="primary"
      size="44"
    >
      <span class="white--text">
        {{ avatarText }}
      </span>
    </v-avatar>

    <div
      class="canvas-container"
      @wheel.prevent="onWheel"
    >
      <div v-if="activeTool">
        <SelectTool
          v-model="activeTool"
          :bounds="bounds"
          @setOffset="setOffset"
        />

        <PointTool
          v-model="activeTool"
          :bounds="bounds"
          @setOffset="setOffset"
          @export="update"
        />

        <BrushTool
          v-model="activeTool"
          :bounds="bounds"
          @setOffset="setOffset"
          @export="update"
        />

        <RectangleTool
          v-model="activeTool"
          :bounds="bounds"
          @setOffset="setOffset"
          @export="update"
        />
      </div>

      <canvas
        ref="canvas"
        resize
      />
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
    tool: {
      type: String,
      default: 'select',
    },
    avatarText: String,
  },
  data() {
    return {
      ...VImg.data,
      activeTool: 'Select',
      zoom: 0.2,
      bounds: {
        xMin: 0,
        xMax: 0,
        yMin: 0,
        yMax: 0,
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
    onLoad(src) {
      const raster = new paper.Raster(src);
      this.$nextTick(() => {
        const { width, height } = raster.bounds;
        const scale = Math.min(
          this.scope.view.bounds.width / width,
          this.scope.view.bounds.height / height,
        );
        raster.scale(scale, scale);
        raster.position = this.scope.view.center;
        this.bounds = {
          xMin: raster.bounds.x,
          xMax: raster.bounds.x + width * scale,
          yMin: raster.bounds.y,
          yMax: raster.bounds.y + height * scale,
          width: width * scale,
          height: height * scale,
        };
        this.$emit('load');
      });
    },
    onError() {
      this.$emit('error');
    },
    update(values) {
      this.$emit('update', { ...values });
    },
    reset() {
      this.scope.project.activeLayer.removeChildren();
    },
    changeZoom(delta, position) {
      const { center, zoom: oldZoom } = this.scope.view;
      const factor = 1 + this.zoom;
      const newZoom = delta < 0 ? oldZoom * factor : oldZoom / factor;
      const beta = oldZoom / newZoom;
      const x = position.subtract(center).multiply(beta);
      const offset = position.subtract(x).subtract(center);
      return { newZoom, offset };
    },
    onWheel({ offsetX, offsetY, deltaY }) {
      const position = this.scope.view.viewToProject(
        new paper.Point(offsetX, offsetY),
      );
      const { newZoom, offset } = this.changeZoom(deltaY, position);
      if (newZoom < 10 && newZoom > 0.5) {
        this.scope.view.zoom = newZoom;
        this.setOffset(offset, false);
      }
    },
    setOffset(offset, subtract = true) {
      if (subtract) {
        offset = this.scope.view.center.subtract(offset);
      } else {
        offset = this.scope.view.center.add(offset);
      }
      this.scope.view.center = offset;
    },
  },
  watch: {
    tool: {
      handler(value) {
        this.activeTool = value;
      },
      immediate: true,
    },
  },
  mounted() {
    const { offsetWidth, offsetHeight } = this.$refs.canvas.parentNode;
    this.$refs.canvas.style.width = `${offsetWidth}px`;
    this.$refs.canvas.style.height = `${offsetHeight}px`;
    this.$nextTick(() => {
      this.scope.setup(this.$refs.canvas);
      this.scope.activate();
    });
  },
  created() {
    this.scope = new paper.PaperScope();
  },
  components: {
    PointTool: () => import('./tools/PointTool.vue'),
    BrushTool: () => import('./tools/BrushTool.vue'),
    SelectTool: () => import('./tools/SelectTool.vue'),
    RectangleTool: () => import('./tools/RectangleTool.vue'),
  },
};
</script>

<style>
.v-image.image-wrapper .v-image__image {
  display: none;
}
</style>

<style scoped>
canvas {
  width: 600px;
  height: 400px;
}

.canvas-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
