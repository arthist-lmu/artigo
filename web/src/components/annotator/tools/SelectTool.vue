<template>
  <div></div>
</template>

<script>
import tool from '@/mixins/annotator/tools';

export default {
  name: 'SelectTool',
  mixins: [tool],
  data() {
    return {
      name: 'select',
    };
  },
  methods: {
    onMouseDrag({ point, downPoint }) {
      const offset = point.subtract(downPoint);
      this.$emit('setOffset', offset);
    },
  },
};
</script>
