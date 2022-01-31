<template>
  <div style="text-align: right;">
    <v-chip
      v-for="tag in tagSizes"
      :key="tag.id"
      :title="tag.name"
      :style="{'font-size': tag.size + 'px'}"
      @click="search(tag.name)"
      class="mr-1 mb-1"
      color="primary"
      x-small
    >
     <span class="clip">{{ tag.name }}</span>
    </v-chip>
  </div>
</template>

<script>
import i18n from '@/plugins/i18n';

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
          size += 2;
        } else if (count > 9) {
          size += 4;
        } else if (count > 14) {
          size += 6;
        }
        if (language === i18n.locale) {
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
