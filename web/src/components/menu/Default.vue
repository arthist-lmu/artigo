<template>
  <span v-if="isAnonymous">
    <v-dialog
      v-model="dialog.login"
      max-width="450"
    >
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          class="ml-2"
          color="grey lighten-2"
          outlined
          rounded
        >
          {{ $t("user.login.title") }}
        </v-btn>
      </template>

      <LoginCard v-model="dialog.login" />
    </v-dialog>

    <v-dialog
      v-model="dialog.register"
      max-width="450"
    >
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          class="ml-2"
          :color="dark ? 'accent' : 'primary'"
          :dark="dark"
          depressed
          rounded
        >
          {{ $t("user.register.title") }}
        </v-btn>
      </template>

      <RegisterCard v-model="dialog.register" />
    </v-dialog>
  </span>
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
      dialog: {
        login: false,
        register: false,
      },
    };
  },
  computed: {
    isAnonymous() {
      return this.$store.state.user.isAnonymous;
    },
  },
  components: {
    LoginCard: () => import('@/components/account/LoginCard.vue'),
    RegisterCard: () => import('@/components/account/RegisterCard.vue'),
  },
};
</script>
