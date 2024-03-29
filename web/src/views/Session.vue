<template>
  <v-container :class="{ 'px-0': $vuetify.breakpoint.mdAndDown }">
    <v-row class="mt-2 mx-n3">
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 4">
        <SummaryCard
          icon="mdi-image-outline"
          :title="$t('session.fields.images')"
          :value="entries.length"
        />
      </v-col>

      <v-col
        :cols="$vuetify.breakpoint.smAndDown ? 12 : 4"
        :class="$vuetify.breakpoint.smAndDown ? 'pt-0' : undefined"
      >
        <SummaryCard
          icon="mdi-tag-outline"
          :title="$t('session.fields.tags')"
          :subtitle="$t('session.fields.per-image')"
          :value="tags.length"
          :subvalue="tags.length / entries.length"
        />
      </v-col>

      <v-col
        :cols="$vuetify.breakpoint.smAndDown ? 12 : 4"
        :class="$vuetify.breakpoint.smAndDown ? 'pt-0' : undefined"
      >
        <SummaryCard
          icon="mdi-star-outline"
          :title="$t('session.fields.score')"
          :subtitle="$t('session.fields.per-image')"
          :value="score"
          :subvalue="score / entries.length"
        />
      </v-col>
    </v-row>

    <v-row
      v-if="tags.length"
      class="mt-0 mb-n2"
    >
      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 9 : 10">
        <v-slide-group
          v-model="slides"
          :title="$t('session.fields.filter-tags')"
          center-active
          show-arrows
          multiple
        >
          <v-slide-item
            v-for="tag in uniqueTags"
            :key="tag"
            v-slot="{ active, toggle }"
          >
            <v-chip
              @click="toggle"
              :color="active ? 'primary' : undefined"
              class="mx-1"
              depressed
              outlined
              rounded
            >
              {{ tag }}
            </v-chip>
          </v-slide-item>
        </v-slide-group>
      </v-col>

      <v-col
        :cols="$vuetify.breakpoint.mdAndDown ? 3 : 2"
        align="right"
      >
        <v-btn
          @click="dialog.score = true"
          :title="$t('user.score.title')"
          icon
        >
          <v-icon>
            mdi-trophy-outline
          </v-icon>
        </v-btn>

        <v-btn
          @click="share"
          class="ml-2"
          icon
        >
          <v-icon>
            mdi-share-variant-outline
          </v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-row class="mx-n1 mt-7">
      <v-slide-group
        class="resource"
        show-arrows
      >
        <v-slide-item
          v-for="entry in entries"
          :key="entry.resource_id"
          v-slot="{ active, toggle }"
        >
          <div
            class="pa-1"
            style="width: 300px"
          >
            <OverviewResultCard
              :entry="entry"
              height="350"
              :opaque="!selectedEntries.includes(entry.resource_id)"
            />
          </div>
        </v-slide-item>
      </v-slide-group>
    </v-row>

    <v-dialog
      v-model="dialog.score"
      max-width="450"
      scrollable
    >
      <ScoreCard v-model="dialog.score" />
    </v-dialog>

    <v-dialog
      v-model="dialog.helper"
      max-width="400"
    >
      <HelperCard
        v-model="dialog.helper"
        :text="$t('user.score.helper')"
        icon="mdi-account-circle-outline"
      >
        <template v-slot:button>
          <v-btn
            @click="dialog.score = true; dialog.helper = false"
            tabindex="0"
            color="primary"
            depressed
            rounded
            block
          >
            {{ $t("user.score.title") }}
          </v-btn>
        </template>
      </HelperCard>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      slides: [],
      dialog: {
        score: false,
        helper: false,
      },
    };
  },
  methods: {
    get(id) {
      this.$store.dispatch('session/get', { id });
    },
    share() {
      const input = document.createElement('input');
      document.body.appendChild(input);
      input.value = window.location.href;
      input.select();
      document.execCommand('copy');
      document.body.removeChild(input);
      const message = {
        details: ['copied_to_clipboard'],
        timestamp: new Date(),
      };
      this.$store.dispatch('utils/setMessage', message);
    },
  },
  computed: {
    entries() {
      return this.$store.state.session.data || [];
    },
    selectedEntries() {
      let entries = [...this.entries];
      if (this.selectedTags.length) {
        entries = entries.filter((entry) => {
          if (entry.tags) {
            const tags = entry.tags.map(({ name }) => name);
            return tags.some((tag) => this.selectedTags.includes(tag));
          }
          return false;
        });
      }
      return entries.map(({ resource_id }) => resource_id);
    },
    tags() {
      const values = this.entries.map(({ tags }) => tags);
      return values.filter((tag) => tag).flat();
    },
    uniqueTags() {
      const names = this.tags.map(({ name }) => name);
      return [...new Set(names)];
    },
    selectedTags() {
      return this.slides.map((i) => this.uniqueTags[i]);
    },
    score() {
      const scores = this.tags.map(({ score }) => score);
      return scores.reduce((x, y) => x + y, 0);
    },
    newGameCols() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 11;
        default: return 'auto';
      }
    },
    shareCols() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 1;
        default: return 'auto';
      }
    },
  },
  watch: {
    '$route.params.id'(id) {
      this.get(id);
    },
  },
  created() {
    this.get(this.$route.params.id);
    if (localStorage.getItem('scoreHelper') === null) {
      localStorage.setItem('scoreHelper', true);
      this.dialog.helper = true;
    }
  },
  components: {
    ScoreCard: () => import('@/components/account/ScoreCard.vue'),
    SummaryCard: () => import('@/components/session/SummaryCard.vue'),
    OverviewResultCard: () => import('@/components/session/OverviewResultCard.vue'),
    HelperCard: () => import('@/components/HelperCard.vue'),
  },
};
</script>

<style>
.resource.v-item-group .v-slide-group__prev,
.resource.v-item-group .v-slide-group__next {
  background-color: rgba(247, 248, 251, 0.85);
  position: absolute;
  height: 100%;
  z-index: 99;
}

.resource.v-item-group .v-slide-group__prev {
  left: 0;
}

.resource.v-item-group .v-slide-group__next {
  right: 0;
}
</style>
