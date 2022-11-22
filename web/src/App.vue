<template>
  <router-view />
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
