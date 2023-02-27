<template>
  <span v-if="!isAnonymous">
    <v-btn
      v-if="type"
      @click="reconcile(type)"
      :title="$t('reconcile.title')"
      color="grey lighten-2"
      icon
    >
      <v-icon>mdi-wiper</v-icon>
    </v-btn>

    <v-menu
      v-else
      open-on-hover
      offset-y
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          :title="$t('reconcile.title')"
          v-bind="attrs"
          v-on="on"
          class="ml-1 mr-n2"
          color="primary"
          icon
        >
          <v-icon>mdi-wiper</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item @click="reconcile('resource')">
          <v-list-item-title>
            {{ $t('reconcile.fields.resource') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item @click="reconcile('creator')">
          <v-list-item-title>
            {{ $t('reconcile.fields.creator') }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </span>
</template>

<script>
export default {
  props: {
    entries: Array,
    type: String,
  },
  methods: {
    reconcile(type) {
      const queries = [];
      this.entries.forEach(({ id, meta }) => {
        switch (type) {
          case 'creator':
            queries.push({
              id,
              name: this.creators(meta),
              type,
            });
            break;
          case 'resource':
            queries.push({
              id,
              name: this.titles(meta),
              type,
            });
            break;
          default:
            break;
        }
      });
      this.$store.dispatch('reconcile/post', { queries });
    },
    titles(meta) {
      const titles = [];
      meta.forEach(({ name, value_str }) => {
        if (name === 'titles' && value_str) {
          titles.push(value_str);
        }
      });
      if (titles.length > 0) {
        return titles[0];
      }
      return this.$t('resource.default.title');
    },
    creators(meta) {
      const creators = [];
      meta.forEach(({ name, value_str }) => {
        if (name === 'creators' && value_str) {
          creators.push(value_str);
        }
      });
      if (creators.length > 0) {
        return creators[0];
      }
      return this.$t('resource.default.creator');
    },
  },
  computed: {
    isAnonymous() {
      return this.$store.state.user.isAnonymous;
    },
  },
};
</script>
