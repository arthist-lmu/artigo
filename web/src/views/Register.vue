<template>
  <Layout dark>
    <Card :isDialog="false" />
  </Layout>
</template>

<script>
export default {
  components: {
    Layout: () => import('@/layouts/Account.vue'),
    Card: () => import('@/components/account/RegisterCard.vue'),
  },
};
</script>
