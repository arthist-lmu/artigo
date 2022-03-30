<template>
  <v-menu
    min-width="225"
    max-width="225"
    :close-on-content-click="false"
    offset-y
    bottom
  >
    <template v-slot:activator="{ attrs, on: menu }">
      <v-btn
        v-bind="attrs"
        v-on="menu"
        icon
      >
        <v-icon color="primary">
          mdi-account-cog
        </v-icon>
      </v-btn>
    </template>

    <v-list
      class="py-0"
      dense
    >
      <v-list-item v-if="!isAnonymous">
        <v-list-item-content class="justify-center px-4 py-6">
          <div class="mx-auto text-center">
            <v-avatar color="primary">
              <span class="white--text text-h5">
                {{ initials }}
              </span>
            </v-avatar>

            <p class="text-caption mt-2 mb-0">
              {{ data.email }}
            </p>

            <p class="text-caption mb-0">
              <i>{{ joined }}</i>
            </p>
          </div>
        </v-list-item-content>
      </v-list-item>

      <v-divider v-if="!isAnonymous" />

      <v-menu offset-x>
        <template v-slot:activator="{ attrs, on: submenu }">
          <v-list-item
            v-bind="attrs"
            v-on="submenu"
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

        <v-list
          class="py-0"
          dense
        >
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
    data() {
      return this.$store.state.user.data;
    },
    joined() {
      const diff = new Date() - new Date(this.data.date_joined);
      const nDays = Math.round(diff / (1000 * 60 * 60 * 24));
      return this.$tc('user.menu.joined', nDays);
    },
    initials() {
      if (this.keyInObj('username', this.data)) {
        return this.data.username.slice(0, 2);
      }
      return '';
    },
    isAnonymous() {
      return this.$store.state.user.isAnonymous;
    },
  },
};
</script>
