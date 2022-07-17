<template>
  <PageTabs v-model="tab" :items="items">
    <template v-slot:default="slotProps">
      <div
        v-if="slotProps.title == $t('about.title')"
        class="mb-8"
      >
        <Contributors />
      </div>
    </template>
  </PageTabs>
</template>

<script>
export default {
  data() {
    return {
      tab: null,
    };
  },
  computed: {
    items() {
      return [
        {
          title: this.$t('about.title'),
          texts: this.$t('about.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
    Contributors: () => import('@/components/Contributors.vue'),
  },
};
</script>
