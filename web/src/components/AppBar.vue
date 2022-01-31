<template>
  <v-app-bar
    height="114"
    clipped-left
    flat
    app
  >
    <v-container
      class="pt-0"
      fluid
    >
      <v-row
        class="mb-2"
        align="center"
        no-gutters
      >
        <v-btn
          v-for="lang in langs"
          :key="lang"
          @click="change(lang)"
          class="lang"
          :color="lang === locale ? 'primary' : 'transparent'"
          depressed
          small
        >
          {{ lang }}
        </v-btn>
      </v-row>

      <v-row
        align="center"
        no-gutters
      >
        <v-btn
          v-for="page in pages"
          :key="page"
          @click="goTo(page)"
          small
          text
        >
          {{ $t(page)["title"] }}
        </v-btn>

        <v-dialog
          v-model="dialog.register"
          max-width="400"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              small
              text
            >
              {{ $t("register.title") }}
            </v-btn>
          </template>

          <RegisterCard
            v-model="dialog.register"
            :isDialog="true"
          />
        </v-dialog>

        <v-dialog
          v-model="dialog.login"
          max-width="400"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              small
              text
            >
              {{ $t("login.title") }}
            </v-btn>
          </template>

          <LoginCard
            v-model="dialog.login"
            :isDialog="true"
          />
        </v-dialog>

        <v-spacer />

        <v-col cols="2">
          <v-combobox
            v-model="query"
            id="search"
            @click:append-outer="search"
            @keyup.enter.native="search"
            :placeholder="$t('search.title')"
            append-outer-icon="mdi-magnify"
            hide-details
            clearable
            outlined
            dense
            solo
            flat
          />
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
import i18n from '@/plugins/i18n';
import router from '@/router/index';

import LoginCard from '@/components/LoginCard.vue';
import RegisterCard from '@/components/RegisterCard.vue';

export default {
  data() {
    return {
      pages: [
        'imprint',
        'privacy-policy',
      ],
      dialog: {
        register: false,
        login: false,
      },
      langs: [
        'en',
        'de',
      ],
      query: null,
    };
  },
  methods: {
    goTo(page) {
      router.push({ name: page });
    },
    change(lang) {
      i18n.locale = lang;
    },
    search() {
      this.$store.dispatch('api/search', { 'query': this.query });
      router.push({ name: 'search' });
    },
  },
  computed: {
    locale() {
      return i18n.locale;
    },
  },
  watch: {
    locale(lang) {
      router.push({ params: { lang } });
      document.documentElement.lang = lang;
    },
  },
  created() {
    document.documentElement.lang = this.locale;
  },
  components: {
    LoginCard,
    RegisterCard,
  },
};
</script>

<style>
.v-toolbar__content {
  align-items: start;
  padding-top: 0;
}

.v-input__slot {
  background-color: transparent !important;
}
</style>

<style scoped>
.v-toolbar {
  background-color: #f9f9f9 !important;
}

.v-btn {
  min-width: 16px !important;
}

.v-btn.lang {
  border-radius: 0 0 4px 4px;
}

.v-autocomplete {
  font-size: 14px;
}
</style>
