<template>
  <v-hover
    v-if="!isDisabled"
    v-slot="{ hover }"
  >
    <div
      @click="showDialog"
      @keyDown="showDialog"
      class="grid-item"
      :disabled="isDisabled"
    >
      <img
        :src="entry.path"
        v-on:error="onError"
        v-on:load="onLoad"
        alt=""
      />

      <v-fade-transition>
        <v-container
          v-if="isLoaded && (hover || selected)"
          class="overlay"
        >
          <v-row style="flex: 0;">
            <v-col class="tags pa-4">
              <TagCloud :tags="tags" />
            </v-col>
          </v-row>

          <v-row></v-row>

          <v-row style="flex: 0;">
            <v-col class="pa-4">
              <div
                class="text-subtitle-1 white--text"
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
            </v-col>
          </v-row>
        </v-container>
      </v-fade-transition>
    </div>
  </v-hover>
</template>

<script>
import tool from '@/mixins/resource';

export default {
  mixins: [tool],
  computed: {
    selected() {
      return Math.random() < 0.15;
    },
  },
  components: {
    TagCloud: () => import('@/components/TagCloud.vue'),
  },
};
</script>

<style scoped>
.grid-item {
  border-radius: 28px;
  position: relative;
  overflow: hidden;
  min-width: 80px;
  cursor: pointer;
  display: block;
  height: 225px;
  flex-grow: 1;
}

.grid-item[disabled] {
  display: none;
}

.grid-item > img {
  transition: transform 0.5s ease;
  transform: scale(1.05);
  object-position: top;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  height: 100%;
}

.grid-item:hover > img {
  transform: scale(1.3);
}

.container {
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
}

.container {
  flex-direction: column;
  display: flex;
  height: 100%;
}

.container .overlay {
  background: linear-gradient(to top, black, #00000000 40%);
  transform: translate(-50%, -50%);
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #ffffff;
  height: 100%;
  left: 50%;
  top: 50%;
}

.container .overlay .col:not(.tags) > * {
  text-overflow: ellipsis;
  line-height: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}

.container .overlay span:not(:first-child):before {
  content: ", ";
}
</style>
