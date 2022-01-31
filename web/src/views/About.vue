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
        {
          title: this.$t('game.fields.default.title'),
          texts: this.$t('game.fields.default.texts'),
        },
      ];
    },
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      if (to.query.tab === 'game') {
        vm.tab = 1;
      } else {
        vm.tab = 0;
      }
    });
  },
  beforeRouteUpdate(to, from, next) {
    if (to.query.tab === 'game') {
      this.tab = 1;
    } else {
      this.tab = 0;
    }
    next();
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
    Contributors: () => import('@/components/Contributors.vue'),
  },
};
</script>
