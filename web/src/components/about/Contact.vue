<template>
  <div class="white--text">
    <span
      v-for="(item, i) in items"
      :key="i"
    >
      <a :href="item.url" target="_blank">
        <span
          v-html="item.text"
          class="mr-1"
        />
      </a>

      <v-icon
        color="accent"
        class="ml-1"
        small
      >
        {{ item.icon }}
      </v-icon>
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
          url: 'https://www.kunstgeschichte.uni-muenchen.de/personen/wiss_ma/schneider/index.html',
          icon: 'mdi-email-outline',
        },
        {
          text: this.$t('contact.texts.press'),
          url: '/assets/press-kit.zip',
          icon: 'mdi-link-variant',
        },
        {
          text: this.$t('contact.texts.bugs'),
          url: 'https://github.com/arthist-lmu/artigo/issues',
          icon: 'mdi-link-variant',
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
