<template>
  <v-card
    :class="disabled ? 'disabled' : ''"
    flat
  >
    <v-card-text>
      <v-row>
        <v-col
          v-if="displayTags"
          cols="3"
        >
          <TagCloud :tags="tags" />
        </v-col>

        <v-col cols="3">
          <v-img
            :src="entry.path"
            class="grey lighten-1"
            v-on:error="onError"
            @click="goToResource"
            style="cursor: pointer;"
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
        </v-col>

        <v-col
          v-if="displayMetadata"
          cols="6"
        >
          <v-row
            justify="space-around"
            no-gutters
          >
            <v-col
              class="align-center d-flex"
              cols="3"
            >
              <span class="capitalize">
                {{ $t("resource.metadata.fields.titles") }}
              </span>
            </v-col>

            <v-col cols="9">
              <v-chip
                v-for="title in titles"
                :key="title"
                :title="title"
                @click="search(title, 'titles')"
                class="mr-1 mb-2"
                outlined
              >
                <span class="clip">{{ title }}</span>
              </v-chip>
            </v-col>
          </v-row>

          <v-row
            justify="space-around"
            no-gutters
          >
            <v-col
              class="align-center d-flex"
              cols="3"
            >
              <span class="capitalize">
                {{ $t("resource.metadata.fields.creators") }}
              </span>
            </v-col>

            <v-col cols="9">
              <v-chip
                v-for="creator in creators"
                :key="creator"
                :title="creator"
                @click="search(creators, 'creators')"
                class="mr-1 mb-2"
                outlined
              >
                <span class="clip">{{ creator }}</span>
              </v-chip>
            </v-col>
          </v-row>

          <v-row
            v-for="(value, field) in metadata"
            :key="value"
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
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import router from '@/router/index';

import TagCloud from '@/components/TagCloud.vue';

export default {
  props: {
    entry: Object,
    displayTags: Boolean,
    displayMetadata: Boolean,
  },
  data() {
    return {
      disabled: false,
    };
  },
  methods: {
    search(value, field) {
      const query = { [field]: value };
      this.$store.dispatch('api/search', { query });
    },
    goToResource() {
      router.push({ name: 'resource', params: { id: this.entry.id } });
    },
    onError() {
      this.disabled = true;
    },
  },
  computed: {
    metadata() {
      const metadata = {};
      const fields = [
        'location',
        'institution',
        'source',
      ];
      this.entry.meta.forEach(({ name, value_str }) => {
        if (fields.includes(name) && value_str) {
          metadata[name] = value_str;
        }
      });
      return metadata;
    },
    titles() {
      const titles = [];
      this.entry.meta.forEach(({ name, value_str }) => {
        if (name === 'titles' && value_str) {
          titles.push(value_str);
        }
      });
      if (titles.length > 0) {
        return titles;
      }
      return [this.$t('resource.default.title')];
    },
    creators() {
      const creators = [];
      this.entry.meta.forEach(({ name, value_str }) => {
        if (name === 'creators' && value_str) {
          creators.push(value_str);
        }
      });
      if (creators.length > 0) {
        return creators;
      }
      return [this.$t('resource.default.creator')];
    },
    tags() {
      if (this.keyInObj('tags', this.entry)) {
        return this.entry.tags;
      }
      return [];
    },
  },
  components: {
    TagCloud,
  },
};
</script>

<style>
.v-card.disabled {
  display: none;
}

.v-image .v-responsive__content {
  width: 1000px !important;
}
</style>
