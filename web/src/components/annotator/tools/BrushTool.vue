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
      name: 'brush',
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
      const {
        xMin, xMax, yMin, yMax,
      } = this.bounds;
      if (x < xMin) {
        x = xMin;
      } else if (x > xMax) {
        x = xMax;
      }
      if (y < yMin) {
        y = yMin;
      } else if (y > yMax) {
        y = yMax;
      }
      return new paper.Point(x, y);
    },
    onMouseDown({ event, point }) {
      if (!event.ctrlKey) {
        this.remove();
        this.path = this.createPath(this.scope);
        this.path.add(this.createPoint(point));
      }
    },
    onMouseDrag({ event, point, downPoint }) {
      if (event.ctrlKey) {
        const offset = point.subtract(downPoint);
        this.$emit('setOffset', offset);
      } else {
        this.path.add(this.createPoint(point));
        this.path.smooth();
      }
    },
    onMouseUp({ event, point }) {
      if (!event.ctrlKey) {
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
      }
    },
  },
};
</script>
