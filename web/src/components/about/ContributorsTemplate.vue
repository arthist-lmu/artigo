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
          class="mr-1 mb-1"
          :title="getPersonTitle(person)"
          :color="getPersonColor(person)"
          :border="getPersonBorder(person)"
          variant="outlined"
          @click="goTo(person.url, extern=true)"
        >
          <v-icon
            v-if="person.leader"
            class="mr-2"
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
          border="md opacity-100"
          variant="outlined"
        >
          <span class="clip">
            {{ person.name }}
          </span>
        </v-chip>
      </template>
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import goTo from '@/composables/useGoTo'

const { t } = useI18n()

function getPersonTitle(person) {
  return person.leader ? t('contributors.fields.leader') : undefined
}
function getPersonColor(person) {
  return person.leader ? 'error' : 'accent'
}
function getPersonBorder(person) {
  return `${getPersonColor(person)} md opacity-100`
}

const items = computed(() => {
  return [
    {
      group: t('contributors.fields.informatics'),
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
        { name: 'Dr. Christoph Wieser' }
      ]
    },
    {
      group: t('contributors.fields.cis'),
      values: [
        { name: 'Prof. Dr. Klaus Schulz', url: 'http://www.cis.uni-muenchen.de/personen/professoren/schulz/' },
        { name: 'Dr. Elena Levushkina' }
      ]
    },
    {
      group: t('contributors.fields.artHistory'),
      values: [
        { name: 'Prof. Dr. Hubertus Kohle', url: 'http://www.kunstgeschichte.uni-muenchen.de/personen/professoren_innen/kohle/' },
        { name: 'Matthias Becker' },
        { name: 'Fabian Bross' },
        { name: 'Laura Commare' },
        { name: 'Stefanie Schneider', url: 'https://www.kunstgeschichte.uni-muenchen.de/personen/wiss_ma/schneider/index.html', leader: true },
        { name: 'Ricarda Vollmer' }
      ]
    },
    {
      group: t('contributors.fields.romanceStudies'),
      values: [
        { name: 'Prof. Dr. Thomas Krefeld', url: 'https://www.romanistik.uni-muenchen.de/personen/emeriti/krefeld/index.html' },
        { name: 'Caterina Campanella' },
        { name: 'Silvia Cramerotti' },
        { name: 'Katharina Jakob' },
        { name: 'Alessandra Puglisi' }
      ]
    },
    {
      group: t('contributors.fields.itg'),
      values: [
        { name: 'Dr. Stephan Lücke', url: 'http://www.itg.uni-muenchen.de/personen/luecke_stephan/' },
        { name: 'Dr. Christian Riepl', url: 'http://www.itg.uni-muenchen.de/personen/riepl_christian/' },
        { name: 'Dr. Gerhard Schön', url: 'http://www.itg.uni-muenchen.de/personen/schoen_gerhard/' },
        { name: 'Eva Schmidt' }
      ]
    }
  ]
})
</script>
