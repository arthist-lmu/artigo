<template>
  <PageTabs :items="items">
    <RegisterCard />
  </PageTabs>
</template>

<script>
import PageTabs from '@/components/PageTabs.vue';
import RegisterCard from '@/components/RegisterCard.vue';

export default {
  computed: {
    items() {
      return [
        {
          title: this.$t('register.title'),
          texts: this.$t('register.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs,
    RegisterCard,
  },
};
</script>

<style scoped>
</style>
