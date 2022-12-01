<template>
  <Card :isDialog="false" />
</template>

<script>
export default {
  components: {
    Card: () => import('@/components/account/RegisterCard.vue'),
  },
};
</script>
