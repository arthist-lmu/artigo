<template>
  <v-card
    max-width="900"
    flat
  >
    <v-card-title v-if="isDialog">
      {{ $t("user.password-reset.title") }}

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
      </v-form>
    </v-card-text>

    <v-card-actions :class="isDialog ? 'pb-6 px-6' : 'pb-8 px-0'">
      <v-btn
        @click="resetPassword"
        :disabled="!isFormValid"
        tabindex="0"
        color="primary"
        depressed
        rounded
        block
      >
        {{ $t("user.password-reset.title") }}
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
    };
  },
  methods: {
    resetPassword() {
      this.user.lang = this.$i18n.locale;  // fix locale
      this.$store.dispatch('user/resetPassword', this.user);
    },
    close() {
      this.$emit('input', false);
    },
    checkLength(value) {
      if (value) {
        if (value.length < 5) {
          return this.$tc('rules.min', 5);
        }
        if (value.length > 75) {
          return this.$tc('rules.max', 75);
        }
        return true;
      }
      return this.$t('field.required');
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
