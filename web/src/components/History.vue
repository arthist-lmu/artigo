<template>
  <v-timeline :dense="$vuetify.breakpoint.smAndDown">
    <v-timeline-item
      v-for="(item, i) in items"
      :key="i"
      :icon="item.icon"
      :color="item.color"
      :small="!item.icon"
    >
      <template v-slot:opposite>
        <v-row :justify="i % 2 !== 0 ? 'start' : 'end'">
          <v-col
            cols="5"
            :order="i % 2 === 0 ? 1 : 2"
            align-self="center"
          >
            <v-dialog max-width="750">
              <template v-slot:activator="{ on, attrs }">
                <v-card
                  v-if="item.image"
                  class="grid-item"
                  flat
                >
                  <img
                    v-bind="attrs"
                    v-on="on"
                    :src="item.image"
                    alt=""
                  />
                </v-card>
              </template>

              <v-card flat>
                <v-img
                  :src="item.image"
                  alt=""
                />
              </v-card>
            </v-dialog>
          </v-col>

          <v-col
            cols="auto"
            :order="i % 2 !== 0 ? 1 : 2"
            align-self="center"
            align="end"
          >
            <span class="font-weight-bold white--text">
              {{ item.year }}
            </span>
          </v-col>
        </v-row>
      </template>

      <div class="py-4">
        <div
          v-if="$vuetify.breakpoint.smAndDown"
          class="mb-4 font-weight-bold white--text"
        >
          {{ item.year }}
        </div>

        <div
          class="font-weight-light white--text"
          v-html="item.text"
        />
      </div>
    </v-timeline-item>
  </v-timeline>
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          year: '2008–2009',
          text: this.$t('history.texts.2008'),
          image: '/assets/images/artigo-version-2008.png',
        },
        {
          year: '2010–2013',
          icon: 'mdi-rocket-launch-outline',
          text: this.$t('history.texts.2010'),
          image: '/assets/images/artigo-version-2010.png',
        },
        {
          year: '2012',
          text: this.$t('history.texts.2012'),
        },
        {
          year: '2018–2019',
          text: this.$t('history.texts.2018'),
          image: '/assets/images/stadt-land-bild.png',
        },
        {
          year: '2021–2022',
          icon: 'mdi-star-outline',
          text: this.$t('history.texts.2021'),
        },
      ];
    },
  },
};
</script>

<style>
.v-timeline-item__body {
  align-self: center !important;
}
</style>

<style scoped>
.grid-item {
  position: relative;
  overflow: hidden;
}

.grid-item > img {
  transition: all 0.5s ease;
  filter: grayscale(100%);
  transform: scale(1.05);
  object-position: top;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  display: block;
  height: 100%;
}

.grid-item:hover > img {
  transform: scale(1.3);
  filter: grayscale(0%);
}
</style>
