<template>
  <v-card
    max-width="450"
    flat
  >
    <v-card-title v-if="isDialog">
      {{ $t("search.title") }}

      <v-btn
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="isDialog ? '' : 'pt-0 px-0'">
      <v-form v-model="isFormValid">
        <v-combobox
          v-for="field in fields"
          :key="field.key"
          v-model="query[field.key]"
          :placeholder="$t('resource.metadata.fields')[field.key]"
          hide-details
          clearable
          multiple
          chips
        >
          <template v-slot:selection="data">
            <v-chip
              color="primary"
              outlined
              close
            >
              {{ data.item }}
            </v-chip>
          </template>
        </v-combobox>
      </v-form>
    </v-card-text>

    <v-card-actions :class="isDialog ? 'pt-8 pb-6 px-6' : 'pb-8 px-0'">
      <v-btn
        @click="search"
        :disabled="!isFormValid"
        color="accent"
        depressed
        rounded
        block
      >
        {{ $t("search.title") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import router from '@/router/index';

export default {
  props: {
    isDialog: Boolean,
    value: Boolean,
  },
  data() {
    return {
      isFormValid: false,
      query: {},
      fields: [
        { key: 'titles', icon: 'mdi-' },
        { key: 'creators', icon: 'mdi-account' },
        { key: 'date', icon: 'mdi-clock' },
        { key: 'location', icon: 'mdi-map-marker' },
        { key: 'tags', icon: 'mdi-tag-multiple' },
      ],
    };
  },
  methods: {
    search() {
      this.$store.dispatch('api/search', { 'query': this.query });
      this.close();
      this.query = {};
      router.push({ name: 'search' });
    },
    close() {
      this.$emit('input', false);
    },
  },
};
</script>

<style>
.v-autocomplete:not(.v-input--is-focused).v-select--chips input {
  max-height: 25px !important;
}
</style>
