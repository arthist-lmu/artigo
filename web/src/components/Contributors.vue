<template>
  <div>
    <span
      v-for="item in items"
      :key="item.group"
    >
      <v-chip
        class="mr-1 mb-1 grey--text text--darken-4"
        color="accent"
      >
        <span
          :title="item.group"
          class="clip"
        >
          {{ item.group }}
        </span>
      </v-chip>

      <template v-for="person in item.values">
        <v-chip
          v-if="person.url"
          :key="person.name"
          @click="goTo(person.url)"
          class="mr-1 mb-1"
          :title="person.leader ? $t('contributors.fields.leader') : undefined"
          :color="person.leader ? 'error' : 'accent'"
          outlined
          dark
        >
          <v-icon
            v-if="person.leader"
            left
          >
            mdi-account-tie
          </v-icon>

          {{ person.name }}
        </v-chip>
        <v-chip
          v-else
          :key="person.name"
          class="mr-1 mb-1"
          color="accent"
          outlined
          dark
        >
          <span class="clip">
            {{ person.name }}
          </span>
        </v-chip>
      </template>
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
          group: this.$t('contributors.fields.informatics'),
          values: [
            { name: 'Prof. Dr. François Bry', url: 'http://www.pms.ifi.lmu.de/mitarbeiter/francois-bry' },
            { name: 'Martin Bogner' },
            { name: 'Martin Josko', url: 'http://www.pms.ifi.lmu.de/mitarbeiter/martin-josko' },
            { name: 'Dr. Fabian Kneißl' },
            { name: 'Maximilian Kristen' },
            { name: 'Anke Regner' },
            { name: 'Dr. Clemens Schefels' },
            { name: 'Corina Schemainda' },
            { name: 'Franz Siglmüller' },
            { name: 'Bartholomäus Steinmayr' },
            { name: 'Florian Störkle' },
            { name: 'Iris Teske' },
            { name: 'Dr. Christoph Wieser' },
          ],
        },
        {
          group: this.$t('contributors.fields.cis'),
          values: [
            { name: 'Prof. Dr. Klaus Schulz', url: 'http://www.cis.uni-muenchen.de/personen/professoren/schulz/' },
            { name: 'Dr. Elena Levushkina' },
          ],
        },
        {
          group: this.$t('contributors.fields.art-history'),
          values: [
            { name: 'Prof. Dr. Hubertus Kohle', url: 'http://www.kunstgeschichte.uni-muenchen.de/personen/professoren_innen/kohle/' },
            { name: 'Matthias Becker' },
            { name: 'Fabian Bross' },
            { name: 'Laura Commare' },
            { name: 'Stefanie Schneider', url: 'https://www.kunstgeschichte.uni-muenchen.de/personen/wiss_ma/schneider/index.html', leader: true },
          ],
        },
        {
          group: this.$t('contributors.fields.romance-studies'),
          values: [
            { name: 'Prof. Dr. Thomas Krefeld', url: 'https://www.romanistik.uni-muenchen.de/personen/emeriti/krefeld/index.html' },
            { name: 'Caterina Campanella' },
            { name: 'Silvia Cramerotti' },
            { name: 'Katharina Jakob' },
            { name: 'Alessandra Puglisi' },
          ],
        },
        {
          group: this.$t('contributors.fields.itg'),
          values: [
            { name: 'Dr. Stephan Lücke', url: 'http://www.itg.uni-muenchen.de/personen/luecke_stephan/' },
            { name: 'Dr. Christian Riepl', url: 'http://www.itg.uni-muenchen.de/personen/riepl_christian/' },
            { name: 'Dr. Gerhard Schön', url: 'http://www.itg.uni-muenchen.de/personen/schoen_gerhard/' },
            { name: 'Eva Schmidt' },
          ],
        },
      ];
    },
  },
};
</script>
