<template>
  <div></div>
</template>

<script>
import paper from 'paper';
import tool from '@/mixins/tool';

export default {
  name: 'PointTool',
  mixins: [tool],
  data() {
    return {
      name: 'Point',
    };
  },
  methods: {
    createPoint({ x, y }) {
      const {
        xMin, xMax, yMin, yMax,
      } = this.bounds;
      if (x < xMin || x > xMax) {
        return null;
      }
      if (y < yMin || y > yMax) {
        return null;
      }
      return new paper.Path.Circle({
        x,
        y,
        fillColor: this.color.stroke,
        radius: 5,
        selected: true,
      });
    },
    onMouseDown({ event, point }) {
      if (!event.ctrlKey) {
        this.remove();
        this.path = this.createPoint(point);
      }
    },
    onMouseDrag({ event, point, downPoint }) {
      if (event.ctrlKey) {
        const offset = point.subtract(downPoint);
        this.$emit('setOffset', offset);
      }
    },
    onMouseUp() {
      if (!event.ctrlKey && this.path) {
        this.set(this.path.strokeBounds, true);
        this.$emit('export', this.roi);
      }
    },
  },
};
</script>
