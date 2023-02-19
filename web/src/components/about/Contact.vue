<template>
  <div class="white--text">
    <span
      v-for="(item, i) in items"
      :key="i"
    >
      <span
        v-html="item.text"
        class="mr-1"
      />

      <v-chip
        v-for="person in item.values"
        :key="person.name"
        @click="goTo(person.url)"
        class="ml-1"
        color="accent"
        outlined
        dark
      >
        {{ person.name }}
      </v-chip>
    </span>
  </div>
</template>

<script>
export default {
  methods: {
    goTo(url) {
      window.open(url, '_blank');
    },
  },
  computed: {
    items() {
      return [
        {
          text: this.$t('contact.texts.cooperate'),
          values: [
            { name: 'Stefanie Schneider', url: 'https://www.kunstgeschichte.uni-muenchen.de/personen/wiss_ma/schneider/index.html' },
          ],
        },
        {
          text: this.$t('contact.texts.bugs'),
          values: [
            { name: 'GitHub', url: 'https://github.com/arthist-lmu/artigo/issues' },
          ],
        },
      ];
    },
  },
};
</script>

<style scoped>
div > span:after {
  content: ' . ';
}
</style>
