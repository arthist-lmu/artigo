<template>
  <div class="white--text">
    <template v-for="(item, i) in items">
      <p
        v-html="item.text"
        :key="`${i}-text`"
      />

      <v-list
        v-if="item.fields"
        :key="`${i}-fields`"
        class="my-6"
        color="transparent"
        rounded="xl"
        outlined
        dense
        dark
        flat
      >
        <v-list-item
          v-for="(field, j) in item.fields"
          :key="`${i}-${j}`"
        >
          <v-list-item-avatar height="20">
            <v-icon color="error">
              mdi-trophy-outline
            </v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            {{ field }}
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </div>
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          text: this.$t('description.texts.preface'),
        },
        {
          text: this.$t('description.texts.principle'),
          fields: [
            this.$tc('description.fields.score-validated', 5),
            this.$tc('description.fields.score-opponent', 5),
            this.$tc('description.fields.score-first', 5),
          ],
        },
        {
          text: this.$t('description.texts.motivation'),
        },
      ];
    },
  },
};
</script>

<style scoped>
.v-list-item .v-list-item__content:after {
  content: ";";
}

.v-list-item:last-child .v-list-item__content:after {
  content: ".";
}
</style>
