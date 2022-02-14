<template>
  <v-img
    ref="image"
    v-bind="computedProps"
    v-on:load="loaded"
  >
    <template v-slot:placeholder>
      <slot name="placeholder"></slot>
    </template>

    <div class="canvas-container">
      <canvas
        ref="canvas"
        class="canvas"
        v-on:mousedown="initialize"
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
    selectType: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      ...VImg.data,
      roi: null,
      color: 'rgba(184, 201, 225, 0.5)',
      image: {
        base: null,
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
    getScale() {
      const imageHeight = this.image.base.naturalHeight;
      const imageWidth = this.image.base.naturalWidth;
      const scaleHeight = this.client.height / imageHeight;
      const scaleWidth = this.client.width / imageWidth;
      const scale = Math.min(scaleHeight, scaleWidth);
      return {
        height: imageHeight * scale,
        width: imageWidth * scale,
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
      this.image.base = image;
      this.$nextTick(() => {
        this.client.height = this.$el.clientHeight;
        this.client.width = this.$el.clientWidth;
        const { width, height } = this.getScale();
        if (width > 0 && height > 0) {
          this.image.width = width;
          this.image.height = height;
          this.scope.view.viewSize.width = width;
          this.scope.view.viewSize.height = height;
        }
      });
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
        strokeColor: this.color,
        strokeWidth: 25,
        strokeCap: 'round',
      });
    },
    createPoint({ x, y }) {
      if (x < 0) {
        x = 0;
      } else if (x > this.image.width) {
        x = this.image.width;
      }
      if (y < 0) {
        y = 0;
      } else if (y > this.image.height) {
        y = this.image.height;
      }
      return new paper.Point(x, y);
    },
    createRectangle({
      x, y, width, height,
    }) {
      if (x < 0) {
        width += x;
        x = 0;
      } else if (x > this.image.width) {
        width = 0;
        x = this.image.width;
      }
      if (x + width > this.image.width) {
        width -= (x + width) - this.image.width;
      }
      if (y < 0) {
        height += y;
        y = 0;
      } else if (y > this.image.height) {
        height = 0;
        y = this.image.height;
      }
      if (y + height > this.image.height) {
        height -= (y + height) - this.image.height;
      }
      return new paper.Rectangle(x, y, width, height);
    },
    setROI(roi, relative = true) {
      if (relative) {
        roi = {
          x: roi.x / this.image.width,
          y: roi.y / this.image.height,
          width: roi.width / this.image.width,
          height: roi.height / this.image.height,
        };
      }
      this.roi = roi;
    },
    initialize() {
      this.tool = this.createTool(this.scope);
      if (this.selectType) {
        this.tool.onMouseDown = this.onMouseDown;
        this.tool.onMouseDrag = this.onMouseDrag;
        this.tool.onMouseUp = this.onMouseUp;
      }
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
      this.path = new paper.Path.Rectangle({
        rectangle,
        strokeColor: this.color,
        strokeWidth: 5,
        selected: true,
      });
      this.setROI(rectangle, true);
      this.$emit('mouseUp', this.roi);
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

<style scoped>
.canvas-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
