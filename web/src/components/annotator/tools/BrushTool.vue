<template>
  <div></div>
</template>

<script>
import paper from 'paper';
import tool from '@/mixins/tool';

export default {
  name: 'BrushTool',
  mixins: [tool],
  data() {
    return {
      name: 'Brush',
    };
  },
  methods: {
    createPath() {
      return new paper.Path({
        strokeColor: this.color.stroke,
        strokeWidth: 25,
        strokeCap: 'round',
      });
    },
    createPoint({ x, y }) {
      if (x < 0) {
        x = 0;
      } else if (x > this.scale.width) {
        x = this.scale.width;
      }
      if (y < 0) {
        y = 0;
      } else if (y > this.scale.height) {
        y = this.scale.height;
      }
      return new paper.Point(x, y);
    },
    onMouseDown({ point }) {
      this.remove();
      this.path = this.createPath(this.scope);
      this.path.add(this.createPoint(point));
    },
    onMouseDrag({ point }) {
      this.path.add(this.createPoint(point));
      this.path.smooth();
    },
    onMouseUp({ point }) {
      this.path.add(this.createPoint(point));
      this.path.smooth();
      const { strokeBounds } = this.path;
      this.remove();
      this.path = new paper.Path.Rectangle({
        rectangle: strokeBounds,
        fillColor: this.color.stroke,
        selected: true,
      });
      this.set(strokeBounds, true);
      this.$emit('export', this.roi);
    },
  },
};
</script>
