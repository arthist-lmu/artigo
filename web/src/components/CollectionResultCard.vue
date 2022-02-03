<template>
  <div
    class="grid-item"
    @click="showModal = true;"
  >
    <v-dialog
      v-model="showModal"
      max-width="750"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-img
          :src="entry.path"
          class="grey lighten-2"
          height="200"
          v-bind="attrs"
          v-on="on"
          v-on:error="onError"
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
      </template>

      <ResourceCard :entry="entry" />
    </v-dialog>

    <div class="overlay">
      <div class="meta">
        <div
          class="text-subtitle-1"
          :title="title"
        >
          {{ title }}
        </div>

        <div
          class="text-caption"
          :title="creators"
        >
          {{ creators }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ResourceCard from '@/components/ResourceCard.vue';

export default {
  props: {
    entry: Object,
    value: Boolean,
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
    title() {
      const titles = [];
      this.entry.meta.forEach(({ name, value_str }) => {
        if (name === 'titles' && value_str) {
          titles.push(value_str);
        }
      });
      if (titles.length > 0) {
        return titles[0];
      }
      return this.$t('resource.default.title');
    },
    creators() {
      const creators = [];
      this.entry.meta.forEach(({ name, value_str }) => {
        if (name === 'creators' && value_str) {
          creators.push(value_str);
        }
      });
      if (creators.length > 0) {
        return creators.join(', ');
      }
      return this.$t('resource.default.creator');
    },
  },
  components: {
    ResourceCard,
  },
};
</script>

<style>
.v-image .v-responsive__content {
  width: 1000px !important;
}
</style>

<style scoped>
.grid-item {
  cursor: pointer;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
  min-width: 80px;
  display: block;
  flex-grow: 1;
  margin: 2px;
}

.grid-item > img {
  transition: transform 0.5s ease;
  transform: scale(1.05);
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  height: 100%;
  opacity: 1;
}

.grid-item:hover > img {
  transform: scale(1.4);
}

.grid-item:hover > .overlay {
  opacity: 1;
}

.grid-item > .overlay {
  background: linear-gradient(to top, black, #00000000 50%);
  transform: translate(-50%, -50%);
  transition: opacity 0.25s ease;
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #ffffff;
  height: 100%;
  opacity: 0;
  left: 50%;
  top: 50%;
}

.grid-item > .overlay .meta {
  position: absolute;
  padding: 5px 10px;
  width: 100%;
  bottom: 0;
  left: 0;
}

.grid-item > .overlay .meta * {
  text-transform: capitalize;
  text-overflow: ellipsis;
  line-height: 1.35rem;
  white-space: nowrap;
  overflow: hidden;
  font-weight: 400;
}
</style>
