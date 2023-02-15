<template>
  <div>
    <div
      v-for="(item, i) in items"
      :key="i"
      class="white--text"
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
      .
    </div>
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
      ];
    },
  },
};
</script>
