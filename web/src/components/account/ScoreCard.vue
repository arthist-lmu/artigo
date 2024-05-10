<template>
  <CardBase
    :title="$t('user.score.title')"
    theme="light"
    @close="close"
  >
    <template v-if="statisticsData">
      <p class="pb-4 text-body-2 text-grey-darken-1">
        {{ $t("user.score.note", { username: changeAnonymousText(userHighscore), taggings: userHighscore.sum_count.toLocaleString() }) }}
      </p>

      <v-data-table
        :headers="tableHeaders"
        :items="statisticsData.current_month"
        :item-class="itemClass"
        density="comfortable"
      >
        <template #[`item.username`]="{ item, index }">
          <template v-if="index < 3">
            <v-icon
              class="mr-1"
              :color="changeTrophyColor(index)"
              small
            >
              mdi-trophy-outline
            </v-icon>
          </template>

          {{ changeAnonymousText(item) }}
        </template>

        <template #[`item.sum_score`]="{ item }">
          {{ item.sum_score.toLocaleString() }}
        </template>

        <template #[`item.sum_count`]="{ item }">
          {{ item.sum_count.toLocaleString() }}
        </template>

        <template #bottom />
      </v-data-table>
    </template>

    <template #actions>
      <p class="text-caption text-grey-darken-1">
        {{ $t("user.score.helper") }}
      </p>
    </template>
  </CardBase>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'
import CardBase from '@/components/utils/CardBase.vue'

const store = useStore()
const { t } = useI18n()

const emit = defineEmits(['close'])
function close() {
  emit('close')
}

function itemClass(item) {
  return item.is_anonymous ? 'transparent' : undefined;
}
function changeTrophyColor(index) {
  if (index === 1) {
    return '#B4B4B4';
  }
  if (index === 2) {
    return '#AD8A56';
  }
  return '#C9B037';
}
function changeAnonymousText(item) {
  return item.is_anonymous ? t('user.score.headers.is_anonymous') : item.username;
}

const statisticsData = computed(() => store.state.statistics.data.scores)
const tableHeaders = computed(() => {
  return [
    { title: t('user.score.headers.username'), value: 'username' },
    { title: t('user.score.headers.sumScore'), value: 'sum_score', align: 'end' },
    { title: t('user.score.headers.sumCount'), value: 'sum_count', align: 'end' }
  ]
})
const userHighscore = computed(() => {
  if (statisticsData.value && statisticsData.value.previous_month.length) {
    return statisticsData.value.previous_month[0]
  }
  return {
    is_anonymous: true,
    sum_score: 0,
    sum_count: 0
  }
})

store.dispatch('statistics/get')
</script>

<style>
tr.transparent > td {
  color: rgba(0 0 0 / 25%);
}

.v-data-table > .v-data-table__wrapper > table > tbody > tr > td {
  padding: 0 20px;
}

.v-data-table > .v-data-table__wrapper > table > thead > tr:first-child > th,
.v-data-table > .v-data-table__wrapper > table > tbody > tr:last-child > td {
  height: 38px;
}

.v-data-table > .v-data-table__wrapper > table > thead > tr:first-child > th {
  padding-top: 6px;
}

.v-data-table > .v-data-table__wrapper > table > tbody > tr:last-child > td {
  padding-bottom: 6px;
}
</style>

<style scoped>
.v-data-table {
  border: 2px solid rgba(0 0 0 / 15%) !important;
  border-radius: 24px;
  overflow: hidden;
}
</style>
