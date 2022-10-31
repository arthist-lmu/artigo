<template>
  <v-menu
    min-width="225"
    max-width="225"
    offset-y
    bottom
  >
    <template v-slot:activator="{ attrs, on }">
      <v-btn
        v-bind="attrs"
        v-on="on"
        class="ml-2"
        icon
      >
        <v-icon :color="dark ? 'accent' : 'primary'">
          mdi-menu
        </v-icon>
      </v-btn>
    </template>

    <v-list dense>
      <v-list-item @click="goTo('search')">
        <v-list-item-content>
          {{ $t("search.title") }}
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    goTo(name) {
      this.$router.push({ name });
    },
  },
};
</script>
