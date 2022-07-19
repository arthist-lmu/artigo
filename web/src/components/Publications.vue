<template>
  <div>
    <v-expansion-panels
      v-model="panels"
      multiple
      flat
    >
      <v-expansion-panel
        v-for="item in items"
        :key="item.group"
      >
        <v-expansion-panel-header>
          {{ item.group }}
        </v-expansion-panel-header>

        <v-expansion-panel-content class="pb-6">
          <v-row
            v-for="value in item.values"
            :key="value.title"
            class="px-6"
          >
            <v-col cols="auto">
              <v-avatar
                color="grey lighten-2"
                size="36"
              >
                <span v-if="value.author">
                  {{ value.author.slice(0, 2) }}
                </span>
              </v-avatar>
            </v-col>

            <v-col>
              <span v-if="value.author">{{ value.author }} </span>
              <span v-if="value.year">({{ value.year }})</span>

              <span>: {{ value.title }}</span>

              <span v-if="value.journal">, in: {{ value.journal }}</span>
              <span v-if="value.institute">, {{ value.institute }} </span>
              <span v-if="value.pages">, {{ value.pages }}</span>
              <span>.</span>
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
export default {
  data() {
    return {
      panels: [0],
    };
  },
  methods: {
    goTo(url) {
      window.open(url, '_blank');
    },
  },
  computed: {
    items() {
      return [
        {
          group: this.$t('publications.fields.journals'),
          values: [
            {
              author: 'Bry, François; Schefels, Clemens; Schemainda, Corina',
              title: 'Eine qualitative Analyse der ARTigo-Annotationen',
              year: 2018,
              journal: 'Computing Art Reader. Einführung in die digitale Kunstgeschichte',
              pages: '96–114',
            },
            {
              author: 'Bry, François; Wieser, Christoph',
              title: 'Squaring and Scripting the ESP Game. Trimming a GWAP to Deep Semantics',
              year: 2012,
              journal: 'SGDA 2012. Serious Games Development and Applications',
              pages: '183–192',
            },
            {
              author: 'Commare, Laura',
              title: 'Social Tagging als Methode zur Optimierung Kunsthistorischer Bilddatenbanken. Eine empirische Analyse des Artigo-Projekts',
              year: 2011,
              journal: 'Kunstgeschichte. Open Peer Reviewed Journal',
            },
            {
              author: 'Kohle, Hubertus',
              title: 'Social Tagging von Kunstwerken oder: Wie bringe ich junge Leute dazu, ins Museum zu gehen',
              year: 2009,
              journal: 'Museum aktuell 161',
              pages: '14–15',
            },
            {
              author: 'Kohle, Hubertus',
              title: 'Artigo. Social image tagging pour les oeuvres d\'art',
              year: 2010,
              journal: 'L’art et la mesure. Histoire de l’art et méthodes quantitatives',
              pages: '153–164',
            },
            {
              author: 'Kohle, Hubertus',
              title: 'Kunstgeschichte goes Social Media. Laien optimieren eine Bilddatenbank – mit einem digitalen Spiel',
              year: 2011,
              journal: 'Aviso. Zeitschrift für Wissenschaft und Kunst in Bayern 3',
              pages: '37–43',
            },
            {
              author: 'Kohle, Hubertus',
              title: 'Social Tagging in the Humanities and the Nature of the Internet Workflow',
              year: 2011,
              journal: 'Kunstgeschichte. Open Peer Reviewed Journal',
            },
            {
              author: 'Kohle, Hubertus',
              title: 'The Wisdom of Crowds',
              year: 2016,
              journal: 'On_Culture. The Open Journal for the Study of Culture',
            },
            {
              author: 'Schefels, Clemens',
              title: 'Eine offene Universität für eine offene Gesellschaft',
              year: 2016,
              journal: 'oead\'news 101',
              pages: '22–23',
            },
            {
              author: 'Schneider, Stefanie; Kohle, Hubertus',
              title: 'The Computer as Filter Machine. A Clustering Approach to Categorize Artworks Based on a Social Tagging Network',
              year: 2017,
              journal: 'Artl@s Bulletin 6.3',
              pages: '81–89',
            },
            {
              author: 'Shah, Philipp; Wieser, Christoph; Bry, François',
              title: 'Parallel Higher-Order SVD for Tag-Recommendations',
              year: 2012,
              journal: 'IADIS International Conference WWW/Internet 2012',
              pages: '257–265',
            },
            {
              author: 'Steinmayr, Bartholomäus; Wieser, Christoph; Kneißl, Fabian; Bry, François',
              title: 'Karido. A GWAP for Telling Artworks Apart',
              year: 2011,
              journal: '16th International Conference on Computer Games (CGAMES)',
              pages: '193–200',
            },
            {
              author: 'Wieser, Christoph, Bry, François, Bérard, Alexandre und Lagrange, Richard',
              title: 'ARTigo. Building an Artwork Search Engine With Games and Higher-Order Latent Semantic Analysis',
              year: 2013,
              journal: 'Proceedings of Disco 2013. Workshop on Human Computation and Machine Learning in Games',
            },
          ],
        },
        {
          group: this.$t('publications.fields.theses'),
          values: [
            {
              author: 'Bogner, Martin',
              title: 'Conception and Implementation of a Collaborative Data Science Platform',
              year: 2016,
              institute: this.$t('contributors.fields.informatics'),
            },
            {
              author: 'Greth, Nicola',
              title: 'Automatic Semantic Categorization of Image Annotations Generated by Games With a Purpose',
              year: 2019,
              institute: this.$t('contributors.fields.informatics'),
            },
            {
              author: 'Levushkina, Elena',
              title: 'Computerlinguistische Methoden in Community-basierten Anwendungen',
              year: 2014,
              institute: this.$t('contributors.fields.cis'),
            },
            {
              author: 'Scherz, Sabine',
              title: 'Kunstgeschichte berechnet. Interdisziplinäre Bilddatenanalyse crowdgesourcter Annotationen',
              year: 2017,
              institute: this.$t('contributors.fields.art-history'),
            },
            {
              author: 'Steinmayr, Bartholomäus',
              title: 'Designing Image Labeling Games for More Informative Tags',
              year: 2011,
              institute: this.$t('contributors.fields.informatics'),
            },
            {
              author: 'Tänzel, Tobias',
              title: 'Measuring Similarity of Artworks Using Multidimensional Data',
              year: 2017,
              institute: this.$t('contributors.fields.informatics'),
            },
            {
              author: 'Wieser, Christoph',
              title: 'Building a Semantic Search Engine with Games and Crowdsourcing',
              year: 2014,
              institute: this.$t('contributors.fields.informatics'),
            },
          ],
        },
      ];
    },
  },
};
</script>
