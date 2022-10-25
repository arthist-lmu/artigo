<template>
  <div></div>
</template>

<script>
import paper from 'paper';
import tool from '@/mixins/annotator/tools';

export default {
  name: 'RectangleTool',
  mixins: [tool],
  data() {
    return {
      name: 'rectangle',
      rectangle: [null, null],
    };
  },
  methods: {
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
        this.rectangle[0] = this.createPoint(point);
        this.rectangle[1] = null;
      }
    },
    onMouseDrag({ event, point, downPoint }) {
      if (event.ctrlKey) {
        const offset = point.subtract(downPoint);
        this.$emit('setOffset', offset);
      } else {
        this.remove();
        this.rectangle[1] = this.createPoint(point);
        this.path = new paper.Path.Rectangle({
          from: this.rectangle[0],
          to: this.rectangle[1],
          fillColor: this.color.stroke,
          selected: true,
        });
      }
    },
    onMouseUp({ event }) {
      if (!event.ctrlKey) {
        this.set(this.path.strokeBounds, true);
        this.$emit('export', this.roi);
      }
    },
  },
};
</script>
