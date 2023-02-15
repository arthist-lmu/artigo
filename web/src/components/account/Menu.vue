<template>
  <v-menu
    v-model="menu"
    min-width="275"
    max-width="425"
    :close-on-content-click="false"
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
          mdi-account-circle-outline
        </v-icon>
      </v-btn>
    </template>

    <v-list dense>
      <template v-if="!isAnonymous">
        <v-list-item>
          <v-list-item-content class="justify-center px-4 py-6">
            <div class="mx-auto text-center">
              <v-avatar color="error">
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

        <v-divider />
      </template>

      <template v-if="isAnonymous && $vuetify.breakpoint.mobile">
        <v-list-item @click="dialog.register = true">
          <v-list-item-content>
            {{ $t("user.register.title") }}
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="dialog.login = true">
          <v-list-item-content>
            {{ $t("user.login.title") }}
          </v-list-item-content>
        </v-list-item>
      </template>

      <v-list-item
        v-if="data.n_gamesessions > 0"
        @click="goTo('sessions')"
      >
        <v-list-item-content>
          {{ $t("sessions.title") }}
        </v-list-item-content>

        <v-list-item-action>
          <v-chip
            class="ml-2"
            style="cursor: pointer;"
            outlined
            small
          >
            {{ data.n_gamesessions }}
          </v-chip>
        </v-list-item-action>
      </v-list-item>

      <template v-if="!isAnonymous">
        <v-list-item @click="goTo('collections')">
          <v-list-item-content>
            {{ $t("collections.title") }}
          </v-list-item-content>

          <v-list-item-action>
            <v-icon
              @click.stop="dialog.collectionUpload = true"
              :title="$t('user.upload.title')"
              color="primary"
              class="ml-2"
            >
              mdi-cloud-upload-outline
            </v-icon>

            <v-chip
              v-if="data.n_collections > 0"
              class="ml-2"
              style="cursor: pointer;"
              outlined
              small
            >
              {{ data.n_collections }}
            </v-chip>
          </v-list-item-action>
        </v-list-item>

        <v-list-item @click="logout">
          <v-list-item-content>
            {{ $t("user.logout.title") }}
          </v-list-item-content>
        </v-list-item>
      </template>

      <v-divider />

      <LanguageMenu />
    </v-list>

    <v-dialog
      v-model="dialog.login"
      max-width="450"
    >
      <LoginCard v-model="dialog.login" />
    </v-dialog>

    <v-dialog
      v-model="dialog.register"
      max-width="450"
    >
      <RegisterCard v-model="dialog.register" />
    </v-dialog>

    <v-dialog
      v-model="dialog.collectionUpload"
      max-width="450"
    >
      <CollectionUploadCard v-model="dialog.collectionUpload" />
    </v-dialog>
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
  data() {
    return {
      menu: false,
      dialog: {
        login: false,
        register: false,
        collectionUpload: false,
      },
    };
  },
  methods: {
    goTo(name) {
      this.$router.push({ name });
    },
    logout() {
      this.$store.dispatch('user/logout');
    },
  },
  computed: {
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
      if (this.keyInObj('email', this.data)) {
        return this.data.email.slice(0, 2);
      }
      return '';
    },
    isAnonymous() {
      return this.$store.state.user.isAnonymous;
    },
  },
  watch: {
    dialog: {
      handler({ register, login }) {
        if (register || login) {
          this.menu = false;
        }
      },
      deep: true,
    },
  },
  components: {
    LoginCard: () => import('@/components/account/LoginCard.vue'),
    RegisterCard: () => import('@/components/account/RegisterCard.vue'),
    CollectionUploadCard: () => import('@/components/collection/UploadCard.vue'),
    LanguageMenu: () => import('@/components/LanguageMenu.vue'),
  },
};
</script>

<style scoped>
.v-list-item__action--stack {
  flex-direction: row;
}
</style>
