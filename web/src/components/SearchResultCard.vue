<template>
  <v-hover v-slot="{ hover }">
    <div
      @click="showDialog"
      @keyDown="showDialog"
      class="grid-item"
      :disabled="isDisabled"
      :style="getCss"
    >
      <img
        :src="entry.path"
        v-on:error="onError"
        v-on:load="onLoad"
        alt=""
      />

      <v-fade-transition>
        <div
          v-if="isLoaded && (hover || selected)"
          class="overlay"
        >
          <div class="pa-4">
            <TagCloud :tags="tags" />
          </div>

          <div class="metadata pa-4">
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
          </div>
        </div>
      </v-fade-transition>
    </div>
  </v-hover>
</template>

<script>
import tool from '@/mixins/resource';

export default {
  mixins: [tool],
  data() {
    return {
      width: 'auto',
      height: '225px',
    };
  },
  computed: {
    selected() {
      return Math.random() < 0.15;
    },
    getCss() {
      return {
        height: this.height,
        width: this.width,
        cursor: 'pointer',
      };
    },
  },
  components: {
    TagCloud: () => import('@/components/TagCloud.vue'),
  },
};
</script>

<style>
.grid-item {
  border-radius: 28px;
  position: relative;
  overflow: hidden;
  min-width: 80px;
  display: block;
  flex-grow: 1;
}

.grid-item[disabled] {
  display: none;
}

.grid-item > img {
  transition: transform 0.5s ease;
  transform: scale(1.05);
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  height: 100%;
}

.grid-item:hover > img {
  transform: scale(1.3);
}

.grid-item > .overlay {
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

.grid-item > .overlay .metadata {
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
}

.grid-item > .overlay .metadata * {
  text-overflow: ellipsis;
  line-height: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}

.grid-item > .overlay span:not(:first-child):before {
  content: ", ";
}
</style>
