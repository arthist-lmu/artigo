<template>
  <PageTabs :items="items">
    <RegisterCard />
  </PageTabs>
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          title: this.$t('user.register.title'),
          texts: this.$t('user.register.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
    RegisterCard: () => import('@/components/RegisterCard.vue'),
  },
};
</script>

<style scoped>
</style>
