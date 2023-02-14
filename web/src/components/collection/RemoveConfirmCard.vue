<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
  >
    <template v-slot:actions>
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
    </template>
  </Card>
</template>

<script>
import Card from '@/components/utils/Card.vue';

export default {
  extends: Card,
  props: {
    entry: Object,
    ...Card.props,
  },
  methods: {
    remove() {
      const entry = { hash_id: this.entry.hash_id };
      this.$store.dispatch('collection/remove', entry).then(() => {
        this.$store.dispatch('collections/post', {});
        this.close();
      });
    },
  },
  components: {
    Card,
  },
};
</script>
