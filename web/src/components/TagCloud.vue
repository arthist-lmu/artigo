<template>
  <div class="tag-container">
    <v-chip
      v-for="tag in tagSizes"
      :key="tag.id"
      :title="tag.name"
      :style="{ 'font-size': tag.size + 'px' }"
      @click.stop="search(tag.name)"
      class="mr-1 mb-1"
      color="primary"
      x-small
    >
     <span class="clip">{{ tag.name }}</span>
    </v-chip>
  </div>
</template>

<script>
export default {
  props: {
    tags: Array,
  },
  methods: {
    search(value) {
      const query = { tags: value };
      this.$store.dispatch('search/post', { query });
    },
  },
  computed: {
    tagSizes() {
      const tags = [];
      this.tags.forEach(({
        id, language, name, count,
      }) => {
        let size = 12;
        if (count > 4) {
          size += 3;
        } else if (count > 9) {
          size += 6;
        } else if (count > 14) {
          size += 9;
        }
        if (
          language === this.$i18n.locale
          || language === undefined
        ) {
          tags.push({ id, name, size });
        }
      });
      if (tags.length > 10) {
        return tags.slice(0, 10);
      }
      return tags;
    },
  },
};
</script>

<style scoped>
.tag-container {
  white-space: break-spaces;
  max-height: 75px;
  overflow: hidden;
}

.v-chip.v-size--x-small {
  height: 20px;
}
</style>
