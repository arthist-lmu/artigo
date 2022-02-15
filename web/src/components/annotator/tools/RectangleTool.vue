<template>
  <div></div>
</template>

<script>
import paper from 'paper';
import tool from '@/mixins/tool';

export default {
  name: 'RectangleTool',
  mixins: [tool],
  data() {
    return {
      name: 'Rectangle',
      rectangle: [null, null],
    };
  },
  methods: {
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
      this.rectangle[0] = this.createPoint(point);
      this.rectangle[1] = null;
    },
    onMouseDrag({ point }) {
      this.remove();
      this.rectangle[1] = this.createPoint(point);
      this.path = new paper.Path.Rectangle({
        from: this.rectangle[0],
        to: this.rectangle[1],
        fillColor: this.color.stroke,
        selected: true,
      });
    },
    onMouseUp() {
      this.set(this.path.strokeBounds, true);
      this.$emit('export', this.roi);
    },
  },
};
</script>
