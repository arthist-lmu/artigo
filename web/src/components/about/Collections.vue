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
              mdi-database-outline
            </v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <span v-html="field" />
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
          text: this.$t('collections.texts.preface'),
        },
        {
          text: this.$t('collections.texts.principle'),
        },
        {
          text: this.$t('collections.texts.mapping'),
          fields: [
            this.$t('collections.texts.file-path'),
            this.$t('collections.texts.title'),
            this.$t('collections.texts.creator'),
            this.$t('collections.texts.created'),
            this.$t('collections.texts.location'),
            this.$t('collections.texts.source'),
            this.$t('collections.texts.tags'),
          ],
        },
        {
          text: this.$t('collections.texts.access'),
        },
      ];
    },
  },
};
</script>

<style scoped>
.v-list-item .v-list-item__content span {
  line-height: 24px;
}

.v-list-item .v-list-item__content span:after {
  content: ";";
}

.v-list-item:last-child .v-list-item__content span:after {
  content: ".";
}
</style>
