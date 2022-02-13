<template>
  <v-img
    ref="image"
    v-bind="computedProps"
    v-on:load="loaded"
  >
    <template v-slot:placeholder>
      <slot name="placeholder"></slot>
    </template>

    <canvas
      ref="canvas"
      class="canvas"
      v-on:mousedown="initialize"
    />
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
      tool: null,
      hue: Math.random() * 360,
    };
  },
  methods: {
    loaded() {
      // this.raster = new paper.Raster({
      //   source: this.$refs.image,
      //   position: paper.view.center,
      // });
    },
    reset(scope) {
      scope.project.activeLayer.removeChildren();
    },
    createTool(scope) {
      scope.activate();
      return new paper.Tool({
        minDistance: 10,
        maxDistance: 45,
      });
    },
    createPath(scope) {
      scope.activate();
      return new paper.Path({
        strokeColor: {
          hue: this.hue,
          saturation: 1,
          brightness: 1,
          alpha: 0.5,
        },
        strokeWidth: 25,
        strokeCap: 'round',
      });
    },
    createPoint({ x, y }) {
      return new paper.Point(x, y);
    },
    createRectangle({
      x, y, width, height,
    }) {
      return new paper.Rectangle(x, y, width, height);
    },
    initialize() {
      this.tool = this.createTool(this.scope);
      this.tool.onMouseDown = this.onMouseDown;
      this.tool.onMouseDrag = this.onMouseDrag;
      this.tool.onMouseUp = this.onMouseUp;
    },
    onMouseDown(event) {
      this.path = this.createPath(this.scope);
      this.path.add(this.createPoint(event.point));
    },
    onMouseDrag(event) {
      this.path.add(this.createPoint(event.point));
      this.path.smooth();
    },
    onMouseUp(event) {
      this.path.add(this.createPoint(event.point));
      this.path.closed = true;
      this.path.smooth();
      const bounds = this.path.strokeBounds;
      this.reset(this.scope);
      this.path = this.createPath(this.scope);
      const rectangle = this.createRectangle(bounds);
      this.path = new paper.Path.Rectangle(rectangle);
      this.path.strokeColor = {
        hue: this.hue,
        saturation: 1,
        brightness: 1,
        alpha: 0.5,
      };
      this.path.strokeWidth = 5;
      this.path.selected = true;
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
};
</script>

<style>
.canvas {
  width: 100%;
  height: 100%;
}
</style>
