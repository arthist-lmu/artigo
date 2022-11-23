<template>
  <v-card
    max-width="900"
    flat
  >
    <v-card-title :class="{ 'pt-6 px-6': !isDialog }">
      {{ $t("user.password-reset.title") }}

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
          v-model="user.new_password1"
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
          v-model="user.new_password2"
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
      </v-form>
    </v-card-text>

    <v-card-actions class="pb-6 px-6">
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
      showPassword: false,
    };
  },
  methods: {
    resetPassword() {
      this.$store.dispatch('user/resetPasswordConfirm', this.user);
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
    checkPasswordRepeat(value) {
      if (value && value === this.user.new_password1) {
        return true;
      }
      return this.$t('rules.password-repeat');
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
  created() {
    let path = this.$route.path.split('/');
    path = path.filter((item) => item);
    this.user = {
      uid: path[path.length - 2],
      token: path[path.length - 1],
    };
  },
};
</script>
