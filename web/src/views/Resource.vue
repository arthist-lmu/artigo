<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <v-card v-if="Object.keys(data).length">
            <v-img
              :src="data.path"
              class="grey lighten-1"
              max-height="500px"
              contain
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" justify="center" align="center">
                  <v-progress-circular indeterminate></v-progress-circular>
                </v-row>
              </template>
            </v-img>

            <v-card-title class="mb-2">
              <div class="text-h5 max-w mb-1">
                {{ title.name }}
              </div>

              <div class="text-h6 max-w grey--text">
                {{ creator.name }}
              </div>
            </v-card-title>

            <v-card-text>
              <div v-if="tags.length" class="mb-2">
                <v-chip
                  v-for="tag in tags"
                  :key="tag.id"
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

              <v-expansion-panels v-model="panels" accordion multiple flat>
                <v-expansion-panel v-if="Object.keys(metadata).length">
                  <v-expansion-panel-header class="pa-0">
                    <v-icon class="mr-3" size="18">
                      mdi-information-outline
                    </v-icon>

                    <span class="text-subtitle-1">
                      {{ $t("resource.metadata.title") }}
                    </span>
                  </v-expansion-panel-header>

                  <v-expansion-panel-content>
                    <v-row
                      v-for="(values, field) in metadata"
                      :key="values"
                      justify="space-around"
                      no-gutters
                    >
                      <v-col cols="3">
                        <span class="capitalize">
                          {{ $t("resource.metadata.fields")[field] }}
                        </span>
                      </v-col>

                      <v-col cols="9">
                        <v-chip
                          v-for="value in values"
                          :key="value"
                          :title="value.name"
                          class="mr-1 mb-2"
                          outlined
                        >
                          {{ value.name }}
                        </v-chip>
                      </v-col>
                    </v-row>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  data() {
    return {
      moreTags: true,
      panels: [0],
    };
  },
  methods: {
    getData(id) {
      const lang = this.$i18n.locale;
      this.$store.dispatch("resource/get", { id, lang });
    },
  },
  computed: {
    data() {
      return this.$store.state.resource.data;
    },
    metadata() {
      const metadata = {};
      const fields = [
        "titles",
        "creators",
        "location",
        "institution",
        "source",
      ];
      Object.keys(this.data).forEach((key) => {
        if (fields.includes(key)) {
          let values = this.data[key];
          if (values && typeof values !== "boolean") {
            if (typeof values === "string") {
              values = [{ name: values }];
            } else if (!this.isArray(values)) {
              values = [values];
            }
            if (this.isArray(values)) {
              metadata[key] = values;
            }
          }
        }
      });
      return metadata;
    },
    title() {
      if (this.keyInObj("titles", this.metadata)) {
        return this.metadata.titles[0];
      }
      return { id: -1, name: this.$t("resource.default.title") };
    },
    creator() {
      if (this.keyInObj("creators", this.metadata)) {
        return this.metadata.creators[0];
      }
      return { id: -1, name: this.$t("resource.default.creator") };
    },
    tags() {
      if (this.keyInObj("tags", this.data)) {
        if (this.moreTags && this.data.tags.length > 20) {
          return this.data.tags.slice(0, 20);
        }
        return this.data.tags;
      }
      return [];
    },
  },
  watch: {
    "$route.params.id": function (id) {
      this.getData(id);
    },
    data() {
      document.title = `${this.title.name} | ${APP_NAME}`;
    },
  },
  created() {
    this.getData(this.$route.params.id);
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

.v-card .v-expansion-panel-content__wrap {
  padding: 0;
}
</style>
