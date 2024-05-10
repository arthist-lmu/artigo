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
        <v-expansion-panel-title>
          {{ item.group }}
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <v-row
            v-for="value in item.values"
            :key="value.title"
          >
            <v-col
              v-if="!mdAndDown"
              cols="auto"
            >
              <v-avatar
                color="surface"
                size="36"
              >
                <span v-if="value.author">
                  {{ value.author.slice(0, 2) }}
                </span>
              </v-avatar>
            </v-col>

            <v-col>
              {{ getAuthorAndYear(value) }}

              <template v-if="value.url">
                <a
                  :href="value.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  style="color: #000;"
                >
                  {{ value.title }}
                </a>

                <v-icon
                  class="ml-1"
                  size="x-small"
                >
                  mdi-link-variant
                </v-icon>
              </template>
              <template v-else>
                {{ value.title }}
              </template>

              {{ getJournalAndPages(value) }}
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const { mdAndDown } = useDisplay()

const panels = defineModel('panels', {
  type: Array,
  default: [0]
})

function getAuthorAndYear(publication) {
  const { author, year } = publication
  let text = author
  if (year) {
    text += ` (${year})`
  }
  text += ': '
  return text
}
function getJournalAndPages(publication) {
  const { journal, institute, pages } = publication
  let text = ''
  if (journal) {
    text += `, in: ${journal}`
  }
  if (institute) {
    text += `, ${institute}`
  }
  if (pages) {
    text += `, ${pages}`
  }
  text += '.'
  return text
}

const items = computed(() => {
  return [
    {
      group: t('publications.fields.journals'),
      values: [
        {
          author: 'Bry, François; Schefels, Clemens; Schemainda, Corina',
          title: 'Eine qualitative Analyse der ARTigo-Annotationen',
          year: 2018,
          journal: 'Computing Art Reader. Einführung in die digitale Kunstgeschichte',
          pages: '96–114',
          url: 'https://books.ub.uni-heidelberg.de/arthistoricum/catalog/book/413/c5771'
        },
        {
          author: 'Bry, François; Wieser, Christoph',
          title: 'Squaring and Scripting the ESP Game. Trimming a GWAP to Deep Semantics',
          year: 2012,
          journal: 'SGDA 2012. Serious Games Development and Applications',
          pages: '183–192',
          url: 'https://link.springer.com/chapter/10.1007%2F978-3-642-33687-4_16'
        },
        {
          author: 'Commare, Laura',
          title: 'Social Tagging als Methode zur Optimierung Kunsthistorischer Bilddatenbanken. Eine empirische Analyse des Artigo-Projekts',
          year: 2011,
          journal: 'Kunstgeschichte. Open Peer Reviewed Journal',
          url: 'https://www.kunstgeschichte-ejournal.net/160/'
        },
        {
          author: 'Kohle, Hubertus',
          title: 'Social Tagging von Kunstwerken oder: Wie bringe ich junge Leute dazu, ins Museum zu gehen',
          year: 2009,
          journal: 'Museum aktuell 161',
          pages: '14–15',
          url: 'http://www.play4science.uni-muenchen.de/docs/social_tag_kunstw.pdf'
        },
        {
          author: 'Kohle, Hubertus',
          title: 'Artigo. Social image tagging pour les oeuvres d\'art',
          year: 2010,
          journal: 'L’art et la mesure. Histoire de l’art et méthodes quantitatives',
          pages: '153–164',
          url: 'https://d-nb.info/1208768840/34'
        },
        {
          author: 'Kohle, Hubertus',
          title: 'Kunstgeschichte goes Social Media. Laien optimieren eine Bilddatenbank – mit einem digitalen Spiel',
          year: 2011,
          journal: 'Aviso. Zeitschrift für Wissenschaft und Kunst in Bayern 3',
          pages: '37–43',
          url: 'http://www.km.bayern.de/download/9324_aviso_2011_3.pdf'
        },
        {
          author: 'Kohle, Hubertus',
          title: 'Social Tagging in the Humanities and the Nature of the Internet Workflow',
          year: 2011,
          journal: 'Kunstgeschichte. Open Peer Reviewed Journal',
          url: 'http://www.kunstgeschichte-ejournal.net/229/'
        },
        {
          author: 'Kohle, Hubertus',
          title: 'The Wisdom of Crowds',
          year: 2016,
          journal: 'On_Culture. The Open Journal for the Study of Culture',
          url: 'http://geb.uni-giessen.de/geb/volltexte/2016/12072/pdf/On_Culture_1_Kohle.pdf'
        },
        {
          author: 'Schefels, Clemens',
          title: 'Eine offene Universität für eine offene Gesellschaft',
          year: 2016,
          journal: 'oead\'news 101',
          pages: '22–23',
          url: 'https://schefels.de/research/schefels_-_eine_offene_Universitaet_fuer_eine_offene_gesellschaft.pdf'
        },
        {
          author: 'Schneider, Stefanie; Kohle, Hubertus',
          title: 'The Computer as Filter Machine. A Clustering Approach to Categorize Artworks Based on a Social Tagging Network',
          year: 2017,
          journal: 'Artl@s Bulletin 6.3',
          pages: '81–89',
          url: 'https://docs.lib.purdue.edu/artlas/vol6/iss3/6/'
        },
        {
          author: 'Schneider, Stefanie; Kristen, Maximilian; Vollmer, Ricarda',
          title: 'Re: ARTigo. Neuentwurf eines Social-Tagging-Frameworks aus funktionalen Programmbausteinen',
          year: 2023,
          journal: 'DHd 2023. Open Humanities, Open Culture. Konferenzabstracts',
          pages: '173–178',
          url: 'https://doi.org/10.5281/zenodo.7688632'
        },
        {
          author: 'Shah, Philipp; Wieser, Christoph; Bry, François',
          title: 'Parallel Higher-Order SVD for Tag-Recommendations',
          year: 2012,
          journal: 'IADIS International Conference WWW/Internet 2012',
          pages: '257–265',
          url: 'http://www.iadisportal.org/digital-library/mdownload/parallel-higher-order-svd-for-tag-recommendations'
        },
        {
          author: 'Steinmayr, Bartholomäus; Wieser, Christoph; Kneißl, Fabian; Bry, François',
          title: 'Karido. A GWAP for Telling Artworks Apart',
          year: 2011,
          journal: '16th International Conference on Computer Games (CGAMES)',
          pages: '193–200',
          url: 'https://www.en.pms.ifi.lmu.de/publications/PMS-FB/PMS-FB-2011-4/PMS-FB-2011-4-paper.pdf'
        },
        {
          author: 'Wieser, Christoph, Bry, François, Bérard, Alexandre und Lagrange, Richard',
          title: 'ARTigo. Building an Artwork Search Engine With Games and Higher-Order Latent Semantic Analysis',
          year: 2013,
          journal: 'Proceedings of Disco 2013. Workshop on Human Computation and Machine Learning in Games',
          url: 'http://www.en.pms.ifi.lmu.de/publications/PMS-FB/PMS-FB-2013-3/PMS-FB-2013-3-paper.pdf'
        }
      ]
    },
    {
      group: t('publications.fields.theses'),
      values: [
        {
          author: 'Bogner, Martin',
          title: 'Conception and Implementation of a Collaborative Data Science Platform',
          year: 2016,
          institute: t('contributors.fields.informatics'),
          url: 'https://www.en.pms.ifi.lmu.de/publications/diplomarbeiten/Martin.Bogner/MA_Martin.Bogner.pdf'
        },
        {
          author: 'Greth, Nicola',
          title: 'Automatic Semantic Categorization of Image Annotations Generated by Games With a Purpose',
          year: 2019,
          institute: t('contributors.fields.informatics'),
          url: 'https://www.en.pms.ifi.lmu.de/publications/diplomarbeiten/Nicola.Greth/MA_Nicola.Greth.pdf'
        },
        {
          author: 'Levushkina, Elena',
          title: 'Computerlinguistische Methoden in Community-basierten Anwendungen',
          year: 2014,
          institute: t('contributors.fields.cis')
        },
        {
          author: 'Scherz, Sabine',
          title: 'Kunstgeschichte berechnet. Interdisziplinäre Bilddatenanalyse crowdgesourcter Annotationen',
          year: 2017,
          institute: t('contributors.fields.artHistory'),
          url: 'https://edoc.ub.uni-muenchen.de/21465/'
        },
        {
          author: 'Steinmayr, Bartholomäus',
          title: 'Designing Image Labeling Games for More Informative Tags',
          year: 2011,
          institute: t('contributors.fields.informatics'),
          url: 'https://www.en.pms.ifi.lmu.de/publications/diplomarbeiten/Bartholomaeus.Steinmayr/DA_Bartholomaeus.Steinmayr.pdf'
        },
        {
          author: 'Tänzel, Tobias',
          title: 'Measuring Similarity of Artworks Using Multidimensional Data',
          year: 2017,
          institute: t('contributors.fields.informatics'),
          url: 'https://www.en.pms.ifi.lmu.de/publications/diplomarbeiten/Tobias.Taenzel/MA_Tobias.Taenzel.pdf'
        },
        {
          author: 'Wieser, Christoph',
          title: 'Building a Semantic Search Engine with Games and Crowdsourcing',
          year: 2014,
          institute: t('contributors.fields.informatics'),
          url: 'https://edoc.ub.uni-muenchen.de/16975/1/Wieser_Christoph.pdf'
        }
      ]
    }
  ]
})
</script>
