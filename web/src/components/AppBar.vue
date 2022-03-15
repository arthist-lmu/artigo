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

        <v-btn
          :href="api"
          target="_blank"
          small
          text
        >
          {{ $t('api.title') }}
        </v-btn>

        <v-dialog
          v-if="!isLoggedIn"
          v-model="dialog.register"
          max-width="400"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              small
              text
            >
              {{ $t("user.register.title") }}
            </v-btn>
          </template>

          <RegisterCard
            v-model="dialog.register"
            :isDialog="true"
          />
        </v-dialog>

        <v-dialog
          v-if="!isLoggedIn"
          v-model="dialog.login"
          max-width="400"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              small
              text
            >
              {{ $t("user.login.title") }}
            </v-btn>
          </template>

          <LoginCard
            v-model="dialog.login"
            :isDialog="true"
          />
        </v-dialog>

        <v-btn
          v-if="isLoggedIn"
          @click="logout"
          small
          text
        >
          {{ $t("user.logout.title") }}
        </v-btn>

        <v-spacer />

        <v-col cols="2">
          <v-combobox
            v-model="query"
            id="search"
            @click:append-outer="search"
            @keyup.enter.native="search"
            :placeholder="$t('search.title')"
            append-outer-icon="mdi-magnify"
            background-color="white"
            hide-details
            clearable
            rounded
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
import { API_LOCATION } from '@/../app.config';

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
      this.$i18n.locale = lang;
    },
    search() {
      this.$store.dispatch('search/post', { 'query': this.query });
    },
    logout() {
      this.$store.dispatch('user/logout');
    },
  },
  computed: {
    locale() {
      return this.$i18n.locale;
    },
    api() {
      return `${API_LOCATION}/schema/redoc`;
    },
    isLoggedIn() {
      return this.$store.state.user.loggedIn;
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
