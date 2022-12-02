<template>
  <component
    :is="this.$route.meta.layout || 'div'"
    :dark="this.$route.meta.dark"
    :opaque="this.$route.meta.opaque"
    :hideSearchBar="this.$route.meta.hideSearchBar"
  >
    <router-view />
  </component>
</template>

<script>
export default {
  computed: {
    locale() {
      return this.$i18n.locale;
    },
  },
  watch: {
    locale(lang) {
      const { query } = this.$route;
      this.$router.push({ params: { lang }, query });
      document.documentElement.lang = lang;
    },
  },
  created() {
    document.documentElement.lang = this.locale;
  },
};
</script>
