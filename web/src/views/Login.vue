<template>
  <PageTabs :items="items">
    <LoginCard />
  </PageTabs>
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          title: this.$t('login.title'),
          texts: this.$t('login.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
    LoginCard: () => import('@/components/LoginCard.vue'),
  },
};
</script>

<style scoped>
</style>
