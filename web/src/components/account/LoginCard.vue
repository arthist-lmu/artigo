<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('user.login.title')"
  >
    <p class="pb-4">{{ $t('user.login.note') }}</p>

    <v-form
      v-model="isFormValid"
      @submit.prevent="login"
    >
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

    <template v-slot:actions>
      <v-row>
        <v-col>
          <v-btn
            @click="login"
            :disabled="!isFormValid"
            type="submit"
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
        </v-col>
      </v-row>
    </template>

    <template v-slot:dialogs>
      <v-dialog
        v-model="dialog.passwordReset"
        max-width="400"
      >
        <PasswordResetCard v-model="dialog.passwordReset" />
      </v-dialog>
    </template>
  </Card>
</template>

<script>
import Card from '@/components/utils/Card.vue';

export default {
  extends: Card,
  props: {
    ...Card.props,
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
      if (this.isFormValid) {
        this.$store.dispatch('user/login', this.user);
      }
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
    Card,
  },
};
</script>
