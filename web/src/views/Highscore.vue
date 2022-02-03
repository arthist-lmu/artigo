<template>
  <PageTabs :items="items">
    <v-expansion-panels
      v-model="panels"
      class="mb-8"
      accordion
      multiple
      flat
    >
      <v-expansion-panel
        v-for="(entries, field) in data"
        :key="field"
        :class="entries.length ? '' : 'disabled'"
      >
        <v-expansion-panel-header class="pa-0">
            <span class="text-subtitle-1">
              {{ $t("highscore.fields")[field] }}
            </span>
        </v-expansion-panel-header>

        <v-expansion-panel-content>
          <v-data-table
            :headers="headers"
            :items="entries"
            hide-default-footer
            dense
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </PageTabs>
</template>

<script>
export default {
  data() {
    return {
      panels: [0],
    };
  },
  computed: {
    items() {
      return [
        {
          title: this.$t('highscore.title'),
          texts: this.$t('highscore.texts'),
        },
      ];
    },
    headers() {
      return [
        { text: this.$t('highscore.headers.name'), value: 'name' },
        { text: this.$t('highscore.headers.count-taggings'), value: 'count_taggings', align: 'end' },
        { text: this.$t('highscore.headers.count-gamerounds'), value: 'count_gamerounds', align: 'end' },
      ];
    },
    data() {
      return this.$store.state.highscore.data;
    },
  },
  created() {
    this.$store.dispatch('highscore/get');
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
  },
};
</script>
