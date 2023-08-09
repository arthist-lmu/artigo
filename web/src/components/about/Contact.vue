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

      <v-btn
        v-for="person in item.values"
        :key="person.url"
        @click="goTo(person.url)"
        class="ml-1 mb-1"
        x-small
        icon
      >
        <v-icon color="accent">
          {{ person.icon }}
        </v-icon>
      </v-btn>
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
            { url: 'https://www.kunstgeschichte.uni-muenchen.de/personen/wiss_ma/schneider/index.html', icon: 'mdi-email-outline' },
          ],
        },
        {
          text: this.$t('contact.texts.press'),
          values: [
            { url: '/assets/press-kit.zip', icon: 'mdi-folder-outline' },
          ],
        },
        {
          text: this.$t('contact.texts.bugs'),
          values: [
            { url: 'https://github.com/arthist-lmu/artigo/issues', icon: 'mdi-github' },
          ],
        },
      ];
    },
  },
};
</script>

<style scoped>
div > span:after {
  content: '. ';
}
</style>
