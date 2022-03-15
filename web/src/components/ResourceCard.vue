<template>
  <v-card
    v-bind="computedProps"
    v-on="listeners$"
    flat
  >
    <v-img
      v-if="showImage"
      :src="entry.path"
      class="grey lighten-2"
      max-height="500px"
      contain
    >
      <template v-slot:placeholder>
        <v-row
          class="fill-height ma-0"
          justify="center"
          align="center"
        >
          <v-progress-circular indeterminate />
        </v-row>
      </template>
    </v-img>

    <v-card-title class="mb-2">
      <div class="text-h5 max-w mb-1">
        {{ title }}

        <ReconcileButton
          :entries="[entry]"
          type="resource"
        />
      </div>

      <div class="text-h6 max-w grey--text">
        <span
          v-for="creator in creators"
          :key="creator"
          class="creator"
        >
          {{ creator }}

          <ReconcileButton
            :entries="[entry]"
            type="creator"
          />
        </span>
      </div>
    </v-card-title>

    <v-card-text>
      <div
        v-if="tags.length"
        class="mb-2"
      >
        <v-chip
          v-for="tag in tags"
          :key="tag.id"
          @click="search(tag.name, 'tags')"
          class="mr-1 mb-2"
          outlined
        >
          <span :title="tag.name">
            {{ tag.name }}
          </span>
        </v-chip>

        <v-btn
          v-if="moreTags"
          @click="moreTags = false"
          class="mb-2"
          color="grey lighten-2"
          depressed
          small
          icon
        >
          <v-icon>mdi-tag-plus</v-icon>
        </v-btn>
        <v-btn
          v-else
          @click="moreTags = true"
          class="mb-2"
          color="grey lighten-2"
          depressed
          small
          icon
        >
          <v-icon>mdi-tag-minus</v-icon>
        </v-btn>
      </div>

      <v-expansion-panels
        v-model="panels"
        accordion
        multiple
        flat
      >
        <v-expansion-panel
          v-if="Object.keys(metadata).length"
          class="mb-n2"
        >
          <v-expansion-panel-header class="pa-0">
            <v-icon
              class="mr-3"
              size="18"
            >
              mdi-information-outline
            </v-icon>

            <span class="text-subtitle-1">
              {{ $t("resource.metadata.title") }}
            </span>
          </v-expansion-panel-header>

          <v-expansion-panel-content>
            <v-row
              v-for="(value, field) in metadata"
              :key="`${field}:${value}`"
              class="mb-2"
              justify="space-around"
              no-gutters
            >
              <v-col
                class="align-center d-flex"
                cols="3"
              >
                <span class="capitalize">
                  {{ $t("resource.metadata.fields")[field] }}
                </span>
              </v-col>

              <v-col cols="9">
                <v-chip
                  :title="value"
                  @click="search(value, field)"
                  class="mr-1"
                  outlined
                >
                  <span class="clip">{{ value }}</span>
                </v-chip>
              </v-col>
            </v-row>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<script>
import { VCard } from 'vuetify/lib';

export default {
  extends: VCard,
  props: {
    ...VCard.props,
    entry: Object,
    showImage: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      ...VCard.data,
      moreTags: true,
      panels: [0],
    };
  },
  methods: {
    search(value, field) {
      const query = { [field]: value };
      this.$store.dispatch('search/post', { query });
    },
  },
  computed: {
    computedProps() {
      return { ...this.$props };
    },
    metadata() {
      const metadata = {};
      const fields = [
        'location',
        'institution',
        'source',
      ];
      if (this.keyInObj('meta', this.entry)) {
        this.entry.meta.forEach(({ name, value_str }) => {
          if (fields.includes(name) && value_str) {
            metadata[name] = value_str;
          }
        });
        if (this.entry.source && this.entry.source.id) {
          metadata.source = this.entry.source.name;
        }
      }
      return metadata;
    },
    title() {
      const titles = [];
      if (this.keyInObj('meta', this.entry)) {
        this.entry.meta.forEach(({ name, value_str }) => {
          if (name === 'titles' && value_str) {
            titles.push(value_str);
          }
        });
        if (titles.length > 0) {
          return titles[0];
        }
      }
      return this.$t('resource.default.title');
    },
    creators() {
      const creators = [];
      if (this.keyInObj('meta', this.entry)) {
        this.entry.meta.forEach(({ name, value_str }) => {
          if (name === 'creators' && value_str) {
            creators.push(value_str);
          }
        });
        if (creators.length > 0) {
          return creators;
        }
      }
      return [this.$t('resource.default.creator')];
    },
    tags() {
      if (this.keyInObj('tags', this.entry)) {
        const tags = [];
        this.entry.tags.forEach(({
          id, language, name, count,
        }) => {
          if (language === this.$i18n.locale) {
            tags.push({ id, name, count });
          }
        });
        if (this.moreTags && tags.length > 20) {
          return tags.slice(0, 20);
        }
        return tags;
      }
      return [];
    },
  },
  components: {
    ReconcileButton: () => import('@/components/ReconcileButton.vue'),
  },
};
</script>

<style>
.v-card .max-w {
  width: 100%;
}

.v-card .v-expansion-panel-header > :not(.v-expansion-panel-header__icon) {
  flex: initial;
}
</style>
