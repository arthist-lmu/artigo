<template>
  <v-card
    max-width="900"
    flat
  >
    <v-card-actions class="pa-0">
      <v-col cols="6">
        <v-btn
          @click="remove"
          tabindex="0"
          color="primary"
          depressed
          rounded
          block
        >
          {{ $t("collections.fields.remove") }}
        </v-btn>
      </v-col>

      <v-col cols="6">
        <v-btn
          @click="close"
          tabindex="0"
          depressed
          rounded
          block
        >
          {{ $t("field.abort") }}
        </v-btn>
      </v-col>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    entry: Object,
    value: Boolean,
    isDialog: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    remove() {
      const entry = { hash_id: this.entry.hash_id };
      this.$store.dispatch('collection/remove', entry).then(() => {
        this.$store.dispatch('collection/post');
        this.close();
      });
    },
    close() {
      this.$emit('input', false);
    },
  },
};
</script>
