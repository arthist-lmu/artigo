<template>
  <v-card
    max-width="600"
    flat
  >
    <v-card-title v-if="isDialog">
      {{ $t("user.register.title") }}

      <v-btn
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="isDialog ? 'pt-4' : 'pt-0 px-0'">
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
          v-model="user.password1"
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

        <v-text-field
          v-model="user.password2"
          @click:append="showPassword = !showPassword"
          :type="showPassword ? 'text' : 'password'"
          :placeholder="$t('user.fields.password-repeat')"
          :rules="[checkLength, checkPasswordRepeat]"
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

        <v-checkbox
          v-model="user.privacy_policy"
          :label="$t('user.fields.privacy-policy')"
          :rules="[checkTrue]"
          class="mt-0"
          on-icon="mdi-check-circle-outline"
          off-icon="mdi-checkbox-blank-circle-outline"
          tabindex="0"
          color="primary"
          hide-details
          dense
        />
      </v-form>
    </v-card-text>

    <v-card-actions :class="isDialog ? 'pb-6 px-6' : 'pb-8 px-0'">
      <v-btn
        @click="register"
        :disabled="!isFormValid"
        tabindex="0"
        color="primary"
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
    };
  },
  methods: {
    register() {
      this.$store.dispatch('user/register', this.user);
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
          return this.$tc('user.register.rules.min', 5);
        }
        if (value.length > 75) {
          return this.$tc('user.register.rules.max', 75);
        }
        return true;
      }
      return this.$t('field.required');
    },
    checkPasswordRepeat(value) {
      if (value && value === this.user.password1) {
        return true;
      }
      return this.$t('user.register.rules.password-repeat');
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
      if (this.status) {
        this.close();
      }
    },
  },
};
</script>
