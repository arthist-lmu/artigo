<template>
  <div>
    <h2 class="mb-2">
      {{ $t('contributors.title') }}
    </h2>

    <ul
      v-for="item in items"
      :key="item.group"
      class="mb-4"
    >
      <li>{{ item.group }}</li>

      <ul>
        <li
          v-for="person in item.persons"
          :key="person.name"
        >
          <a
            v-if="person.url"
            :href="person.url"
            target="_blank"
          >
            {{ person.name }}
          </a>
          <span v-else>
            {{ person.name }}
          </span>
        </li>
      </ul>
    </ul>
  </div>
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          group: this.$t('contributors.fields.informatics'),
          persons: [
            { name: 'Prof. Dr. François Bry', url: 'http://www.pms.ifi.lmu.de/mitarbeiter/francois-bry' },
            { name: 'Martin Bogner' },
            { name: 'Martin Josko', url: 'http://www.pms.ifi.lmu.de/mitarbeiter/martin-josko' },
            { name: 'Dr. Fabian Kneißl' },
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
          persons: [
            { name: 'Prof. Dr. Klaus Schulz', url: 'http://www.cis.uni-muenchen.de/personen/professoren/schulz/' },
            { name: 'Dr. Elena Levushkina', url: '' },
          ],
        },
        {
          group: this.$t('contributors.fields.art-history'),
          persons: [
            { name: 'Prof. Dr. Hubertus Kohle', url: 'http://www.kunstgeschichte.uni-muenchen.de/personen/professoren_innen/kohle/' },
            { name: 'Matthias Becker' },
            { name: 'Fabian Bross' },
            { name: 'Laura Commare' },
            { name: 'Stefanie Schneider', url: 'https://www.kunstgeschichte.uni-muenchen.de/personen/wiss_ma/schneider/index.html' },
          ],
        },
        {
          group: this.$t('contributors.fields.romance-studies'),
          persons: [
            { name: 'Prof. Dr. Thomas Krefeld', url: 'http://www.romanistik.uni-muenchen.de/personen/professoren/krefeld/' },
            { name: 'Caterina Campanella' },
            { name: 'Silvia Cramerotti' },
            { name: 'Katharina Jakob' },
            { name: 'Alessandra Puglisi' },
          ],
        },
        {
          group: this.$t('contributors.fields.itg'),
          persons: [
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
