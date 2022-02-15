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
    onMouseDown({ point }) {
      this.path = new paper.Path.Circle({
        x: point.x,
        y: point.y,
        fillColor: this.color.stroke,
        radius: 5,
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
