<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('user.score.title')"
  >
    <template v-if="data">
      <p>{{ $t("user.score.note", { username: changeAnonymousText(lastHighscorer), taggings: lastHighscorer.sum_count.toLocaleString() }) }}</p>

      <v-data-table
        :headers="headers"
        :items="data.current_month"
        :item-class="itemClass"
        hide-default-footer
        dense
      >
        <template v-slot:[`item.username`]="{ item, index }">
          <template v-if="index < 3">
            <v-icon
              class="mr-1"
              :color="changeTrophyColor(index)"
            >
              mdi-trophy-outline
            </v-icon>
          </template>

          {{ changeAnonymousText(item) }}
        </template>

        <template v-slot:[`item.sum_score`]="{ item }">
          {{ item.sum_score.toLocaleString() }}
        </template>

        <template v-slot:[`item.sum_count`]="{ item }">
          {{ item.sum_count.toLocaleString() }}
        </template>
      </v-data-table>
    </template>
  </Card>
</template>

<script>
import Card from '@/components/utils/Card.vue';

export default {
  extends: Card,
  props: {
    ...Card.props,
  },
  computed: {
    data() {
      return this.$store.state.statistics.data.scores;
    },
    headers() {
      return [
        { text: this.$t('user.score.headers.username'), value: 'username' },
        { text: this.$t('user.score.headers.sum-score'), value: 'sum_score', align: 'end' },
        { text: this.$t('user.score.headers.sum-count'), value: 'sum_count', align: 'end' },
      ];
    },
    lastHighscorer() {
      if (this.data && this.data.previous_month.length) {
        return this.data.previous_month[0];
      }
      return {
        is_anonymous: true,
        sum_score: 0,
        sum_count: 0,
      };
    },
  },
  methods: {
    itemClass(item) {
      return item.is_anonymous ? 'transparent' : undefined;
    },
    changeTrophyColor(index) {
      if (index === 1) {
        return '#B4B4B4';
      }
      if (index === 2) {
        return '#AD8A56';
      }
      return '#C9B037';
    },
    changeAnonymousText(item) {
      return item.is_anonymous ? this.$t('user.score.headers.is_anonymous') : item.username;
    },
  },
  watch: {
    value(visible) {
      if (visible) {
        this.$store.dispatch('statistics/get');
      }
    },
  },
  created() {
    this.$store.dispatch('statistics/get');
  },
  components: {
    Card,
  },
};
</script>

<style>
tr.transparent > td {
  color: rgba(0, 0, 0, 0.25);
}
</style>
