<template>
  <v-card
    max-width="600"
    flat
  >
    <v-card-title :class="{ 'pt-6 px-6': !isDialog }">
      {{ $t("user.register.title") }}

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
          :rules="[checkTrue]"
          class="mt-0"
          on-icon="mdi-check-circle-outline"
          off-icon="mdi-checkbox-blank-circle-outline"
          tabindex="0"
          color="primary"
          hide-details
          dense
        >
          <template v-slot:label>
            {{ $t('user.fields.privacy-policy') }}

            <v-btn
              @click.stop
              class="ml-1"
              href="https://www.kunstgeschichte.uni-muenchen.de/funktionen/datenschutz/index.html"
              target="_blank"
              small
              icon
            >
              <v-icon>
                mdi-link-variant
              </v-icon>
            </v-btn>
          </template>
        </v-checkbox>
      </v-form>
    </v-card-text>

    <v-card-actions class="pb-6 px-6">
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
      if (value && value === this.user.password1) {
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
};
</script>
