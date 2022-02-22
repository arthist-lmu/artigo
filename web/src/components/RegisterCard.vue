<template>
  <v-card
    max-width="450"
    flat
  >
    <v-card-title v-if="isDialog">
      {{ $t("register.title") }}

      <v-btn
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="isDialog ? '' : 'pt-0 px-0'">
      <v-form v-model="isFormValid">
        <v-text-field
          v-model="user.username"
          :placeholder="$t('user.fields.username')"
          :rules="[checkLength]"
          prepend-icon="mdi-account"
          counter="75"
          clearable
        />

        <v-text-field
          v-model="user.email"
          :placeholder="$t('user.fields.email')"
          :rules="[checkLength]"
          prepend-icon="mdi-email"
          counter="75"
          clearable
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
          prepend-icon="mdi-lock"
          counter="75"
          clearable
        />

        <v-text-field
          v-model="user.password_repeat"
          @click:append="showPassword = !showPassword"
          :type="showPassword ? 'text' : 'password'"
          :placeholder="$t('user.fields.password-repeat')"
          :rules="[checkLength, checkPasswordRepeat]"
          :append-icon="
            showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
          "
          prepend-icon="mdi-lock"
          counter="75"
          clearable
        />

        <v-checkbox
          v-model="user.privacy_policy"
          :label="$t('user.fields.privacy-policy')"
          :rules="[checkTrue]"
          on-icon="mdi-check-circle-outline"
          off-icon="mdi-checkbox-blank-circle-outline"
          color="primary"
        />
      </v-form>
    </v-card-text>

    <v-card-actions :class="isDialog ? 'pt-0 pb-6 px-6' : 'pb-8 px-0'">
      <v-btn
        @click="register"
        :disabled="!isFormValid"
        color="accent"
        depressed
        rounded
        block
      >
        {{ $t("user.register.title") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    isDialog: Boolean,
    value: Boolean,
  },
  data() {
    return {
      showPassword: false,
      isFormValid: false,
      user: {},
    };
  },
  methods: {
    register() {
      this.$store.dispatch('user/register', this.user);
      this.close();
      // TODO: go to user-specific page if successful?
    },
    close() {
      this.$emit('input', false);
    },
    checkTrue(value) {
      if (value) {
        return true;
      }
      return this.$t('field.required');
    },
    checkLength(value) {
      if (value) {
        if (value.length < 5) {
          return this.$t('user.register.rules.min');
        }
        if (value.length > 75) {
          return this.$t('user.register.rules.max');
        }
        return true;
      }
      return this.$t('field.required');
    },
    checkPasswordRepeat(value) {
      if (value && value === this.user.password) {
        return true;
      }
      return this.$t('user.register.rules.password-repeat');
    },
  },
};
</script>
