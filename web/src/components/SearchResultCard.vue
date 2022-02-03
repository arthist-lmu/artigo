<template>
  <v-card
    :class="value ? 'disabled' : ''"
    flat
  >
    <v-card-text>
      <v-row>
        <v-col
          v-if="cols.tags > 0"
          :cols="cols.tags"
        >
          <TagCloud
            v-if="displayTags"
            :tags="tags"
          />
        </v-col>

        <v-col :cols="cols.image">
          <v-dialog
            v-model="showModal"
            max-width="750"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-img
                :src="entry.path"
                class="grey lighten-1"
                v-bind="attrs"
                v-on="on"
                v-on:error="onError"
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
            </template>

            <ResourceCard :entry="entry" />
          </v-dialog>
        </v-col>

        <v-col
          v-if="displayMetadata && cols.metadata > 0"
          :cols="cols.metadata"
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
import TagCloud from '@/components/TagCloud.vue';
import ResourceCard from '@/components/ResourceCard.vue';

export default {
  props: {
    entry: Object,
    value: Boolean,
    displayTags: Boolean,
    displayMetadata: Boolean,
  },
  data() {
    return {
      showModal: false,
    };
  },
  methods: {
    search(value, field) {
      const query = { [field]: value };
      this.$store.dispatch('search/post', { query });
    },
    onError() {
      this.$emit('input', true);
    },
  },
  computed: {
    cols() {
      if (!this.displayMetadata) {
        if (!this.displayTags) {
          return { tags: 0, image: 12, metadata: 0 };
        }
        return { tags: 6, image: 6, metadata: 0 };
      }
      return { tags: 3, image: 3, metadata: 6 };
    },
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
    ResourceCard,
  },
};
</script>

<style>
.v-image .v-responsive__content {
  width: 1000px !important;
}
</style>
