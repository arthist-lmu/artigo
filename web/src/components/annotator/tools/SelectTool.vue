<template>
  <div></div>
</template>

<script>
import tool from '@/mixins/tool';

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
