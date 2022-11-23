<template>
  <v-card
    max-width="900"
    flat
  >
    <v-card-title :class="{ 'pt-6 px-6': !isDialog }">
      {{ $t("user.login.title") }}

      <v-btn
        v-if="isDialog"
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="[isDialog ? undefined : 'px-6', 'pt-4']">
      <v-form v-model="isFormValid">
        <v-text-field
          v-model="user.username"
          :placeholder="$t('user.fields.username')"
          :rules="[checkLength]"
          tabindex="0"
          counter="75"
          clearable
          outlined
          rounded
          dense
        />

        <v-text-field
          v-model="user.email"
          :placeholder="$t('user.fields.email')"
          :rules="[checkLength]"
          tabindex="0"
          counter="75"
          clearable
          outlined
          rounded
          dense
        />

        <v-text-field
          v-model="user.password"
          @click:append="showPassword = !showPassword"
          :type="showPassword ? 'text' : 'password'"
          :placeholder="$t('user.fields.password')"
          :rules="[checkLength]"
          :append-icon="
            showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
          "
          tabindex="0"
          counter="75"
          clearable
          outlined
          rounded
          dense
        />
      </v-form>
    </v-card-text>

    <v-card-actions
      class="pb-6 px-6"
      style="display: block;"
    >
      <v-btn
        @click="login"
        :disabled="!isFormValid"
        tabindex="0"
        color="primary"
        depressed
        rounded
        block
      >
        {{ $t("user.login.title") }}
      </v-btn>

      <v-btn
        @click="resetPassword"
        class="mt-2 ml-0"
        tabindex="0"
        rounded
        small
        plain
        block
        text
      >
        {{ $t("user.password-reset.title") }}
      </v-btn>
    </v-card-actions>

    <v-dialog
      v-model="dialog.passwordReset"
      max-width="400"
    >
      <PasswordResetCard v-model="dialog.passwordReset" />
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  props: {
    isDialog: {
      type: Boolean,
      default: true,
    },
    value: Boolean,
  },
  data() {
    return {
      user: {},
      isFormValid: false,
      showPassword: false,
      dialog: {
        passwordReset: false,
      },
    };
  },
  methods: {
    login() {
      this.$store.dispatch('user/login', this.user);
    },
    close() {
      this.$emit('input', false);
    },
    checkLength(value) {
      if (value) {
        if (value.length < 4) {
          return this.$tc('rules.min', 4);
        }
        if (value.length > 75) {
          return this.$tc('rules.max', 75);
        }
        return true;
      }
      return this.$t('field.required');
    },
    resetPassword() {
      this.dialog.passwordReset = true;
    },
  },
  computed: {
    status() {
      const { error, loading } = this.$store.state.utils.status;
      return !loading && !error;
    },
    timestamp() {
      return this.$store.state.utils.status.timestamp;
    },
  },
  watch: {
    timestamp() {
      if (this.isFormValid && this.status) {
        if (this.isDialog) {
          this.close();
        } else {
          this.$router.push({ name: 'home' });
        }
      }
    },
  },
  components: {
    PasswordResetCard: () => import('./PasswordResetCard.vue'),
  },
};
</script>
