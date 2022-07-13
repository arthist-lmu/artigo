<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :disabled="disabled"
      flat
    >
      <v-img
        @click="showDialog"
        @keyDown="showDialog"
        :src="entry.path"
        v-on:error="onError"
        v-on:load="onLoad"
        style="cursor: pointer;"
        class="grey lighten-2"
        :height="height"
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

        <v-btn
          color="primary"
          style="min-width: 50px !important;"
          depressed
          absolute
          rounded
          bottom
          right
        >
          <v-icon left>
            mdi-tag-outline
          </v-icon>

          {{ tags.length }}
        </v-btn>

        <v-fade-transition>
          <div v-if="isLoaded && hover">
            <div class="pa-4">
              <TagCloud :tags="tags" />
            </div>
          </div>
        </v-fade-transition>
      </v-img>

      <v-card-title class="metadata">
        <div
          class="text-subtitle-1"
          :title="title"
        >
          <b>{{ title }}</b>
        </div>

        <div class="text-caption">
          <span
            v-for="creator in creators"
            :key="creator"
            :title="creator"
          >
            {{ creator }}
          </span>
        </div>
      </v-card-title>
    </v-card>
  </v-hover>
</template>

<script>
import tool from '@/mixins/resource';

export default {
  mixins: [tool],
  props: {
    height: {
      type: String,
      default: '225',
    },
  },
  computed: {
    score() {
      const scores = this.tags.map(({ score }) => score);
      return scores.reduce((x, y) => x + y, 0);
    },
  },
  components: {
    TagCloud: () => import('@/components/TagCloud.vue'),
  },
};
</script>

<style scoped>
.metadata,
.metadata > div {
  width: 100%;
}

.metadata * {
  text-overflow: ellipsis;
  line-height: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}

.metadata span:not(:first-child):before {
  content: ", ";
}
</style>
