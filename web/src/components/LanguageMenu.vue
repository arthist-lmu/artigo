<template>
  <v-menu offset-x>
    <template v-slot:activator="{ attrs, on }">
      <v-list-item
        v-bind="attrs"
        v-on="on"
      >
        <v-list-item-content>
          {{ $t("language.title") }}
        </v-list-item-content>

        <v-list-item-action>
          <v-icon>
            mdi-chevron-right
          </v-icon>
        </v-list-item-action>
      </v-list-item>
    </template>

    <v-list dense>
      <v-list-item
        v-for="lang in langs"
        :key="lang"
        @click="changeLang(lang)"
      >
        <v-list-item-avatar size="32">
          <v-icon
            v-if="lang === locale"
            class="mr-2"
          >
            mdi-check
          </v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          {{ $t("language.fields")[lang] }}
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  data() {
    return {
      langs: [
        'en',
        'de',
      ],
    };
  },
  methods: {
    changeLang(lang) {
      this.$i18n.locale = lang;
    },
  },
  computed: {
    locale() {
      return this.$i18n.locale;
    },
  },
};
</script>
