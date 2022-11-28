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
      :max-height="imageHeight"
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
      <div class="text-h5 max-w">
        <b>{{ title }}</b>

        <ReconcileButton
          :entries="[entry]"
          type="resource"
        />
      </div>

      <div class="text-h6 max-w grey--text">
        <span
          v-for="creator in creators"
          :key="creator"
          @click="search(creator, 'creators')"
          @keydown="search(creator, 'creators')"
          class="creator"
          style="cursor: pointer;"
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
          :title="tag.name"
          class="mr-1 mb-1"
          color="primary"
        >
          {{ tag.name }}

          <v-avatar
            v-if="tag.count > 1"
            :title="$t('resource.metadata.fields.has-tag', { tag: tag.name, n: tag.count })"
            class="primary lighten-1"
            right
          >
            {{ tag.count }}
          </v-avatar>
        </v-chip>

        <v-btn
          v-if="moreTags"
          @click="moreTags = false"
          class="mb-1"
          color="grey lighten-2"
          height="32"
          depressed
          small
          icon
        >
          <v-icon>mdi-tag-plus</v-icon>
        </v-btn>
        <v-btn
          v-else
          @click="moreTags = true"
          class="mb-1"
          color="grey lighten-2"
          height="32"
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
              color="grey lighten-2"
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
                cols="4"
              >
                <span class="capitalize">
                  {{ $t(`resource.metadata.fields.${field}`) }}
                </span>
              </v-col>

              <v-col cols="8">
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
      imageHeight: 500,
      moreTags: true,
      panels: [0],
    };
  },
  methods: {
    search(value, field) {
      const query = { [field]: value };
      this.$store.dispatch('search/post', { query });
    },
    setImageHeight() {
      this.imageHeight = window.innerHeight / 3;
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
          return Array.from(new Set(creators));
        }
      }
      return [this.$t('resource.default.creator')];
    },
    tags() {
      const tags = [];
      if (this.keyInObj('tags', this.entry)) {
        this.entry.tags.forEach(({
          id, language, name, count,
        }) => {
          if (
            language === this.$i18n.locale
            || language === undefined
          ) {
            if (count === undefined) count = 1;
            tags.push({ id, name, count });
          }
        });
        tags.sort((a, b) => b.count - a.count);
        if (this.moreTags && tags.length > 15) {
          return tags.slice(0, 15);
        }
      }
      return tags;
    },
  },
  mounted() {
    this.setImageHeight();
  },
  created() {
    window.addEventListener('resize', this.setImageHeight);
  },
  destroyed() {
    window.removeEventListener('resize', this.setImageHeight);
  },
  components: {
    ReconcileButton: () => import('@/components/ReconcileButton.vue'),
  },
};
</script>
